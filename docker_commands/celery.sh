#!/bin/bash

if [[ "${1}" == "worker" ]]; then
  celery --app=settings.celery:app worker -l info
elif [[ "${1}" == "flower" ]]; then
  celery --app=settings.celery:app flower
elif [[ "${1}" == "beat" ]]; then
  celery --app=settings.celery:app beat
fi
