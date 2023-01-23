#!/bin/bash

set -e

if [ ! -f "/home/indy/config/genesis.txn" ] && [ -z "${GENESIS_URL}" ] && [ -z "${GENESIS_FILE}" ]; then
  bash ./scripts/init_genesis.sh
fi

pip3 install -U pip &&
pip install --no-cache-dir -r server/requirements.txt

# link node ledgers where webserver can find them
#for node in 1 2 3 4; do
#    ln -sfn /home/indy/.mnt/node${node}/sandbox/data/Node${node} \
#            /home/indy/ledger/sandbox/data/node${node}
#done

python -m server.server
