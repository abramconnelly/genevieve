#!/bin/bash

rabbitmq-server -detached

su -l genevieve -c " cd /home/genevieve/genevieve && \
  workon genevieve && \
  python manage.py runserver 0.0.0.0:8000 " &


su -l genevieve -c " cd /home/genevieve/genevieve && \
  workon genevieve && \
  celery -A genevieve worker -l info " &


while [ true ]
do
  echo ping
  sleep 3
done
