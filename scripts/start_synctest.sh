#!/bin/bash

set -e

if [ ! -f "/home/indy/config/genesis.txn" ] && [ -z "${GENESIS_FILE}" ]; then
  bash ./scripts/init_genesis.sh
fi

pip3 install -U pip &&
pip install --no-cache-dir -r server/requirements.txt

python -m server.synctest
