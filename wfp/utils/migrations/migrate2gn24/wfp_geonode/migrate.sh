# to run on the source database before geonode migrate.sh
# 0. only WFP: run wfp/schema_changes.sql
# 1. run wfp/update_esri_gn_store.sql
# 2. run wfp/set_owner_when_is_null.sql
python $DIR/migrate_base_metadata.py

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Note: the first script must be run from the server!!!
python $DIR/migrate_wfpdocs.py
python $DIR/migrate_trainings.py
python $DIR/migrate_omep_group.py

