#!/bin/bash
set -e
python3 -m pip install --upgrade build
pip install -r requirements.txt
pip list --outdated
pylint waterstand/*.py
pytest
rm dist/*
python -m build
