#!/usr/bin/env bash
# exit on error
set -o errexit

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - --uninstall
curl -sSL https://install.python-poetry.org | python3 -
poetry self update
poetry install

python manage.py collectstatic --no-input
python manage.py migrate