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
    PWD=$2

    ssh -p $SSH_PORT -i "$KEY_DIR/$SERVER.key" root@"$SERVER" "mysqldump --password=${PWD} -A > /root/mysql/databases.sql"
    echo $?
}

function dumpAllMysql() {
    for ((i=0;i<${#MYSQL_HOSTS[@]};++i)); do
        echo "Dumping MySQL database on ${MYSQL_HOSTS[i]}..."
        dumpMysql "${MYSQL_HOSTS[i]}" "${MYSQL_PASS[i]}"
    done
}

function rsync() {
    SERVER=$1
    PORT=$2
    KEY=$3
}

# Parse commandline args
MODE=$1
shift

. $PWD/backup.config

if [ "$MODE" == "cron" ]; then
    echo "cron"
elif [ "$MODE" == "mysql" ]; then
    echo "Dumping MySQL databases"
    dumpAllMysql
else
    printHelp
    exit 1
fi