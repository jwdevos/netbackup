#!/bin/bash

LOG_PATH="/home/user/customers/home/logs/"
BCK_PATH="/home/user/customers/home/backups/"
CSV_PATH="/home/user/customers/home/cfg/.csv"
ENV_PATH="/home/user/customers/home/cfg/.env"

source /home/user/python/netbackup/bin/activate
python /home/user/python/netbackup/main.py -l $LOG_PATH -b $BCK_PATH -c $CSV_PATH -e $ENV_PATH
