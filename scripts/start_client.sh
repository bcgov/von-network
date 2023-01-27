#!/bin/bash

set -e

bash ./scripts/init_genesis.sh

mkdir -p .indy_client/pool/sandbox
cp /home/indy/ledger/sandbox/pool_transactions_genesis .indy_client/pool/sandbox/sandbox.txn

indy-cli "$@"
