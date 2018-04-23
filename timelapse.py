#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20180423
# Version:   1.1
# Homepage:   http://custom-build-robots.com
# This program is developed to generate time-lapse videos.

from flask import Flask, render_template, flash
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os
import time
import subprocess

from datetime import datetime  
from datetime import timedelta 

# intervall is the time between each picture in seconds
intervall = 1
intervall *= 1000

# print messages
debug = True

dest_pic = ""
dest_video = ""
time_string = ""
output_ffmpeg = ""
output_raspistill = ""

global time_until
time_until = datetime.now()

# Enable / Disable automatic ffmpeg calculation.
ffmpeg = True

# mount usb drive as usual
os.system("sudo mount -t exfat -o utf8,uid=pi,gid=pi,noatime /dev/sda1 /media/usbstick >> /home/pi/mount.log 2>&1 &")
time.sleep(2)

# Function to make the path in which the pictures should be stored
def create_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Generates and returns the path for the pictures
def getpath():
    # get a string with the current date and time
    time_string = time.strftime("%Y%m%d%H%M%S")
    # picture destination path
    dest_pic = "/media/usbstick/pictures/pictures_"+time_string+"/"
    return dest_pic, time_string

app = Flask(__name__, static_folder='/media/usbstick/preview',)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'well-secret-password'

class MyForm(Form):
    name = StringField(label='Timelapse duration (minutes)', validators=[DataRequired()], default="15")
    intervall = StringField(label='Picture intervall (seconds)', validators=[DataRequired()], default="1")
    width   = StringField(label='Resolution ', validators=[DataRequired()], default="1920")
    height   = StringField(label=' x ', validators=[DataRequired()], default="1080")
    quality   = StringField(label='Quality (...%): ', validators=[DataRequired()], default="80")

    #name = StringField(label='Time in minutes', [validators.Required("15")])
    starting = SubmitField(label='Start recording')
    preview  = SubmitField(label='Preview picture')
    reboot   = SubmitField(label='Raspberry reboot')
    ending   = SubmitField(label='Raspberry shutdown')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    global time_until

    flash(
        "USB drive status: {usb}".format(
            usb = str(subprocess.check_output("df -h | grep sda1", shell=True))
        )
    )

    if time_until > datetime.now():
        flash(
            "Timelapse now active until: {time_to}".format(
            time_to=time_until.strftime('%Y-%m-%d %H:%M:%S')
        )
        )

    if form.validate_on_submit():
        if form.starting.data:
            runtime_min = int(form.name.data)
            runtime_sec = runtime_min * 60 + 30
            runtime_mili = runtime_min * 60000
            intervall = int(form.intervall.data)
            intervall *= 1000

            dest_pic, time_string = getpath()
            dest_video = "/media/usbstick/video/"


            width = int(form.width.data)
            height = int(form.height.data)
            quality = int(form.quality.data)

            # create path
            create_path(dest_pic)
            
            # record time until
            time_until = datetime.now() + timedelta(minutes=runtime_min)
            # print "Value : {name}".format(name=form.name.data)
            flash(
            "Start recording for {name} minutes until {time_to}.".format(
                name=form.name.data,
                time_to=time_until.strftime('%Y-%m-%d %H:%M:%S')
            )
            )
            flash(
            "Folder name: {folder}".format(
                folder=str(dest_pic)
            )
            )

            # Raspistill call
            os.system("raspistill -t "+str(runtime_mili)+" -tl "+str(intervall)+" -o "+ dest_pic +"image%06d.jpg -q "+ str(quality) +" -w "+ str(width) +" -h "+ str(height) +" >> "+dest_pic+"raspistill.log 2>&1 &")

            # ffmpeg calculation call.
            if ffmpeg:
                os.system("sh /home/pi/timelapse/ffmpeg.sh "+str(dest_pic)+" "+str(time_string)+" "+str(dest_video)+" "+str(runtime_sec)+" >> "+dest_pic+"ffmpeg.log 2>&1 &")

        elif form.preview.data:
            dest_pic, time_string = getpath()

            width = int(form.width.data)
            height = int(form.height.data)
            quality = int(form.quality.data)

            os.system("raspistill -o /media/usbstick/preview/preview.jpg -q "+ str(quality) +" -w "+ str(width) +" -h "+ str(height))
        
        elif form.ending.data:
            flash(
            "Shutting down the Raspberry Pi."
            )
            os.system("sudo halt")

        elif form.reboot.data:
            flash(
            "Shutting down the Raspberry Pi."
            )
            os.system("sudo reboot")    

        return render_template('index.html', form=form)

    if form.errors:
        for error_field, error_message in form.errors.iteritems():
            flash("Field : {field}; error : {error}".format(field=error_field, error=error_message))

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=False)

