
# light.py
# script to read luxes from an I2C sensor on a linux embedded system
#
# Oriol Sanchez, 2013/10/31
# 
# Changelog:
# V0 2013/10/31
# 
# Readme: The sensor used was a BH1750FVI 
# Instructions: - execute phyton light.py from the shell inside the arm
#


#!/usr/bin/python
import smbus    #I2C library
import time as t #time library
addr=0x23    #I2C address, for instance 68 hex
#Define a new class called I2CDevice()
class I2CDevice():
        #Select the I2C device on /dev/i2c-0
        b=smbus.SMBus(0)
        def config(self):
                #CONFIG THE I2C DEVICE
                self.b.write_byte(addr,0x11) #Set resolution 0.5lx at 120ms
                #.... until ending device configuration
        def getValue(self):
               #RETRIEVE DATA FROM THE I2C DEVICE
                data = self.b.read_i2c_block_data(addr,0x11)

                print "Luminosity %.1f luxes" % ((data[1] + (256 *
data[0])) / 1.2)
                #print "Luminosity " + str((data[1] + (256 * data[0]))
/ 1.2) + " luxes"
                t.sleep(0.5)

#Main script
#Create and I2CDevice object called chip
chip = I2CDevice()
#Run the configuration of the device
chip.config()
#Retrieve the information from the device
while 1:
        value=chip.getValue()