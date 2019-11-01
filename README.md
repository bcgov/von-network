# VON Network

A portable development level Indy Node network, including a Ledger Browser. The Ledger Browser (for example the BC Gov's [Ledger for the GreenLight Demo Application](http://greenlight.bcovrin.vonx.io/)) allows a user to see the status of the nodes of a network and browse/search/filter the Ledger Transactions.

`von-network` is being developed as part of the Verifiable Organizations Network (VON). For more information on VON see https://vonx.io.  Even, better - join in with what we are doing and contribute to VON and the Indy community.


## The VON-Network Ledger Browser and API

With the Ledger Browser (for example: [http://greenlight.bcovrin.vonx.io/](http://greenlight.bcovrin.vonx.io/)), you can see:

- The status of the Ledger nodes
- The detailed status of the Ledger Nodes in JSON format (click the "Detailed Status" link)
- The three ledger's of an Indy Network - Domain, Pool and Config (click the respective links)
- The Genesis Transactions for the Indy Network instance.
  - In an Indy Agent, use the URL `<server>/genesis` to GET the genesis file to use in initializing the Agent.

By using the "Authenticate a new DID" part of the UI or posting the appropriate JSON to the VON-Network API (see an example script [here](https://github.com/bcgov/von-agent-template/blob/d1abcbeaa299ce6149570349848bb51716752457/init.sh#L90)), a new DID can be added to the Ledger. A known and published *Trust Anchor* DID is used to write the new DID to the Ledger.  This operation would not be permitted in this way on the Sovrin Main Network. However, it is a useful mechanism on sandbox Indy Networks used for testing.

In the `Domain` Ledger screen ([example](http://greenlight.bcovrin.vonx.io/browse/domain)), you can browse through all of the transactions that have been created on this instance of the Ledger.  As well, you can use a drop down filter to see only specific Ledger transaction types (`nym` - aka DID, `schema`, `CredDef`, etc.), and search for strings in the content of the transactions.

## Indy-Cli Container Environment

This repository also provides a fully containerized Indy-Cli environment which allows you to use the Indy-Cli without having to build or install the Indy-SDK or any of it's dependencies on your machine.

The environment provides a set of batch script templates and a simple variable substitution layer that allows the scripts to be reused for a number of purposes.

For examples of how to use this environment, refer to [Writing Transactions to a Ledger for an Un-privileged Author](./docs/Writing%20Transactions%20to%20a%20Ledger%20for%20an%20Un-privileged%20Author.md)


## VON Quick Start Guide

The [VON Quick Start Guide](https://github.com/bcgov/greenlight/blob/master/docker/VONQuickStartGuide.md) provides the instructions for running a local instance of the VON applications, including an Indy Network, an instance of [TheOrgBook](https://github.com/bcgov/TheOrgBook) and [GreenLight](https://github.com/bcgov/greenlight). This is a great way to see the **VON Network** in action.

## Running the Network Locally

1. First, install Docker. Download the installer for your operating system [here](https://store.docker.com/search?type=edition&offering=community). Once it is installed, keep the Docker daemon running in the background.

2. Linux users will also need to [install docker-compose](https://github.com/docker/compose/releases). Mac and Windows users will have this already.

3. Once Docker has been installed, open a terminal session, change directories to where you store repos, and clone the von-network repository:

```bash
git clone <repository url> von-network
```

4. Move to the new directory:

```bash
cd von-network
```

5. Build the docker images that will be used to run the Indy network containers (this process will take several minutes):

```bash
./manage build
```

The `./manage` script has a number of commands. Run it without arguments to see the set of options.

6. Once the build process completes, you can test the build to make sure everything works properly:

```bash
./manage start
```

Monitor the logs for error messages as the nodes start up.

7. Verify the network is running

In a browser, go to [http://localhost:9000](http://localhost:9000). You should see the VON Indy Ledger Browser and the status of the four nodes of the Indy Network. All should show a lovely, complete blue circle. If not - check the logs in the terminal.

8. Stopping the Network

To stop the scrolling logs and get to a command prompt, hit **Ctrl-C**.  To stop and remove the network persistence (the Ledger), run:

```bash
./manage down
```

If necessary, you can use `stop` instead of `down` to stop the containers but retain the persistence.


## Running the the web server in Docker against another ledger

1. Run docker to start the ledger, and pass in GENESIS_URL and LEDGER_SEED parameters:

For example to connect to the STN:

```bash
./manage start-web \
   GENESIS_URL=https://raw.githubusercontent.com/sovrin-foundation/sovrin/master/sovrin/pool_transactions_sandbox_genesis
```


## Running the the web server on your local machine

You can run the web server/ledger browser on its own, and point to another Indy/Sovrin network.

1. Install python and pip (recommend to use a virtual environment such as virtualenv)

2. Download this repository:

```bash
git clone https://github.com/bcgov/von-network.git
cd von-network
```

3. If using virtualenv, setup a virtual environment and activate it:

```bash
virtualenv --python=python3.6 venv
source venv/bin/activate
```

4. Install requirements:

```bash
pip install -r server/requirements.txt
```

5. Run the server, you can specify a genesis file, or a url from which to download a genesis file - you can also specify a seed for the DID to use to connect to this ledger:

```bash
GENESIS_FILE=/tmp/some-genesis.txt PORT=9000 python -m server.server
```

Or:

```bash
GENESIS_URL=https://some.domain.com/some-genesis.txt LEDGER_SEED=000000000000000000000000SomeSeed PORT=9000 python -m server.server
```

For example to connect to the STN:

```bash
GENESIS_URL=https://raw.githubusercontent.com/sovrin-foundation/sovrin/master/sovrin/pool_transactions_sandbox_genesis LEDGER_SEED=000000000000000000000IanCostanzo PORT=9000 python -m server.server
```

## Running the Network on a VPS

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
    curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
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

4. Build the Docker container:

    ```bash
    ./manage build
    ```

5. Run the network of nodes:

    ```bash
    # This command requires the publicly accessible ip address of the machine `public_ip_address`
    # WEB_SERVER_HOST_PORT maps the docker service port to a public port on the machine
    # LEDGER_INSTANCE_NAME sets the display name of the ledger on the page headers.
    ./manage start public_ip_address WEB_SERVER_HOST_PORT=80 "LEDGER_INSTANCE_NAME=My Ledger" &
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

## Extra Features for Development

Running BCovrin also runs a thin webserver (at [http://localhost:9000](http://localhost:9000) when using docker) to expose some convenience functions:


#### Genesis Transaction Exposed

The genesis transaction record required to connect to the node pool is made available at:

`<ip_address>/genesis`

#### Write new did for seed

The node pool can have a trust anchor write a did for you. That feature is available in the UI.

## Customize your Ledger Browser Deployment

It is possible to customize some of the aspects of the Ledger Browser at run-time, by using the following environment variables:

- `REGISTER_NEW_DIDS`: if set to `True`, it will enable the user interface allowing new identity owners to write a DID to the ledger. It defaults to `False`.
- `LEDGER_INSTANCE_NAME`: the name of the ledger instance the Ledger Brwoser is connected to. Defaults to `Ledger Browser`.
- `INFO_SITE_URL`: a URL that will be displayed in the header, and can be used to reference another external website containing details/resources on the current ledger browser instance.
- `INFO_SITE_TEXT`: the display text used for the `INFO_SITE_URL`. If not specified, it will default to the value set for `INFO_SITE_URL`.
- `WEB_ANALYTICS_SCRIPT`: the JavaScript code used by web analytics servers. Populate this environment variable if you want to track the usage of your site with Matomo, Google Analytics or any other JavaScript based trackers. Include the whole ```<script type="text/javascript">...</script>``` tag, ensuring quotes are escaped properly for your command-line interpreter (e.g.: bash, git bash, etc.).
- `LEDGER_CACHE_PATH`: if set, it will instruct the ledger to create an on-disk cache, rather than in-memory.  The image supplies a folder for this purpose; `$HOME/.indy_client/ledger-cache`.  The file should be placed into this directory (e.g.: `/home/indy/.indy-client/ledger-cache/ledger_cache_file` or `$HOME/.indy_client/ledger-cache/ledger_cache_file`).
