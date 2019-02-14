# Running on OpenShift
The supplied [openshift-project-tools](https://github.com/BCDevOps/openshift-project-tools) compatible scripts and configurations provide a simplified method of deploying the ledger browser into an OpenShift environment.  The extended param files have not been generated simply to keep things clean.

Publishing the deployment configuration:
```
genDepls.sh -e prod
```

Updating the deployment configuration:
```
genDepls.sh -u -e prod
```