#!/bin/sh

echo "Persistir dados migration do SQLite no Projeto..."
python manage.py migrate --no-input

exec "$@"

chmod +x persistir_migration.sh