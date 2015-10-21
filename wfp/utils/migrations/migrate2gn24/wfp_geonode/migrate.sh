# to run on the source database before geonode migrate.sh
# only WFP: run wfp_geonode/schema_changes.sql
# run wfp_geonode/update_esri_gn_store.sql
# run wfp_geonode/update_osm_store.sql
# run wfp_geonode/set_owner_when_is_null.sql
# run wfp_geonode/remove_bing_maps.sql
python $DIR/migrate_base_metadata.py

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Note: to be run from the server
python $DIR/migrate_wfpdocs.py
python $DIR/migrate_trainings.py
python $DIR/migrate_omep_group.py
python $DIR/migrate_gis.py

