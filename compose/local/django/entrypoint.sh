#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z django-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"


echo "Making makemigartions at django"
python /usr/src/app/src/manage.py migrate

echo "Making migrate at django"
python /usr/src/app/src/manage.py migrate

echo "Making runserver at django"
python /usr/src/app/src/manage.py runserver 0.0.0.0:8000
