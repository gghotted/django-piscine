#!/bin/sh

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

python d04/manage.py migrate
python d04/manage.py runserver
