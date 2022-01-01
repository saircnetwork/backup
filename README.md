# Backup Fab Script
This script allows backups of each server to be downloaded for storage elsewhere. Every day a snapshot is taken and every week the latest snapshot
is compressed into an archive.

## Prerequisites
This script requires Python 3 and Fabric 2.6.0.

Fabric can be installed using
`pip install fabric

## Cron backup
The cron backup can be ran from the directory by running
`fab cron