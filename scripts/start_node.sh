#!/bin/bash

set -e

HOST="${HOST:-0.0.0.0}"
export NODE_NUM="${1}"
START_PORT="9700"
NODE_PORT=$((START_PORT + ( NODE_NUM * 2 ) - 1 ))

if [ ! -d "/home/indy/ledger/sandbox/keys" ]; then
    echo "Ledger does not exist - Creating..."
    bash ./scripts/init_genesis.sh
fi


echo start_indy_node "Node""$NODE_NUM" $HOST $NODE_PORT $HOST $(( NODE_PORT + 1 ))
start_indy_node "Node""$NODE_NUM" $HOST $NODE_PORT $HOST $(( NODE_PORT + 1 ))
