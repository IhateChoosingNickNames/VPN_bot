#!/bin/bash

echo "Make migrations"
cd db && alembic revision --autogenerate

echo "Run migrations"
alembic upgrade head

echo "Starting bot."
cd .. && python manage.py start_bot