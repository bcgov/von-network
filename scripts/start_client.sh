#!/bin/bash

set -e

if [ ! -z "$IPS" ]; then
    echo von_generate_transactions -s "$IPS"
    von_generate_transactions -s "$IPS"
elif [ ! -z "$IP" ]; then
    echo von_generate_transactions -i "$IP"
    von_generate_transactions -i "$IP"
else
    echo von_generate_transactions
    von_generate_transactions
fi

mkdir -p .indy_client/pool/sandbox
cp /home/indy/ledger/sandbox/pool_transactions_genesis .indy_client/pool/sandbox/sandbox.txn

indy-cli "$@"