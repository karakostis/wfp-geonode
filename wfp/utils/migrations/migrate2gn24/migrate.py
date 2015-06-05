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
# 4. run wfp/migrate_wfpdocs

migrate_people
migrate_account
migrate_accountemails
migrate_avatars
migrate_resourcebase # TODO regions, categories and other fields
migrate_layers
migrate_attributes
migrate_maps
migrate_maplayers
migrate_documents
migrate_tags
migrate_permissions (*)
migrate_contactroles
# wfp
migrate_wfpdocs
migrate_trainings
migrate_traininglayers

# things not being migrated
# actstream, agon_ratings, announcements, dialogos, notifications, messages
