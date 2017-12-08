#! /usr/bin/python3

import asyncio
import json
import subprocess

from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent
from von_agent.agents import BaseAgent


from sanic import Sanic
from sanic.response import text, json as sanic_json

app = Sanic(__name__)
app.static('/', './static/index.html')
app.static('/include', './static/include')
app.static('/favicon.ico', './static/favicon.ico')

python_path = "/usr/bin/python3"


def json_reponse(data):
  headers = {'Access-Control-Allow-Origin': '*'}
  return sanic_json(data, headers=headers)


def validator_info(node_name, as_json=True):
  args = [python_path, "/usr/local/bin/validator-info", "-v"]
  if as_json:
    args.append("--json")
  args.extend(["--basedir", "/home/indy/.mnt/" + node_name + "/sandbox/"])
  proc = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True)
  if as_json:
    return json.loads(proc.stdout)
  return proc


def read_ledger(ledger, seq_no=0, seq_to=100, node_name='node1', pretty=False):
  if ledger != "domain" and ledger != "pool" and ledger != "config":
    raise ValueError("Unsupported ledger type: {}".format(ledger))
  args = [python_path, "/usr/local/bin/read_ledger", "--type", ledger]
  if seq_no > 0:
    args.extend(["--seq_no", str(seq_no)])
  args.extend(["--to", str(seq_to)])
  args.extend(["--base_dir", "/home/indy/.mnt/" + node_name])
  proc = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True)

  if pretty:
    lines = proc.stdout.splitlines()
    resp = []
    for line in lines:
        parsed = json.loads(line)
        resp.append(json.dumps(parsed, indent=4, sort_keys=True))
    return "\n\n".join(resp)

  return proc.stdout


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
    nodes = ["node1", "node2", "node3", "node4"]

    response = []
    for idx,node_name in enumerate(nodes):
      parsed = validator_info(node_name)
      if parsed:
        response.append(parsed)

    return json_reponse(response)


@app.route("/status/text")
async def status(request):
    nodes = ["node1", "node2", "node3", "node4"]

    response_text = ""
    for idx,node_name in enumerate(nodes):
      proc = validator_info(node_name)
      if idx > 0:
        response_text += "\n"
      response_text += node_name + "\n\n" + proc.stdout

    return text(response_text)


@app.route("/ledger/<ledger_name>")
async def ledger(request, ledger_name):
    response = read_ledger(ledger_name)
    return text(response)


@app.route("/ledger/<ledger_name>/pretty")
async def ledger_pretty(request, ledger_name):
    response = read_ledger(ledger_name, pretty=True)
    return text(response)


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