# Time-lapse program for Raspberry Pi
This is my solution for a time-lapse program with included web interface running on a Raspberry Pi 2 Model B. I am using this solution to create MP4 videos out of thousands of recorded pictures with the Raspberry Pi camera.
I build this solution with a Raspberry Pi camera to preserve the mechanics of a DSLR system. If you create 10.000 pictures for a single video a non-mechanical and silent solution is very smart.

A detailed description of my solution is available on my blog: https://custom-build-robots.com/top-story-de/raspberry-pi-timelapse-fotografie-tutorial-bilder-im-zeitraffer-video/9970 in German only (sorry I will translate the posts in the future).


![timelapse web interface](https://custom-build-robots.com/wp-content/uploads/2018/03/Raspberry_Pi_Zeitraffer_control_center_v_1_1-241x300.jpg)

## Planned features
- set a start time for the time lapse like 4:30 am
- set the end time of the time lapse like 5:45 pm
- Option to enable / disable the automatic ffmpeg calculation
- display the pictures folders for which no ffmpeg calculation was done

## Known problems
I used the latest Raspberry Pi 3 Model B+ and together with raspistill I actual see many reboots. Now I switched back to my old Raspberry Pi 2 Model B to record the pictures and the system works very well over 10 hours.
