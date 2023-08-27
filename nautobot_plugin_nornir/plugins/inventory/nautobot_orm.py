"""Inventory Plugin for Nornir designed to work with Nautobot ORM."""
# pylint: disable=unsupported-assignment-operation,unsubscriptable-object,no-member,duplicate-code

from typing import Any, Dict
from copy import deepcopy

from django.db.models import QuerySet
from django.utils.module_loading import import_string

from nornir.core.inventory import (
    ConnectionOptions,
    Defaults,
    Group,
    Groups,
    Host,
    Hosts,
    Inventory,
    ParentGroups,
)
from nornir_nautobot.exceptions import NornirNautobotException

from nautobot.dcim.models import Device

from nautobot_plugin_nornir.constants import CONNECTION_SECRETS_PATHS, PLUGIN_CFG


def _set_dict_key_path(dictionary, key_path, value):
    *keys, last_key = key_path.split(".")
    pointer = dictionary
    for key in keys:
        pointer = pointer.setdefault(key, {})
    pointer[last_key] = value


def _build_out_secret_paths(connection_options, device_secret):
    for nornir_provider, nornir_options in connection_options.items():
        # Offers extensibility to nornir plugins not listed in constants.py under CONNECTION_SECRETS_PATHS.
        if nornir_options.get("connection_secret_path"):
            secret_path = nornir_options.pop("connection_secret_path")
        elif CONNECTION_SECRETS_PATHS.get(nornir_provider):
            secret_path = CONNECTION_SECRETS_PATHS[nornir_provider]
        else:
            continue
        _set_dict_key_path(connection_options, secret_path, device_secret)


def _set_host(data: Dict[str, Any], name: str, groups, host, defaults) -> Host:
    connection_option = {}
    for key, value in data.get("connection_options", {}).items():
        connection_option[key] = ConnectionOptions(
            hostname=value.get("hostname"),
            port=value.get("port"),
            username=value.get("username"),
            password=value.get("password"),
            platform=value.get("platform"),
            extras=value.get("extras"),
        )
    return Host(
        name=name,
        hostname=host["hostname"],
        username=host["username"],
        password=host["password"],
        platform=host["platform"],
        data=data,
        groups=groups,
        defaults=defaults,
        connection_options=connection_option,
    )


class NautobotORMInventory:
    """Construct a inventory object for Nornir based on a Nautobot ORM."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        queryset: QuerySet = None,
        filters: Dict = None,
        credentials_class: str = "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
        credentials_params: Dict = None,
        params: Dict = None,
        defaults: Dict = None,
        **kwargs: Any,
    ) -> None:
        """Inventory for Nornir designed to work with Django ORM within Nautobot.

        Args:
            queryset (QuerySet): Django Queryset
            filters (dict): Django Queryset filter in form of a dict
            credentials_class (string): Name/location of the credential class to use
            credentials_params (dict): parameters to pass to the credentials class
            params (dict): a generic dictionary of additional parameters
            defaults (dict): a generic dictionary of default parameters
            **kwargs: Any:
        """
        # Initialize the Credentials Management Object
        # Based on the class name defined in the parameters
        # At creation time, pass the credentials_params dict to the class
        if isinstance(queryset, QuerySet) and not queryset:
            raise NornirNautobotException("There was no matching results from the query.")
        self.queryset = queryset
        self.filters = filters
        if isinstance(credentials_class, str):
            self.cred_class = import_string(credentials_class)
        else:
            raise NornirNautobotException(
                f"A valid credentials class path (as defined by Django's import_string function) is required, but got {credentials_class} which is not importable. See https://github.com/nautobot/nautobot-plugin-nornir#credentials for details."
            )
        self.credentials_params = credentials_params
        self.params = params
        self.defaults = defaults or {}

    def load(self) -> Inventory:
        """Standard Nornir 3 load method boilerplate."""
        if not self.credentials_params:
            self.credentials_params = {}

        # Initialize QuerySet
        if isinstance(self.queryset, QuerySet) and not self.queryset:
            self.queryset = Device.objects.all()

        if self.filters:
            self.queryset = self.queryset.filter(**self.filters)

        if not self.params:
            self.params = {}

        self.queryset = self.queryset.select_related(
            "device_role",
            "device_type",
            "device_type__manufacturer",
            "site",
            "platform",
            "tenant",
        )

        # Initialize Hosts and Groups vars
        hosts = Hosts()
        defaults = Defaults(data=self.defaults)
        groups = Groups()

        if self.credentials_params:
            cred = self.cred_class(params=self.credentials_params)
        else:
            cred = self.cred_class()

        # Create all hosts
        for device in self.queryset:
            host = self.create_host(device=device, cred=cred, params=self.params)
            hosts[device.name] = _set_host(
                data=host["data"], name=host["name"], groups=host["groups"], host=host, defaults=defaults
            )

            # Initialize all groups if they don't already exist
            for group in hosts[device.name].groups:
                if group not in groups.keys():
                    groups[group] = Group(name=group, defaults=defaults)

        for _host in hosts.values():
            _host.groups = ParentGroups([groups[_group] for _group in _host.groups])
        for _group in groups.values():
            _group.groups = ParentGroups([groups[_group] for _group in _group.groups])

        return Inventory(hosts=hosts, groups=groups, defaults=defaults)

    def create_host(self, device, cred, params: Dict):
        """Create a Nornir host from a Nautobot device object.

        Args:
            device (dcim.models.Device): Nautobot Device object
            cred (credential_class): A Credential class intance
            params (dict): Optional set of parameters


        Returns:
            (dict): Nornir Host dictionary
        """
        host = {"data": {}}
        if "use_fqdn" in params and params.get("use_fqdn"):
            host["hostname"] = f"{device.name}.{params.get('fqdn')}"
        else:
            if device.primary_ip:
                host["hostname"] = str(device.primary_ip.address.ip)
            else:
                host["hostname"] = device.name
        host["name"] = device.name

        if not device.platform:
            raise NornirNautobotException(f"Platform missing from device {device.name}, preemptively failed.")
        host["platform"] = device.platform.slug
        host["data"]["id"] = device.id
        host["data"]["type"] = device.device_type.slug
        host["data"]["site"] = device.site.slug
        host["data"]["role"] = device.device_role.slug
        host["data"]["config_context"] = dict(device.get_config_context())
        host["data"]["custom_field_data"] = device.custom_field_data
        host["data"]["obj"] = device

        username, password, secret = cred.get_device_creds(device=device)  # pylint:disable=unused-variable

        # require username for now
        host["username"] = username
        # require password for now
        host["password"] = password

        global_options = PLUGIN_CFG.get("connection_options", {"netmiko": {}, "napalm": {}, "scrapli": {}})
        if PLUGIN_CFG.get("use_config_context", {}).get("connection_options"):
            config_context_options = (
                device.get_config_context().get("nautobot_plugin_nornir", {}).get("connection_options", {})
            )
            conn_options = {**global_options, **config_context_options}
        else:
            conn_options = global_options

        _build_out_secret_paths(conn_options, secret)

        host["data"]["connection_options"] = deepcopy(conn_options)
        host["groups"] = self.get_host_groups(device=device)

        if device.platform.napalm_driver:
            if not host["data"]["connection_options"].get("napalm"):
                host["data"]["connection_options"]["napalm"] = {}
            host["data"]["connection_options"]["napalm"]["platform"] = device.platform.napalm_driver
        return host

    @staticmethod
    def get_host_groups(device):
        """Get the names of the groups a given device should be part of.

        Args:
            device (dcim.models.Device): Device obj

        Returns:
            (list): List of group names the device should be part of
        """
        groups = [
            "global",
            f"site__{device.site.slug}",
            f"role__{device.device_role.slug}",
            f"type__{device.device_type.slug}",
            f"manufacturer__{device.device_type.manufacturer.slug}",
        ]

        if device.platform:
            groups.append(f"platform__{device.platform.slug}")

        if device.tenant:
            groups.append(f"tenant__{device.tenant.slug}")

        return groups
