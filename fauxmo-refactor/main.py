#!/usr/bin/env python

from fauxmo import *
import sys
import time

# See README.md file for explanation and overview of functionality.

# uncomment RPi imports if you are launching or using on a raspberry pi.
# references will need to be uncommented here (line 9 & 70) as well
# as in the Handler.py file (import and gpio class definition).
import RPi.GPIO as GPIO


# NOTE: As of 2015-08-17, the Echo appears to have a hard-coded limit of
# 16 switches it can control. Only the first 16 elements of the FAUXMOS
# list will be used.


# Provide a list of virtual 'devices' you want to provide control for by
# defining a FAUXMOS array of handlers. Use any handler class defined in the
# Handler.py file or define your own.
#
# Each item in the array is a list with the following elements:
# 	- index 0 - name of the virtual switch or device
# 	- index 1 - object with 'on' and 'off' methods
# 	- index 2 - port # (optional; may be omitted)


# Array of virtual devices that will be visible on the network. 
FAUXMOS = [

# Rest devices, defined urls will be called when on/off actions are triggered.
#     ['office lights', Handler.rest('http://192.168.5.4/ha-api?cmd=on&a=office', 'http://192.168.5.4/ha-api?cmd=off&a=office')],
#     ['kitchen lights', Handler.rest('http://192.168.5.4/ha-api?cmd=on&a=kitchen', 'http://192.168.5.4/ha-api?cmd=off&a=kitchen')],

# Dummy devices that simply log to the console when called.
        ['office lights', fmHandler.dummy("officelight"), 52581],
        ['kitchen lights', fmHandler.dummy("kitchenlight"), 52582],

# Run script devices, when called the script specified will be executed when device is turned 'ON'.
# Script should be a python file, 'file' handler expects the name of a script, it should be located
# in the same directory as the 'main.py' file.
# When you say "Alexa, turn on Twitter Trends", the 'fetch_news.py' script will be executed and send
# an email to the address you specify in the cred.json file.
#        ['twitter trends', fmHandler.file('fetch_news'), 52583]

# Raspberry pi GPIO devices. For office lights gpio pin 35 will be turned on/off... etc.
#         ['office lights', Handler.gpio(35)],
#         ['kitchen lights', Handler.gpio(37)],
    ]

# if you run this script with the -d flag, then enable logging for verbosity.
if len(sys.argv) > 1 and sys.argv[1] == '-d':
    fmUtilities.DEBUG = True

# Set up our singleton for polling the sockets for data ready
p = fmPoller.poller()

# Set up our singleton listener for UPnP broadcasts
u = fmResponder.upnp_broadcast_responder()
u.init_socket()

# Add the UPnP broadcast listener to the poller so we can respond
# when a broadcast is received.
p.add(u)

# Create our FauxMo virtual switch devices
for item in FAUXMOS:
    if len(item) == 2:
        # a fixed port wasn't specified, use a dynamic one
        item.append(0)
    switch = fauxmo.fauxmo(item[0], u, p, None, item[2], action_handler = item[1])

# log if enabled
fmUtilities.dbg("Entering main loop\n")

while True:
    try:
        # Allow time for a ctrl-c to stop the process
        p.poll(100)
        time.sleep(0.1)
    except Exception, e:
        GPIO.cleanup()
        fmUtilities.dbg(e)
        break

