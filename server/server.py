#! /usr/bin/python3

import asyncio
from datetime import datetime
import json
import subprocess

from von_agent.nodepool import NodePool
from von_agent.demo_agents import TrustAnchorAgent
from von_agent.agents import BaseAgent


from sanic import Sanic
from sanic.response import text as sanic_text, json as sanic_json, html as sanic_html

app = Sanic(__name__)
app.static('/', './static/index.html')
app.static('/include', './static/include')
app.static('/favicon.ico', './static/favicon.ico')

python_path = "/usr/bin/python3"

indy_txn_types = {
    "0": "NODE",
    "1": "NYM",
    "3": "GET_TXN",
    "100": "ATTRIB",
    "101": "SCHEMA",
    "102": "CLAIM_DEF",
    "103": "DISCO",
    "104": "GET_ATTR",
    "105": "GET_NYM",
    "107": "GET_SCHEMA",
    "108": "GET_CLAIM_DEF",
    "109": "POOL_UPGRADE",
    "110": "NODE_UPGRADE",
    "111": "POOL_CONFIG",
    "112": "CHANGE_KEY",
}

indy_role_types = {
  "0": "TRUSTEE",
  "2": "STEWARD",
  "100": "TGB",
  "101": "TRUST_ANCHOR",
}


def json_reponse(data):
  headers = {'Access-Control-Allow-Origin': '*'}
  return sanic_json(data, headers=headers)


def validator_info(node_name, as_json=True):
  args = [python_path, "/usr/local/bin/validator-info"]
  if as_json:
    args.append("--json")
  else:
    args.append("-v")
  args.extend(["--basedir", "/home/indy/.mnt/" + node_name + "/sandbox/"])
  proc = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True)
  if as_json:
    return json.loads(proc.stdout)
  return proc


def read_ledger(ledger, seq_no=0, seq_to=100, node_name='node1', format="data"):
  if ledger != "domain" and ledger != "pool" and ledger != "config":
    raise ValueError("Unsupported ledger type: {}".format(ledger))
  args = [python_path, "/usr/local/bin/read_ledger", "--type", ledger]
  if seq_no > 0:
    args.extend(["--seq_no", str(seq_no)])
  args.extend(["--to", str(seq_to)])
  args.extend(["--base_dir", "/home/indy/.mnt/" + node_name])
  proc = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True)

  if format == "pretty" or format == "data":
    lines = proc.stdout.splitlines()
    resp = []
    for line in lines:
        parsed = json.loads(line)
        if format == "pretty":
          resp.append(json.dumps(parsed, indent=4, sort_keys=True))
        else:
          resp.append(parsed)
    if format == "pretty":
      return "\n\n".join(resp)
    return resp

  # format = json
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
      proc = validator_info(node_name, as_json=False)
      if idx > 0:
        response_text += "\n"
      response_text += node_name + "\n\n" + proc.stdout

    return sanic_text(response_text)


@app.route("/ledger/<ledger_name>")
async def ledger(request, ledger_name):
    response = read_ledger(ledger_name, format="json")
    return sanic_text(response)


@app.route("/ledger/<ledger_name>/pretty")
async def ledger_pretty(request, ledger_name):
    response = read_ledger(ledger_name, format="pretty")
    return sanic_text(response)


@app.route("/ledger/<ledger_name>/text")
async def ledger_text(request, ledger_name):
    response = read_ledger(ledger_name)
    text = []
    for seq_no, txn in response:
      if len(text):
        text.append("")

      type_name = indy_txn_types.get(txn['type'], txn['type'])
      text.append("[" + str(seq_no) + "]  TYPE: " + type_name)

      if type_name == "NYM":
        text.append("DEST: " + txn['dest'])

        role = txn.get('role')
        if role != None:
          role_name = indy_role_types.get(role, role)
          text.append("ROLE: " + role_name)

        verkey = txn.get('verkey')
        if verkey != None:
          text.append("VERKEY: " + verkey)

      ident = txn.get('identifier')
      if ident != None:
        text.append("IDENT: " + ident)

      txnTime = txn.get('txnTime')
      if txnTime != None:
        ftime = datetime.fromtimestamp(txnTime).strftime('%Y-%m-%d %H:%M:%S')
        text.append("TIME: " + ftime)

      reqId = txn.get('reqId')
      if reqId != None:
        text.append("REQ ID: " + str(reqId))

      refNo = txn.get('ref')
      if refNo != None:
        text.append("REF: " + str(refNo))

      txnId = txn.get('txnId')
      if txnId != None:
        text.append("TXN ID: " + txnId)

      if type_name == "SCHEMA" or type_name == "CLAIM_DEF" or type_name == "NODE":
        data = txn.get('data')
        text.append("DATA:")
        text.append(json.dumps(data, indent=4))

      sig = txn.get('signature')
      if sig != None:
        text.append("SIGNATURE: " + sig)

      sig_type = txn.get('signature_type')
      if sig_type != None:
        text.append("SIGNATURE TYPE: " + sig_type)

    return sanic_text("\n".join(text))


# Expose genesis transaction for easy connection.
@app.route("/genesis")
async def genesis(request):
    with open(
        '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis',
            'r') as content_file:
        gensis = content_file.read()
    return sanic_text(gensis)


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

    return sanic_text(new_did.did + ' successfully written to ledger')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(boot())
    loop.close()
    app.run(host="0.0.0.0", port=8000, debug=True)


# BC-Registrar-Agent-0000000000000