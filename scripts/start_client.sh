#!/bin/bash

if [ -z $IP ]; then
    von_generate_transactions
else
    von_generate_transactions -i $IP
fi

indy
