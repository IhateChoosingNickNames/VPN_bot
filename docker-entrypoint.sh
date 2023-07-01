#!/bin/bash

echo "Move to db folder"
cd db

echo "Make migrations"
exec alembic revision --autogenerate

echo "Apply migrations"
exec alembic upgrade head

echo "Move back"
cd ..

echo "Starting bot."
exec python manage.py start_bot