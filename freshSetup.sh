#!/bin/bash
python3 -m venv venv         # create virtual env folder named 'venv' (if not done yet)
. venv/bin/activate     # activate the virtual environment
pip install --upgrade pip    # update pip inside venv
pip install -r requirements.txt

