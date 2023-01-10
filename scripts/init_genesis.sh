#!/bin/bash

set -e

if [ ! -d "/home/indy/config" ]; then
    echo "Missing config directory, must be mounted"
    exit 1
fi
if [ -f "/home/indy/config/genesis.txn" ]; then
    echo "Genesis transactions file already exists"
    exit
fi

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

cp /home/indy/ledger/sandbox/pool_transactions_genesis /home/indy/config/genesis.txn
