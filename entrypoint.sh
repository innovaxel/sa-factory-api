#!/bin/sh

python manage.py makemigrations accounts admin jobs sessions token_blacklist
python manage.py migrate

exec "$@"
