#!/bin/bash
set -e
pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url=https://pypi.org/simple/ -r requirements.txt
pip install setuptools pip --upgrade
pip list --outdated
pylint *.py
python setup.py sdist
