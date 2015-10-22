#!/bin/bash
#set -o verbose

# this script helps to reconfigure my dev box with current copy of GeoNode databases
# and GeoServer data directory

# read configuration
# we need to have a gnadmin postgres user in place, with same password as in production
CWD=$(pwd)
DATE="20151018"
VEDIR="/home/capooti/git/codeassist/wfp-geonode/env"
GEOSERVER_DATA_DIRECTORY="/home/capooti/git/github/geonode/geoserver"
APP_NAME="training"
BACKUP_DIR="/home/capooti/git/codeassist/wfp-geonode-deploy/backup/"$APP_NAME
DB_DJANGO=$APP_NAME"_django"
DUMP_DJANGO=$APP_NAME"_django.sql"
DB_DATA=$APP_NAME"_uploads"
DUMP_DATA=$APP_NAME"_uploads.sql"

echo $APP_NAME
echo $DB_DJANGO

cd $BACKUP_DIR

# remove old backup files and scp new ones
function dowload_backup {
    rm $BACKUP_DIR/$DATE
    scp -r capooti@thebeast:/gis/backup/data/$APP_NAME/data/$DATE $BACKUP_DIR
}

# restore gn_django
function restore_django {
    tar -xvf $BACKUP_DIR/$DATE/postgres.tar.gz $DUMP_DJANGO -C $BACKUP_DIR
    psql -U gnadmin -c "DROP DATABASE $DB_DJANGO;" postgres
    psql -U gnadmin -c "CREATE DATABASE $DB_DJANGO OWNER gnadmin;" postgres
    psql -U gnadmin -c "CREATE EXTENSION POSTGIS;" $DB_DJANGO
    psql -U gnadmin -f /usr/share/postgresql/9.3/contrib/postgis-2.1/legacy.sql $DB_DJANGO
    psql -U gnadmin $DB_DJANGO < $BACKUP_DIR/$DUMP_DJANGO 2> error_$DB_DJANGO.log
}

# restore gn_uploads
function restore_uploads {
    tar -xvf $BACKUP_DIR/$DATE/postgres.tar.gz $DUMP_DATA -C $BACKUP_DIR
    psql -U gnadmin -c "DROP DATABASE $DB_DATA;" postgres
    psql -U gnadmin -c "CREATE DATABASE $DB_DATA OWNER gnadmin;" postgres
    psql -U gnadmin -c "CREATE EXTENSION POSTGIS;" $DB_DATA
    psql -U gnadmin -f /usr/share/postgresql/9.3/contrib/postgis-2.1/legacy.sql $DB_DATA
    psql -U gnadmin $DB_DATA < $BACKUP_DIR/$DUMP_DATA 2> error_$DB_DATA.log
}

# restore geoserver
function restore_geoserver {
    rm -rf $GEOSERVER_DATA_DIRECTORY/data
    cd /tmp
    rm /tmp/geoserver
    tar -xvf $BACKUP_DIR/$DATE/geoserver.tar.gz
    mv /tmp/geoserver $GEOSERVER_DATA_DIRECTORY/data
    cd $CWD
    sed -i 's/geonode.wfp.org/localhost:8000/g' $GEOSERVER_DATA_DIRECTORY/data/security/auth/geonodeAuthProvider/config.xml
}

# restore media files
function restore_media {
    UPLOAD_DIR=/home/capooti/git/codeassist/wfp-geonode/www/uploaded
    mkdir $UPLOAD_DIR
    tar -xvf $BACKUP_DIR/$DATE/django.tar.gz
    mv django/* $UPLOAD_DIR
}

# main
dowload_backup
restore_django
restore_uploads
restore_geoserver
restore_media
