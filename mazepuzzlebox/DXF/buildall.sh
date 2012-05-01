#!/bin/bash
# boxid, thickness, json maze description
export DJANGO_SETTINGS_MODULE=mazepuzzlebox.settings
rootdir=/var/www/mazepuzzlebox
#rootdir=~/work/python/mazepuzzlebox
export PYTHONPATH=$rootdir

cd $rootdir/mazepuzzlebox/DXF/
python buildall.py
