#!/bin/bash

set -e

HOST="${HOST:-0.0.0.0}"
NODE_NUM="${1}"
START_PORT="9700"
NODE_PORT=$((START_PORT + ( NODE_NUM * 2 ) - 1 ))

if [ ! -d "/home/indy/ledger/sandbox/keys" ]; then
    echo "Ledger does not exist - Creating..."

    if [ ! -z "$IPS" ]; then
        echo von_generate_transactions -s "$IPS" -n "$NODE_NUM"
        von_generate_transactions -s "$IPS" -n "$NODE_NUM"
    elif [ ! -z "$IP" ]; then
        echo von_generate_transactions -i "$IP" -n "$NODE_NUM"
        von_generate_transactions -i "$IP" -n "$NODE_NUM"
    else
        echo von_generate_transactions -n "$NODE_NUM"
        von_generate_transactions -n "$NODE_NUM"
    fi
fi


echo start_indy_node "Node""$NODE_NUM" $HOST $NODE_PORT $HOST $(( NODE_PORT + 1 ))
start_indy_node "Node""$NODE_NUM" $HOST $NODE_PORT $HOST $(( NODE_PORT + 1 ))
