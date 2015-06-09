# preliminary steps
# 0. configure computer with a new geonode database (2.4) and with old database (2.0)
# 1. restore media files from backup
# 2. copy GeoServer data directory to GeoServer included with GeoNode 2.4

# migration steps
# 0. only WFP: run wfp/schema_changes.sql
# 1. run migration scripts
# 2. run updatelayers
# 3. run ./manage.py shell < wfp/utils/migrations/migrate2gn24/update_resources.py

# specific for wfp
# 1. run wfp/update_esri_gn_store.sql
# 2. run wfp/migrate_wfpdocs

python migrate_people
python migrate_account
python migrate_accountemails
python migrate_avatars
python migrate_resourcebase # TODO regions, categories and other fields
python migrate_layers
python migrate_attributes
python migrate_maps
python migrate_maplayers
python migrate_documents
python migrate_tags
python migrate_user_permissions
python create_authenticated_group
python migrate_group_permissions (*)
python migrate_contactroles (*)
# wfp
python migrate_wfpdocs
python migrate_trainings
python migrate_traininglayers

# things not being migrated
# actstream, agon_ratings, announcements, dialogos, notifications, messages
