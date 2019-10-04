import asyncio
import json
import logging
import os
import sys

from indy.error import ErrorCode, IndyError
from indy import did, ledger, pool, wallet

LOGGER = logging.getLogger(__name__)

GENESIS_FILE = (
    os.getenv("GENESIS_FILE") or "/home/indy/ledger/sandbox/pool_transactions_genesis"
)

POOL = 0
DOMAIN = 1
CONFIG = 2

LEDGER_SEED = "000000000000000000000000Trustee1"


async def sync():

    pool_name = "nodepool"
    pool_cfg = {}

    await pool.set_protocol_version(2)

    pool_names = {cfg["pool"] for cfg in await pool.list_pools()}
    if pool_name not in pool_names:
        await pool.create_pool_ledger_config(
            pool_name, json.dumps({"genesis_txn": GENESIS_FILE})
        )

    pool_handle = await pool.open_pool_ledger(pool_name, json.dumps(pool_cfg))
    LOGGER.info("Connected to ledger pool")

    wallet_cfg = {"id": "trustee_wallet", "freshness_time": 0}
    wallet_access = {"key": "key"}

    try:
        await wallet.create_wallet(
            config=json.dumps(wallet_cfg), credentials=json.dumps(wallet_access)
        )
    except IndyError as e:
        if e.error_code == ErrorCode.WalletAlreadyExistsError:
            LOGGER.info("Wallet already exists")
        else:
            raise

    wallet_handle = await wallet.open_wallet(
        config=json.dumps(wallet_cfg), credentials=json.dumps(wallet_access)
    )
    LOGGER.info("Opened wallet")

    try:
        (my_did, my_verkey) = await did.create_and_store_my_did(
            wallet_handle, json.dumps({"seed": LEDGER_SEED})
        )
        LOGGER.info("Created wallet DID")
    except IndyError as e:
        if e.error_code == ErrorCode.DidAlreadyExistsError:
            LOGGER.info("DID already exists in wallet")
        else:
            raise

    get_aml_req = await ledger.build_get_acceptance_mechanisms_request(
        my_did, None, None
    )
    rv_json = await ledger.sign_and_submit_request(
        pool_handle, wallet_handle, my_did, get_aml_req
    )
    print("AML", rv_json)

    get_taa_req = await ledger.build_get_txn_author_agreement_request(my_did, None)
    rv_json = await ledger.sign_and_submit_request(
        pool_handle, wallet_handle, my_did, get_taa_req
    )
    print("TAA", rv_json)

    for ledger_name in ("DOMAIN",):
        txn_idx = 1
        while True:
            req_json = await ledger.build_get_txn_request(my_did, ledger_name, txn_idx)
            rv_json = await ledger.submit_request(pool_handle, req_json)
            rv = json.loads(rv_json)
            if not rv["result"]["data"]:
                break
            print(ledger_name, txn_idx)
            txn_idx += 1
        # await asyncio.sleep(0.1)


if __name__ == "__main__":
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(stream=sys.stdout, level=level)
    logging.getLogger("indy.libindy").setLevel(logging.WARNING)
    try:
        asyncio.get_event_loop().run_until_complete(sync())
    except Exception:
        LOGGER.exception("Error running sync test")
