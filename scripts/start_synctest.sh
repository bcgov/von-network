#!/bin/bash

set -e

if [ ! -f "/home/indy/ledger/sandbox/pool_transactions_genesis" ] && [ -z "${GENESIS_URL}" ] && [ -z "${GENESIS_FILE}" ]; then
  echo "Ledger does not exist - Creating genesis data..."
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
fi

python -m server.synctest
