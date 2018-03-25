# Autor:   Ingmar Stapel
# Datum:   20170521
# Version:   1.0
# Homepage:   https://www.byteyourlife.com/
# program to create timelapse videos with a Raspberry Pi 

from flask import Flask, render_template, flash
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os
#import errno
import time
import subprocess

# intervall is the time between each picture in seconds
intervall = 1
intervall *= 1000

# print messages
debug = True

dest_pic = ""
time_string = ""
output_ffmpeg = ""
output_raspistill = ""
# mount usb drive as usual
os.system("sudo mount -t exfat -o utf8,uid=pi,gid=pi,noatime /dev/sda1 /media/usbstick >> /home/pi/mount.log 2>&1 &")
time.sleep(4)

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
    dest_pic = "/media/usbstick/pictures_"+time_string+"/"
    return dest_pic, time_string

app = Flask(__name__, static_folder='/media/usbstick/preview',)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'well-secret-password'


class MyForm(Form):
    name = StringField(label='Timelapse duration (minutes)', validators=[DataRequired()], default="15")
    intervall = StringField(label='Picture intervall (seconds)', validators=[DataRequired()], default="1")
    #name = StringField(label='Time in minutes', [validators.Required("15")])
    starting = SubmitField(label='Start recording')
    preview  = SubmitField(label='Preview picture')
    reboot   = SubmitField(label='Raspberry reboot')
    ending   = SubmitField(label='Raspberry shutdown')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()

    if form.validate_on_submit():
        if form.starting.data:
            runtime_min = int(form.name.data)
            runtime_sec = runtime_min * 60 + 30
            runtime_mili = runtime_min * 60000
            intervall = int(form.intervall.data)
            intervall *= 1000

            dest_pic, time_string = getpath()

            # create path
            create_path(dest_pic)
            
            # print "Value : {name}".format(name=form.name.data)
            flash(
            "Start recording for {name} Minutes. Folder name: {folder}".format(
                name=form.name.data,
                folder=str(dest_pic)
            )
            )

            os.system("raspistill -t "+str(runtime_mili)+" -tl "+str(intervall)+" -o "+ dest_pic +"image%06d.jpg -w 1920 -h 1080 >> "+dest_pic+"raspistill.log 2>&1 &")
            os.system("sh /home/pi/flask_test/ffmpeg.sh "+str(dest_pic)+" "+str(time_string)+" "+str(runtime_sec)+" >> "+dest_pic+"ffmpeg.log 2>&1 &")

        elif form.preview.data:
            dest_pic, time_string = getpath()

            # create path
            create_path(dest_pic)
            flash(
            "Creating preview image preview.jpg"
            )
            
            os.system("raspistill -o /media/usbstick/preview/preview.jpg -w 480 -h 270")
        
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

