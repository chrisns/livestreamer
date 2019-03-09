#!/bin/sh
set -e
python ./run.py --broadcast-title ${BROADCAST_TITLE}-$(date '+%Y-%m-%dT%H:%M:%S') --stream-title ${BROADCAST_TITLE}-$(date '+%Y-%m-%dT%H:%M:%S')
ffmpeg -f lavfi \
  -i anullsrc \
  -rtsp_transport udp \
  -i ${BROADCAST_URL} \
  -vcodec mpeg4 \
  -pix_fmt + \
  -c:v libx264 \
  -f flv rtmp://a.rtmp.youtube.com/live2/$(cat /tmp/streamname.txt)
