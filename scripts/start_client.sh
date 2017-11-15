#!/bin/bash

# Get ip addresses from docker container names
IP1="$(getent hosts node1 | awk '{ print $1 }')"
IP2="$(getent hosts node2 | awk '{ print $1 }')"
IP3="$(getent hosts node3 | awk '{ print $1 }')"
IP4="$(getent hosts node4 | awk '{ print $1 }')"

# If we don't explicitely set IP, then discover nodes internally
if [ -z "$IP" ]; then
    if [ -z "$IP1" ] || [ -z "$IP2" ] || [ -z "$IP3" ] || [ -z "$IP4" ]; then
        echo "Cannot discover node ips. Are the nodes running?"
        exit 1
    fi

    echo generate_indy_pool_transactions \
        --nodes 4 \
        --clients 0 \
        --ips $IP1,$IP2,$IP3,$IP4

    generate_indy_pool_transactions \
        --nodes 4 \
        --clients 0 \
        --ips "$IP1",$IP2,$IP3,$IP4
# Otherwise, generate transaction file using supplied IP (for remote server)
else
    echo generate_indy_pool_transactions \
        --nodes 4 \
        --clients 0 \
        --ips $IP,$IP,$IP,$IP

    generate_indy_pool_transactions \
        --nodes 4 \
        --clients 0 \
        --ips "$IP",$IP,$IP,$IP
fi

indy
