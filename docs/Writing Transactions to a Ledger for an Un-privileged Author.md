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
  indy-cli export-wallet \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  exportPath=/tmp/myorg_issuer_wallet_initialized_with_did.export
```
**Note:** This will make a backup of the wallet in it's initialized state.  There will be nothing else in the wallet other than a DID at this point.  It's good practice to make a backup after each step.  That way if something goes wrong you can roll back the wallet to a previous state and then move forward again.

### 2. Playing the role of the Author - Write the (author signed) schema to a file so it can be signed by the (intended) endorser.

```
./manage \
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

**Export a copy of the wallet in it's current state:**
```
./manage \
  indy-cli export-wallet \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  exportPath=/tmp/myorg_issuer_wallet_did_schema.export
```

As the author you would send the resulting file to your endorser for signing.

### 3. Playing the role of the Endorser - Initialize a local wallet:

```
./manage \
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

Use the value of the `seqNo` you noted in the previous step as the value for `schemaId` in the following call.

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

### 7. Playing the role of the Author - Write the (author signed) cred def to a file so it can be signed by the (intended) endorser.  Plug in the `schemaId` and `primaryKey` you noted from earlier operations.

```
./manage \
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
  primaryKey='{"rctxt":"54315105665899191969800013595012002778071782908268772603844704728739698579575455035339105610300893622075052386553145215352019408862676253110071535364292346933826289796277389414109642982429090624263682735584524776048406476200877480082132024102646432958869319201916033848480749492289166918653617545116574416214604403397852314843838386422056097090461095800290948909233530099396842026869108270974597815338965644429881219968106705484056966859156007285125418665180084367904784410053473352184174928251745501667172617881712991289959052167947125462006588223040285979898645222088076925154700992069276570301963282652610139166716","z":"11587109351433884524755696971869531794171473771024594490558384399466554500629687386310534969601521720799321613982272251567023031437759719351855654653963432199322279556139410737153763368489808709712309282336432860476139742386740815454800169130241583121278054610989176928781482631677058704852952715517031257151036352335789199807066940287109265748756367530743107760214314921609982929676292451608300723996920274972167019729248945741750048009596947692164215894482593513015567088150264253633561184361493806429442415571107513515883296088749116981313322123642329230252851373729070414623788823707105885424841683353322406982330","n":"89852286203944676236941315545203564123896751296339347743251615686323071021120833554242392120862882023223333311361902988922463355078456047449546828889622658729159346533093802962985370460195289849486677302431995393567332453327508303378173197692310966741008356100612755513349599953036483288435836799576434871572808634280691028480707593198192307114665362343777211496085128624962211950892731224992968831657547521497207091926196830340691319665844987454842276752022375071379934539121304838957692073259212164310645259047445468580002771208810027925385889094624837266860742701285493354172028847928146435486721788280682093852629","s":"50571776180953640416915126026247199465402876014679139120645305453619583256966990981833853742474324504375961082652802888720979553951009662022973931419544186270629845451637695501035717779029955426666115198240774858614651336359681838754297120368346076481103267973429672291309369509983497853585336015972081266103718670754470990009635477008600334207786057196969875814880448524715529015289084152990372421911676367022868155776213180131821465047872390508672964822748964684129081139336424874706540296601917791796007911935100904563390294731831149258219046899541179647469980050638617457660924485581007693811418300794712239871152","r":{"legal_name":"13726541422323885397167495734168597424484907664950528143558889687713059819277727326713393014654260628355975292192362670729049586480806361612617064027183882999713558461072053913282326672221022125922751438387390113157488362536229189987724317251578411016322155853174557209233395143566642006316247303637897501650481541830666601317950621208735851710759838958354848585845052332741357813344693024526131792682116444424229214619548666153251877187079430379809305434041606716057326149648436894645157181888885376586006076960547500239712137330957443930926069837614323279640330004227450952000774132962075080372903209056124099725599","master_secret":"48358750727818881758098564739323563478662941599624298928661190085109155372305759597323830478872596754877799344747899738461022168716087754161894271051308832254541159038913329528414080020496210741019534450779440336570034894148316118974041212660635968111401482686495504690214175146450309069023837711074928671789479456212021835314917645996831723764358819405571154474297300038543135050693498589855122633506213500534286101085880958695072479580500763695294358697471251067985232984548214486937398266902231497606094276866427423018319479407790260871852455208003545683544815806048094799606029961357726322610704397885882921384389","permit_status":"27082095451948779136977884318728610175053723471854039005593702359963004124594256528054145831699043502942242946553585193043686504639977938529570120476623472435863484542150788246063914577065507766070116567634958551941399666147088947600257584354922499686437770746377777583489506477740218888518306176783670898178190803923228564151887824675469179913544447027218808926671767410217036029867465335761014385249301011404044198123921164827886172285926930499289581629959160163186815220247175064336005431851700157358033080716528617040681174254634672978363253378098511852194329143572650945530959720638238448328622681170136158362863","corp_num":"40328532335232532309139381366732654693610000189254939665878622664348036817379229826167918489239981357281944057239641221942811169932285164399483103991674219538584700171545251273951522338368718139732774388104313697237541825532603782619448124305621959895595577726531784840170491202222139728965655322538372888551553008994033189684556396028975832114192837678453701106390021220042506545343964341826035469193648501322425096339058217813071845890383711645083553130580139739160060874237980705265233262411365010723174931772911471312418664281917992264465507889030862266678924677592863894411236765176824236150591016471102788445512","effective_date":"7074333450041177511502300767065898447478362241315103803697542348893813387299137169159466307821443680264600045425573648969580444937711084570482533516331689004245759070392128628567553942958471324978695824893345907892224998529280626547929174615314199053747630767343470799004531243962151046973828078656067101487165580513691278224449442935638981832871529487498264573109089253794618886845541111838112144618667135465116689671958652791699487547385000557720830603603734075443633829461222961784444522055954209762399878676435878463383129015269206465551065605431825278897264901020333478878087676062408241966739247811850065410491","permit_issued_date":"19642195641421815238528952585771811764934961740553951906210454556625160321899146735286425714583480152513154352800302226878825682793735936786148229506733257634413040151824575230426945097648337125691843500465558844749305647957834408066514328399507471522165709496696051198256806942181255379997555138893217687738655309887243907105993706488663546635235472967438720510233738221404432468431480047679529681331430701539120486315015812776860987794579244724613813118354062397971352063593695242699582665719130670776816883037932906191998095153420475343515637295440223062246446088667569454859599010593012718649832883973006150523334","permit_id":"19535021967359384114826776225532752940297229334993117327492125143405656708828494919563963311488205241434868532893377688975919484358972217839058432955404326749206562356968154975243168164154938517522163585211583433829703646645696595541112997890081979447954016757728767968816617492788421444693889221242436941064128234284666675460697552001355543113181533435413856541061415563000788502565318172768376745186801013622366736586327266878829821438882207945471558219639381592804340400203008545740118555466765797454162077320617975435717214669994168450761661440769526551316562723852407984882914023126060462306152319454384260140027","permit_type":"50188573003030390541269929520609088906297039354847958987026511236491788034400718446472628707748711503479404278439898905931163996160853142643419665819492007199070877349210711244504337973732161701244546024728631374330132017117635691425585897674689760269984591223560631591971494959294707537647710247580299082169387534477827059230141398269057538311767511785546976898326394743418882168988412776693912343324334069259653038897837279819208163813953085504760392835290001545621593882517740042092786088293208752889306658347509469050979399692984974769993330677714455467062051912327029917369886647714440381569678552361325295193764"}}' \
  outputFile=/tmp/ian-permit.ian-co_author_signed_cred_def.txn
  ```

**Export a copy of the wallet in it's current state:**
```
./manage \
  indy-cli export-wallet \
  walletName=myorg_issuer \
  storageType=postgres_storage \
  storageConfig='{"url":"192.168.65.3:5435"}' \
  storageCredentials='{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}' \
  exportPath=/tmp/myorg_issuer_wallet_did_schema_cred-def.export
```  

As the author you would send the resulting file to your endorser for signing.


### 8. Playing the role of the Endorser - Endorse the cred-def transaction and write it to a file:

```
./manage \
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
  indy-cli write-transaction \
  poolName=localpool \
  authorDid=NFP8kaWvCupbDQHQhErwXb \
  endorserDid=DFuDqCYpeDNXLuc3MKooX3 \
  inputFile=/tmp/ian-permit.ian-co_endorser_signed_cred_def.txn
```
```
Response:
{"op":"REPLY","result":{"txnMetadata":{"txnTime":1570554695,"seqNo":13,"txnId":"NFP8kaWvCupbDQHQhErwXb:3:CL:9:tag"},"reqSignature":{"values":[{"value":"3LBc8KXiN8LYJtbMVrYVMGzw8exPqzUFPFwyv4dyHKy1ubkdVra6nh97LSP5pmsx9tpC2AY8xHgozqjzkZKpEUsx","from":"DFuDqCYpeDNXLuc3MKooX3"},{"value":"34Kmi3N3E8yx8zHL6VYfWNtRekZB56jn9cVa63WLUE2MZqUDfRBFpbzAEiPtt4cxHasHZjuVi1PfWjhXfgXUpSuo","from":"NFP8kaWvCupbDQHQhErwXb"}],"type":"ED25519"},"ver":"1","rootHash":"6iapGjMdDLDMVd9P4bs9DSD1TwYcrte2h7zStzouZWw4","txn":{"data":{"data":{"primary":{"rctxt":"54315105665899191969800013595012002778071782908268772603844704728739698579575455035339105610300893622075052386553145215352019408862676253110071535364292346933826289796277389414109642982429090624263682735584524776048406476200877480082132024102646432958869319201916033848480749492289166918653617545116574416214604403397852314843838386422056097090461095800290948909233530099396842026869108270974597815338965644429881219968106705484056966859156007285125418665180084367904784410053473352184174928251745501667172617881712991289959052167947125462006588223040285979898645222088076925154700992069276570301963282652610139166716","n":"89852286203944676236941315545203564123896751296339347743251615686323071021120833554242392120862882023223333311361902988922463355078456047449546828889622658729159346533093802962985370460195289849486677302431995393567332453327508303378173197692310966741008356100612755513349599953036483288435836799576434871572808634280691028480707593198192307114665362343777211496085128624962211950892731224992968831657547521497207091926196830340691319665844987454842276752022375071379934539121304838957692073259212164310645259047445468580002771208810027925385889094624837266860742701285493354172028847928146435486721788280682093852629","r":{"effective_date":"7074333450041177511502300767065898447478362241315103803697542348893813387299137169159466307821443680264600045425573648969580444937711084570482533516331689004245759070392128628567553942958471324978695824893345907892224998529280626547929174615314199053747630767343470799004531243962151046973828078656067101487165580513691278224449442935638981832871529487498264573109089253794618886845541111838112144618667135465116689671958652791699487547385000557720830603603734075443633829461222961784444522055954209762399878676435878463383129015269206465551065605431825278897264901020333478878087676062408241966739247811850065410491","permit_id":"19535021967359384114826776225532752940297229334993117327492125143405656708828494919563963311488205241434868532893377688975919484358972217839058432955404326749206562356968154975243168164154938517522163585211583433829703646645696595541112997890081979447954016757728767968816617492788421444693889221242436941064128234284666675460697552001355543113181533435413856541061415563000788502565318172768376745186801013622366736586327266878829821438882207945471558219639381592804340400203008545740118555466765797454162077320617975435717214669994168450761661440769526551316562723852407984882914023126060462306152319454384260140027","corp_num":"40328532335232532309139381366732654693610000189254939665878622664348036817379229826167918489239981357281944057239641221942811169932285164399483103991674219538584700171545251273951522338368718139732774388104313697237541825532603782619448124305621959895595577726531784840170491202222139728965655322538372888551553008994033189684556396028975832114192837678453701106390021220042506545343964341826035469193648501322425096339058217813071845890383711645083553130580139739160060874237980705265233262411365010723174931772911471312418664281917992264465507889030862266678924677592863894411236765176824236150591016471102788445512","permit_type":"50188573003030390541269929520609088906297039354847958987026511236491788034400718446472628707748711503479404278439898905931163996160853142643419665819492007199070877349210711244504337973732161701244546024728631374330132017117635691425585897674689760269984591223560631591971494959294707537647710247580299082169387534477827059230141398269057538311767511785546976898326394743418882168988412776693912343324334069259653038897837279819208163813953085504760392835290001545621593882517740042092786088293208752889306658347509469050979399692984974769993330677714455467062051912327029917369886647714440381569678552361325295193764","master_secret":"48358750727818881758098564739323563478662941599624298928661190085109155372305759597323830478872596754877799344747899738461022168716087754161894271051308832254541159038913329528414080020496210741019534450779440336570034894148316118974041212660635968111401482686495504690214175146450309069023837711074928671789479456212021835314917645996831723764358819405571154474297300038543135050693498589855122633506213500534286101085880958695072479580500763695294358697471251067985232984548214486937398266902231497606094276866427423018319479407790260871852455208003545683544815806048094799606029961357726322610704397885882921384389","legal_name":"13726541422323885397167495734168597424484907664950528143558889687713059819277727326713393014654260628355975292192362670729049586480806361612617064027183882999713558461072053913282326672221022125922751438387390113157488362536229189987724317251578411016322155853174557209233395143566642006316247303637897501650481541830666601317950621208735851710759838958354848585845052332741357813344693024526131792682116444424229214619548666153251877187079430379809305434041606716057326149648436894645157181888885376586006076960547500239712137330957443930926069837614323279640330004227450952000774132962075080372903209056124099725599","permit_status":"27082095451948779136977884318728610175053723471854039005593702359963004124594256528054145831699043502942242946553585193043686504639977938529570120476623472435863484542150788246063914577065507766070116567634958551941399666147088947600257584354922499686437770746377777583489506477740218888518306176783670898178190803923228564151887824675469179913544447027218808926671767410217036029867465335761014385249301011404044198123921164827886172285926930499289581629959160163186815220247175064336005431851700157358033080716528617040681174254634672978363253378098511852194329143572650945530959720638238448328622681170136158362863","permit_issued_date":"19642195641421815238528952585771811764934961740553951906210454556625160321899146735286425714583480152513154352800302226878825682793735936786148229506733257634413040151824575230426945097648337125691843500465558844749305647957834408066514328399507471522165709496696051198256806942181255379997555138893217687738655309887243907105993706488663546635235472967438720510233738221404432468431480047679529681331430701539120486315015812776860987794579244724613813118354062397971352063593695242699582665719130670776816883037932906191998095153420475343515637295440223062246446088667569454859599010593012718649832883973006150523334"},"z":"11587109351433884524755696971869531794171473771024594490558384399466554500629687386310534969601521720799321613982272251567023031437759719351855654653963432199322279556139410737153763368489808709712309282336432860476139742386740815454800169130241583121278054610989176928781482631677058704852952715517031257151036352335789199807066940287109265748756367530743107760214314921609982929676292451608300723996920274972167019729248945741750048009596947692164215894482593513015567088150264253633561184361493806429442415571107513515883296088749116981313322123642329230252851373729070414623788823707105885424841683353322406982330","s":"50571776180953640416915126026247199465402876014679139120645305453619583256966990981833853742474324504375961082652802888720979553951009662022973931419544186270629845451637695501035717779029955426666115198240774858614651336359681838754297120368346076481103267973429672291309369509983497853585336015972081266103718670754470990009635477008600334207786057196969875814880448524715529015289084152990372421911676367022868155776213180131821465047872390508672964822748964684129081139336424874706540296601917791796007911935100904563390294731831149258219046899541179647469980050638617457660924485581007693811418300794712239871152"}},"ref":9,"tag":"tag","signature_type":"CL"},"metadata":{"reqId":1570554573803315900,"digest":"b998b9060272c14d8c681e69293a7d79bd1302ec3cb871aed76ad02c0b1f3e71","payloadDigest":"9cfc3cb999a3fc586929da61b9d6d18b555b50dc809d66a28ba13d1cba7f8ffe","from":"NFP8kaWvCupbDQHQhErwXb","endorser":"DFuDqCYpeDNXLuc3MKooX3"},"type":"102","protocolVersion":2},"auditPath":["2hP7ZNwYE8VPqGpD4AngxR2w7jfMxtnJWaUXP8zMBdPE","ELQvYy5kajZbC4sNmcxSrVSW3Py3SM1ufRY3RGoWKBU6"]}}
```


### 10. Playing the role of the Author - Make a final backup of your wallet

```
./manage \
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
  indy-cli import-wallet \
  walletName=lcrb_wallet \
  storageType=postgres_storage \
  storageConfig='{"url":"host.docker.internal:5444"}' \
  storageCredentials='{"account":"USER_ewnp","password":"DLKD0sd098hsd9jsdf","admin_account":"postgres","admin_password":"98s7df987w4hfn90wemofwf2j0"}' \
  importPath=/tmp/lcrb_wallet_with_schemas_cred_defs_and_metadata.export
```