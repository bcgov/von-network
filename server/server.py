#!/usr/bin/python3

from sanic import Sanic
from sanic.response import text

app = Sanic(__name__)


@app.route("/genesis")
async def test(request):
    with open(
        '/home/indy/.indy-cli/networks/sandbox/pool_transactions_genesis',
            'r') as content_file:
        gensis = content_file.read()
    return text(gensis)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
