#!/bin/sh
cd /app/server
nginx -g 'daemon off;' &
python3 main.py
