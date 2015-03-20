#!/bin/bash
#set -o verbose

# TODO here donwload backup archives

# read configuration
# we need to have a gnadmin postgres user in place, with same password as in production
CWD=$(pwd)
DATE="20150315"
BACKUP_DIR="/home/capooti/backup/geonode"
VEDIR="/home/capooti/git/codeassist/wfp-geonode/env"

cd $BACKUP_DIR

# remove old backup files and scp new ones
function dowload_backup {
    rm $BACKUP_DIR/$DATE
    scp -r capooti@thebeast:/gis/backup/data/sdi/$DATE $BACKUP_DIR
}

# restore gn_django
function restore_django {
    DB=sdi_django
    DUMP=sdi_django.sql
    tar -xvf $BACKUP_DIR/$DATE/postgres.tar.gz $DUMP
    psql -U gnadmin -c "DROP DATABASE $DB;" postgres
    psql -U gnadmin -c "CREATE DATABASE $DB OWNER gnadmin;" postgres
    psql -U gnadmin -c "CREATE EXTENSION POSTGIS;" $DB
    psql -U gnadmin -f /usr/share/postgresql/9.2/contrib/postgis-2.1/legacy.sql $DB
    psql -U gnadmin $DB < $BACKUP_DIR/$DUMP 2> error_$DB.log
}

# restore gn_uploads
function restore_uploads {
    DB=sdi_uploads
    DUMP=sdi_uploads.sql
    tar -xvf $BACKUP_DIR/$DATE/postgres.tar.gz $DUMP -C $BACKUP_DIR
    psql -U gnadmin -c "DROP DATABASE $DB;" postgres
    psql -U gnadmin -c "CREATE DATABASE $DB OWNER gnadmin;" postgres
    psql -U gnadmin -c "CREATE EXTENSION POSTGIS;" $DB
    psql -U gnadmin -f /usr/share/postgresql/9.2/contrib/postgis-2.1/legacy.sql $DB
    psql -U gnadmin $DB < $BACKUP_DIR/$DUMP 2> error_$DB.log
}

# restore geoserver
function restore_geoserver {
    GEOSERVER_DATA_DIRECTORY=/home/capooti/git/codeassist/geonode/geoserver
    rm -rf $GEOSERVER_DATA_DIRECTORY/data
    cd /tmp
    rm /tmp/geoserver
    tar -xvf $BACKUP_DIR/$DATE/geoserver.tar.gz
    mv /tmp/geoserver $GEOSERVER_DATA_DIRECTORY/data
    cd $CWD
    sed -i 's/geonode.wfp.org/localhost:8000/g' $GEOSERVER_DATA_DIRECTORY/data/security/auth/geonodeAuthProvider/config.xml
}

# set site name
function set_site_name {
    . $VEDIR/bin/activate
    ./manage.py shell < wfp/utils/set_sitedomain.py
}

# main
dowload_backup
restore_django
restore_uploads
restore_geoserver
set_site_name

# migrations
#./manage.py migrate base --fake 0002
#./manage.py migrate documents --fake 0001
#./manage.py migrate documents
#./manage.py migrate layers --fake 0001




