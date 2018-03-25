#!/bin/bash
DATE=$(date +"%Y%m%d%H%M")

# ffmpeg -y -f image2 -i /home/pi/time_laps/image%06d.jpg -r 24 -vcodec libx264 -profile high -preset slow /media/usbstick/animation.mp4
# '/media/usbstick/pictures/'
#ffmpeg -y -f image2 -pattern_type glob -i '/home/pi/time_laps/*.jpg' -r 24 -vcodec libx264 -profile high -preset slow /media/usbstick/animation.mp4
#ffmpeg -y -f image2 -pattern_type glob -i '/media/usbstick/pictures/*.jpg' -r 24 -vcodec libx264 -profile high -preset slow /media/usbstick/Animation_$DATE.mp4
sleep $3
#ffmpeg -y -f image2 -pattern_type glob -i $1'*.jpg' -r 24 -vcodec libx264 -profile high -preset slow $1Animation_$2.mp4 >> $1ffmpeg.log 2>&1 &
ffmpeg -y -f image2 -pattern_type glob -i $1'*.jpg' -r 24 -vcodec libx264 -profile high -preset slow $1Animation_$2.mp4