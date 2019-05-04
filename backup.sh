#!/bin/bash
#
# Copyright San Andreas IRC Network
# All Rights Reserved
#

function printHelp() {
    echo "Usage: "
}

function dumpMysql() {
    SERVER=$1
    PORT=$2
    KEY=$3
    PWD=$4

    ssh -p $PORT -i $KEY root@$SERVER "mysqldump --password=${PWD} -A > /root/mysql/databases.sql"
}

function rsync() {
    SERVER=$1
    PORT=$2
    KEY=$3
}

# Parse commandline args
MODE=$1
shift

if [ "$MODE" == "cron" ]; then
else
    printHelp
    exit 1
fi