#!/bin/bash
#set -o verbose

# TODO here donwload backup archives

# read configuration
# we need to have a gnadmin postgres user in place, with same password as in production
CWD=$(pwd)
DATE="20150906"
BACKUP_DIR="/home/capooti/backup/geonode"
VEDIR="/home/capooti/git/codeassist/wfp-geonode/env"
GEOSERVER_DATA_DIRECTORY=/home/capooti/git/github/geonode/geoserver
DB_DJANGO=sdi_django
DUMP_DJANGO=sdi_django.sql
DB_DATA=sdi_uploads
DUMP_DATA=sdi_uploads.sql

cd $BACKUP_DIR

# remove old backup files and scp new ones
function dowload_backup {
    rm $BACKUP_DIR/$DATE
    scp -r capooti@thebeast:/gis/backup/data/sdi/data/$DATE $BACKUP_DIR
}

# restore gn_django
function restore_django {
    tar -xvf $BACKUP_DIR/$DATE/postgres.tar.gz $DUMP_DJANGO -C $BACKUP_DIR
    psql -U gnadmin -c "DROP DATABASE $DB_DJANGO;" postgres
    psql -U gnadmin -c "CREATE DATABASE $DB_DJANGO OWNER gnadmin;" postgres
    psql -U gnadmin -c "CREATE EXTENSION POSTGIS;" $DB_DJANGO
    psql -U gnadmin -f /usr/share/postgresql/9.2/contrib/postgis-2.1/legacy.sql $DB_DJANGO
    psql -U gnadmin $DB_DJANGO < $BACKUP_DIR/$DUMP_DJANGO 2> error_$DB_DJANGO.log
}

# restore gn_uploads
function restore_uploads {
    tar -xvf $BACKUP_DIR/$DATE/postgres.tar.gz $DUMP_DATA -C $BACKUP_DIR
    psql -U gnadmin -c "DROP DATABASE $DB_DATA;" postgres
    psql -U gnadmin -c "CREATE DATABASE $DB_DATA OWNER gnadmin;" postgres
    psql -U gnadmin -c "CREATE EXTENSION POSTGIS;" $DB_DATA
    psql -U gnadmin -f /usr/share/postgresql/9.2/contrib/postgis-2.1/legacy.sql $DB_DATA
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

# main
dowload_backup
restore_django
restore_uploads
restore_geoserver
