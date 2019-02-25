# Running on OpenShift
The supplied [openshift-project-tools](https://github.com/BCDevOps/openshift-project-tools) compatible scripts and configurations provide a simplified method of deploying the ledger browser into an OpenShift environment.  The extended param files have not been generated simply to keep things clean.

## Builds:
At the time of writing (2019.02.25) the OpenShift builds in our OpenShift (v3.11) environment ([devex-von-tools](https://console.pathfinder.gov.bc.ca:8443/console/project/devex-von-tools/overview)) do not fully support all Docker directives.  Specifically the `ADD --chown` flag.  Full support for these features are available in `buildah` which will be available when the platform is upgraded to v4.x.  Until then it is easier to build the image locally and push it into the project registry.

Build the image locally using Docker.  From the root project directory run:
```
./manage build
```

Push the image to the project registry (oc-push-image.sh is part of  [openshift-project-tools](https://github.com/BCDevOps/openshift-project-tools)):
```
oc-push-image.sh -i von-network-base:latest -n devex-von-tools
```

Tag the image for deployment:
```
oc -n devex-von-tools tag von-network-base:latest von-network-base:prod
```

## Deployments:
Publishing the deployment configuration:
```
genDepls.sh -e prod
```

Updating the deployment configuration:
```
genDepls.sh -u -e prod
```