from datetime import datetime
import json
import os
import shutil
import subprocess
import re

from aiohttp import web

from .anchor import AnchorHandle, NotReadyException


PATHS = {
  'python': shutil.which('python3'),
  'validator-info': shutil.which('validator-info'),
  'read_ledger': shutil.which('read_ledger'),
}

INDY_TXN_TYPES = {
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

INDY_ROLE_TYPES = {
  "0": "TRUSTEE",
  "2": "STEWARD",
  "100": "TGB",
  "101": "TRUST_ANCHOR",
}

INDY_LEDGER_TYPES = {
  "0": "DOMAIN",
  "1": "POOL",
  "2": "CONFIG",
}


os.chdir(os.path.dirname(__file__))

APP = web.Application()
ROUTES = web.RouteTableDef()

@ROUTES.get('/')
async def index(request):
  return web.FileResponse('static/index.html')

@ROUTES.get('/favicon.ico')
async def favicon(request):
  return web.FileResponse('static/favicon.ico')

ROUTES.static('/include', './static/include')

TRUST_ANCHOR = AnchorHandle()


def json_response(data):
  # FIXME - use aiohttp-cors
  headers = {'Access-Control-Allow-Origin': '*'}
  return web.json_response(data, headers=headers)


def validator_info(node_name, as_json=True):
  args = [PATHS['validator-info']]
  if as_json:
    args.append("--json")
  else:
    args.append("-v")
  args.extend(["--basedir", "/home/indy/.mnt/" + node_name + "/sandbox/"])
  proc = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True)
  if as_json:
    # The result is polluted with logs in the latest version.
    # We pull out json
    m = re.search(r'(?s)\n({.*})', proc.stdout)
    corrected_stdout = m.group(1) if m else proc.stdout
    return json.loads(corrected_stdout)
  return proc


def read_ledger(ledger, seq_no=0, seq_to=1000, node_name='node1', format="data"):
  if ledger != "domain" and ledger != "pool" and ledger != "config":
    raise ValueError("Unsupported ledger type: {}".format(ledger))
  args = [PATHS['read_ledger'], "--type", ledger]
  if seq_no > 0:
    args.extend(["--seq_no", str(seq_no)])
  args.extend(["--to", str(seq_to)])
  #args.extend(["--base_dir", "/home/indy/.mnt/" + node_name])
  args.extend(["--node_name", node_name])
  proc = subprocess.run(args, stdout=subprocess.PIPE, universal_newlines=True)

  if format == "pretty" or format == "data":
    lines = proc.stdout.splitlines()
    resp = []
    for line in lines:
      _seq_no, txn = line.split(' ', 2)
      parsed = json.loads(txn)
      if format == "pretty":
        parsed = json.dumps(parsed, indent=4, sort_keys=True)
      resp.append(parsed)
    if format == "pretty":
      return "\n\n".join(resp)
    return resp

  # format = json
  return proc.stdout


@ROUTES.get("/status")
async def status(request):
  try:
    response = await TRUST_ANCHOR.validator_info()
  except NotReadyException:
    return web.Response(status=503)
  return json_response(response)


@ROUTES.get("/status/text")
async def status_text(request):
  nodes = ["node1", "node2", "node3", "node4"]

  response_text = ""
  for idx,node_name in enumerate(nodes):
    proc = validator_info(node_name, as_json=False)
    if idx > 0:
      response_text += "\n"
    response_text += node_name + "\n\n" + proc.stdout

  return web.Response(text=response_text)


@ROUTES.get("/status/pretty")
async def status_pretty(request):
  response = await validator_info_request()
  data = json.dumps(parsed, indent=4, sort_keys=True)
  return web.Response(text=data)


@ROUTES.get("/ledger/{ledger_name}")
async def ledger_json(request):
  response = read_ledger(request.match_info['ledger_name'], format="json")
  return web.Response(text=response)


@ROUTES.get("/ledger/{ledger_name}/pretty")
async def ledger_pretty(request):
  response = read_ledger(request.match_info['ledger_name'], format="pretty")
  return web.Response(text=response)


@ROUTES.get("/ledger/{ledger_name}/text")
async def ledger_text(request):
  response = read_ledger(request.match_info['ledger_name'])
  text = []
  for seq_no, txn in response:
    if len(text):
      text.append("")

    type_name = INDY_TXN_TYPES.get(txn['type'], txn['type'])
    text.append("[" + str(seq_no) + "]  TYPE: " + type_name)

    if type_name == "NYM":
      text.append("DEST: " + txn['dest'])

      role = txn.get('role')
      if role != None:
        role_name = INDY_ROLE_TYPES.get(role, role)
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

  return web.Response(text="\n".join(text))


@ROUTES.get("/ledger/{ledger_name}/{sequence_number:\d+}")
async def ledger_seq(request):
  seq_no = int(request.match_info['sequence_number'])
  ledger = request.match_info['ledger_name']
  try:
    data = await TRUST_ANCHOR.get_txn(seq_no, ledger)
  except NotReadyException:
    return web.Response(status=503)
  return json_response(data)


# Expose genesis transaction for easy connection.
@ROUTES.get("/genesis")
async def genesis(request):
  with open(
    '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis',
      'r') as content_file:
    genesis = content_file.read()
  return web.Response(text=genesis)


# Easily write dids for new identity owners
@ROUTES.post('/register')
async def register(request):
  if not TRUST_ANCHOR.ready:
    return web.Response(status=503)

  body = await request.json()
  if not body:
    return web.Response(
      text='Expected json request body',
      status=400
    )

  seed = body.get('seed')
  did = body.get('did')
  verkey = body.get('verkey')
  alias = body.get('alias')
  role = body.get('role', 'TRUST_ANCHOR')

  if seed:
    if not 0 <= len(seed) <= 32:
      return web.Response(
        text='Seed must be between 0 and 32 characters long.',
        status=400
      )
    # Pad with zeroes
    seed += '0' * (32 - len(seed))
  else:
    if not did or not verkey:
      return web.Response(
        text='Either seed the seed parameter or the did and verkey parameters must be provided.',
        status=400
      )

  if not did or not verkey:
    did, verkey = await TRUST_ANCHOR.seed_to_did(seed)

  print('\n\nRegister agent\n\n')
  try:
    await TRUST_ANCHOR.register_did(did, verkey, alias, role)
  except NotReadyException:
    return web.Response(status=503)

  return json_response({
    'seed': seed,
    'did': did,
    'verkey': verkey
  })


async def boot(app):
  print('Creating trust anchor...')
  init = app['anchor_init'] = app.loop.create_task(TRUST_ANCHOR.open())
  init.add_done_callback(lambda _task: print('--- Trust anchor initialized ---'))


if __name__ == '__main__':
  APP.add_routes(ROUTES)
  APP.on_startup.append(boot)
  print('Running webserver...')
  web.run_app(APP, host='0.0.0.0', port=8000)
