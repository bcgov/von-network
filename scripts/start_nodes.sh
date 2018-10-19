#!/bin/bash

set -e

HOST="${HOST:-0.0.0.0}"
START_PORT="9700"
NODE_NUM="1 2 3 4"

if [ ! -d "/var/lib/indy/sandbox/keys" ]; then
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
logLevel = error
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

[program:logs]
command=tail -F node1.log node2.log node3.log node4.log
directory=/tmp
stdout_logfile=/dev/fd/1
stdout_logfile_maxbytes=0

EOF

echo "Starting validator nodes"
supervisord
