#!/bin/bash
set -e
python3 -m pip install --upgrade build
pylint waterstand/*.py
pytest
rm dist/*
python -m build
