# VON Network
A portable development level Indy Node network.

## Running the Network

First, install Docker. Download the installer for your operating system [here](https://store.docker.com/search?type=edition&offering=community). Once it is installed, keep the Docker daemon running in the background.

Once Docker has been installed, open a terminal session and clone this repository:

```bash
git clone <repository url> von-network
```

Move to the new directory:

```bash
cd von-network
```

Now you can build the Dockerfile into an image which we will use to run containers (this process will take several minutes):

```bash
./manage build
```

Once the build process completes, you can test the build to make sure everything works properly:

```bash
./manage start
```

## Connecting to the Network

Once the nodes are all running and have connected to each other, you can run the Indy client to test the connection in a separate terminal window:

```bash
./manage cli
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
connect test
```

What you should see is:

```
indy> connect test
New wallet Default created
Active wallet set to "Default"
Active wallet set to "Default"
Client indy9f7060 initialized with the following node registry:
    Node1C listens at 172.21.0.2 on port 9702
    Node2C listens at 172.21.0.5 on port 9704
    Node3C listens at 172.21.0.3 on port 9706
    Node4C listens at 172.21.0.4 on port 9708
Active client set to indy9f7060
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ listening for other nodes at 0.0.0.0:6001
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ looking for Node1C at 172.21.0.2:9702
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ looking for Node2C at 172.21.0.5:9704
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ looking for Node3C at 172.21.0.3:9706
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ looking for Node4C at 172.21.0.4:9708
Connecting to test...
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node1C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node2C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node3C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node4C
CATCH-UP: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ completed catching up ledger 0, caught up 0 in total
Connected to test.
```

**Specifically**:

```
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node1C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node2C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node3C
CONNECTION: iSLwBzaiCrnG5LBv4MmM18TGwY8RNquYwMMx2az6BNQ now connected to Node4C
...
Connected to test.
```

If you see this, congratulations! Your nodes are running correctly and you have a connection to the network.
