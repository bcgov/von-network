"""
Example demonstrating how to write Schema and Cred Definition on the ledger
As a setup, Steward (already on the ledger) adds Trust Anchor to the ledger.
After that, Steward builds the SCHEMA request to add new schema to the ledger.
Once that succeeds, Trust Anchor uses anonymous credentials to issue and store
claim definition for the Schema added by Steward.

ledger custom context
Transaction stored into context: "{\"endorser\":\"DFuDqCYpeDNXLuc3MKooX3\",\"identifier\":\"VePGZfzvcgmT3GTdYgpDiT\",\"operation\":{\"data\":{\"attr_names\":[\"age\",\"name\"],\"name\":\"dev_schema\",\"version\":\"1.2\"},\"type\":\"101\"},\"protocolVersion\":2,\"reqId\":1568154574190172000,\"signatures\":{\"DFuDqCYpeDNXLuc3MKooX3\":\"3x14Ygzf31EeLExUfMSjmx6HMgQPGBstvsHHVvHw44vNqJR3kBJFDwuJZDankVyvW3hYJ7x3ZQDrrnnG1kuxAhBK\",\"VePGZfzvcgmT3GTdYgpDiT\":\"4P37W4gr52ivo5QAf3hWZb8RbpHqhY8CxGXMmz93anLoEPczT89G3jbxcDGGovog394y3gntdQk68N3qa5Rs5DU1\"}}".
Would you like to send it? (y/n)
Response: 
{"op":"REPLY","result":{"rootHash":"61EH3J6iXAdwUFT9zGss7dSDPdUJwFvJp32QmVTAvRDw","reqSignature":{"values":[{"value":"3x14Ygzf31EeLExUfMSjmx6HMgQPGBstvsHHVvHw44vNqJR3kBJFDwuJZDankVyvW3hYJ7x3ZQDrrnnG1kuxAhBK","from":"DFuDqCYpeDNXLuc3MKooX3"},{"value":"4P37W4gr52ivo5QAf3hWZb8RbpHqhY8CxGXMmz93anLoEPczT89G3jbxcDGGovog394y3gntdQk68N3qa5Rs5DU1","from":"VePGZfzvcgmT3GTdYgpDiT"}],"type":"ED25519"},"txn":{"metadata":{"endorser":"DFuDqCYpeDNXLuc3MKooX3","reqId":1568154574190172000,"digest":"6ba64dced37fc521af14068a43f3ff8cf7f850d1ca181f1a597001e4773159b9","from":"VePGZfzvcgmT3GTdYgpDiT","payloadDigest":"e307a539c5f9a3ae6ffd05c02e8c11a0d55918049db9b050205d23d908b1333a"},"data":{"data":{"attr_names":["age","name"],"version":"1.2","name":"dev_schema"}},"type":"101","protocolVersion":2},"auditPath":["FmxWWUzAJwovuzGX5w4XfuHRZYygCzrL7GbUV8SZxezk","6csF72LgqDN73eeopkqkC9bmRdCpZhWCpkb8oLzzfq7D","AvQXbGgKZjNvncEAgFKPooaSJYUCVCpaFbKNJs1AbZSu","E4X7V7EccEJdYWY1JKTnk3g69Mw59QFYUN14J68yJoLP","EmviEJYzYq4UsT7RvR2H8Ypb7mhKMabhz45LWasgERN"],"txnMetadata":{"seqNo":70211,"txnTime":1568154721,"txnId":"VePGZfzvcgmT3GTdYgpDiT:2:dev_schema:1.2"},"ver":"1"}}

:indy> ledger get-schema did=VePGZfzvcgmT3GTdYgpDiT name=dev_schema version=1.2
Following Schema has been received.
Metadata:
+------------------------+-----------------+---------------------+---------------------+
| Identifier             | Sequence Number | Request ID          | Transaction time    |
+------------------------+-----------------+---------------------+---------------------+
| DFuDqCYpeDNXLuc3MKooX3 | 70211           | 1568154820447785000 | 2019-09-10 22:32:01 |
+------------------------+-----------------+---------------------+---------------------+
Data:
+------------+---------+--------------+
| Name       | Version | Attributes   |
+------------+---------+--------------+
| dev_schema | 1.2     | "age","name" |
+------------+---------+--------------+

This script returns:
{'id': 'DFuDqCYpeDNXLuc3MKooX3:3:CL:1',
 'schemaId': '1',
 'tag': 'tag',
 'type': 'CL',
 'value': {'primary': {'n': '109330248353590897319389070001241417443720503932971588287006464922388229178334793336510417955875881059871543804578087088276791800083305615121644511248337970131893077241681758874562815652760517127419781690778951536164836285458183775012778319181918711231775022070055487033667781997555780000964033080223070801890480454130338986221023468272183501187404600365439161142989665555780971754563754309510943630872371340817447612828969885782344790492881494591201224675720837407955083191745600556967629527217606100951074519486650521288615897758074209367922751727352657076430733961205538551220485786837438600982766853425186252644017',
                       'r': {'age': '73308673216472493575090598174963399948529629134006496210571752239581655779012920152879390449719574107939536194125393138485840251400105908560965343195463986660046396898151291844591150186299279740115095392914394151816733033421421781471599302173575425800443185010936709144943232555123378965813972641717797624815066173821197309970706537526529635178157107747878761192927131531306789978613595162689363565628723311165111774867707907441698784714369233660014225193452769768361969161868978698182387153720193894374602878251447258528578841422721713848011884183426934563483417227006937242841853827004235408539062962437389057557466',
                             'master_secret': '68361484436365673061072041624647294914425855902623496297375686496312847852294891269292033386069491663411635310339094263142698298689132782329339987266934634535728272777489921087755693951033987277703390817896541076260102142585504616782084149039016192790475658619096435661926936093335858078539362316056330917248469510038667267988488591837331636897350889581870219495748565872958952115592906821121236209205411654897745071778422593295566925294862162049245508656755995167332502259192551948308838679613532706595396718914348820966604241737677454847945523997559921590852327709685893644680377213866453241491125951811592264674385',
                             'name': '47956700491301067281258647205353751258983285450131303607847093059046267200221967853146726991503228245603799976265038836926279273756505065304549666555819258018152979494728703569302125080586313807600151910235972765806376471411615253734993567102101608092977530540217931683348869413718435281288986248345335344018542983222736766375500635662856035064726147913925488526522192025619312494021637149847804815197911363884756275007799195202034451124167367439201703744060644702991961222569708991445106308180298048676620063203473029844891286050419366140751942222786439647012450277116627707784993011702899356860514634641379792471881'},
                       'rctxt': '85822465136763484750224903111930923618937001868097822592103216386643211499337898367784057120826066430186818827320375097357041704110495665025997489429045658165162147907795204346206877770526428837895201878621908877672713195000392657196945094035963718417455273866302452201821774685040248478392362268576673532904049764968773578332077261408115307685949804917889275660854872818155274730122917471074855046658920937068414071937936393976713715659099504318383054607840309655173598188730099851335185640343544202013064216095459208905638997738029996011970156760774708328892008498934772831156833716387364110926733423726356601343689',
                       's': '106345188679199089125597322701414631094937145030314613341378947140738361187874138161772329427608423907567247428077450395652493629986745542580472189756730607466150103643195464371742896667685304340461985111222457560719775350966587953014029845146432673104558897228576416276655693758576076167730137327545172086773323375530896947049176540552702297043676954245462417720544877461007526007923822646362581648140569373776087100702971388864141862849461540636711884781495543149191950953666057015608051814287517402916176848788512328682250948222207557803534778301129658621242780466275103890365613475979127357941024766695451697885176',
                       'z': '47107036540803311469435904351406772134330713253387217487860154283622977007467454258519685096545379994908750889467439958454982798929251155494690304601387525503696682822022729189520351495627997108947442055176478587213869104400238227223946797194814057365368583932995967095555966182151943614690693513901167896619168429109522378359328460889950835611914690332686684663213810934909998666094622585987936453973281713802447375961016451674180164951212112576812042153386412793986139385065180612574606273328511899790711670508882466261670565204415908876341282665166564296557762007159015012163706719247955095314823816627774810936820'}},
 'ver': '1.0'}
"""
import os
import string
import asyncio
import json
import pprint
from ctypes import *

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import ErrorCode, IndyError

pool_name = os.getenv('poolName', 'local_pool')
PROTOCOL_VERSION = 2

wallet_name = os.getenv('walletName', 'local_wallet')
wallet_storage_type = os.getenv('storageType', 'postgres_storage')
wallet_storage_config = json.loads(os.getenv('storageConfig', '{"url":"localhost:5435"}'))
wallet_storage_credentials = json.loads(os.getenv('storageCredentials', '{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}'))
wallet_key = os.getenv('walletKey', 'key')

wallet_config = json.dumps({"id": wallet_name, "storage_type": wallet_storage_type, "storage_config": wallet_storage_config})
wallet_credentials = json.dumps({"key": wallet_key, "storage_credentials": wallet_storage_credentials})

author_did = os.getenv('authorDid', 'VePGZfzvcgmT3GTdYgpDiT')
seq_no = int(os.getenv('schemaId', '10'))
schema_name = os.getenv('schemaName', 'ian-permit.ian-co')
schema_version = os.getenv('schemaVersion', '1.0.0')
schema_attributes = os.getenv('schemaAttributes', 'corp_num,legal_name,permit_id,permit_type,permit_issued_date,permit_status,effective_date').split(",")

cred_def_tag = os.getenv('tag', 'tag')
cred_def_type = os.getenv('type', 'CL')

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def write_schema_and_cred_def(cred_def_primary_file="/tmp/primarykey.txt"):
    try:
        pool_ = {
            'name': pool_name
        }
        print_log("Open Pool Ledger: {}".format(pool_['name']))

        # Set protocol version 2 to work with Indy Node 1.4
        await pool.set_protocol_version(PROTOCOL_VERSION)
        pool_['handle'] = await pool.open_pool_ledger(pool_['name'], None)

        # 4.
        print_log('\n4. Open wallet and get handle from libindy\n')
        print(wallet_config)
        print(wallet_credentials)
        wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

        print(wallet_handle)

        # 9.
        print_log('\n9. Build the SCHEMA request to add new schema to the ledger as a Steward\n')
        # get the seq # from the Sovrin schema transaction
        schema = {
            'seqNo': seq_no,
            'dest': author_did,
            'data': {
                'id': author_did + ':2:' + schema_name + ':' + schema_version,
                'seqNo': seq_no,
                'name': schema_name,
                'version': schema_version,
                'ver': '1.0',
                'attrNames': schema_attributes
            }
        }
        schema_data = schema['data']
        print(schema)

        # 11.
        print_log('\n11. Creating and storing CRED DEFINITION using anoncreds as Trust Anchor, for the given Schema\n')
        cred_def_config = json.dumps({"support_revocation": False})

        (cred_def_id, cred_def_json) = await anoncreds.issuer_create_and_store_credential_def(
                        wallet_handle, author_did, json.dumps(schema_data),
                        cred_def_tag, cred_def_type, cred_def_config)

        print_log('Credential definition: ')
        cred_def = json.loads(cred_def_json)
        pprint.pprint(cred_def)
        print_log('\nCred def primary: ')
        cred_def_primary = cred_def['value']['primary']
        cred_def_primary_output = json.dumps(cred_def_primary).translate({ord(c): None for c in string.whitespace})
        print(cred_def_primary_output)
        with open(cred_def_primary_file, "w") as text_file:
            text_file.write(cred_def_primary_output)

    except IndyError as e:
        print('Error occurred: %s' % e)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_schema_and_cred_def())
    loop.close()

if __name__ == '__main__':
    print("Loading postgres")
    stg_lib = CDLL("libindystrgpostgres.so")
    result = stg_lib["postgresstorage_init"]()
    if result != 0:
        print("Error unable to load wallet storage", result)
        parser.print_help()
        sys.exit(0)
    print(result)

    main()
