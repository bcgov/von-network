# Writing Transactions to a Ledger for an Un-privileged Author
The following steps describe, by example, how schema and cred-def transactions are generated, signed, and written to the ledger for a non-privileged author.  The process uses a fully containerized Indy-CLI environment so there is no need to have the Indy-CLI or any of it's dependencies installed on your machine.

The procedure can be used to write transactions to any ledger by simply initializing the containerized Indy-CLI environment with the genesis file from the desired pool.

## Prerequisites

The following process uses the Indy-CLI container from [von-network](https://github.com/bcgov/von-network) which provides a containerized `indy-cli` environment and facilities to mount a volume containing `indy-cli` batch script templates and perform variable substitution on those templates, turning them into reusable scripts.

Build and start [von-network](https://github.com/bcgov/von-network); `./manage build`, `./manage start`.

Register DIDs (using seeds) for the following purposes using the `von-network` interface `http://localhost:9000`:
- TOB
  - Seed: the_org_book_0000000000000000000
  - DID: Leave blank
  - Alias: the-org-book
  - Role: None

  - Resulting Registration:
    - DID: 25GuF6zjiywpU1iF4kNJPQ
    - Verkey: awcJaDCU36RQxeqMeRKcrVHvXRZU3Ysbj6sCf6W7Q6A

- Agent
  - Seed: 0000000000000000000000000MyAgent
  - DID: Leave blank
  - Alias: my-agent
  - Role: None

  - Resulting Registration:
    - DID: NFP8kaWvCupbDQHQhErwXb
    - Verkey: Cah1iVzdB6UF5HVCJ2ENUrqzAKQsoWgiWyUopcmN3WHd

- Endorser
  - Seed: ENDORSER123450000000000000000000
  - DID: Leave blank
  - Alias: my-endorser
  - Role: Endorser

  - Resulting Registration:
    - DID: DFuDqCYpeDNXLuc3MKooX3
    - Verkey: 7gTxoFyCpMGfxuwBNXYn1icuyh8DqDpRGi12hj5S2pHk

Reset your Indy-CLI container's environment:
```
./manage cli reset
```

Initialize the pool for your Indy-CLI container's environment:
```
./manage cli init-pool localpool http://192.168.65.3:9000/genesis
```

## Start up the applications


### 1. Run OrgBook Ledger connection parameters (assuming you have already done the `./manage build` to initialize):
```
seed=the_org_book_0000000000000000000 AUTO_REGISTER_DID=0 LEDGER_URL=not_used GENESIS_URL=http://192.168.65.3:9000/genesis ./manage start
```

### 2. Run von-agent-template (assuming you have already done the `. init.sh` and `./manage build` to initialize):

```
INDY_LEDGER_URL="" AUTO_REGISTER_DID=0 INDY_GENESIS_URL=http://192.168.65.3:9000/genesis WALLET_SEED_VONX=0000000000000000000000000MyAgent ./manage start
```

**Note:** The DID for the application must already exist on the ledger.

**Note:** The agent will fail to fully synchronize since it's DID doesn't have privileges to write the schema(s) and cred-defs to the ledger.

**Note:** Leave the OrgBook and VON Agent services running, we will be using the agent's wallet database.

## Create and Write the Schema and Cred Def to the Ledger

_In the following examples:_
- Commands are run in your `von-network` directory, as we are using the Indy-CLI container.
- `/c/von-network/cli-scripts` is the absolute path to the scripts contained in this repository.
- The examples are using a local docker environment so some services are being accessed via the DOCKERHOST IP address (192.168.65.3 in these examples).  For Windows and MAC environments you can use `host.docker.internal`.  If you need to determine the DOCKERHOST IP address run `./manage dockerhost`

**Note:** The following example uses an existing wallet created by an agent.  If you are performing these operations on a wallet you have created using the Indy-Cli, be sure to initialize the wallet with DID metadata to ensure it is compatible with agents expecting this information.  Refer to to the **Pro Tips** section below for details.

### 1. Optional/Recommened - Playing the role of the Author - Export the agent's wallet - it will contain a VON-compatible DID with metadata

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli export-wallet \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  exportPath=/tmp/myorg_issuer_wallet_initialized_with_did.export
```
**Note:** This will make a backup of the wallet in it's initialized state.  There will be nothing else in the wallet other than a DID at this point.

### 2. Playing the role of the Author - Write the (author signed) schema to a file so it can be signed by the (intended) endorser.

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli create-signed-schema \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  schemaName=ian-permit.ian-co \
  schemaVersion=1.0.0 \
  schemaAttributes=corp_num,legal_name,permit_id,permit_type,permit_issued_date,permit_status,effective_date \
  outputFile=/tmp/ian-permit.ian-co_author_signed_schema.txn
```

As the author you would send the resulting file to your endorser for signing.

### 3. Playing the role of the Endorser - Initialize a local wallet:

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli create-wallet \
  walletName=endorser_wallet \
  storageType=default \
  storageConfig='{}' \
  storageCredentials='{}' \
  walletSeed=ENDORSER123450000000000000000000
```

### 4. Playing the role of the Endorser - Endorse the schema transaction and write it to a file:

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli endorse-transaction \
  walletName=endorser_wallet \
  storageType=default \
  storageConfig='{}' \
  storageCredentials='{}' \
  poolName=localpool \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_author_signed_schema.txn \
  outputFile=/tmp/ian-permit.ian-co_endorser_signed_schema.txn
```

As the endorser you would send the resulting file to the author to write to the ledger.

### 5. Playing the role of the Author - Write the signed schema transaction to the ledger:

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli write-transaction \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_endorser_signed_schema.txn
```
```
Response:
{"op":"REPLY","result":{"auditPath":["FHqp8LQ93M1bUTifLyrDsKXNCmxeKdBGHZjF8JzYGP1M","A1DbL6E9t6SjAXze5vcrM5yeWcUxFq54GsHVaupykiF"],"ver":"1","txn":{"type":"101","data":{"data":{"attr_names":["permit_status","legal_name","permit_id","effective_date","corp_num","permit_issued_date","permit_type"],"name":"ian-permit.ian-co","version":"1.0.0"}},"metadata":{"reqId":1570206701374096100,"digest":"6e8510241a55aa8137f458a832d0bfd29e627bbc40e5771215ac49651c8f747f","payloadDigest":"dc4566c75351782cd08dae6cdbf291d0373b93d91103ff47d0aa96093d2cace4","from":"NFP8kaWvCupbDQHQhErwXb","endorser":"DFuDqCYpeDNXLuc3MKooX3"},"protocolVersion":2},"rootHash":"4uVeu6q5QKt2EEQYffqz2E5iRSk4xE1cGsjxVoHKDNvg","reqSignature":{"values":[{"from":"DFuDqCYpeDNXLuc3MKooX3","value":"2rsfmc23QY3Jf7TgdM8sun23h2TAXK5ndjoz5DeCFovafKv9QMgoVmckY7CA8UAFskrauHto5XTH8MogC7ChqKf4"},{"from":"NFP8kaWvCupbDQHQhErwXb","value":"4dDERHW9QfMdTiYwiCMArgcEe41meA3fLiaVwqfRbJxsq87MbUEgsdQuSNSjDzYTDfW2TaXP5kXo16yA15LqPAR3"}],"type":"ED25519"},"txnMetadata":{"txnTime":1570206783,"txnId":"NFP8kaWvCupbDQHQhErwXb:2:ian-permit.ian-co:1.0.0","seqNo":10}}}
```

Make a note of the `seqNo` (`"seqNo":10` in this example), you will need to use it for the `schemaId` later


### 6. Playing the role of the Author - Create the cred def in the wallet:

a. Attach the wallet

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli attach-wallet \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}'
```

b. Create the cred def in the wallet.  Use the value of the `seqNo` you noted in the previous step as the value for `schemaId` in the following call.

```
./manage \
  -v /c/von-network/cli-scripts/ \
  cli \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  walletKey=key \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  schemaId=10 \
  schemaName=ian-permit.ian-co \
  schemaVersion=1.0.0 \
  schemaAttributes=corp_num,legal_name,permit_id,permit_type,permit_issued_date,permit_status,effective_date \
  python cli-scripts/cred_def.py
```

Make a note of the `primary` (the **Cred def primary**) produced by this script, you will need to use it for the `primaryKey` later

c. Detach the wallet

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli detach-wallet \
  walletName=myorg_issuer
```

### 7. Playing the role of the Author - Write the (author signed) cred def to a file so it can be signed by the (intended) endorser.  Plug in the `schemaId` and `primaryKey` you noted from earlier operations.

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli create-signed-cred-def \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  schemaId=10 \
  signatureType=CL \
  tag=tag \
  primaryKey='{"n":"83119582963432746215686319796172653418705782899965293988574166382508611865186858793093702870967109747819897710742014781605393376195068801834452268334211521692589392079683383144826791154100428403165552815504697121164642726588324586645652386655942182612653525671363701488403660461085353146089265862651401896911926629969359457892135391469430338176540643947600959303134995799072784718187762577362903451138079631849167299202460097696661131075083897208962866941193549286351752880830424973398728175725767105692034945390480139394838402244109017258420291840803473878440730010569534633457259450283797827690449394871899943488517","s":"29732246552616011333122488293395693234028805948128921850148963472158465821273314711387105103638365385956988924606935005616897196782737335492864364542015705404849582854647219700828261279119585800545465712114560723394972594525495226899790506836651512823088229520988657862390126927524390310765016677401075808755929250848704283349130804736821468816748620353377690891946560802996815631500900255222092145923204597219833813630890493938878998072015754336241653671380458997378821495666489784118055880239425733239953069234945269234744110601577339224185096635114740146389401340828794133123419166905669247476619715199876804819430","z":"51830053398673769879017155270298896156503208513344361662919189697120082335953361625639382363387227074582293539947968382109975852839860504203625991669295810856311178443568755269400427855287230316600634323401938920721753086828829667997569419565953727282720243314689489555635952563191667484552882679367949736166338551066592384147375988344383682980508095863466832007605610817798733409110176638949679017853591295740918106423211844954360358716625364255315539815176028726321721425394400043187181669164813802163850173845213732616801212951283915659245146874297821897272405870217462877221497205292738037352927519755244958630626","r":{"master_secret":"74297991024030030383300472466934416853802340152345955134859770699706411123935907033199635305419932897671193903079961257181687574258343408869444814310121799771790801474166845940099842214434617049091360494735113423628869001493022676898652253658336006330159346934154341857693212257795130620846471835851230777074530123962458098702437528801457065024500491079884240984666538956307607098044899708360613310251626711313485858283065057381870078965502811366144112912989477015931803230198579121727791517033953271805956664386571544509337745996006674428330419574047822980125030498468325270201886329504296166084688365667341515955192","corp_num,legal_name,permit_id,permit_type,permit_issued_date,permit_status,effective_date":"33131871678943027609313793424590617387690260781906837533126802498951146497818441362292124890332688057348872193572852087678730173943825635132782680165793408729739755313501488925888196445825936397579642058239995048327964689998059410623089838703760434079719268936671351949387556014275808076944271777720242499843242262584340200144779961380909852917113919267966793155363397698376623189045773401315981844862645366605455940667325495567233283214243605379479150727434695562649926364916943547905645904588990069780865488058379525651132781562098370331899914969344727882238180679350646871717242650421234188388334970289852453484932"},"rctxt":"50692344880138563997955400921814207318465065544247140642303790744937528248567434944671128045870194616842227940544371583667310833886101310736344790076183953529709345534096210941035804252472331282988445846695832303354147067438092511424512617690607548011053949755214463882336227242145613084586016565421000308688673922722569720534783262349702794357858609914816250049907024749888645617720375533326475644491822746205080143632684416271732012420077943459435878283069046224538968336675597683422369343340868474310658116821952888028043859667977152891527196051859277558276377144640584218039780234011368064833898738812933952177811"}' \
  outputFile=/tmp/ian-permit.ian-co_author_signed_cred_def.txn
  ```

As the author you would send the resulting file to your endorser for signing.


### 8. Playing the role of the Endorser - Endorse the cred-def transaction and write it to a file:

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli endorse-transaction \
  walletName=endorser_wallet \
  storageType=default \
  storageConfig='{}' \
  storageCredentials='{}' \
  poolName=localpool \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_author_signed_cred_def.txn \
  outputFile=/tmp/ian-permit.ian-co_endorser_signed_cred_def.txn
```

As the endorser you would send the resulting file to the author to write to the ledger.


### 9. Playing the role of the Author - Write the signed cred-def transaction to the ledger:

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli write-transaction \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_endorser_signed_cred_def.txn
```
```
Response:
{"result":{"ver":"1","txn":{"data":{"ref":10,"data":{"primary":{"r":{"corp_num,legal_name,permit_id,permit_type,permit_issued_date,permit_status,effective_date":"33131871678943027609313793424590617387690260781906837533126802498951146497818441362292124890332688057348872193572852087678730173943825635132782680165793408729739755313501488925888196445825936397579642058239995048327964689998059410623089838703760434079719268936671351949387556014275808076944271777720242499843242262584340200144779961380909852917113919267966793155363397698376623189045773401315981844862645366605455940667325495567233283214243605379479150727434695562649926364916943547905645904588990069780865488058379525651132781562098370331899914969344727882238180679350646871717242650421234188388334970289852453484932","master_secret":"74297991024030030383300472466934416853802340152345955134859770699706411123935907033199635305419932897671193903079961257181687574258343408869444814310121799771790801474166845940099842214434617049091360494735113423628869001493022676898652253658336006330159346934154341857693212257795130620846471835851230777074530123962458098702437528801457065024500491079884240984666538956307607098044899708360613310251626711313485858283065057381870078965502811366144112912989477015931803230198579121727791517033953271805956664386571544509337745996006674428330419574047822980125030498468325270201886329504296166084688365667341515955192"},"n":"83119582963432746215686319796172653418705782899965293988574166382508611865186858793093702870967109747819897710742014781605393376195068801834452268334211521692589392079683383144826791154100428403165552815504697121164642726588324586645652386655942182612653525671363701488403660461085353146089265862651401896911926629969359457892135391469430338176540643947600959303134995799072784718187762577362903451138079631849167299202460097696661131075083897208962866941193549286351752880830424973398728175725767105692034945390480139394838402244109017258420291840803473878440730010569534633457259450283797827690449394871899943488517","s":"29732246552616011333122488293395693234028805948128921850148963472158465821273314711387105103638365385956988924606935005616897196782737335492864364542015705404849582854647219700828261279119585800545465712114560723394972594525495226899790506836651512823088229520988657862390126927524390310765016677401075808755929250848704283349130804736821468816748620353377690891946560802996815631500900255222092145923204597219833813630890493938878998072015754336241653671380458997378821495666489784118055880239425733239953069234945269234744110601577339224185096635114740146389401340828794133123419166905669247476619715199876804819430","z":"51830053398673769879017155270298896156503208513344361662919189697120082335953361625639382363387227074582293539947968382109975852839860504203625991669295810856311178443568755269400427855287230316600634323401938920721753086828829667997569419565953727282720243314689489555635952563191667484552882679367949736166338551066592384147375988344383682980508095863466832007605610817798733409110176638949679017853591295740918106423211844954360358716625364255315539815176028726321721425394400043187181669164813802163850173845213732616801212951283915659245146874297821897272405870217462877221497205292738037352927519755244958630626","rctxt":"50692344880138563997955400921814207318465065544247140642303790744937528248567434944671128045870194616842227940544371583667310833886101310736344790076183953529709345534096210941035804252472331282988445846695832303354147067438092511424512617690607548011053949755214463882336227242145613084586016565421000308688673922722569720534783262349702794357858609914816250049907024749888645617720375533326475644491822746205080143632684416271732012420077943459435878283069046224538968336675597683422369343340868474310658116821952888028043859667977152891527196051859277558276377144640584218039780234011368064833898738812933952177811"}},"tag":"tag","signature_type":"CL"},"metadata":{"endorser":"DFuDqCYpeDNXLuc3MKooX3","from":"NFP8kaWvCupbDQHQhErwXb","payloadDigest":"33599f2e3cf03935944cd70ecd4110490fba1d6f4e6adc65af63d776d52cb06b","digest":"4145b372e6c2c71be621fa22f2f90a9dafb1730b29c327012f0a44d4fcb39850","reqId":1570206979266610400},"protocolVersion":2,"type":"102"},"rootHash":"E5f72f4NaTqSAySZhxxz9557r65YpfSe9ufguHcECpBM","reqSignature":{"type":"ED25519","values":[{"from":"DFuDqCYpeDNXLuc3MKooX3","value":"xEmH6G852yrUuMFRSUucv8U6U1z9UziqYB6U6PLhfqnjrw8anPT3db6pFp9nHxwvKKKiXPHGuxyGKmTt9ozmATj"},{"from":"NFP8kaWvCupbDQHQhErwXb","value":"4Rmfco7papuwfpyiMM99mWMtNuoYLKR372YSLhwpq8uhpvpjh9YdFrbLgKJfEHs4UjWrTaodBYpSXLWjFeh1rD7S"}]},"auditPath":["AfcoCoVxkL7h7aAvbmrDdSoFns471AnQAQXXBAL56vTt","A1DbL6E9t6SjAXze5vcrM5yeWcUxFq54GsHVaupykiF"],"txnMetadata":{"txnId":"NFP8kaWvCupbDQHQhErwXb:3:CL:10:tag","txnTime":1570207621,"seqNo":11}},"op":"REPLY"}
```


### 10. Playing the role of the Author - Make a final backup of your wallet

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli export-wallet \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  exportPath=/tmp/myorg_issuer_wallet_registration_complete.export
```

## Restart the Agent with the Initialized Wallet

### 1. Restart the Agent

```
./manage stop
```
```
INDY_LEDGER_URL="" AUTO_REGISTER_DID=0 INDY_GENESIS_URL=http://192.168.65.3:9000/genesis WALLET_SEED_VONX=0000000000000000000000000MyAgent ./manage start
```

**Note:** Make sure you ./manage `stop` and *NOT* `rm`

God willing, you will see output something like this:

```
myorg-agent_1      | 2019-09-12 01:03:24,236 INFO [von_anchor.wallet]: Created wallet bctob-Verifier-Wallet
myorg-agent_1      | 2019-09-12 01:03:24,633 INFO [von_anchor.wallet]: Opened wallet bctob-Verifier-Wallet on handle 6
myorg-agent_1      | 2019-09-12 01:03:24,641 INFO [von_anchor.wallet]: Wallet bctob-Verifier-Wallet set seed hash metadata for DID NFP8kaWvCupbDQHQhErwXb
myorg-agent_1      | 2019-09-12 01:03:25,052 INFO [von_anchor.wallet]: Opened wallet myorg_issuer on handle 7
myorg-agent_1      | 2019-09-12 01:03:25,059 INFO [von_anchor.wallet]: Wallet myorg_issuer got verkey GcWd3dYwmptFdGBf4DFMi5jUxmcgBNVoDWRV2ritLh4r for existing DID NFP8kaWvCupbDQHQhErwXb
myorg-agent_1      | 2019-09-12 01:03:26,168 INFO [von_anchor.anchor.base]: myorg_issuer endpoint already set as http://192.168.65.3:5001
myorg-agent_1      | 2019-09-12 01:03:26,168 INFO [vonx.indy.service]: messages.Endpoint stored: http://192.168.65.3:5001
myorg-agent_1      | 2019-09-12 01:03:26,168 INFO [vonx.indy.service]: Checking for schema: ian-permit.ian-co (1.0.7)
myorg-agent_1      | 2019-09-12 01:03:26,333 INFO [von_anchor.anchor.base]: BaseAnchor.get_schema: got schema SchemaKey(origin_did='NFP8kaWvCupbDQHQhErwXb', name='ian-permit.ian-co', version='1.0.7') from ledger
myorg-agent_1      | 2019-09-12 01:03:26,335 INFO [vonx.indy.service]: Checking for credential def: ian-permit.ian-co (1.0.7)
myorg-agent_1      | 2019-09-12 01:03:26,654 INFO [von_anchor.anchor.base]: BaseAnchor.get_cred_def: got cred def NFP8kaWvCupbDQHQhErwXb:3:CL:70371:tag from ledger
myorg-agent_1      | 2019-09-12 01:03:26,654 INFO [vonx.indy.service]: Indy agent synced: ian-co
myorg-agent_1      | 2019-09-12 01:03:27,049 INFO [von_anchor.wallet]: Opened wallet bctob-Verifier-Wallet on handle 13
myorg-agent_1      | 2019-09-12 01:03:27,051 INFO [von_anchor.wallet]: Wallet bctob-Verifier-Wallet got verkey GcWd3dYwmptFdGBf4DFMi5jUxmcgBNVoDWRV2ritLh4r for existing DID NFP8kaWvCupbDQHQhErwXb
myorg-agent_1      | 2019-09-12 01:03:27,217 INFO [von_anchor.anchor.base]: BaseAnchor.get_endpoint: got endpoint for NFP8kaWvCupbDQHQhErwXb from cache
myorg-agent_1      | 2019-09-12 01:03:28,367 INFO [vonx.indy.service]: messages.Endpoint stored: None
myorg-agent_1      | 2019-09-12 01:03:28,367 INFO [vonx.indy.service]: Indy agent synced: bctob
myorg-agent_1      | 2019-09-12 01:03:28,368 WARNING [vonx.indy.tob]: No file found at logo path: ../config/../assets/img/ian-co-logo.jpg
myorg-agent_1      | 2019-09-12 01:03:30,154 INFO [vonx.common.service]: Starting sync: indy
```

## Test by Posting a Credential to the Agent

```
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
        "permit_issued_date": "2017-11-01T08:00:00+00:00",
        "permit_status": "ACT",
        "effective_date": "2017-11-01T08:00:00+00:00"
    },
    "schema": "ian-permit.ian-co",
    "version": "1.0.0"
}
]
'
```

You should receive a success message something like this;
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   502  100    98  100   404    272   1125 --:--:-- --:--:-- --:--:--  1398[{"success": true, "result": "d1e4d28a-9ea0-4b11-a34a-4626b84bf19b", "served_by": "d5645b756b28"}]
```

## Resetting your local environment between runs

In between runs of the above:

Run the following for `von-network`, `TheOrgBook`, and `von-agent-template`:
```
./manage rm
```

This will delete all the data for each of the applications.  You'll have to re-initialize the environment from the beginning.

# Pro Tips

## Creating a Wallet using the Indy-Cli Container

The above example performs all operations on an existing wallet created by an agent.  Sometimes it is not possible or practical to operate on an existing wallet or the restored export of and existing wallet.  In some cases it is simply easier to start from the beginning using a local wallet.

### Creating a new local wallet

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli create-wallet \
  walletName=lcrb_wallet \
  storageType=default \
  storageConfig='{}' \
  storageCredentials='{}' \
  walletSeed=<YourWalletSeedHere/>
```

*You will be prompted for the wallet key by the script.  Make sure you record your wallet seed and key somewhere safe.*

This will create a new wallet initialized with a DID, but without any DID metadata.  Some agent implementations expect there to be DID metadata.  If non-exists the agent can run into startup issues.

### Setting DID Metadata

```
./manage \
  -v /c/von-network/cli-scripts/ \
  cli \
  walletName=lcrb_wallet \
  storageType=default \
  storageConfig='{}' \
  storageCredentials='{}' \
  walletDid=<YourWalletDidHere/> \
  walletSeed=<YourWalletSeedHere/> \
  walletKey=<YourWalletKeyHere/> \
  python cli-scripts/set_did_metadata.py
```

This will write DID metadata to the wallet.  It assumes the DID you have specified is a public data and to calculates a hash for the seed.  You can see the results using `did-list`.

## Listing DIDs

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli did-list \
  walletName=lcrb_wallet \
  storageType=default \
  storageConfig='{}' \
  storageCredentials='{}'
```

```
did list
+------------------------+-------------------------+---------------------------------------------------------------------------------------------------+
| Did                    | Verkey                  | Metadata                                                                                          |
+------------------------+-------------------------+---------------------------------------------------------------------------------------------------+
| JNXZGR4Kfyakzi7Wu4Qics | ~KQy2B3fgyC2CiYyTAKRjnR | {"public": true, "seed_hash": "363887f3464914629f0f93370bc18d7cd96ef92bffde2876da13abbbe8fa2183"} |
+------------------------+-------------------------+---------------------------------------------------------------------------------------------------+
```

## Importing the Resulting Wallet into an Agent Running on OpenShift

### Prep the Agent's Wallet database

Determine the name of the existing wallet database for the Agent.  This is typically found in the Agent configuration; you'll need this when importing.

Make a backup of the database if needed.

Drop the database.
- From a terminal connected to the wallet database pod; `psql -c 'drop database <TheNameOfTheWalletDatabase/>'`

### Port forward your agent's wallet database to your local machine.

For example:
```
oc -n devex-von-bc-registries-agent-dev port-forward wallet-db-3-xcp56 5444:5432
```

*This will port forward wallet-db-3-xcp56:5444 to localhost:5444.*

### Import the backup into the Agent's wallet

*`host.docker.internal` is used to access `localhost` on your local machine from within the Indy_Cli container.  This feature is only available on Windows and MAC at the moment.  If you are running on Linux you can work with the VON team to find an alternative, for some reason this does not work when using the DockerHost IP address.*

*Import the database using the same name and credentials used by the Agent.  If you don't the Agent will not be able to connect to the database.*

For example:
```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli import-wallet \
  walletName=lcrb_wallet \
  storageType=postgres_storage \
  storageConfig='{"url":"host.docker.internal:5444"}' \
  storageCredentials='{"account":"USER_ewnp","password":"DLKD0sd098hsd9jsdf","admin_account":"postgres","admin_password":"98s7df987w4hfn90wemofwf2j0"}' \
  importPath=/tmp/lcrb_wallet_with_schemas_cred_defs_and_metadata.export
```