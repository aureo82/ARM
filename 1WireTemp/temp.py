
# temp.py
# script to read temp from a 1 Wire sensor on the AriaG25
#
# Oriol Sanchez, 2013/10/31
# 
# Changelog:
# V0 2013/10/31
# 
# Readme: The sensor used was a MAX31820 instead of the DS18B20
#         adlib from acme boards library that defines the 1 wire
#         bus within the embedded linux system didn't make any 
#         difference bewteen both sensors.
# Instructions: - execute phyton temp.py from the shell inside the arm
#


#!/usr/bin/env python

import ablib as a
#from ablib import w1buslist #1 Wire library
import time as t #time library

#Define a new class called 1WDevice()
class OneWDevice():
        def id(self):
                #ID THE 1WIRE DEVICE
                print "Scan for the available thermal sensors"
                #print device
                for device in a.w1buslist():   #REMEMBER THAT THE
LIBRARY IS ACCESED THROUGH "a" IN THIS CASE
                 print "Sensor ID = " + device
        def getValue(self):
                #RETRIEVE DATA FROM THE I2C DEVICE
                sensor = a.DS18B20("00000559a8e0")
                data=(sensor.getTemp())
                print "Temp=%.2f Celsius" % data
                t.sleep(0.2)

#Main script
#Create and I2CDevice object called chip
chip = OneWDevice()
#Run the configuration of the device
chip.id()
#Retrieve the information from the device
while 1:
        value=chip.getValue()


