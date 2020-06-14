import os
import asyncio
import json
import pprint
from ctypes import *
from hashlib import sha256

from indy import pool, ledger, wallet, did, anoncreds
from indy.error import ErrorCode, IndyError

wallet_name = os.getenv('walletName', 'local_wallet')
wallet_storage_type = os.getenv('storageType', 'postgres_storage')
wallet_storage_config = json.loads(os.getenv('storageConfig', '{"url":"localhost:5435"}'))
wallet_storage_credentials = json.loads(os.getenv('storageCredentials', '{"account":"DB_USER","password":"DB_PASSWORD","admin_account":"postgres","admin_password":"mysecretpassword"}'))
wallet_key = os.getenv('walletKey', 'key')

wallet_config = json.dumps({"id": wallet_name, "storage_type": wallet_storage_type, "storage_config": wallet_storage_config})
wallet_credentials = json.dumps({"key": wallet_key, "storage_credentials": wallet_storage_credentials})

wallet_did = os.getenv('walletDid', 'VePGZfzvcgmT3GTdYgpDiT')
did_seed = os.getenv('didSeed', '0000000000000000000000000MyAgent')

metadata = json.loads(os.getenv('didMetadata', '{}'))

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

async def set_did_metadata():
    try:
        print_log('\nOpening wallet ...\n')
        print(wallet_config)
        print(wallet_credentials)
        wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

        print_log('\nGenerating seed hash ...')
        seed_hash = sha256(did_seed.encode()).hexdigest()
        did_metadata = {**(metadata or {}), 'public': True, 'seed_hash': seed_hash}
        
        print_log('\nWriting metadata for DID ...')
        print_log('DID: ' + wallet_did)
        print_log('Metadata: ' + json.dumps(did_metadata))
        await did.set_did_metadata(wallet_handle, wallet_did, json.dumps(did_metadata))

    except IndyError as e:
        print('Error occurred: %s' % e)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_did_metadata())
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
