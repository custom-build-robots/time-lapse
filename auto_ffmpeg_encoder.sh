#!/bin/bash
# Autor:   Ingmar Stapel
# Datum:   20180425
# Version:   1.0
# Homepage:   http://custom-build-robots.com

# If you have disabled the automatic video generation in the python
# program this script will help you to auto generate time-lapse 
# movies out of all picture folder generated by the python program.

DATE=$(date +"%Y.%m.%d_%H:%M:%S")

# set the directory in which the folders are stored with the pictures.
pictures_dir="/media/usbstick/pictures/"

# set the directory in which the generated MP4 movie will be stored.
video_dir="/media/usbstick/video/"

if ! [ -d "$pictures_dir" ]; then
    # Example command to mount a samba share from the picture recording Raspberry Pi SBC.
    # sudo mount.cifs //192.168.1.38/timelapse /media/usbstick -o user=pi,password=raspberry,nounix,sec=ntlmssp

    # This command will mount the usb drive /dev/sda1 which I use between the picture recording Raspberry Pi SBC
    # and the ffmpeg / video generating Raspberry Pi 3 Model B+.
    sudo mount -t exfat -o utf8,uid=pi,gid=pi,noatime /dev/sda1 /media/usbstick
fi

sleep 2s

for Dir in $(find $pictures_dir* -maxdepth 0 -type d ); 
do
    FolderName=$(basename $Dir);

    if ! [ -e $Dir/$FolderName.log ]
    then
        echo "Starting ffmpeg encoding $DATE." >> $Dir/$FolderName.log 2>&1
        ffmpeg -y -f image2 -hide_banner -loglevel panic -pattern_type glob -i $Dir/'*.jpg' -r 24 -vcodec libx264 -profile high -preset slow $video_dir$FolderName.mp4 >> $Dir/$FolderName.log 2>&1
        echo "End ffmpeg video encoding $DATE." >> $Dir/$FolderName.log 2>&1
    fi
done