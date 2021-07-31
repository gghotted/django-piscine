#!/bin/sh

brew install postgresql

virtualenv ./django_env
source ./django_env/bin/activate
pip install -r requirement.txt
