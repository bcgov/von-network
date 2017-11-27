#! /usr/bin/python3

import asyncio
import json
import subprocess

from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent
from von_agent.agents import BaseAgent


from sanic import Sanic
from sanic.response import text

app = Sanic(__name__)


async def boot():
    global pool
    global trust_anchor

    pool = NodePool(
        'nodepool',
        '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis')
    await pool.open()

    trust_anchor = TrustAnchorAgent(
        pool,
        '000000000000000000000000Trustee1',
        'trustee_wallet',
        None,
        '127.0.0.1',
        9700,
        'api/v0')
    await trust_anchor.open()


@app.route("/")
async def index(request):
    proc = subprocess.run(
      ["validator-info", "-v"],
      stdout=subprocess.PIPE,
      universal_newlines=True)
    return text(proc.stdout)


# Expose genesis transaction for easy connection.
@app.route("/genesis")
async def genesis(request):
    with open(
        '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis',
            'r') as content_file:
        gensis = content_file.read()
    return text(gensis)


# Easily write dids for new identity owners
@app.route("/register")
async def register(request):

    try:
        seed = request.args['seed'][0]
    except KeyError as e:
        return text('Missing query parameter: seed')

    new_did = BaseAgent(
        pool,
        seed,
        seed + '-wallet',
        None)

    await new_did.open()

    # Register agent on the network
    print('\n\nRegister agents\n\n')
    for ag in (trust_anchor, new_did):
        print('\n\nGet Nym: ' + str(ag) + '\n\n')
        if not json.loads(await trust_anchor.get_nym(ag.did)):
            # pass
            print('\n\nSend Nym: ' + str(ag) + '\n\n')
            await trust_anchor.send_nym(ag.did, ag.verkey)

    return text(new_did.did + ' successfully written to ledger')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(boot())
    loop.close()
    app.run(host="0.0.0.0", port=8000, debug=True)


# BC-Registrar-Agent-0000000000000