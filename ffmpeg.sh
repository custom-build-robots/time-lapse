#!/bin/bash
DATE=$(date +"%Y%m%d%H%M")

# manual usage
#ffmpeg -y -f image2 -pattern_type glob -i '/media/usbstick/pictures_XXX*.jpg' -r 24 -vcodec libx264 -profile high -preset slow /media/usbstick/video/Animation_XXX.mp4
sleep $4

# automatic usage
echo "Starting ffmpeg" >> $3Animation_$2.log 2>&1
#ffmpeg -y -f image2 -pattern_type glob -i $1'*.jpg' -r 24 -vcodec libx264 -profile high -preset slow $1Animation_$2.mp4 >> $1ffmpeg.log 2>&1 &
ffmpeg -y -f image2 -pattern_type glob -i $1'*.jpg' -r 24 -vcodec libx264 -profile high -preset slow $3Animation_$2.mp4 >> $3Animation_$2.log 2>&1
echo "Finished ffmpeg" >> $3Animation_$2.log 2>&1