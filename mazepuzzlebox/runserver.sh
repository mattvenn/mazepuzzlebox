#!/bin/bash

source /home/mpb/.virtualenvs/mpb/bin/activate

cd /home/mpb/mazepuzzlebox/mazepuzzlebox/
exec gunicorn www.wsgi:application -b localhost:8001
