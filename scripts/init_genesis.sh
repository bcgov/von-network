#!/bin/bash

set -e

PARAMS=""

if [ ! -z "$IPS" ]; then
    PARAMS+=" -s \"$IPS\""
elif [ ! -z "$IP" ]; then
    PARAMS+=" -s \"$IP\""
fi

if [ ! -z "$NODE_PORTS" ]; then
    PARAMS+=" -p $NODE_PORTS"
fi

if [ ! -z "$NODE_NUM" ]; then
    PARAMS+=" -n $NODE_NUM"
fi

echo von_generate_transactions $PARAMS
von_generate_transactions $PARAMS
