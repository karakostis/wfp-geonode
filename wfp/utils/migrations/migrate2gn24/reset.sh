psql -U gnadmin -c "DROP DATABASE sdi_django_24;" postgres
psql -U gnadmin -c "CREATE DATABASE sdi_django_24 OWNER gnadmin;" postgres
psql -U gnadmin -c "CREATE EXTENSION POSTGIS;" sdi_django_24
psql -U gnadmin -f /usr/share/postgresql/9.3/contrib/postgis-2.1/legacy.sql sdi_django
python ~/git/codeassist/wfp-geonode/manage.py syncdb --noinput
