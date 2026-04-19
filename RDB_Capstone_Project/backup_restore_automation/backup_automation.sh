#!/bin/bash

DATABASE="sales"
backupfolder=/home/theia/backups
keep_day=10

timestamp=$(date +%d-%m-%Y_%H-%M-%S)
sqlfile=$backupfolder/backup_sales_$timestamp.sql
zipfile=$backupfolder/backup_sales_$timestamp.gz

echo "Starting backup process..."

if [ ! -d "$backupfolder" ]; then
    echo "backup folder not found...creating"
    mkdir -p "$backupfolder"
fi

if ! mysql -e "USE $DATABASE" 2>/dev/null; then
    echo "Database '$DATABASE' does not exist!"
    exit 1
fi

if mysqldump "$DATABASE" > "$sqlfile"; then
    echo "SQL dump created"

    if gzip -c "$sqlfile" > "$zipfile"; then
        echo "backup compressed file successful"
        rm "$sqlfile"
    else
        echo "error compressing files"
        exit 1
    fi
else
    echo "mysql dump failed. no backup created!"
    exit 1
fi

find "$backupfolder" -name "*.gz" -mtime +$keep_day -delete

echo "Backup process completed"

