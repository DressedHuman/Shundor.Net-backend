#!/bin/bash
# This script updates the expected_tables array in new_migration.sh to include all tables for models in all installed apps.
# It should be run after adding new apps/models.

set -e

# Path to your Django manage.py
MANAGE=./manage.py
MIGRATION_SCRIPT=new_migration.sh

# Get all model table names from Django
TABLES=$(python3 $MANAGE inspectdb --database=default 2>/dev/null | grep -E '^class ' | sed -E 's/^class ([^(]+)\(models.Model\):/\1/' | tr 'A-Z' 'a-z')

# Or, more reliably, use Django's db introspection:
TABLES=$(python3 -c "import django; django.setup(); from django.apps import apps; print(' '.join([m._meta.db_table for m in apps.get_models()]))" 2>/dev/null)

# Format as bash array
ARRAY="expected_tables=(\n"
for tbl in $TABLES; do
    ARRAY+="    \"$tbl\""
    ARRAY+=" "
done
ARRAY+="\n)"

# Replace the expected_tables array in new_migration.sh
awk -v newarr="$ARRAY" '
    BEGIN {inarr=0}
    /^expected_tables=\(/ {print newarr; inarr=1; next}
    inarr && /^\)/ {inarr=0; next}
    !inarr {print}
' "$MIGRATION_SCRIPT" > tmp_nmig.sh && mv tmp_nmig.sh "$MIGRATION_SCRIPT"

echo "✅ expected_tables updated in $MIGRATION_SCRIPT."
