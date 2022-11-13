#!/bin/bash

set -e

HOST="${HOST:-0.0.0.0}"
START_PORT="9700"
NODE_NUM="1 2 3 4 5"

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
command=start_indy_node Node1 $HOST 9701 $HOST 9702
directory=/home/indy
stdout_logfile=/tmp/node1.log
stderr_logfile=/tmp/node1.log

[program:node2]
command=start_indy_node Node2 $HOST 9703 $HOST 9704
directory=/home/indy
stdout_logfile=/tmp/node2.log
stderr_logfile=/tmp/node2.log

[program:node3]
command=start_indy_node Node3 $HOST 9705 $HOST 9706
directory=/home/indy
stdout_logfile=/tmp/node3.log
stderr_logfile=/tmp/node3.log

[program:node4]
command=start_indy_node Node4 $HOST 9707 $HOST 9708
directory=/home/indy
stdout_logfile=/tmp/node4.log
stderr_logfile=/tmp/node4.log

[program:node5]
command=start_indy_node Node4 $HOST 9709 $HOST 9710
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
