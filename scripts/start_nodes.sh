#!/bin/bash

set -e

HOST="${HOST:-0.0.0.0}"
export NODE_NUM="1 2 3 4"
DEFAULT_START_PORT="9700"

NODE1_PORT1="${1}"
NODE1_PORT2="${2}"
if [[ -z "$NODE1_PORT1" ]] ; then
    NODE1_PORT1=$(( DEFAULT_START_PORT + ( 1 * 2 ) - 1 ))
fi
if [[ -z "$NODE1_PORT2" ]] ; then
    NODE1_PORT2=$(( NODE1_PORT1 + 1 ))
fi

NODE2_PORT1="${3}"
NODE2_PORT2="${4}"
if [[ -z "$NODE2_PORT1" ]] ; then
    NODE2_PORT1=$(( DEFAULT_START_PORT + ( 2 * 2 ) - 1 ))
fi
if [[ -z "$NODE2_PORT2" ]] ; then
    NODE2_PORT2=$(( NODE2_PORT1 + 1 ))
fi

NODE3_PORT1="${5}"
NODE3_PORT2="${6}"
if [[ -z "$NODE3_PORT1" ]] ; then
    NODE3_PORT1=$(( DEFAULT_START_PORT + ( 3 * 2 ) - 1 ))
fi
if [[ -z "$NODE3_PORT2" ]] ; then
    NODE3_PORT2=$(( NODE3_PORT1 + 1 ))
fi

NODE4_PORT1="${7}"
NODE4_PORT2="${8}"
if [[ -z "$NODE4_PORT1" ]] ; then
    NODE4_PORT1=$(( DEFAULT_START_PORT + ( 4 * 2 ) - 1 ))
fi
if [[ -z "$NODE4_PORT2" ]] ; then
    NODE4_PORT2=$(( NODE4_PORT1 + 1 ))
fi



if [ ! -d "/home/indy/ledger/sandbox/keys" ]; then
    echo "Ledger does not exist - Creating..."
    bash ./scripts/init_genesis.sh
fi

cat <<EOF > supervisord.conf
[supervisord]
logfile = /tmp/supervisord.log
logfile_maxbytes = 50MB
logfile_backups=10
loglevel = info
pidfile = /tmp/supervisord.pid
nodaemon = true
minfds = 1024
minprocs = 200
umask = 022
user = indy
identifier = supervisor
directory = /tmp
nocleanup = true
childlogdir = /tmp
strip_ansi = false

[program:node1]
command=start_indy_node Node1 $HOST $NODE1_PORT1 $HOST $NODE1_PORT2
directory=/home/indy
stdout_logfile=/tmp/node1.log
stderr_logfile=/tmp/node1.log

[program:node2]
command=start_indy_node Node2 $HOST $NODE2_PORT1 $HOST $NODE2_PORT2
directory=/home/indy
stdout_logfile=/tmp/node2.log
stderr_logfile=/tmp/node2.log

[program:node3]
command=start_indy_node Node3 $HOST $NODE3_PORT1 $HOST $NODE3_PORT2
directory=/home/indy
stdout_logfile=/tmp/node3.log
stderr_logfile=/tmp/node3.log

[program:node4]
command=start_indy_node Node4 $HOST $NODE4_PORT1 $HOST $NODE4_PORT2
directory=/home/indy
stdout_logfile=/tmp/node4.log
stderr_logfile=/tmp/node4.log

[program:printlogs]
command=tail -F /tmp/supervisord.log /tmp/node1.log /tmp/node2.log /tmp/node3.log /tmp/node4.log
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0

EOF

echo "Starting indy nodes"
supervisord
