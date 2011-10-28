#!/bin/bash
# boxid, thickness, json maze description
export DJANGO_SETTINGS_MODULE=mazepuzzlebox.settings
export PYTHONPATH=~/work/python/mazepuzzlebox

cd ~/work/python/mazepuzzlebox/mazepuzzlebox/DXF/
python buildall.py
