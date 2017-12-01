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
app.static('/', './static/index.html')


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


@app.route("/status")
async def status(request):
    response_text = ""
    response_text += "NODE 1:\n\n"

    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/validator-info", "-v", "--basedir", "/home/indy/.mnt/node1/sandbox/"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    response_text += proc.stdout
    response_text += "\n\n"
    response_text += "NODE 2:\n\n"

    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/validator-info", "-v", "--basedir", "/home/indy/.mnt/node2/sandbox/"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    response_text += proc.stdout
    response_text += "\n\n"
    response_text += "NODE 3:\n\n"

    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/validator-info", "-v", "--basedir", "/home/indy/.mnt/node3/sandbox/"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    response_text += proc.stdout
    response_text += "\n\n"
    response_text += "NODE 4:\n\n"

    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/validator-info", "-v", "--basedir", "/home/indy/.mnt/node4/sandbox/"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    response_text += proc.stdout
    response_text += "\n\n"

    return text(response_text)


@app.route("/ledger/domain")
async def ledger_domain(request):
    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/read_ledger", "--type", "domain", "--base_dir", "/home/indy/.mnt/node1"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    return text(proc.stdout)


@app.route("/ledger/domain/pretty")
async def ledger_domain_pretty(request):
    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/read_ledger", "--type", "domain", "--base_dir", "/home/indy/.mnt/node1"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    resp_text = ""

    lines = proc.stdout.splitlines()
    for line in lines:
        parsed = json.loads(line)
        resp_text += json.dumps(parsed, indent=4, sort_keys=True) + "\n\n"

    return text(resp_text)


@app.route("/ledger/pool")
async def ledger_pool(request):
    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/read_ledger", "--type", "pool", "--base_dir", "/home/indy/.mnt/node1"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    return text(proc.stdout)


@app.route("/ledger/pool/pretty")
async def ledger_pool_pretty(request):
    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/read_ledger", "--type", "pool", "--base_dir", "/home/indy/.mnt/node1"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    resp_text = ""

    lines = proc.stdout.splitlines()
    for line in lines:
        parsed = json.loads(line)
        resp_text += json.dumps(parsed, indent=4, sort_keys=True) + "\n\n"

    return text(resp_text)


@app.route("/ledger/config")
async def ledger_config(request):
    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/read_ledger", "--type", "config", "--base_dir", "/home/indy/.mnt/node1"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    return text(proc.stdout)


@app.route("/ledger/config/pretty")
async def ledger_config_pretty(request):
    proc = subprocess.run(
      ["/usr/bin/python3", "/usr/local/bin/read_ledger", "--type", "config", "--base_dir", "/home/indy/.mnt/node1"],
      stdout=subprocess.PIPE,
      universal_newlines=True)

    resp_text = ""

    lines = proc.stdout.splitlines()
    for line in lines:
        parsed = json.loads(line)
        resp_text += json.dumps(parsed, indent=4, sort_keys=True) + "\n\n"

    return text(resp_text)


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