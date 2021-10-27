import os
import logging
import base64
import argparse
import asyncio
import sys
# Import server.anchor from the path relative to where the scripts are being executed.
sys.path.insert(1, './server')
from anchor import AnchorHandle

logging.getLogger().setLevel(logging.ERROR)

async def generate_did(seed):
    TRUST_ANCHOR = AnchorHandle()
    did, verkey = await TRUST_ANCHOR.seed_to_did(seed)
    print(f"\nSeed: {seed}")
    print(f"DID: {did}")
    print(f"Verkey: {verkey}")

def main(seed):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_did(seed))
    loop.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generates a DID and Verkey from a Seed.")
    parser.add_argument("--seed", required=True, default=os.environ.get('SEED'), help="The seed to use to generate the DID and Verkey.")
    args, unknown = parser.parse_known_args()

    testseed = args.seed
    if testseed.endswith("="):
        testseed = base64.b64decode(testseed).decode("ascii")

    if not len(testseed) == 32:
        print("Seed must be 32 characters long.")
        exit()

    main(args.seed)