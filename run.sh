#!/usr/bin/with-contenv bashio

echo "Hello world!"
TVIP=$(bashio::config 'tv')

mkdir -p /media/theframe
echo "tv-ip ${TVIP}"
python3 art.py --tvip ${TVIP}
echo "done, closing now!"
kill -s SIGHUP 1

