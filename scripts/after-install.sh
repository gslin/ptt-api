#!/bin/bash

~/.pyenv/shims/pip install -U -r /srv/ptt-api.hasname.com/requirements.txt
pkill -INT uwsgi
LANG=en_US.UTF-8 ~/.pyenv/shims/uwsgi --ini /srv/ptt-api.hasname.com/uwsgi.ini > /dev/null 2>&1 &
