import os

from paver.easy import task
from paver.easy import sh, info

# TODO read from configuration
# we need to have a gnadmin postgres user in place, with same password as in production
DATE = "20140727"
BACKUP_DIR = "/home/capooti/backup/geonode/backup_tar_gz"
GEOSERVER_DATA_DIRECTORY = '/home/capooti/git/codeassist/geonode/geoserver'
VE_DIR = "/home/capooti/.venvs/geonode"
DJANGO_DB_NAME = 'training_django'
UPLOADS_DB_NAME = 'training_upload'

# TODO move to paver this
# remove old backup files and scp new ones
# rm $BACKUP_DIR/*
# scp gis@thebeast:/gis/backup/data/$DATE/sdi/geoserver.tar.gz $BACKUP_DIR
# scp gis@thebeast:/gis/backup/data/$DATE/sdi/postgres.tar.gz $BACKUP_DIR


@task
def restore_django_db():
    """
    Restore genode django database.
    """
    restore_db(DJANGO_DB_NAME)


@task
def restore_uploads_db():
    """
    Restore genode uploads database.
    """
    restore_db(UPLOADS_DB_NAME)


def restore_db(dbname):
    sh('tar xvf %s/postgres.tar.gz %s.sql' % (BACKUP_DIR, dbname))
    sh('psql -c "DROP DATABASE %s;" postgres' % dbname)
    sh('psql -c "CREATE DATABASE %s OWNER gnadmin;" postgres' % dbname)
    sh('psql %s < %s.sql' % (dbname, dbname))
    sh('rm %s.sql' % (dbname))
    info('geonode %s database restored.' % dbname)


@task
def restore_geoserver():
    """
    Restore the geoserver configuration.
    """
    sh('rm -rf %s/data' % GEOSERVER_DATA_DIRECTORY)
    sh('tar -xvzf %s/geoserver.tar.gz' % BACKUP_DIR)
    sh('mv geoserver %s/data' % GEOSERVER_DATA_DIRECTORY)
    sh(
        'sed -i "s/geonode.wfp.org/localhost:8000/g" %s/data/security/auth/geonodeAuthProvider/config.xml'
        % GEOSERVER_DATA_DIRECTORY
    )
    info('geoserver restored.')


@task
def restore_django():
    """
    Restore django configuration.
    """
    sql = "UPDATE django_site SET domain = 'localhost:8000', name = 'localhost:8000';"
    os.environ['PGPASSWORD'] = os.environ['geonode_pwd']
    sh('psql -U gnadmin -c "%s" %s' % (sql, DJANGO_DB_NAME))
    # TODO change db name form gn_uploads to sdi_uploads
