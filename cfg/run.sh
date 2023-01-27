#!/bin/bash

LOG_PATH="/home/user/customers/customer-1/logs/"
BCK_PATH="/home/user/customers/customer-1/backups/"
CSV_PATH="/home/user/customers/customer-1/cfg/.csv"
ENV_PATH="/home/user/customers/customer-1/cfg/.env"
REP_PATH="/home/user/customers/customer-1/cfg/report.j2"

source /home/user/python/netbackup/bin/activate
python /home/user/python/netbackup/main.py -l $LOG_PATH -b $BCK_PATH -c $CSV_PATH -e $ENV_PATH -r $REP_PATH
