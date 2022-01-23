#!/bin/bash

echo "Waiting for mysql to start..."
until mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" &> /dev/null
do
    sleep 1
done


echo "_______________________________________________________"
cd app/db && alembic upgrade head
echo "_______________________________________________________"

cd ../../ && uvicorn app.main:app --reload --port=8000 --host=0.0.0.0
