# 1. restore media files from backup
# 2. copy GeoServer data directory to GeoServer included with GeoNode 2.4

# migration steps
# 1. run migration scripts
# 2. run updatelayers
# 3. run ./manage.py shell < wfp/utils/migrations/migrate2gn24/update_resources.py

# specific for wfp
# 1. run wfp/update_esri_gn_store.sql
# 2. run wfp/migrate_wfpdocs

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python $DIR/migrate_people.py
python $DIR/migrate_account.py
#python $DIR/migrate_accountemails.py TODO check what is not working here
python $DIR/migrate_avatars.py
python $DIR/migrate_resourcebases.py # TODO regions, categories and other fields
python $DIR/migrate_layers.py
python $DIR/migrate_attributes.py
python $DIR/migrate_maps.py
python $DIR/migrate_maplayers.py
./manage.py updatelayers --ignore-errors
python $DIR/migrate_documents.py
python $DIR/create_auth_group_and_update_res.py
# here migrate other resourcebase based models
# now tags, regions and permissions
python $DIR/migrate_tags.py
python $DIR/migrate_regions.py
python $DIR/migrate_user_permissions.py
python $DIR/migrate_group_permissions.py # check if is ok
# python migrate_contactroles.py # TODO

# things not being migrated, PR are welcome :)
# actstream, agon_ratings, announcements, dialogos, notifications, messages
