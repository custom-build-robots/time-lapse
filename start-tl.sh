#!/bin/bash
/bin/sleep 20
sudo python /home/pi/timelapse/timelapse.py >> /home/pi/time_lapse.log 2>&1 &
