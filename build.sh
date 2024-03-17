#!/bin/bash
set -e
pip install -i https://test.pypi.org/simple/ -r requirements.txt
pip install setuptools pip --upgrade
pip list --outdated
pylint *.py
python setup.py sdist
