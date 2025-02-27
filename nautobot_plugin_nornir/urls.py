"""Django urlpatterns declaration for nautobot_plugin_nornir app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

# Uncomment the following line if you have views to import
# from nautobot_plugin_nornir import views


app_name = "nautobot_plugin_nornir"
router = NautobotUIViewSetRouter()

# Here is an example of how to register a viewset, you will want to replace views.NautobotPluginNornirUIViewSet with your viewset
# router.register("nautobot_plugin_nornir", views.NautobotPluginNornirUIViewSet)


urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("nautobot_plugin_nornir/docs/index.html")), name="docs"),
]

urlpatterns += router.urls
