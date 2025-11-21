#!/bin/bash


# List of Django apps with models/migrations
apps=(
    "user" "brand" "category" "product" "order" "cart" "wishlist" "review" "ip_block" "fraud_api" "contact" "shipping_charge" "site_setting" "banner"
)

# Optionally reset DB, migration history, and uploaded media (for dev/test only!)
if [[ "$1" == "--reset" ]]; then
    echo "⚠️  Resetting database, migration history, and uploaded media (dev/test only!)..."
    rm -f db.sqlite3
    for app in "${apps[@]}"; do
        find "$app/migrations" -type f -name "[0-9]*_*.py" -not -name "__init__.py" -delete 2>/dev/null || true
    done
    # Remove all uploaded media files (not tracked in git)
    if [ -d "media" ]; then
        find media -type f -delete
        find media -type d -empty -delete
    fi
    echo "✅ Database, migration files, and media files reset."
fi


echo "🧹 Cleaning __pycache__..."
for app in "${apps[@]}"; do
    if [ -d "$app" ]; then
        find "$app" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    fi
done


echo "📦 Making migrations (user first to avoid dependency ordering issues)..."
python3 manage.py makemigrations user --noinput || true
echo "📦 Making migrations for remaining apps..."
python3 manage.py makemigrations --noinput || true


echo "📥 Applying migrations..."
if python3 manage.py migrate --noinput; then
    echo "✅ Migrations applied successfully."
else
    echo "⚠️ migrate failed. Attempting automatic fix for inconsistent migration history (sqlite only)..."
    DB_FILE="db.sqlite3"
    if [ -f "$DB_FILE" ]; then
        COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM django_migrations WHERE app='user' AND name='0001_initial';" 2>/dev/null || echo 0)
        if [ "$COUNT" -eq 0 ]; then
            echo "🛠 Inserting user.0001_initial into django_migrations to fix dependency order..."
            sqlite3 "$DB_FILE" "INSERT INTO django_migrations(app, name, applied) VALUES('user','0001_initial', datetime('now'));" || true
        else
            echo "ℹ️ user.0001_initial already present in django_migrations."
        fi
        echo "🔁 Retrying migrations..."
        python3 manage.py migrate --noinput || {
            echo "❌ migrate still failed after attempting sqlite fix. Check errors above.";
            exit 1;
        }
    else
        echo "❌ Database file '$DB_FILE' not found — cannot apply sqlite fix. Please inspect migration errors manually.";
        exit 1
    fi
    echo "✅ Migrations applied successfully after fix."
fi

# Check for missing tables after migration
echo "🔎 Checking for missing tables after migration..."
expected_tables=(
    "user_user" "brand_brand" "category_category" "product_product" "order_order" "cart_cart" "wishlist_wishlist" "review_review" "ip_block_blockedip" "fraud_api_fraudapi" "contact_contact" "shipping_charge_shippingcharge" "site_setting_sitesetting" "banner_banner"
)
missing=()
for tbl in "${expected_tables[@]}"; do
    if ! sqlite3 db.sqlite3 ".tables" | grep -qw "$tbl"; then
        missing+=("$tbl")
    fi
done
if [ ${#missing[@]} -gt 0 ]; then
    echo "❌ WARNING: The following tables are still missing after migration: ${missing[*]}"
    echo "   This usually means migration history is still broken. Try running: $0 --reset"
    exit 2
else
    echo "✅ All expected tables are present."
fi
