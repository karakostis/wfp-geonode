#!/bin/bash
#set -o verbose

# TODO here donwload backup archives

# read configuration
# we need to have a gnadmin postgres user in place, with same password as in production
CWD=$(pwd)
DATE="20140525"
BACKUP_DIR="/home/capooti/backup/geonode/backup_tar_gz"
VEDIR="/home/capooti/.venvs/geonode"

# remove old backup files and scp new ones
rm $BACKUP_DIR/postgres/*
rm $BACKUP_DIR/geoserver/*
scp backup@production:/home/backup/geoserver/backup/$DATE.tar.gz $BACKUP_DIR/geoserver
scp backup@production:/home/backup/postgres/backup/$DATE.tar.gz $BACKUP_DIR/postgres

# restore gn_django
DB=gn_django
DUMP=gn_django.sql
tar -xvf $BACKUP_DIR/postgres/$DATE.tar.gz $DATE/gn_django.sql
psql -c "SELECT pg_terminate_backend(pg_stat_activity.procpid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB' AND procpid <> #pg_backend_pid();" postgres
psql -c "DROP DATABASE $DB;" postgres
psql -c "CREATE DATABASE $DB OWNER gnadmin;" postgres
psql $DB < $DATE/$DUMP

# restore gn_uploads
DB=gn_uploads
DUMP=gn_uploads.sql
tar -xvf $BACKUP_DIR/postgres/$DATE.tar.gz $DATE/gn_uploads.sql
psql -c "SELECT pg_terminate_backend(pg_stat_activity.procpid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB' AND procpid <> pg_backend_pid();" postgres
psql -c "DROP DATABASE $DB;" postgres
psql -c "CREATE DATABASE $DB OWNER gnadmin;" postgres
psql $DB < $DATE/$DUMP

# restore geoserver
GEOSERVER_DATA_DIRECTORY=/home/capooti/git/github/capooti/geonode/geoserver
rm -rf $GEOSERVER_DATA_DIRECTORY/data
cd $GEOSERVER_DATA_DIRECTORY
tar -xvzf $BACKUP_DIR/geoserver/$DATE.tar.gz $DATE
mv $DATE data
cd $CWD
sed -i 's/geonode.wfp.org/localhost:8000/g' $GEOSERVER_DATA_DIRECTORY/data/security/auth/geonodeAuthProvider/config.xml

# remove directory
rm -rf $DATE

# set site name
. $VEDIR/bin/activate
./manage.py shell < wfp/utils/set_sitedomain.py

# migrations
./manage.py migrate base --fake 0002
./manage.py migrate documents --fake 0001
./manage.py migrate documents
./manage.py migrate layers --fake 0001




