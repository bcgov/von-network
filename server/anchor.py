import json

from indy import ledger

from von_anchor import AnchorSmith
from von_anchor.anchor.base import _BaseAnchor
from von_anchor.nodepool import NodePool
from von_anchor.wallet import Wallet


class NotReadyException(Exception):
  pass


class AnchorHandle:
  def __init__(self):
    self._instance = None

    pool_cfg = None # {'protocol': protocol_version}
    self._pool = NodePool(
      'nodepool',
      '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis',
      pool_cfg
    )

    self._ready = False

    self._wallet = Wallet(
      '000000000000000000000000Trustee1',
      'trustee_wallet'
    )

  async def open(self):
    await self._pool.open()
    await self._wallet.create()
    self._instance = AnchorSmith(self._wallet, self._pool)
    await self._instance.open()
    self._ready = True

  @property
  def did(self):
    return self._wallet and self._wallet.did

  @property
  def instance(self):
    return self._instance

  @property
  def pool(self):
    return self._pool

  @property
  def ready(self):
    return self._ready

  @property
  def wallet(self):
    return self._wallet


  async def get_nym(self, did):
    """
    Fetch a nym from the ledger
    """
    if not self.ready:
      raise NotReadyException()

    data = await self._instance.get_nym(did)
    return json.loads(data)


  async def get_txn(self, seq_no, ledger_ident=None):
    """
    Fetch a transaction by sequence number
    """
    if not self.ready:
      raise NotReadyException()

    if ledger_ident and isinstance(ledger_ident, str):
      ledger_ident = ledger_ident.upper()
    req_json = await ledger.build_get_txn_request(self.did, ledger_ident, seq_no)
    resp = json.loads(await self._instance._submit(req_json))
    rv_json = self.pool.protocol.txn2data(resp)
    return json.loads(rv_json)


  async def register_did(self, did, verkey, alias=None, role=None):
    """
    Register a DID and verkey on the ledger
    """
    if not self.ready:
      raise NotReadyException()

    print('\nGet Nym: ' + str(did) + '\n')
    if not await self.get_nym(did):
      print('\nSend Nym: ' + str(did) + '/' + str(verkey) + '\n')
      await self._instance.send_nym(did, verkey, alias, role)


  async def seed_to_did(self, seed):
    """
    Resolve a DID and verkey from a seed
    """
    wallet = Wallet(
      seed,
      seed + '-wallet'
    )
    async with _BaseAnchor(await wallet.create(), self.pool) as new_agent:
      did = new_agent.did
      verkey = new_agent.verkey
      return (did, verkey)


  async def validator_info(self):
    """
    Fetch the status of the validator nodes
    """
    if not self.ready:
      raise NotReadyException()

    req_json = await ledger.build_get_validator_info_request(self.did)
    result = await self._instance._sign_submit(req_json)
    node_data = json.loads(result)
    node_aliases = list(node_data.keys())
    node_aliases.sort()

    ret = []
    for node in node_aliases:
      reply = json.loads(node_data[node])
      if "result" not in reply:
        continue
      data = reply["result"].get("data")
      data["Node_info"]["Name"] = node
      ret.append(data)
    return ret
