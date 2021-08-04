-- psql postgres < init_database.sql
CREATE USER djangouser WITH ENCRYPTED PASSWORD 'secret';
CREATE DATABASE djangotraining OWNER djangouser ENCODING 'utf-8';
