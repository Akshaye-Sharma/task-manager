#!/bin/bash
. venv/bin/activate
nohup python3 run.py > /dev/null 2>&1 &

