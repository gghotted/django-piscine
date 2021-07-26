#!/bin/sh
curl $1 -s | grep href | cut -f2 -d'"'
