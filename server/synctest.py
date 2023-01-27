import asyncio
import logging
import os
import sys

import indy_vdr
from indy_vdr import ledger, open_pool

LOGGER = logging.getLogger(__name__)

GENESIS_FILE = os.getenv("GENESIS_FILE") or "/home/indy/ledger/sandbox/pool_transactions_genesis"

POOL = 0
DOMAIN = 1
CONFIG = 2

LEDGER_SEED = "000000000000000000000000Trustee1"


async def sync():
    LOGGER.info("Connecting to ledger pool")

    indy_vdr.set_protocol_version(2)

    pool = await open_pool(transactions_path=GENESIS_FILE)

    LOGGER.info("Connected to ledger pool")

    get_aml_req = ledger.build_get_acceptance_mechanisms_request()
    rv = await pool.submit_request(get_aml_req)
    print("AML", rv)

    get_taa_req = ledger.build_get_txn_author_agreement_request()
    rv = await pool.submit_request(get_taa_req)
    print("TAA", rv)

    for ledger_name in ("DOMAIN",):
        txn_idx = 1
        while True:
            request = ledger.build_get_txn_request(None, ledger_name, txn_idx)
            rv = await pool.submit_request(request)
            if not rv["data"]:
                break
            print(ledger_name, txn_idx)
            txn_idx += 1
        # await asyncio.sleep(0.1)


if __name__ == "__main__":
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(stream=sys.stdout, level=level)
    try:
        asyncio.get_event_loop().run_until_complete(sync())
    except Exception:
        LOGGER.exception("Error running sync test")
