#!/usr/bin/with-contenv bashio

TVIP=$(bashio::config 'tv')

mkdir -p /media/theframe
echo "Using ${TVIP} as the IP of the Samsung Frame"
python3 art.py --tvip ${TVIP}
echo "done, closing now!"
kill -s SIGHUP 1

