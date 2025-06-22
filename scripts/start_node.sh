#!/bin/bash

set -e

HOST="${HOST:-0.0.0.0}"
export NODE_NUM="${1}"
DEFAULT_START_PORT="9700"
NODE_PORT1="${2}"
NODE_PORT2="${3}"

if [[ -z "$NODE_PORT1" ]] ; then
    NODE_PORT1=$(( DEFAULT_START_PORT + ( NODE_NUM * 2 ) - 1 ))
fi
if [[ -z "$NODE_PORT2" ]] ; then
    NODE_PORT2=$(( NODE_PORT1 + 1 ))
fi

if [ ! -d "/home/indy/ledger/sandbox/keys" ]; then
    echo "Ledger does not exist - Creating..."
    bash ./scripts/init_genesis.sh
fi


echo start_indy_node "Node""$NODE_NUM" $HOST $NODE_PORT1 $HOST $NODE_PORT2
start_indy_node "Node""$NODE_NUM" $HOST $NODE_PORT1 $HOST $NODE_PORT2
