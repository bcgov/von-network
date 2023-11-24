import asyncio
import base64
from datetime import datetime
import json
import logging
import os
import shutil
import yaml
import aiohttp_jinja2
import jinja2

from aiohttp import web

from .anchor import (
    AnchorHandle,
    NotReadyException,
    INDY_ROLE_TYPES,
    INDY_TXN_TYPES,
    REGISTER_NEW_DIDS,
)

logging.basicConfig(level=(os.getenv("LOG_LEVEL", "").upper() or logging.INFO))
LOGGER = logging.getLogger(__name__)

PATHS = {"python": shutil.which("python3")}

os.chdir(os.path.dirname(__file__))

LOGGER.info("REGISTER_NEW_DIDS is set to %s", REGISTER_NEW_DIDS)

LEDGER_INSTANCE_NAME = os.getenv("LEDGER_INSTANCE_NAME", "Ledger Browser")
LOGGER.info('LEDGER_INSTANCE_NAME is set to "%s"', LEDGER_INSTANCE_NAME)

WEB_ANALYTICS_SCRIPT = os.getenv("WEB_ANALYTICS_SCRIPT", "")
LOGGER.info(
    "Web analytics are %s", "ENABLED" if not "WEB_ANALYTICS_SCRIPT" else "DISABLED"
)


INFO_SITE_URL = os.getenv("INFO_SITE_URL")
INFO_SITE_TEXT = os.getenv("INFO_SITE_TEXT") or os.getenv("INFO_SITE_URL")
INDY_SCAN_URL = os.getenv("INDY_SCAN_URL")
INDY_SCAN_TEXT = os.getenv("INDY_SCAN_TEXT") or os.getenv("INDY_SCAN_URL")

APP = web.Application()
aiohttp_jinja2.setup(APP, loader=jinja2.FileSystemLoader("./static"))

ROUTES = web.RouteTableDef()
TRUST_ANCHOR = AnchorHandle()


@ROUTES.get("/")
@aiohttp_jinja2.template("index.html")
async def index(request):
    return {
        "REGISTER_NEW_DIDS": TRUST_ANCHOR._register_dids,
        "LEDGER_INSTANCE_NAME": LEDGER_INSTANCE_NAME,
        "WEB_ANALYTICS_SCRIPT": WEB_ANALYTICS_SCRIPT,
        "INFO_SITE_TEXT": INFO_SITE_TEXT,
        "INFO_SITE_URL": INFO_SITE_URL,
        "INDY_SCAN_URL": INDY_SCAN_URL,
        "INDY_SCAN_TEXT": INDY_SCAN_TEXT,
    }


@ROUTES.get("/browse/{ledger_ident:.*}")
@aiohttp_jinja2.template("ledger.html")
async def browse(request):
    return {
        "LEDGER_INSTANCE_NAME": LEDGER_INSTANCE_NAME,
        "WEB_ANALYTICS_SCRIPT": WEB_ANALYTICS_SCRIPT,
        "INFO_SITE_TEXT": INFO_SITE_TEXT,
        "INFO_SITE_URL": INFO_SITE_URL,
    }


@ROUTES.get("/favicon.ico")
async def favicon(request):
    return web.FileResponse("static/favicon.ico")


ROUTES.static("/include", "./static/include")


def json_response(data, status=200, **kwargs):
    # FIXME - use aiohttp-cors
    kwargs["headers"] = {"Access-Control-Allow-Origin": "*"}
    kwargs["text"] = json.dumps(data, indent=2, sort_keys=True)
    if "content_type" not in kwargs:
        kwargs["content_type"] = "application/json"
    return web.Response(status=status, **kwargs)


def not_ready_json():
    return web.json_response(data={"detail": "Not ready"}, status=503)


@ROUTES.get("/status")
async def status(request):
    status = TRUST_ANCHOR.public_config
    if status["ready"] and not status["anonymous"] and request.query.get("validators"):
        try:
            status["validators"] = await TRUST_ANCHOR.validator_info()
        except NotReadyException:
            return not_ready_json()
        except asyncio.CancelledError:
            raise
        except Exception:
            LOGGER.exception("Error retrieving validator info")
            status["validators"] = None
    return json_response(status)


@ROUTES.get("/status/text")
async def status_text(request):
    try:
        response = await TRUST_ANCHOR.validator_info()
    except NotReadyException:
        return not_ready_json()

    text = []
    for node in response:
        id = node["Node_info"]["Name"]
        text.append(id)
        text.append("")
        text.append(yaml.dump(node))
        text.append("")

    return web.Response(text="\n".join(text))


@ROUTES.get("/ledger/{ledger_name}")
async def ledger_json(request):
    if not TRUST_ANCHOR.ready:
        return not_ready_json()

    page = int(request.query.get("page", 1))
    page_size = int(request.query.get("page_size", 100))
    start = (page - 1) * page_size + 1
    end = start + page_size - 1
    query = request.query.get("query")
    if query is not None and not query.strip():
        query = None
    txn_type = request.query.get("type")
    if txn_type is not None and not txn_type.strip():
        txn_type = None

    if txn_type is not None or query is not None:
        rows, count = await TRUST_ANCHOR.get_txn_search(
            request.match_info["ledger_name"], query, txn_type, page_size, start - 1
        )
    else:
        rows = await TRUST_ANCHOR.get_txn_range(
            request.match_info["ledger_name"], start, end
        )
        count = await TRUST_ANCHOR.get_max_seqno(request.match_info["ledger_name"])
    last_modified = None
    results = []
    for row in rows:
        try:
            last_modified = max(last_modified, row[1]) if last_modified else row[1]
        except TypeError:
            last_modified = row[1]
        results.append(json.loads(row[3]))
    if not results and page > 1:
        data = {"detail": "Invalid page."}
        response = json_response(data, status=404)
    else:
        data = {
            "total": count,
            "page_size": page_size,
            "page": page,
            "first_index": start,
            "last_index": start + len(results) - 1,
            "results": results,
        }
        response = json_response(data)
        response.charset = "utf-8"
        response.last_modified = last_modified
    return response


@ROUTES.get("/ledger/{ledger_name}/text")
async def ledger_text(request):
    if not TRUST_ANCHOR.ready:
        return not_ready_json()

    response = web.StreamResponse()
    response.content_type = "text/plain"
    response.charset = "utf-8"
    await response.prepare(request)

    rows = await TRUST_ANCHOR.get_txn_range(request.match_info["ledger_name"])

    first = True
    for seq_no, added, row in rows:
        text = []
        if not first:
            text.append("")
        first = False
        row = json.loads(row)
        txn = row["txn"]
        data = txn["data"]
        metadata = txn["metadata"]

        type_name = INDY_TXN_TYPES.get(txn["type"], txn["type"])
        text.append("[" + str(seq_no) + "]  TYPE: " + type_name)

        ident = metadata.get("from")
        if ident is not None:
            text.append("FROM: " + ident)

        if type_name == "NYM":
            text.append("DEST: " + data["dest"])

            role = data.get("role")
            if role is not None:
                role_name = INDY_ROLE_TYPES.get(role, role)
                text.append("ROLE: " + role_name)

            verkey = data.get("verkey")
            if verkey is not None:
                text.append("VERKEY: " + verkey)

        txnTime = txn.get("txnTime")
        if txnTime is not None:
            ftime = datetime.fromtimestamp(txnTime).strftime("%Y-%m-%d %H:%M:%S")
            text.append("TIME: " + ftime)

        reqId = metadata.get("reqId")
        if reqId is not None:
            text.append("REQ ID: " + str(reqId))

        refNo = data.get("ref")
        if refNo is not None:
            text.append("REF: " + str(refNo))

        txnId = row["txnMetadata"].get("txnId")
        if txnId is not None:
            text.append("TXN ID: " + txnId)

        if type_name == "SCHEMA" or type_name == "CLAIM_DEF" or type_name == "NODE":
            data = data.get("data")
            text.append("DATA:")
            text.append(json.dumps(data, indent=4))

        sig = data.get("signature")
        if sig is not None:
            text.append("SIGNATURE: " + sig)

        sig_type = data.get("signature_type")
        if sig_type is not None:
            text.append("SIGNATURE TYPE: " + sig_type)

        text.append("")
        await response.write("\n".join(text).encode("utf-8"))

    await response.write_eof()
    return response


@ROUTES.get("/ledger/{ledger_name}/{txn_ident}")
async def ledger_seq(request):
    ident = request.match_info["txn_ident"]
    ledger = request.match_info["ledger_name"]
    try:
        data = await TRUST_ANCHOR.get_txn(ledger, ident)
        if not data:
            return web.Response(status=404)
    except NotReadyException:
        return not_ready_json()
    return json_response(json.loads(data[3]))


# Expose genesis transaction for easy connection.
@ROUTES.get("/genesis")
async def genesis(request):
    if not TRUST_ANCHOR.ready:
        return not_ready_json()
    genesis = await TRUST_ANCHOR.get_genesis()
    return web.Response(text=genesis)


# Easily write dids for new identity owners
@ROUTES.post("/register")
async def register(request):
    if not TRUST_ANCHOR.ready:
        return not_ready_json()

    body = await request.json()
    if not body:
        return web.Response(text="Expected json request body", status=400)

    seed = body.get("seed")
    did = body.get("did")
    verkey = body.get("verkey")
    alias = body.get("alias")
    role = body.get("role", "ENDORSER")
    if role == "TRUST_ANCHOR":
        role = "ENDORSER"

    if seed:
        if seed.endswith("="):
            testseed = base64.b64decode(seed).decode("ascii")
            if len(testseed) != 32:
                return web.Response(text="Seed must be 32 characters long.", status=400)
        elif not 0 <= len(seed) <= 32:
            return web.Response(
                text="Seed must be between 0 and 32 characters long.", status=400
            )
        # Pad with zeroes
        seed += "0" * (32 - len(seed))
    else:
        if not did or not verkey:
            return web.Response(
                text=(
                  "Either seed the seed parameter or the did and "
                  "verkey parameters must be provided."),
                status=400,
            )

    if not did or not verkey:
        auto_did, verkey = await TRUST_ANCHOR.seed_to_did(seed)
        if not did:
            did = auto_did

    try:
        await TRUST_ANCHOR.register_did(did, verkey, alias, role)
    except NotReadyException:
        return not_ready_json()

    return json_response({"seed": seed, "did": did, "verkey": verkey})


async def boot(app):
    LOGGER.info("Creating trust anchor...")
    init = app["anchor_init"] = app.loop.create_task(TRUST_ANCHOR.open())
    init.add_done_callback(
        lambda _task: LOGGER.info("--- Trust anchor initialized ---")
    )


if __name__ == "__main__":
    APP.add_routes(ROUTES)
    APP.on_startup.append(boot)
    LOGGER.info("Running webserver...")
    PORT = int(os.getenv("PORT", "8000"))
    web.run_app(APP, host="0.0.0.0", port=PORT)

