#!/bin/bash
# Autor:   Ingmar Stapel
# Datum:   20180423
# Version:   1.1
# Homepage:   http://custom-build-robots.com
# This script is used to generate time-lapse videos via ffmpeg.
DATE=$(date +"%Y%m%d%H%M")

# manual usage
#ffmpeg -y -f image2 -pattern_type glob -i '/media/usbstick/pictures_XXX/*.jpg' -r 24 -vcodec libx264 -profile high -preset slow /media/usbstick/video/Animation_XXX.mp4
sleep $4

# automatic usage via a python program "timelapse.py".
echo "Starting ffmpeg" >> $3Animation_$2.log 2>&1
ffmpeg -y -f image2 -pattern_type glob -i $1'*.jpg' -r 24 -vcodec libx264 -profile high -preset slow $3Animation_$2.mp4 >> $3Animation_$2.log 2>&1
echo "Finished ffmpeg" >> $3Animation_$2.log 2>&1
