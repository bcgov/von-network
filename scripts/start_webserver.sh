#!/bin/bash

set -e

  if [ ! -d "/home/indy/.indy-cli/networks/sandbox" ]; then
    echo "Ledger does not exist - Creating..."
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

cd server && pipenv run python server.py