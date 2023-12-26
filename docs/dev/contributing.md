# Contributing to the App

Information on how to contribute fixes, functionality, or documentation changes back to the project.

The project is packaged with a light [development environment](dev_environment.md) based on `docker-compose` to help with the local development of the project and to run tests.

The project is following Network to Code software development guidelines and is leveraging the following:

- Black, Pylint, Bandit, flake8, yamllint, and pydocstyle for Python linting and formatting.
- Django unit test to ensure the app is working properly.

Documentation is built using [mkdocs](https://www.mkdocs.org/). The [Docker based development environment](dev_environment.md#docker-development-environment) automatically starts a container hosting a live version of the documentation website on [http://localhost:8001](http://localhost:8001) that auto-refreshes when you make any changes to your local files.

## Branching Policy

The branching policy includes the following tenets:

- The develop branch is the primary branch to develop off of
- If there is a reason to have a patch version, the maintainers may use cherry-picking strategy
- PRs intended to add new features should be sourced from the develop branch.
- PRs intended to address bug fixes and security patches should be sourced from the develop branch.
- PRs intended to add new features that break backward compatibility should be discussed before a PR is created.

Nautobot App Nornir will observe semantic versioning, as of 1.0. This may result in an quick turn around in minor versions to keep pace with an ever growing feature set.

## Release Policy

Nautobot App Nornir has currently no intended scheduled release schedule, and will release new features in minor versions.

When a new release is created the following should happen.

- A release PR is created with:
    - Update to the changelog in `docs/admin/release_notes/version_<major>.<minor>.md` file to reflect the changes.
    - Change the version from `<major>.<minor>.<patch>-beta` to `<major>.<minor>.<patch>` in pyproject.toml.
    - Set the PR to the main
- Ensure the tests for the PR pass.
- Merge the PR.
- Create a new tag:
    - The tag should be in the form of `v<major>.<minor>.<patch>`.
    - The title should be in the form of `v<major>.<minor>.<patch>`.
    - The description should be the changes that were added to the `version_<major>.<minor>.md` document.
- If merged into `main`, then push from `main` to `develop`, in order to retain the merge commit created when the PR was merged
- A post release PR is created with.
    - Change the version from `<major>.<minor>.<patch>` to `<major>.<minor>.<patch + 1>-beta` pyproject.toml.
    - Set the PR to the `develop`.
    - Once tests pass, merge.
