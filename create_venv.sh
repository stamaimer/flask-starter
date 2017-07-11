#!/usr/bin/env bash
# create_venv.sh

virtualenv .venv -p python2.7

source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com
