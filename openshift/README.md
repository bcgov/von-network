# Running on OpenShift
The supplied [openshift-project-tools](https://github.com/BCDevOps/openshift-project-tools) compatible scripts and configurations provide a simplified method of deploying the ledger browser into an OpenShift environment.  The extended param files have not been generated simply to keep things clean.

## Warning
The provided scripts and configurations are for deploying **ONLY** the ledger browser portion of `von-network`.  This is possible because the ledger browser acts as a client.  Client applications work well in OpenShift.

**Hosting a complete instance of `von-network` (specifically the ledger network/nodes) in OpenShift is not recommended.**  Although possible, it can be very complicated, and the use case is exceptionally limiting since the provisioned ledger will only be available to the clients within the OpenShift project in which the ledger was provisioned.

The limiting factors exist in the differences between how OpenShift is designed to handle addressing and how Indy-Node is designed to handle addressing.  Indy-Node uses static IP:PORT addressing exclusively, where each Node is assigned a unique static IP:PORT address; this is by design and for good reasons we won't get into here.  Pods in OpenShift, on the other hand, are dynamically assigned IP addresses, and addressing (routing) is accomplished using resolvable URIs (URLs / routes) that completely abstract the underlying and highly dynamic nature of any IP:PORT mapping that occurs in OpenShift.  The two are simply not very compatible concepts, but both are designed for specific purposes solving different issues.  The dynamic nature of OpenShift makes it complicated to startup/initialize the ledger network and generate a functional genesis file for clients in the first place.  Once you've overcome the ledger startup/initialization issues the resulting genesis file is unusable for any clients that exist outside the OpenShift project in which the ledger resides, since they will not be able to resolve/reach the addresses listed in the generated genesis file.  To further complicate matters pod restarts/deploys of your ledger nodes will affect their assigned IP addresses, meaning the new node needs to initialize itself and join the existing network, and the genesis file must be updated to reflect the current state of the ledger for new or restarted clients.

If you want to host your own complete, provisional, instance of `von-network` we recommend using a service where your host machine is assigned a public static IP address.

## Builds:
Due to the lack of support for all Docker directives (e.g.: the `ADD --chown` flag) no build configurations are available for the project.It is easier to build the image locally and push it into the project registry.

Build the image locally using Docker.  From the root project directory run:
```
./manage build
```

Push the image to the project registry (oc-push-image.sh is part of  [openshift-project-tools](https://github.com/BCDevOps/openshift-project-tools)):
```
oc-push-image.sh -i von-network-base:latest -n ca7f8f-tools
```

Tag the image for deployment:
```
oc -n ca7f8f-tools tag von-network-base:latest von-network-base:prod
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
