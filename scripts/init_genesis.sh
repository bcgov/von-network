#!/bin/bash

set -e

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
