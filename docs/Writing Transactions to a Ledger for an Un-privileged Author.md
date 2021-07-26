# Production Writes

## Introduction

In this document, we mimic an entity writing Indy objects (schema and credential definition) to a production ledger where that entity (the transaction author) does not have full write permission to the ledger. To be permitted to execute the writes, the transaction author must create the transactions, sign them and get an endorser (who has write permissions) to sign the transactions before the transactions can be submitted to the ledger.

The process uses a fully containerized Indy-CLI environment so there is no need to have the Indy-CLI or any of its dependencies installed on your machine. You can generalize the procedure to write transactions to any ledger by initializing the containerized Indy-CLI environment with the genesis file from the desired pool and tweaking the commands presented below.

## Things We Don't Cover

There are a few things we don't cover in this workshop.

On the Sovrin MainNet production network, the transaction author and endorser must agree to legal documents based on their role (author or endorser), and a payment is required for the writes. The Transaction Author Agreement (TAA) must be agreed to online, while the Transaction Endorser Agreement is a more formal agreement that is physically signed by the parties involved. We don't cover those parts of the process.

How the DIDs for the author and endorser formally get created on a production ledger is not covered. In the workshop, we use the VON Network's "Register DID" capability to create the DIDs. Further, we don't cover how an author gets connected with an endorser. In this example, we assume that both are together on the same system. We'll point out where text files would be transferred between the participants to complete the process. Note that there is no private information (no private keys) in the shared text files, so there is no need for special handling requirements for the files. The files contain the same data that will be written to the ledger, plus some cryptographic signatures.

## Process Automation

The process we'll go through is very manual. At the time of writing this, that's OK (if a bit/very painful) because to now there have been few issuers, and each has few credentials they issue (and hence few objects to write to the ledger). As the volume of transactions increases, this will process **must** become automated. Perhaps those developers going through this document will be the ones to automate the process!

## Agent Storage Management

During this process, the transaction author builds up the contents of their agent storage (aka Indy Wallet) that they will later use in their running agent. As such, the contents of the wallet must be carefully preserved&mdash;backed up and available for restoration whenever needed. We'll only show the process for backing up agent storage once, but will indicate where you might want to backup the agent storage during the process. We will also use a very simple key&mdash;the word "key"&mdash;but for a production system we would use a more formal process.

## Scenario

We are borrowing a scenario from the BC Government's [VON](https://vonx.io) project. We'll be running an instance of the VON Network (an Indy ledger), and two agents:

- an instance of TheOrgBook, a verifiable credential holder, and
- a VON Issuer, an instance of an issuer of verifiable credentials.

In our scenario, the VON Issuer is new and must create a new schema and credential definition on the ledger. As well, we'll have an endorser available. The endorser will not be running an agent, but will have a agent storage (for it's DID). The endorser will only use the Indy Command Line Interface (CLI).

## Process Overview

During this process, we'll initialize all of the participants, and then will write the two objects (a schema and credential definition) to the ledger. During initialization, we'll see that the issuer agent will not be able to find or create (because they lack permissions) the objects they need to issue credentials.

For each object (the schema and credential definition) to be written to the ledger, the following must occur:

1. The issuer agent (transaction author) creates the object in their wallet.
2. The issuer extracts the ledger parts of the object from the wallet, cryptographically signs the object, and saves it to a file.
3. The endorser accesses the signed transaction file, cryptographically signs the object, and saves it to a new file.
4. The issuer submits the file with the doubly signed transaction and submits it to the Indy network to be written to the ledger.
5. The Indy network verifies the signatures and the permissions of the referenced DIDs, and if all is valid, writes the transaction to the ledger.

Since there are two objects, we'll go through those steps twice. At the end of the process, we'll restart the issuer agent, verify that it can start and issue a credential.

**Note:** *In this example the `DHOST` variable is set with the DockerHost IP address.  This (correctly) assumes the wallet to which you are connecting is hosted in docker.  If you are, instead, post forwarding the wallet database, review the **Pro Tips** section at the end of this document for additional details.*

## The Production Writes Workshop

To get started, open a bash shell on your local system that is capable of running git and docker. If you need more information about the prerequisites, you can [learn more here](https://github.com/cloudcompass/ToIPLabs/blob/master/docs/LFS173x/RunningLabs.md#running-on-docker-locally). We'll be cloning three repos, so we recommend that you start in an empty directory that will be easy to clean up after the process.

If things go wrong, there are instructions at the [end of this document](#resetting-the-environment) for resetting everything so you can start again.

### Clone the Repos and Build

We'll start by getting the repositories, building the code and initializing each one. Change to the directory you are going to run this process and copy the following steps and paste them into your shell. The builds will take some time.

```bash
git clone https://github.com/bcgov/von-network
pushd von-network
./manage build
mkdir tmp
chmod a+rws tmp cli-scripts
export DHOST=$(./manage dockerhost | sed '/^$/d;s~DockerHost:[[:space:]]~~') && echo "DHOST set to ${DHOST}"
export key=key
popd
git clone https://github.com/bcgov/TheOrgBook
pushd TheOrgBook/docker
./manage build
popd
git clone https://github.com/bcgov/von-agent-template

```

**Check**: You should be back at the command line in the same directory you started.

### Create the DIDs

Start VON-Network by copying and pasting the following into the terminal:

```bash
pushd von-network
./manage start
popd

```

Wait about 20 seconds and then in your browser go to [http://localhost:9000](http://localhost:9000), which is the ledger browser for the Indy network you just started. If you get there too soon (before the network comes up), just hit refresh. On the right side of the screen, got to the `Register DIDs` section and create the following DIDs with the following roles:

- `the_org_book_0000000000000000000`, role "(None)"
  - Check that the DID is `25GuF6zjiywpU1iF4kNJPQ` and the Verkey is `awcJaDCU36RQxeqMeRKcrVHvXRZU3Ysbj6sCf6W7Q6A`
- `0000000000000000000000000MyAgent`, role "(None)"
  - Check that the DID is `NFP8kaWvCupbDQHQhErwXb` and the Verkey is `Cah1iVzdB6UF5HVCJ2ENUrqzAKQsoWgiWyUopcmN3WHd`
- `ENDORSER123450000000000000000000`, role "Endorser"
  - Check that the DID is `DFuDqCYpeDNXLuc3MKooX3` and the Verkey is `7gTxoFyCpMGfxuwBNXYn1icuyh8DqDpRGi12hj5S2pHk`

**Check**: Make sure the DIDs have the proper roles and you are back to the starting directory in the terminal session.

### Initialize the Indy CLI for the Author and Endorser

Run the following commands to initialize the Indy Command Line Interface (CLI) for the author and endorser:

```bash
pushd von-network
./manage cli reset; ./manage cli init-pool localpool http://${DHOST}:9000/genesis
```

**Check**: You should see the successfully completion of the two `cli` commands. Run the following command to return to the starting directory run:

```bash
popd

```

### Start the TheOrgBook

Start TheOrgBook by running the following commands:

```bash
pushd TheOrgBook/docker
seed=the_org_book_0000000000000000000 AUTO_REGISTER_DID=0 LEDGER_URL=not_used GENESIS_URL=http://${DHOST}:9000/genesis ./manage start

```

You will see the logs of TheOrgBook starting up. Wait for about 20 or 30 seconds looking for errors until the logging slows down. Hit Ctrl-C to return to the command line, and then run the following to return to the starting directory run:

```bash
popd

```

Check: To verify TheOrgBook started successfully, in your browser go to [http://localhost:8080](http://localhost:8080) to see the home page of TheOrgBook. Your terminal session should be back at the starting directory.

### Initialize and Start the Issuer Agent

Now it's time to start the Issuer agent. This is the one step in the process that you **should** see an error. The error will be because the Issuer agent does not have sufficient permissions to put a schema and credential definition on the ledger. Run the following to make that happen.

```bash
pushd von-agent-template
./init.sh <<-EOF
Ian Company
ian-co
ian-permit
2
EOF
cd docker
./manage build
INDY_LEDGER_URL="http://${DHOST}:9000" AUTO_REGISTER_DID=0 INDY_GENESIS_URL=http://${DHOST}:9000/genesis WALLET_SEED_VONX=0000000000000000000000000MyAgent ./manage start

```

You will see the logs of the agent starting up, until it gets to a point where an error message is printed about not being able to create the schema on the ledger (`Ledger rejected transaction request`) because the Issuer agent's DID lacks permission. That's expected and is what we will do in the remaining steps to fix.

Hit Ctrl-C to return to the command line, and then run the following to return to the starting directory run:

```bash
popd
pushd von-network

```

**Check**: The agent started up and displayed the expected error message. Your terminal session should be in the root of the `von-network` repo clone. We'll work from there for the rest of the process.

### Backing up Indy Agent Storage

Now that we're initialized, we'll perform a backup of the Issuer agent's wallet. Right now it only has a DID in it, and if needed we could recreate it if necessary. However, once it has a credential definition in it, it cannot be created from scratch. As such, doing a production run of this process, we recommend backing up agent storage on each step.

To backup the wallet, run the command below. When prompted, enter `key` for both the wallet key and the export key. Obviously, in a production deploy you would use more secure keys, let alone the fact that you would not type them into a terminal session!

```bash
./manage \
  indy-cli export-wallet \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"${DHOST}:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  exportPath=/tmp/myorg_issuer_wallet_initialized_with_did.export
```

**Check**: The command should run without an error and the backup created in the `tmp` folder of the current directory. Use `ls tmp` to see that the export file is created. The export file is an encrypted version of the wallet export.

**If** any of the `cli` command fail (generates an error) and you are left at a prompt `indy>`, you are still in the Indy CLI. To continue, do the following:

- Run: `wallet list` to get a list of the active wallets. There should be one.
- Run: `wallet detach <wallet>` using the name of the active wallet (either `myorg_issuer` or `endorser_wallet`).
- Run: `exit`

That will return you to the command line and (hopefully!) you can correct and retry the command that failed.  Worst case, clean up the environment (instructions at the bottom of this document) and start again.

### Create the Signed Schema Transaction File

After all that, we are ready to **start** the transaction creation/execution process. Finally!

The transaction author will execute this command to create the schema, sign it, prepare it for the endorser to sign and export the signed transaction to a text file.

In the following note a number of things are hard-coded, including the the schema name (`permit.ian-co`), version (`1.0.0`), and attributes. Normally, we would do something like use a set of environment variables in a script to define those for each run of this process.

```bash
./manage \
  indy-cli create-signed-schema \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"${DHOST}:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  schemaName=ian-permit.ian-co \
  schemaVersion=1.0.0 \
  schemaAttributes=corp_num,legal_name,permit_id,permit_type,permit_issued_date,permit_status,effective_date \
  outputFile=/tmp/ian-permit.ian-co_author_signed_schema.txn
```

**Check**: The command runs without an error and the transaction file is created. To review it, you can run:

```bash
cat tmp/ian-permit.ian-co_author_signed_schema.txn; echo ""

```

In a production use case, you might want to backup the wallet again at this point.

### Endorsing the Schema Transaction

The next step is run by the endorser. First we'll create the endorser's wallet using the following command:

```bash
./manage \
  indy-cli create-wallet \
  walletName=endorser_wallet
```
When prompted for the `seed` enter `ENDORSER123450000000000000000000`.

Next, the endorser will execute the following command to read in the file with the signed transaction from the author, sign it, and write out the doubly signed version of the transaction. The endorser can get the file from the author in whatever way is convenient&mdash;email, file transfer, etc.

```bash
./manage \
  indy-cli endorse-transaction \
  walletName=endorser_wallet \
  poolName=localpool \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_author_signed_schema.txn \
  outputFile=/tmp/ian-permit.ian-co_endorser_signed_schema.txn
```

**Check**: The command runs without an error and the transaction file is created. To review it, you can run:

```bash
cat tmp/ian-permit.ian-co_endorser_signed_schema.txn; echo ""

```

### Write the Schema Transaction to the Ledger

Finally, we get to update the ledger! Either the author or the endorser (or anyone else) can perform this step&mdash;what matters is that both the endorser and the author have signed the transaction.

```bash
./manage \
  indy-cli write-transaction \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_endorser_signed_schema.txn
```

After this executes, you have to find and set an environment variable based on the output of the step. Scan the text to find the string `seqNo` and get the number that follows. Likely it is `10`. Run the following command, replacing the `10` with whatever number you found:

```bash
export schemaID=10
```

**Check**: Barring errors, the schema has been written to the ledger. Go to the ledger browser ([http://localhost:9000](http://localhost:9000)), click on the `Domain` link (near the bottom) and scan/filter the transactions to find the new schema.

### Create the Credential Definition

With the schema now written, it's time to repeat the steps to write the credential definition.

The first step of the process is for the transaction author to create the credential definition in their wallet. Use the following command to do that:

```bash
./manage \
  -v ${PWD}/cli-scripts/ \
  cli \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"${DHOST}:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  walletKey=${key} \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  schemaId=${schemaID} \
  schemaName=ian-permit.ian-co \
  schemaVersion=1.0.0 \
  schemaAttributes=corp_num,legal_name,permit_id,permit_type,permit_issued_date,permit_status,effective_date \
  tag=tag \
  python cli-scripts/cred_def.py
```

A by-product of running this script is that the information needed for the credential definition is exported into a text file. We'll use that in the next step to create the transaction that will be submitted to the ledger.

**Check**: The command runs without an error. To look at the attributes that will be put on the ledger, run the following:

```bash
cat tmp/primarykey.txt
```

You'll see the file contains a lot of very large numbers that will be used by the cryptographic routines that construct a verifiable credential and verify the claims from a verifiable credential.

In a production run, this would be a good time to make another backup of the agent wallet.

### The Author Signs the Transaction

Now that the credential definition has been created and we have the ledger attributes to be written, the author has to create and sign the ledger transaction. Run the following command to do that.

```bash
./manage \
  indy-cli create-signed-cred-def \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"${DHOST}:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  schemaId=${schemaID} \
  signatureType=CL \
  tag=tag \
  primaryKey='$(cat tmp/primarykey.txt)' \
  outputFile=/tmp/ian-permit.ian-co_author_signed_cred_def.txn
```

**Check**: The command runs without an error and the transaction file is created. To review it, you can run:

```bash
cat tmp/ian-permit.ian-co_author_signed_cred_def.txn

```

### The Endorser Signs the Transaction

The endorser will execute the following command to read in the file with the signed transaction from the author, sign it, and write out the doubly signed version of the transaction. This is the same process that we did for the schema.

```bash
./manage \
  indy-cli endorse-transaction \
  walletName=endorser_wallet \
  poolName=localpool \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_author_signed_cred_def.txn \
  outputFile=/tmp/ian-permit.ian-co_endorser_signed_cred_def.txn
```

**Check**: The command runs without an error and the transaction file is created. To review it, you can run:

```bash
cat tmp/ian-permit.ian-co_endorser_signed_cred_def.txn

```

### Write the Credential Definition Transaction to the Ledger

Last step&mdash;write the credential definition to the ledger! Again, either the author or the endorser (or anyone else) can perform this step.

```bash
./manage \
  indy-cli write-transaction \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_endorser_signed_cred_def.txn
```

**Check**: Barring errors, the credential definition has been written to the ledger. Go to the ledger browser ([http://localhost:9000](http://localhost:9000)), click on `Domain` and scan/filter the transactions to find the newly written transaction.

### Restart the Agent

With that, the writing is done, and we should be able to successfully run the Issuer agent. Run the following commands to restart the Issuer agent. Of course, we have to do that **WITHOUT** the Issuer agent's wallet being deleted. The `stop` option of the `./manage` script stops the agent but preserves the storage.

```bash
cd ../von-agent-template/docker
./manage stop
INDY_LEDGER_URL="http://${DHOST}:9000" AUTO_REGISTER_DID=0 INDY_GENESIS_URL=http://${DHOST}:9000/genesis WALLET_SEED_VONX=0000000000000000000000000MyAgent ./manage start

```

**Check**: The Agent should start up without errors, getting past the `permission denied` error we saw earlier. Success! The agent storage and the ledger are in sync. As another check, let's issue a credential.  Run the command below:

```bash
curl -X POST \
  http://localhost:5001/ian-co/issue-credential \
  -H 'content-type: application/json' \
  -d '[
  {
    "attributes": {
        "corp_num": "1234567890",
        "legal_name": "My Test Corp",
        "permit_id": "123834234234999",
        "permit_type": "Unlimited Use Authorization",
        "permit_issued_date": "2020-03-07T08:00:00+00:00",
        "permit_status": "ACT",
        "effective_date": "2020-03-07T08:00:00+00:00"
    },
    "schema": "ian-permit.ian-co",
    "version": "1.0.0"
  }
]
'
```

If you see `"success": true`, the credential was issued. **Done**!!!

To get back to the starting directory so that you can reset the environment, run:

```bash
popd

```

Go ahead and say it: *That was easy*!

## Resetting the Environment

Once you are through the exercise, or you if want to start again, here's a set of commands you can run to reset the environment. Before running this, change to the starting directory, the one containing the cloned directories.  The `rm` option on each of the `./manage` commands stops the docker containers and removes the persisted data related to the containers.

**NOTE:** If you don't run these commands, the docker containers will still be running. Make sure you run the commands to clean up the environment.

```bash
pushd von-network
rm -f tmp/*
./manage rm
popd
pushd TheOrgBook/docker
./manage rm
popd
pushd von-agent-template/docker
./manage rm
popd

```

# Pro Tips

## Connecting to a Wallet Hosted on OpenShift

### Port forward your agent's wallet database to your local machine.

For example:
```
oc -n devex-von-bc-registries-agent-dev port-forward wallet-db-3-xcp56 5444:5432
```

*This will port forward wallet-db-3-xcp56:5432 to localhost:5444.*

### Example - Exporting the Agent's wallet

*When a database is port-forwared from OpenShift, `host.docker.internal` is used to access `localhost` on your local machine from within the Indy-Cli container.  The `host.docker.internal` feature is only available on Windows and MAC at the moment.  If you are running on Linux you can work with the VON team to find an alternative, for some reason using the DockerHost IP address does not work when connecting to port-forwared databases.*

*If importing (the opposite of this example) the database, make sure you use the same name and credentials used by the Agent.  If you don't the Agent will not be able to connect to the database.*

For example:
```bash
./manage \
  indy-cli export-wallet \
  walletName=agent_buybc_wallet \
  storageType=postgres_storage \
  storageConfig='{"url":"host.docker.internal:5444","max_connections":5}' \
  storageCredentials='{"account":"<User_Name>","password":"<Password>","admin_account":"postgres","admin_password":"<Admin_Password>"}' \
  exportPath=/tmp/buybc_issuer_wallet_initialized_with_did.export
```