#!/bin/bash
set -e
LOGFILE=/home/artminster/logs/artminster_gunicorn.access.log
ERRORFILE=/home/artminster/logs/artminster_gunicorn.error.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
#The below address:port info will be used later to configure Nginx with Gunicorn
ADDRESS=unix:/var/run/artminster.sock
# user/group to run as
#USER=your_unix_user
#GROUP=your_unix_group
cd /home/artminster/sites/artminster/repository
source ../env/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/artminster/sites/artminster/repository/allauth
export PYTHONPATH=$PYTHONPATH:/home/artminster/sites/artminster/repository/rawjam
export PYTHONPATH=$PYTHONPATH:/home/artminster/sites/artminster/repository/artminster
test -d $LOGDIR || mkdir -p $LOGDIR
exec ../env/bin/gunicorn_django -w $NUM_WORKERS --bind=$ADDRESS \
--log-level=debug --settings=artminster.configs.production.settings \
--log-file=$LOGFILE 2>>$LOGFILE  1>>$ERRORFILE
