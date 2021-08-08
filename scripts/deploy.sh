#!/usr/bin/env bash

cd /home/ihfazh/palugada
docker-compose -f production.yml pull
docker-compose -f production.yml run --rm django python manage.py migrate
docker-compose -f production.yml down
docker-compose -f production.yml up -d
