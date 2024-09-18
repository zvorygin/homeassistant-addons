#!/usr/bin/with-contenv bashio

TVIP=$(bashio::config 'tv')

mkdir -p /media/frame
echo "Using ${TVIP} as the IP's of the Samsung Frame"

PARAMS=""

if bashio::config.true 'googleart'; then
    PARAMS="${PARAMS} --google-art"
fi
if bashio::config.true 'bing_wallpapers'; then
    PARAMS="${PARAMS} --bing-wallpapers"
fi
if bashio::config.true 'media_folder'; then
    PARAMS="${PARAMS} --media-folder"
fi
if bashio::config.true 'download_high_res'; then
    PARAMS="${PARAMS} --download-high-res"
fi

python3 art.py --tvip ${TVIP} ${PARAMS}

echo "done, closing now!"
kill -s SIGHUP 1
