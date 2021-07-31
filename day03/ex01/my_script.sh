#!/bin/sh
# https://pypi.org/project/path/
# https://github.com/jaraco/path

# rm -rf ./local_lib/

pip3 --version
pip3 install git+https://github.com/jaraco/path.git \
     -t ./local_lib/ \
     --log install.log \
     --upgrade
