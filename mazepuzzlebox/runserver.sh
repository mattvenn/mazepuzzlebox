#!/bin/bash

source /srv/users/mazepuzzle/mpb-venv/bin/activate

cd /srv/users/mazepuzzle/mazepuzzlebox/mazepuzzlebox
exec gunicorn wsgi:application -b localhost:8001
