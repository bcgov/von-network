#!/bin/bash

set -e

if [ ! -f "/home/indy/ledger/sandbox/pool_transactions_genesis" ] && [ -z "${GENESIS_URL}" ] && [ -z "${GENESIS_FILE}" ]; then
  echo "Ledger does not exist - Creating genesis data..."
  bash ./scripts/init_genesis.sh
fi

# link node ledgers where webserver can find them
#for node in 1 2 3 4; do
#    ln -sfn /home/indy/.mnt/node${node}/sandbox/data/Node${node} \
#            /home/indy/ledger/sandbox/data/node${node}
#done

python -m server.server
