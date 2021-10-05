# Tutorial: Using VON Network<!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Building and Starting](#building-and-starting)
- [Browsing the Ledger](#browsing-the-ledger)
- [Viewing Transactions](#viewing-transactions)
- [Creating a DID](#creating-a-did)
- [Viewing the Genesis File](#viewing-the-genesis-file)
- [Using the CLI](#using-the-cli)
- [Stopping and Removing a VON Network](#stopping-and-removing-a-von-network)
- [Next Steps](#next-steps)

This tutorial provides guidance for newcomers on what you can do with a running VON Network instance.

## Prerequisites

We recommend going through this tutorial on your local docker instance or on [Play with Docker](https://labs.play-with-docker.com/). If you new are new to either, use this guidance on getting set up with a [local docker instance](https://github.com/cloudcompass/ToIPLabs/blob/master/docs/LFS173x/RunningLabs.md#running-on-docker-locally) or [Play with Docker](https://github.com/cloudcompass/ToIPLabs/blob/master/docs/LFS173x/RunningLabs.md#running-on-play-with-docker).

## Building and Starting

Begin by getting to a `bash` command line and clone the `von-network `repo:

```
git clone https://github.com/bcgov/von-network
cd von-network

```

Once the repo has been cloned, we'll build docker images for the VON Network and then start your Indy network:


```
./manage build
./manage start --logs

```

As the nodes of the Indy network start up, monitor the logs for error messages. Note the `--logs` entry on the start command. Once you get used to running a VON Network instance, you may want to leave that parameter off so you get right back to the command line for whatever else you are doing.

The [`./manage`](../manage) bash script simplifies the process of running the VON Network, providing the common entry points that you need to use. It also provides a number of environment variables you can use to customize the running of the script.

The docker container images are built using scripts that encapsulate the steps to create `indy-node` from scratch, starting with base Docker images that contain all necessary prerequisites. The base images are created once per `indy-node` release, so that the entire community can benefit from that work.

To see what you can do with the script `./manage`, after your network is running (from the commands above), hit Ctrl-C in the terminal to get back to the command prompt. Your network is still running. Run the command with no arguments to see the usage info for the script.

```
./manage

```

If you want to get back to seeing the logging data from the nodes, run with the “logs” parameter:

```
./manage logs

```

## Browsing the Ledger

Once the ledger is running, you can see the ledger by going to the web server running on port 9000. On localhost, that means going to [http://localhost:9000](http://localhost:9000).
If you are using Play with Docker, click on the "9000" link in the header of the page--that will open up the page on which the web server is running.
If you don't see the VON Network web server, or there are error messages, check the logs in your terminal session.

From VON Network web server you can:

*   See the status of the nodes of the network.
*   Look at the genesis file for the network.
*   Create a DID.
*   Browser the three ledgers that make up an Indy network:
    *   The Domain ledger, where the DIDs, schema, etc. reside.
    *   The Pool ledger, where the set of nodes on the network are tracked.
    *   The Config ledger, where changes to the network configuration are tracked.

## Viewing Transactions

Click the “Domain Ledger” link from the main menu to see the transactions on the ledger. On a brand new ledger, there will be five transactions, the first for the trustee DID and the next four for each of the stewards on the network. The stewards are the operators of the four nodes operating on the network.

**Note:** _You can search on the ledger by transaction type or by the text in the transactions. For example, in the “Filter,” type “trustee” and hit enter. The four “steward” transactions will be hidden and you will see just one transaction. Not too useful with only five transactions on the ledger, but really useful when there are 100,000!_

## Creating a DID

To create a DID, go to the Ledger Browser (at port 9000) and find the “Authenticate a New DID” section. There are various options, but we’ll do the simplest case:

1. Make sure that “Register from Seed” is selected.
2. Type your first name in the “Wallet Seed” field, and your full name in the “Alias” field.
3. Click “Register DID.”

You should get a response back with the details of the newly created DID.

1. Next, go to the Domain Ledger and find the transaction. Put the alias you used for the DID in the filter to see that you can search for the DID.

## Viewing the Genesis File

From the main menu of the Ledger Browser, click on the “Genesis Transaction” link to see the genesis file for the network. When running a VON Network instance with the Ledger Browser, you always get the genesis file from the /genesis endpoint—which is something we can use as a startup parameter for an Aries agent. 

If you want to see the connection between the genesis file and the ledger entries, copy and paste the “from” item value from one of the lines of the genesis file (e.g. “`TWwCRQRZ2ZHMJFn9TzLp7W`”), and then go back to the Domain Ledger and search for a transaction with that same ID.

**Note:** _The DIDs in the genesis file (the “from” values) are the same for any instance of an indy sandbox ledger, hence the ID in the previous paragraph. Once you are using production (or production-like) ledgers, the contents of the files will be different._

Another thing to notice about the ledger file is the IP addresses for the ledger nodes. Since the nodes are running in a Docker container, the IP address is that of the Docker container, not localhost. One of the benefits of using the VON Network is that it takes care of details like that, making sure that the genesis file is always accurate for the network that is running.

## Using the CLI

`von-network` provides a way to get to an Indy command line interface (CLI). To get to the Indy CLI for the network, get to the command prompt (using Ctrl-C if necessary) and run the command:

```
./manage indy-cli
```

Run the “help” command to see what you can do, and “exit” to get out of the CLI session.

We won’t go into the Indy CLI here, but it has powerful capability that you can use to create scripts for configuring an Indy network and adding objects to the ledger. If you find any Indy CLI tutorials on other sites, you can run them using this mechanism, without any of the bother of getting everything running before you start the CLI.

For more information refer to [Using the containerized `indy-cli`](./Indy-CLI.md)

## Stopping and Removing a VON Network

To stop and delete a running VON Network, get to a command line prompt (using Ctrl-C if necessary), and then run the command:

```
./manage down

```

You would normally do that when you have done some development, completed your testing and want to start again fresh.

If you want to stop the network **WITHOUT** deleting the data on the ledger, use the following command: 

```
./manage stop

```

You can later restart the ledger by running the normal command for starting the network:

```
./manage start

```

Make sure that you keep your agent storage and ledger in sync. If you delete/reset one, delete/reset the other.

## Next Steps

The [README](../README.md) for the repo contains information on various options for running VON Network instances, and how you can access publicly accessible instances so you don't have to run your own.
