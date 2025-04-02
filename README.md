[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Lifecycle:Stable](https://img.shields.io/badge/Lifecycle-Stable-97ca00)](https://github.com/bcgov/repomountie/blob/master/doc/lifecycle-badges.md)

# VON Network

A portable development level Indy Node network, including a Ledger Browser. The Ledger Browser (for example the BC Gov's [Ledger for the GreenLight Demo Application](http://greenlight.bcovrin.vonx.io/)) allows a user to see the status of the nodes of a network and browse/search/filter the Ledger Transactions.

`von-network` is being developed as part of the Verifiable Organizations Network (VON). For more information on VON see https://vonx.io.  Even, better - join in with what we are doing and contribute to VON, Aries and Indy communities.

# VON Network is Not a Production Level Indy Node Network

VON Network is not a production level Indy Node network.  It was designed as a provisional network for development and testing purposes only.  It provides you with an exceptionally simple way to spin up an Indy Node network, but is lacking many of the features and safeguards needed for a production level network.

VON Network is provided as is for development and testing.  Please do not use it for production environments.

## The VON-Network Ledger Browser and API

With the Ledger Browser (for example: [http://greenlight.bcovrin.vonx.io/](http://greenlight.bcovrin.vonx.io/)), you can see:

- The status of the Ledger nodes
- The detailed status of the Ledger Nodes in JSON format (click the "Detailed Status" link)
- The three ledger's of an Indy Network - Domain, Pool and Config (click the respective links)
- The Genesis Transactions for the Indy Network instance.
  - In an Indy Agent, use the URL `<server>/genesis` to GET the genesis file to use in initializing the Agent.

By using the "Authenticate a new DID" part of the UI or posting the appropriate JSON to the VON-Network API (see an example script [here](https://github.com/bcgov/von-agent-template/blob/d1abcbeaa299ce6149570349848bb51716752457/init.sh#L90)), a new DID can be added to the Ledger. A known and published *Trust Anchor* DID is used to write the new DID to the Ledger.  This operation would not be permitted in this way on the Sovrin Main Network. However, it is a useful mechanism on sandbox Indy Networks used for testing.

In the `Domain` Ledger screen ([example](http://greenlight.bcovrin.vonx.io/browse/domain)), you can browse through all of the transactions that have been created on this instance of the Ledger.  As well, you can use a drop down filter to see only specific Ledger transaction types (`nym` - aka DID, `schema`, `CredDef`, etc.), and search for strings in the content of the transactions.

## VON Network Quick Start Guide

New to VON Network?  We have a [tutorial about using VON Network](docs/UsingVONNetwork.md) to get you started.

Note that in order to use Docker Desktop (> version 3.4.0), make sure you uncheck the "Use Docker Compose V2" in Docker Desktop > Preferences > General.  Refer to this issue for additional details; [#170](https://github.com/bcgov/von-network/issues/170#issuecomment-972898014)



Want to see a full demo that includes applications and verifiable credentials being issued? The [VON Quick Start Guide](https://github.com/bcgov/greenlight/blob/master/docker/VONQuickStartGuide.md) provides the instructions for running a local instance of a full demo of the components, including an Indy Network, an instance of [TheOrgBook](https://github.com/bcgov/TheOrgBook) and [GreenLight](https://github.com/bcgov/greenlight). This is a great way to see the **VON Network** in action.

## Indy-Cli Container Environment

This repository includes a fully containerized Indy-Cli environment, allowing you to use the Indy-Cli without having to build or install the Indy-SDK or any of its dependencies on your machine.

For more information refer to [Using the containerized `indy-cli`](./docs/Indy-CLI.md)

## Ledger Troubleshooting

Refer to the [Troubleshooting](./docs/Troubleshooting.md) document for some tips and tools you can use to troubleshoot issues with a ledger.

## VON Quick Start Guide
The environment provides a set of batch script templates and a simple variable substitution layer that allows the scripts to be reused for a number of purposes.

For examples of how to use this capability, refer to [Writing Transactions to a Ledger for an Un-privileged Author](./docs/Writing%20Transactions%20to%20a%20Ledger%20for%20an%20Un-privileged%20Author.md)

## Running the Network Locally

The [tutorial about using VON Network](docs/UsingVONNetwork.md) has information on starting (and stopping) the network locally.

## Running the web server in Docker against another ledger


1. Run docker to start the ledger, and pass in GENESIS_URL and LEDGER_SEED parameters:

For example to connect to the Sovrin Test Network:

```bash
./manage build
GENESIS_URL=https://raw.githubusercontent.com/sovrin-foundation/sovrin/master/sovrin/pool_transactions_sandbox_genesis ./manage start-web
```

Note that it takes some time to get the transactions and status from the network. Once the UI appears, try getting the `Genesis Transaction` that the server started up properly.

## Running the web server on your local machine

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
    curl -L https://github.com/bcgov/von-network/archive/main.zip > bcovrin.zip && \
        unzip bcovrin.zip && \
        cd von-network-main && \
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

### AWS EC2 Security considerations

If you are installing on an Amazon EC2 node you may find the Indy nodes are failing to connect to each other. The signature for this will be a repeating message every 60 seconds when you view the logs via "./manage log"

```bash
node2_1 | 2020-05-07 23:56:30,728|NOTIFICATION|primary_connection_monitor_service.py|Node2:0 primary has been disconnected for too long
node2_1 | 2020-05-07 23:56:30,729|INFO|primary_connection_monitor_service.py|Node2:0 The node is not ready yet so view change will not be proposed now, but re-scheduled.
node2_1 | 2020-05-07 23:56:30,730|INFO|primary_connection_monitor_service.py|Node2:0 scheduling primary connection check in 60 sec
node2_1 | 2020-05-07 23:56:30,730|NOTIFICATION|primary_connection_monitor_service.py|Node2:0 primary has been disconnected for too long
node2_1 | 2020-05-07 23:56:30,730|INFO|primary_connection_monitor_service.py|Node2:0 The node is not ready yet so view change will not be proposed now, but re-scheduled.
```

The Indy nodes are configured to talk to each other via their "public" address not the Virtual Private Cloud address of the EC2 node. It is common practice to tightly restrict traffic inbound to public IPs when first setting up a deployment in AWS.  You will need to adjust the Inbound and Outbound traffic rules on your Security Groups to allow traffic specifically from the public EC2 address.


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

It is possible to customize some of the aspects of the Ledger Browser at run-time, by using the following environment variables.  Defaults are listed in the [`<default-state>`] brackets beside each variable:

- `REGISTER_NEW_DIDS` [`False`]: When set to `True` the "Authenticate a New DID" interface will be enabled, allowing new identity owners to write a DID to the ledger.  When set to `False` the interface and associated API will be disabled.

- `ENABLE_LEDGER_CACHE` [`True`]: Enables the ledger cache used for the built in ledger browsing features. Setting to `False` disables the cache, which is useful when you only want to use the browser for monitoring the nodes.

- `ENABLE_BROWSER_ROUTES` [`True`]: Enables the ledger browser API used by the  built in ledger browsing features. Setting to `False` disables the ledger browser API, which is useful when you only want to use the browser for monitoring the nodes.

- `DISPLAY_LEDGER_STATE` [`True`]: Enables the ledger state interface which contains the links to browse the state of the ledgers. Setting to `False` disables the interface.

- `LEDGER_INSTANCE_NAME` [`Ledger Browser`]: The name of the ledger instance the browser is connected to.

- `LEDGER_DESCRIPTION` [`Contributed by the Province of British Columbia`]: A description of the ledger instance.

- `INFO_SITE_TEXT` [value of `INFO_SITE_URL`]: The display text used for the `INFO_SITE_URL`.

- `INFO_SITE_URL`: A URL that will be displayed in the header, and can be used to reference another external website containing details/resources on the current ledger instance.

- `WEB_ANALYTICS_SCRIPT` [`<empty>`]: the JavaScript code used by web analytics servers. Populate this environment variable if you want to track the usage of your site with Matomo, Google Analytics or any other JavaScript based trackers. Include the whole ```<script type="text/javascript">...</script>``` tag, ensuring quotes are escaped properly for your command-line interpreter (e.g.: bash, git bash, etc.).

- `LEDGER_CACHE_PATH` [`<empty>`]: If set, it will instruct the ledger browser to create an on-disk cache, rather than in-memory cache.  The image supplies a folder for this purpose; `$HOME/.indy_client/ledger-cache`.  The file should be placed into this directory (e.g.: `/home/indy/.indy-client/ledger-cache/ledger_cache_file` or `$HOME/.indy_client/ledger-cache/ledger_cache_file`).

- `INDY_SCAN_TEXT` [value of `INDY_SCAN_URL`]: The display text used for the `INDY_SCAN_URL`.

- `INDY_SCAN_URL` [`<empty>`]: The URL to the external IndyScan ledger browser instance for the network.  This will replace the links to the builtin ledger browser tools.

## Using IndyScan with VON Network

[IndyScan](https://github.com/Patrik-Stas/indyscan) is production level transaction explorer for Hyperledger Indy networks.  It's a great tool for exploring and searching through the transactions on the various ledgers.

You might be asking...  Why would I want to use IndyScan with `von-network`, when `von-network` has a built-in ledger browser?

The short answer is performance at scale.  The built-in ledger browser works great for most local development purposes.  However, it starts running into performance issues when your instance contains over 100,000 transactions.  IndyScan on the other hand is backed by Elasticsearch and can easily scale well beyond that limitation.  So if you're hosting an instance of `von-network` for your organization to use for testing, like BC Gov does with [BCovrin Test](http://test.bcovrin.vonx.io/), you'll want to look into switching over to IndyScan as your ledger browser.

To use IndyScan as your ledger browser for `von-network`, you're responsible for setting up and hosting your own instance of IndyScan.  Please refer to the [IndyScan](https://github.com/Patrik-Stas/indyscan) repository for information on how to accomplish this.  Once your IndyScan instance is up and running you can configure your `von-network` instance to provide a link to it on the main page by using the `INDY_SCAN_URL` and `INDY_SCAN_TEXT` variables described in the previous section.  The link to your IndyScan instance will replace the links to `von-network`'s built in ledger browser tools.

## Contributing

**Pull requests are always welcome!**

Please see the [Contributions Guide](./CONTRIBUTING.md) for the repo.

You may also create an issue if you would like to suggest additional resources to include in this repository.

All contrbutions to this repository should adhere to our [Code of Conduct](./CODE_OF_CONDUCT.md).
