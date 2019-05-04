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

function rsyncDownload() {
    SERVER=$1
    HOST=$2

    if [ ! -d $BACKUP_DIR/$SERVER ]; then
        echo "Making directory for $SERVER..."
        mkdir $BACKUP_DIR/$SERVER
    fi

    if [ ! -d $BACKUP_DIR/$SERVER/daily.0 ]; then
        mkdir $BACKUP_DIR/$SERVER/daily.0
    fi

    if [ ! -d $BACKUP_DIR/$SERVER/current ]; then
        echo "Link to current does not exist. Creating it..."
        ln -s $BACKUP_DIR/$SERVER/daily.0 $BACKUP_DIR/$SERVER/current
    fi

    rsync -aPqz --delete --include=/etc --include=/home --include=/root --include=/usr --include=/var --exclude=/* --link-dest=$BACKUP_DIR/$SERVER/current -e "ssh -p $SSH_PORT -i $KEY_DIR/$SERVER.key" root@$HOST:/ $BACKUP_DIR/$SERVER/latest
    echo $?

    if [ -d $BACKUP_DIR/$SERVER/daily.6 ]; then
        rm -rf $BACKUP_DIR/$SERVER/daily.6
    fi
    if [ -d $BACKUP_DIR/$SERVER/daily.5 ]; then
        mv $BACKUP_DIR/$SERVER/daily.5 $BACKUP_DIR/$SERVER/daily.6
    fi
    if [ -d $BACKUP_DIR/$SERVER/daily.4 ]; then
        mv $BACKUP_DIR/$SERVER/daily.4 $BACKUP_DIR/$SERVER/daily.5
    fi
    if [ -d $BACKUP_DIR/$SERVER/daily.3 ]; then
        mv $BACKUP_DIR/$SERVER/daily.3 $BACKUP_DIR/$SERVER/daily.4
    fi
    if [ -d $BACKUP_DIR/$SERVER/daily.2 ]; then
        mv $BACKUP_DIR/$SERVER/daily.2 $BACKUP_DIR/$SERVER/daily.3
    fi
    if [ -d $BACKUP_DIR/$SERVER/daily.1 ]; then
        mv $BACKUP_DIR/$SERVER/daily.1 $BACKUP_DIR/$SERVER/daily.2
    fi
    if [ -d $BACKUP_DIR/$SERVER/daily.0 ]; then
        mv $BACKUP_DIR/$SERVER/daily.0 $BACKUP_DIR/$SERVER/daily.1
    fi
    mv $BACKUP_DIR/$SERVER/latest $BACKUP_DIR/$SERVER/daily.0
}

function rsyncAll() {
    for ((i=0;i<${#SERVERS[@]};++i)); do
        echo "Downloading from ${SERVERS[i]}..."
        rsyncDownload "${SERVERS[i]}" "${SERVER_HOSTS[i]}"
    done
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
elif [ "$MODE" == "rsync" ]; then
    echo "Downloading all files"
    rsyncAll
else
    printHelp
    exit 1
fi