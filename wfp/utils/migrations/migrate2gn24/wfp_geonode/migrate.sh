# 0. only WFP: run wfp/schema_changes.sql
# 1. run wfp/update_esri_gn_store.sql

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python $DIR/migrate_wfpdocs.py
python $DIR/migrate_trainings.py

