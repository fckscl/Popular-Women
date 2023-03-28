#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python tutor_selfedu/manage.py collectstatic --no-input
python tutor_selfedu/manage.py migrate