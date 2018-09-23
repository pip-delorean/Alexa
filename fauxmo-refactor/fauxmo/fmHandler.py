#!/usr/bin/env python

import requests
import importlib
import RPi.GPIO as GPIO

# This file defines custom handlers to be used with Fauxmo to
# provide various functionality enhancements.

# The fauxmo class expects handlers to be instances of objects
# that have on() and off() methods that return True on success
# and False otherwise.


# This dummy class simply logs the name of the switch with 'ON' or 'OFF'
# for easy debugging during development.
class dummy(object):
    def __init__(self, name):
        self.name = name

    def on(self):
        print(self.name, "ON")
        return True

    def off(self):
        print(self.name, "OFF")
        return True

# This rest class takes two full URLs that should be requested when an on
# and off command are invoked respectively. It ignores any return data.
class rest(object):
    def __init__(self, on_cmd, off_cmd):
        self.on_cmd = on_cmd
        self.off_cmd = off_cmd

    def on(self):
        r = requests.get(self.on_cmd)
        return r.status_code == 200

    def off(self):
        r = requests.get(self.off_cmd)
        return r.status_code == 200

# This file class takes the name of a python script to execute when an
# on or off command is invoked. These scripts could implement any desired
# custom behavior, triggering alerts to your phone, emails, or other
# custom functionality.
class file(object):
    def __init__(self, name):
        self.name = name

    def on(self):
        print(self.name, "ON")
        # execute the script
        module = importlib.import_module(self.name)
        return True

    def off(self):
        print(self.name, "OFF")
        return True

# This gpio class takes a pin number to switch on/off for use with
# a raspberry pi. These pins can control or switch physical devices
# or control anything that you desire to connect to them.
class gpio(object):
    def __init__(self, pin_number):
        self.pin = pin_number
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_number, GPIO.OUT)

    def on(self):
        print(self.pin, "ON")
        GPIO.output(self.pin, 0)
        return True

    def off(self):
        print(self.pin, "OFF")
        GPIO.output(self.pin, 1)
        return True
