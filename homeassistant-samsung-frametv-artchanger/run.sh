#!/usr/bin/with-contenv bashio

TVIP=$(bashio::config 'tv')

mkdir -p /media/frame
echo "Using ${TVIP} as the IP's of the Samsung Frame"

PARAMS=""

if bashio::config.true 'google_art'; then
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
if bashio::config.true 'same_image'; then
    PARAMS="${PARAMS} --same-image"
fi
if bashio::config.true 'google_photos'; then
    GOOGLE_PHOTOS_ALBUM=$(bashio::config 'google_photos_album')
    GOOGLE_PHOTOS_CLIENT_ID=$(bashio::config 'google_photos_client_id')
    GOOGLE_PHOTOS_CLIENT_SECRET=$(bashio::config 'google_photos_client_secret')
    export GOOGLE_PHOTOS_CLIENT_ID
    export GOOGLE_PHOTOS_CLIENT_SECRET
    PARAMS="${PARAMS} --google-photos --google-photos-album \"${GOOGLE_PHOTOS_ALBUM}\""
fi

python3 art.py --tvip ${TVIP} ${PARAMS}

echo "done, closing now!"
kill -s SIGHUP 1
