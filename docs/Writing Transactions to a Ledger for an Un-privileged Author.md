# Writing Transactions to a Ledger for an Un-privileged Author
The following steps descride, by example, how schema and cred-def transactions are generated, signed, and written to the ledger for a non-privilaged author.  The process uses a fully containerized Indy-CLI environment so there is no need to have the Indy-CLI or any of it's dependancies installed on your machine.

The procedure can be used to write transactions to any ledger by simply initializing the containerized Indy-CLI environment with the genisis file from the desired pool.

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


1. Run OrgBook Ledger connection parameters (assuming you have already done the `./manage build` to initialize):
```
seed=the_org_book_0000000000000000000 AUTO_REGISTER_DID=0 LEDGER_URL=not_used GENESIS_URL=http://192.168.65.3:9000/genesis ./manage start
```

2. Run von-agent-template (assuming you have already done the `. init.sh` and `./manage build` to initialize):

```
INDY_LEDGER_URL="" AUTO_REGISTER_DID=0 INDY_GENESIS_URL=http://192.168.65.3:9000/genesis WALLET_SEED_VONX=0000000000000000000000000MyAgent ./manage start
```

**Note:** The DID for the application must already exist on the ledger.

**Note:** The agent will fail to fully syncronize since it's DID doesn't have privileges to write the schema(s) and cred-defs to the ledger.

**Note:** Leave the OrgBook and VON Agent services running, we will be using the agent's wallet database.

## Create and Write the Schema and Cred Def to the Ledger

_In the following examples:_
- Commands are run in your `von-network` directory, as we are using the Indy-CLI container.
- `/c/von-network/cli-scripts` is the abosulte path to the scripts contained in this repository.
- The examples are using a local docker environment so some services are being accessed via the DOCKERHOST IP address (192.168.65.3 in these examples).

1. Optional/Recommened - Playing the role of the Author - Export the agent's wallet - it will contain a VON-compatible DID with metadata

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

2. Playing the role of the Author - Write the (author signed) schema to a file so it can be later signed and written to the ledger by the (intended) endorser.

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


3. Playing the role of the Endorser - Initialize a local wallet:

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


4. Playing the role of the Endorser - Sign the transaction and write to the ledger:

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli write-signed-transaction \
  walletName=endorser_wallet \
  storageType=default \
  storageConfig='{}' \
  storageCredentials='{}' \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_author_signed_schema.txn
```
```
Response:
{"result":{"auditPath":["6hokYVzPdjWCMk1wBLv1EHEEM4r3tD74yAPS7aECTFES","42T88rYvNWBh83QUkvNHUVfHUikWCBWh1zmP5AUUJLZ3"],"reqSignature":{"values":[{"value":"4UTrHUaZqZYwN7jkitB1n6wcyMo6CApE7BouLxS7rdrUJiWT8KM9FkXBUeTmTaoYwegupVmY8TUqcNFYRdjJPaf7","from":"DFuDqCYpeDNXLuc3MKooX3"},{"value":"nrGatoL1VjKvpLV4EBvGkrqPMiSTeJ4A7QeykjTAmb34CtE4VG32ddT8KGAszdoko659E7XRwy38jC42cJPPAPN","from":"NFP8kaWvCupbDQHQhErwXb"}],"type":"ED25519"},"rootHash":"DSsBgS5T6WPMiC3AxnzAsywDaHzVH2ptvezwNweQHF1v","txn":{"protocolVersion":2,"metadata":{"digest":"39c2efb17b75edda9b6da5e7939131bbcc1cc86671bb5d4e9dc6b940c39e61e6","payloadDigest":"397051e80fca9b81a77adae5e08e59fa784bdc16dc11b788d9d421ac8b0205e4","endorser":"DFuDqCYpeDNXLuc3MKooX3","from":"NFP8kaWvCupbDQHQhErwXb","reqId":1569428405919642000},"data":{"data":{"name":"ian-permit.ian-co","attr_names":["legal_name","permit_type","permit_status","effective_date","permit_id","permit_issued_date","corp_num"],"version":"1.0.0"}},"type":"101"},"ver":"1","txnMetadata":{"txnTime":1569438675,"seqNo":10,"txnId":"NFP8kaWvCupbDQHQhErwXb:2:ian-permit.ian-co:1.0.0"}},"op":"REPLY"}
```

Make a note of the `seqNo` (`"seqNo":10` in this example), you will need to use it for the `schemaId` later

5. Playing the role of the Author - Create the cred def in the wallet:

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

6. Playing the role of the Author - Write the (author signed) cred def to a file so it can be later signed and written to the ledger by the (intended) endorser.  Plug in the `schemaId` and `primaryKey` you noted from earlier operations.

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
  primaryKey='{"s":"30757889667122330147640240038410441399697308008134494575679551728290696931357172658909788891218035940106201599615579444363457784752905871956411141374331105360135412530299878577484706300643846444714709246712910704238385246602581921746739874151993642953630243090382619045982669201549972850243806920185898369517903964211016341607307698179244207537329287210501539428235110320143944656242881149183650098420828888022071691867516674558154979850054845024764222962827617545273402128783155423940474215772965940051530134504886616785183920508251427208778354649898684442840107067092949080458098462173160699529383213163776091712079","n":"88203649656127442642628572246232981308877309389461859524112147258462047901543434241412506903047914786375464038323023641922966939919722538597183645310293399983203425143816274006475019801379567525053774978148688529399267854815917399562942833590486844389975979888555975389213832622248136895468689631183530526528170751751173800791418950724856115073233136198900458058821654266157675984908351200539929875633769884651670385743792708186315652433606938935762180109609519478882926645285477722495714841553069922690402388605206189765251312734142703988541637956764681337779733796504286869710734883123404059537223236176819956163053","z":"48612341238944863516597606940187025078187134965967719159804252386028452842977917131657837224876256121799524885178964566913188372800229020081298709607069317339526887374119542002673808078305964469237783351838964824767531193332395936923249984510616953912764389740879199275732235656604356813938607089368611789314648157068235501002762416533972527103439589241871609910498359902103691257116715392048432663355110064083578191873843883580421292089025890652482025820147681491161784282642138030305588310482394198296048871311224820675431104536178145284463064721787951334903798946810696826258821699965492775662465392358976900034500","rctxt":"78654945094588596800224001496357037443353305845218404584967476556791188182327036112350572942216603769870131114314194346737701769407379848410611811443653500701291996102610528348285266340317059461265626196517383666236650680976629458216114716059408447079344992398841167955978880687456316031706544707109526609238788770841086759646932022640329026004716382296088241746826047930986752155399727968985085377715186258944421236193193173796986577875732714843209023743395058021504212175579845307360462478739625398640062714510766958631200126181947781364304487544573009629737209567103357597564015509782138709303224050946468441299820","r":{"permit_id":"61332847708982782195050165385411702261141376000089291523621294546148801437197297031030038739485261222411380692853924260414498142655955546639611382844703952629401843103265252971446206031946180795664450862770246479089939211438689413718198638068497818448510390096623920235349637106476039772883175340227010408458843098123761268080317468962265590828575908530090472757846657129003940722322277263649950767784331379253502012628289417780744089445342966122403701483382264977147234672714667402998527797620035589052924192662366415309815540200631085729030865963201424994857959484514384106297379389034204637302560737859771803570072","legal_name":"79524898057474366379587555334787777534979154490245028428331770854155984028094522717604551280831139176195492937074690105891505117530197419798261465994522325628710753631989827952360104406778337958752201709363584477187830736045691403235427328057591344443941783990732351786082511745851084128118289801087408549235485943882956707069057697010795389463405807177487004804115250461427574115556953829799173123883099384802378568331942170419015819653303572635403071585905258715883906276166722843227368847623638708116893952307117380327286571724684337200632600297332899745301313362253357462566656722157486408661678174860688064249883","master_secret":"88042170121136289851304577468207881663846699185235819351929682297699418984612363800329704554096169234506635132879762474068771764075457969505958334858677847278538210347914912578172422036286546773502360084402832475901072829805287377040684002905431631502040790637441103904264661136050928998520743612212102462220310584327569826139702761382235452185221704680159013793915937849467955463430462497114529366080230657483200759911927171885713465667921246906547165922666054517119662789329549490302153470006824110100240568597899452341583445494274575974771114396431800185388643830421406009373917765994583238140029245593459507380519","effective_date":"6665595432931246021740360836666433942547320764396664812625851047262403642703256793404338137026963109524210216456598650694621136332081313753258922085247782044708406665841454120977905641532162952973377748213218506924390796235179096333782095728848902088343335360348775994115848366804031261441560416062648685500654784373316943581296905140737293418113963263199073691883890711731924871639375611793544147140308941098928718435113017439009131761530008151414454050654185172407139045115888755286147592181168618806511591475364890516589551665999768464133124373995934891423072925148848541284379677729509456580885776836941143648188","permit_issued_date":"2815497590838425011078102849123997184025138006182522262073898926959331472557134606799358033297243915789458057668739559060414048466994034349414401817152412741656301749080034430415862574255935741233909957885937578110003629849642580441972346853664442544756291361278635157932829932884981360721851078820469111548875399971256368798427815573860601400941573095379384813882245050186160188618366495222762509340714500153025108250710829046609711747845855682848450982524448043963180712210548328640571092535833518739361545371246501065921968061024232704238398480708381781577170031300863544280320480031519266073320155176994213188691","corp_num":"56273513875479118876000953025745078056342391943750869352712600190864759093795413474327601575558588957922704553291075865381740493734226666985304603539652698528673412677240479838922660379753764443002473850879803822152084381476612571056144307029440706449663301264630558789537001666876144626863101384099359470844105616532954268461595814456953178256339777427477671115145280954053887794606956052486229345835719690971530788129531400126823820683822494868207710308294439527885168926738108265910377255687757539116000109364477377296118746712287633477563568465347766214996718391408455133200568894279865421340907162424420645411599","permit_type":"72356269316237681429875229394556834187166327164484463529643088693779336142871149928442980232434508025774288856912175608402921351824828014379102639297425833862296691662251706687201774453303991681244141032554195618882020525766423655376608481175840407243190003154660129826148404308031262288663597905396903533094771456291627111559398185642843126462998755111958216209175967904307473718550979209868258204588714013256506636076837834707678779616823815970014341844446886160676332548030272577039029005454660218450605863134864740951999278889648758241417293642576105729400550080709161626795344410573651323247202370980700447843143","permit_status":"62880987787347736400883272411738366024381844287468095353315937297606598993146345668597500063169153667927320702746817088159056971696711421224187112335898122834442316283122949526391292944319812649399611696351267169709492971396304050887816643880202972726851298727050226871081731789683196702741355604918785839668423583128753300480236112633438191904232993896055655998379775528877060172362446964009319753535527328416234341463176903076592795321437971193473250967668913734343580241940450683972802919838236997083309141817063286043880280807261467816411989980014902432168743250074048301120034329340080449499854358407732850593450"}}' \
  outputFile=/tmp/ian-permit.ian-co_author_signed_cred_def.txn
  ```

7. Playing the role of the Endorser - Sign and write the Cred Def to the ledger

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli write-signed-transaction \
  walletName=endorser_wallet \
  storageType=default \
  storageConfig='{}' \
  storageCredentials='{}' \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_author_signed_cred_def.txn
  ```


8. Playing the role of the Author - Make another backup of your wallet

```
./manage \
  -v /c/von-network/cli-scripts \
  indy-cli export-wallet \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  exportPath=/tmp/myorg_issuer_wallet_initialization_complete.export
```

## Restart the Agent with the Initialized Wallet

1. Restart the Agent

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