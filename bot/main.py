#!/usr/bin/python
# -*- coding:utf-8 -*-
import time

from bottle import get, post, run, route, request, template, static_file
from bot.bot import AlphaBot
from bot.bot import Infrared
from bot.bot import PCA9685
import threading

Ab = AlphaBot()
infra = Infrared()
pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

forward = False

# Set the Horizontal servo parameters
HPulse = 1500  # Sets the initial Pulse
HStep = 0  # Sets the initial step length
pwm.setServoPulse(0, HPulse)

# Set the vertical servo parameters
VPulse = 1500  # Sets the initial Pulse
VStep = 0  # Sets the initial step length
pwm.setServoPulse(1, VPulse)


@get("/")
def index():
    return template("index")


@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./')


@route('/fonts/<filename>')
def server_fonts(filename):
    return static_file(filename, root='./fonts/')


@post("/cmd")
def cmd():
    global HStep, VStep, forward
    code = request.body.read().decode()
    speed = request.POST.get('speed')
    side = request.POST.get('side')
    print(code)
    if side == 'left':
        Ab.setPWMB(float(speed))
        print(speed)
    if side == 'right':
        Ab.setPWMA(float(speed))
        print(speed)
    if code == "stop":
        HStep = 0
        VStep = 0
        Ab.stop()
        forward = False
    elif code == "forward":
        Ab.forward()
        forward = True
    elif code == "backward":
        Ab.backward()
    elif code == "turnleft":
        Ab.left()
    elif code == "turnright":
        Ab.right()
    elif code == "up":
        VStep = -5
    elif code == "down":
        VStep = 5
    elif code == "left":
        HStep = 5
    elif code == "right":
        HStep = -5
    return "OK"


def timerfunc():
    global HPulse, VPulse, HStep, VStep, pwm, forward

    if HStep != 0:
        HPulse += HStep
        if HPulse >= 2500:
            HPulse = 2500
        if HPulse <= 500:
            HPulse = 500
        # set channel 2, the Horizontal servo
        pwm.setServoPulse(0, HPulse)

    if VStep != 0:
        VPulse += VStep
        if VPulse >= 2500:
            VPulse = 2500
        if VPulse <= 500:
            VPulse = 500
        # set channel 3, the vertical servo
        pwm.setServoPulse(1, VPulse)

    if forward:
        if infra.getLeft() == 0:
            Ab.right()
            time.sleep(0.002)
            Ab.forward()

        if infra.getRight() == 0:
            Ab.left()
            time.sleep(0.002)
            Ab.forward()

    global t  # Notice: use global variable!
    t = threading.Timer(0.02, timerfunc)
    t.start()


t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()

run(host="0.0.0.0", port="8001")
