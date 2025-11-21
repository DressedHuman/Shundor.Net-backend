#!/bin/bash

# Usage: ./create_django_superuser.sh <username> <email> <password>

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <username> <email> <password>"
    exit 1
fi

PHONE=$1
EMAIL=$2
PASSWORD=$3

# Navigate to your Django project directory
# Replace this with your actual Django project path
PROJECT_DIR="./"

cd "$PROJECT_DIR" || { echo "Project directory not found: $PROJECT_DIR"; exit 1; }

# Activate your virtual environment
# Replace this with your virtualenv activation path if needed
source ./venv/bin/activate

# Create superuser non-interactively using Django's shell
python3 manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(phone_number='$PHONE').exists():
    User.objects.create_superuser('$PHONE', '$PASSWORD')
    print('Superuser created successfully.')
else:
    print('Superuser already exists.')
EOF
