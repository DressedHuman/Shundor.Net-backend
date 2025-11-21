#!/bin/bash

# Exit on error
set -e

# Change to the directory where your manage.py file is
cd "$(dirname "$0")"

# Set environment variables (optional)
export DJANGO_SETTINGS_MODULE=config.settings  # Replace with your settings path
export PYTHONUNBUFFERED=1  # Optional: ensures real-time output

# # Activate virtual environment
# echo "Activating virtual environment..."
# source venv/bin/activate  # Change this path if your venv is located elsewhere

# Apply migrations using the safer script

echo "Applying database migrations using new_migration.sh (robust flow)..."
if [ -x "$(dirname "$0")/new_migration.sh" ]; then
	"$(dirname "$0")/new_migration.sh"
	status=$?
	if [ $status -eq 2 ]; then
		echo "❌ Migration completed but some tables are missing. Try: ./new_migration.sh --reset"
		exit 2
	elif [ $status -ne 0 ]; then
		echo "❌ Migration failed. See errors above."
		exit $status
	fi
else
	echo "⚠️ new_migration.sh not found or not executable — falling back to manage.py migrate"
	python3 manage.py migrate --noinput
fi


# Collect static files (optional, skip in dev)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# If arguments are passed, forward them to manage.py (like run_command.sh)
if [ "$#" -gt 0 ]; then
	echo "Running custom Django command: $@"
	python3 manage.py "$@"
else
	echo "Starting Django development server..."
	python3 manage.py runserver 0.0.0.0:8000
fi