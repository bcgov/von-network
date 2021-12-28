# Using the containerized `indy-cli`

This repository includes a fully containerized `indy-cli` environment, allowing you to use the `indy-cli` without ever having to build or install the `indy-sdk` or any of its dependencies on your machine.

The following `indy-cli` examples are performed using a local instance of `von-network`, however the `indy-cli` environment can be connected to any number of `indy` ledgers.  In order to use some `indy-cli` commands you'll need to have a DID already registered on that network.  The process of starting the `indy-cli` and generating a local wallet will generate the DID and Verkey you could then have registered on that network.

## Example Prerequisites

### Build `von-network`

```
./manage build
```

### Generate a set of Secrets

The first thing you'll need is a set of secrets, a `seed`: used to generate your DID, and a `key`: used as the encryption key for your wallet.

These two values are very sensitive.  Make sure you store them in a safe place such as a secure password manager application.  If someone gets hold of your `seed`, they can regenerate your `DID` and `Verkey` and impersonate you.  If someone gains access to your wallet and your wallet `key`, they can impersonate you AND have control over all of the credentials in your wallet.  So, make sure you keep your `seed` and wallet `key` a secret.

The `./manage` script makes this easy to generate these values randomly, just run:

```
./manage generateSecrets
```
```
Seed: 2yMTRs+zBBPF75OE5i1WCY5uDcQYUdt4
Key: b+StO9VtqyvdEeUsUQknR6uB+UoXK09kHzskSjIYIZ0GQmG4O0bLULc7NlY42/Bh
```

For the remainder of the examples we'll use the seed and key from above for consistency.

### Generate your DID

The `generateDid` command can be used with or without a seed to generate a DID.  When used without a seed it will generate a random seed and use that to generate a DID and Verkey.

```
./manage generateDid 2yMTRs+zBBPF75OE5i1WCY5uDcQYUdt4
```
```
Seed: 2yMTRs+zBBPF75OE5i1WCY5uDcQYUdt4
DID: 5DHNJswc1LjkCWPYYrzYVX
Verkey: 3J9F2QpresMoukCSJTbvM2YmaovfqveVDgg1P1azMsJP
```

### Start an instance of `von-network`

```
./manage start
```

### Register your DID on the network

1. Browse to http://localhost:9000/.
2. In the **Authenticate a New DID** section enter the seed (created above) in the **Wallet seed (32 characters or base64)** field and `my-did` in the Alias (optional) field.
3. Click **Register DID**

You should see the following message written to the screen:
```
Identity successfully registered:
Seed: 2yMTRs+zBBPF75OE5i1WCY5uDcQYUdt4
DID: 5DHNJswc1LjkCWPYYrzYVX
Verkey: 3J9F2QpresMoukCSJTbvM2YmaovfqveVDgg1P1azMsJP
```

_Now on to working with the `indy-cli` ..._

## Register the network (ledger) with the `indy-cli` environment

This command downloads and registers the network's genesis file with the `indy-cli`.

Note we're using the internal docker host IP address to access the locally running network since it's also running in docker.  This IP can be obtained by running `./manage dockerhost`.

```
./manage cli init-pool local_net http://192.168.65.3:9000/genesis
```
```
Creating von_client_run ... done
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3092  100  3092    0     0  1006k      0 --:--:-- --:--:-- --:--:-- 1006k
```

To register another network (say Sovrin BuilderNet) you would run the command like this:
```
./manage cli init-pool builder_net https://raw.githubusercontent.com/sovrin-foundation/sovrin/stable/sovrin/pool_transactions_builder_genesis
```

## Create a wallet

```
./manage \
  indy-cli create-wallet \
  walletName=local_net_trustee_wallet
```

When prompted, enter the wallet encryption key to create the wallet:
```
Creating von_client_run ... done
load-plugin library=libindystrgpostgres.so initializer=postgresstorage_init
Plugin has been loaded: "libindystrgpostgres.so"

wallet create local_net_trustee_wallet key storage_type=default storage_config={} storage_credentials={}
Enter value for key:

```

When prompted, enter the wallet encryption key to open the wallet:
```
Wallet "local_net_trustee_wallet" has been created

wallet open local_net_trustee_wallet key storage_credentials={}
Enter value for key:

```

When prompted, enter your seed:
```
Wallet "local_net_trustee_wallet" has been opened

did new seed
Enter value for seed:

```

```
Did "5DHNJswc1LjkCWPYYrzYVX" has been created with "~ATfU5eKehb2Y1WkqHbmLvT" verkey

did list
+------------------------+-------------------------+----------+
| Did                    | Verkey                  | Metadata |
+------------------------+-------------------------+----------+
| 5DHNJswc1LjkCWPYYrzYVX | ~ATfU5eKehb2Y1WkqHbmLvT | -        |
+------------------------+-------------------------+----------+

wallet close
Wallet "local_net_trustee_wallet" has been closed

wallet detach local_net_trustee_wallet
Wallet "local_net_trustee_wallet" has been detached

exit

Goodbye...
```

## Export (backup) a wallet

```
./manage \
  indy-cli export-wallet \
  walletName=local_net_trustee_wallet \
  exportPath=/tmp/local_net_trustee_wallet.export
```

When prompted, enter the wallet encryption key to open the wallet:
```
Creating von_client_run ... done
load-plugin library=libindystrgpostgres.so initializer=postgresstorage_init
Plugin has been loaded: "libindystrgpostgres.so"

-wallet attach local_net_trustee_wallet storage_type=default storage_config={}
Wallet "local_net_trustee_wallet" has been attached

wallet open local_net_trustee_wallet key storage_credentials={}
Enter value for key:

```

When prompted, enter the wallet encryption key to encrypt the wallet export:
```
Wallet "local_net_trustee_wallet" has been opened

wallet export export_path=/tmp/local_net_trustee_wallet.export export_key
Enter value for export_key:

```

```
Wallet "local_net_trustee_wallet" has been exported to the file "/tmp/local_net_trustee_wallet.export"

wallet close
Wallet "local_net_trustee_wallet" has been closed

wallet detach local_net_trustee_wallet
Wallet "local_net_trustee_wallet" has been detached

exit

Goodbye...
```

## Import a wallet Export (backup) file

```
./manage \
  indy-cli import-wallet \
  walletName=local_net_trustee_wallet \
  importPath=/tmp/local_net_trustee_wallet.export
```

When prompted, enter the encryption key of the export (backup) file:
```
Creating von_client_run ... done
load-plugin library=libindystrgpostgres.so initializer=postgresstorage_init
Plugin has been loaded: "libindystrgpostgres.so"

wallet import local_net_trustee_wallet key export_path=/tmp/local_net_trustee_wallet.export export_key storage_type=default storage_config={} storage_credentials={}       
Enter value for key:

```

When prompted, enter the wallet encryption key for the restore process:
```
Enter value for export_key:

```

When prompted, enter the wallet encryption key to open the wallet:
```
Wallet "local_net_trustee_wallet" has been created

wallet open local_net_trustee_wallet key storage_credentials={}
Enter value for key:

```
```
Wallet "local_net_trustee_wallet" has been opened

did list
+------------------------+-------------------------+----------+
| Did                    | Verkey                  | Metadata |
+------------------------+-------------------------+----------+
| 5DHNJswc1LjkCWPYYrzYVX | ~ATfU5eKehb2Y1WkqHbmLvT | -        |
+------------------------+-------------------------+----------+

wallet close
Wallet "local_net_trustee_wallet" has been closed

wallet detach local_net_trustee_wallet
Wallet "local_net_trustee_wallet" has been detached

exit

Goodbye...
```

## Open an interactive `indy-cli` session

This command starts an `indy-cli` session with a given ledger and opens the specified wallet and sets the session context using the `did use` command.

The command is setup to use an `indy-cli` config file to indicate the TAA acceptance mechanism.  Create the file `./tmp/cliconfig.json` in the `von-network` folder (i.e. `.../von-network/tmp/cliconfig.json`) and save the following content:
```
{
  "taaAcceptanceMechanism": "for_session"
}
```

The `./tmp` folder gets mounted automatically into the docker container's `/tmp` folder.


```
./manage \
  indy-cli --config /tmp/cliconfig.json start-session \
  walletName=local_net_trustee_wallet \
  poolName=local_net \
  useDid=5DHNJswc1LjkCWPYYrzYVX
```

When prompted, enter the wallet encryption key to open the wallet:
```
Creating von_client_run ... done
"for_session" is used as transaction author agreement acceptance mechanism
load-plugin library=libindystrgpostgres.so initializer=postgresstorage_init
Plugin has been loaded: "libindystrgpostgres.so"

pool connect local_net
Pool "local_net" has been connected

-wallet attach local_net_trustee_wallet storage_type=default storage_config={}
Wallet "local_net_trustee_wallet" has been attached

wallet open local_net_trustee_wallet key storage_credentials={}
Enter value for key:

```
```
Wallet "local_net_trustee_wallet" has been opened

did use 5DHNJswc1LjkCWPYYrzYVX
Did "5DHNJswc1LjkCWPYYrzYVX" has been set as active

pool(local_net):local_net_trustee_wallet:did(5DH...YVX):indy>
```

You are now ready to issue commands/transactions to the ledger using your DID's context.

### Try it out

Read your DID from the ledger by entering the following command on the `indy-cli` command prompt:
```
ledger get-nym did=5DHNJswc1LjkCWPYYrzYVX
```
```
Following NYM has been received.
Metadata:
+------------------------+-----------------+---------------------+---------------------+
| Identifier             | Sequence Number | Request ID          | Transaction time    |
+------------------------+-----------------+---------------------+---------------------+
| 5DHNJswc1LjkCWPYYrzYVX | 10              | 1633469176534450900 | 2021-10-05 20:02:27 |
+------------------------+-----------------+---------------------+---------------------+
Data:
+------------------------+------------------------+----------------------------------------------+----------+
| Identifier             | Dest                   | Verkey                                       | Role     |
+------------------------+------------------------+----------------------------------------------+----------+
| V4SGRU86Z58d6TV7PBUe6f | 5DHNJswc1LjkCWPYYrzYVX | 3J9F2QpresMoukCSJTbvM2YmaovfqveVDgg1P1azMsJP | ENDORSER |
+------------------------+------------------------+----------------------------------------------+----------+
pool(local_net):local_net_trustee_wallet:did(5DH...YVX):indy>
```

When done type `exit` and press enter:
```
pool(local_net):local_net_trustee_wallet:did(5DH...YVX):indy> exit
Pool "local_net" has been disconnected
Wallet "local_net_trustee_wallet" has been closed
Goodbye...
```

## Open an interactive `indy-cli` command line

```
./manage   indy-cli
```
```
Creating von_client_run ... done
indy>
```

You are now on an interactive `indy-cli` command line.  For `help` with the commands type `help`.  This will give you information about the top level commands.  To get help about a specific command, or sub-command type the `<command> [sub-command]` followed by help; for example `ledger help`, or `ledger get-nym help`.

When done type `exit` and press enter:
```
indy> exit
Goodbye...
```

## Reset your `indy-cli` environment

**Use with caution.  This deletes everything in your `indy-cli` environment.  Make sure you have things backed up if needed.**
```
./manage cli reset
```

## Other Commands

### Generate Genesis Files

This command generates pool and domain genesis files from data input via csv files.

```
./manage generategenesisfiles <trustees_csv_file> <stewards_csv_file>
```        
It is a convenience command wrapped around the Steward Tools script for generating genesis files found here; https://github.com/sovrin-foundation/steward-tools/tree/master/create_genesis

The script is downloaded and hosted in a running container which has the required packages installed.

Examples of the csv files can be downloaded from here; https://docs.google.com/spreadsheets/d/1LDduIeZp7pansd9deXeVSqGgdf0VdAHNMc7xYli3QAY/edit#gid=0

Download each sheet separately in csv format and fill them out with the data specific to your network.

The input csv files must be placed into the `./tmp/` folder.
The resulting output `pool_transactions_genesis` and `domain_transactions_genesis` files will be placed
in the `./tmp/` folder.

Example:
```
./manage generategenesisfiles "./tmp/CANdy Beta Genesis File Node info - Trustees.csv" "./tmp/CANdy Beta Genesis File Node info - Stewards.csv"
```
