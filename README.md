# VON Network
A portable development level Indy Node network.

## Quick Start Guide

A **Quick Start Guide** for a working set of applications is maintained here; [Running a Complete Provisional VON Network](https://github.com/bcgov/TheOrgBook/blob/master/docker/README.md#running-a-complete-provisional-von-network).  This is a great way to see the **VON Network** component in action.

## Running the Network Locally

1. First, install Docker. Download the installer for your operating system [here](https://store.docker.com/search?type=edition&offering=community). Once it is installed, keep the Docker daemon running in the background.

2. Linux users will also need to [install docker-compose](https://github.com/docker/compose/releases). Mac and Windows users will have this already.

3. Once Docker has been installed, open a terminal session and clone this repository:

```bash
git clone <repository url> von-network
```

4. Move to the new directory:

```bash
cd von-network
```

5. Now you can build the Dockerfile into an image which we will use to run containers (this process will take several minutes):

```bash
./manage build
```

6. Once the build process completes, you can test the build to make sure everything works properly:

```bash
./manage start
```

## Running the Network on a VPS

### Special requirements for BC

Because outbound traffic from openshift is limited, we use proxies to redirect traffic from open ports by overloading ports 80 and 9418 (git).

Run 4 extra VMs as proxies (proxy_1, proxy_2, proxy_3, proxy4). Traffic should be forwarded in the following formation:

- proxy_1:9418 -> von-network:9701
- proxy_1:80 -> von-network:9702
- proxy_2:9418 -> von-network:9703
- proxy_2:80 -> von-network:9704
- proxy_3:9418 -> von-network:9705
- proxy_3:80 -> von-network:9706
- proxy_4:9418 -> von-network:9707
- proxy_1:80 -> von-network:9708


### Requirements

- ubuntu 16.04
- at least 1GB RAM
- accepting incoming TCP connections on ports 9701-9708
- root access

1. Install unzip utility:

```bash
# Requires root privileges
apt install unzip
```

2. Install Docker and Docker Compose:

```bash
curl -fsSL get.docker.com -o get-docker.sh
```

```bash
# Requires root privileges
sh get-docker.sh
```

```bash
curl -L https://github.com/docker/compose/releases/download/1.17.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```

```bash
chmod +x /usr/local/bin/docker-compose
```

3. Download this repository:

```bash
curl -L https://github.com/bcgov/von-network/archive/master.zip > bcovrin.zip && \
    unzip bcovrin.zip && \
    cd von-network-master && \
    chmod a+w ./server/
```

3. Map service port to 80 in docker-compose.yml

Change

```yaml
    ports:
      - 9000:8000
```

to

```yaml
    ports:
      - 80:8000
```

4. Build the Docker container:

```bash
./manage build
```

5. Run the network of nodes:

```bash
# This command requires the publicly accesible ip address of the machine
./manage start proxy_1,proxy_2,proxy_3,proxy_4 &
```

## Connecting to the Network

### With the CLI
Once the nodes are all running and have connected to each other, you can run the Indy client to test the connection in a separate terminal window:

```bash
./manage cli
```

If you want to connect to a remote indy-node pool, you can optionally supply an ip address. (Currently only supports a test network running on a single machine with a single ip address.)

```bash
./manage cli <ip address>
```

The Indy CLI should boot up and you should see the following:

```
Indy-CLI (c) 2017 Evernym, Inc.
Type 'help' for more information.
Running Indy 1.1.159

indy>
```

Now connect to our new Indy network to make sure network is running correctly:

```
pool connect sandbox
```

What you should see is:

```
indy> pool connect sandbox
Pool "sandbox" has been connected
```

If you see this, congratulations! Your nodes are running correctly and you have a connection to the network.

<!-- ### With the Indy SDK

The Docker container that is built by this environment provides a `von_generate_transactions` command that to automatically discover node ip addresses and generate an accurate genesis transaction file.

To use this tool, you must ensure that you a running a Docker container that inherits from `von-base` and that your docker environment is running a docker network called `von`.

Once you have done this, your environment should be able to automatically connect to the node pool by running `von_generate_transactions` before running any software that uses the Indy SDK.

See [von-connector](https://github.com/nrempel/von-connector) for an example.
 -->

### Extra Features for Development

Running BCovrin also runs a thin webserver to expose some convenience functions:


#### Genesis Transaction Exposed

The genesis transaction record required to connect to the node pool is made available at:

`<ip_address>/genesis`

#### Write new did for seed

The node pool can have a trust anchor write a did for you — available in the UI.
