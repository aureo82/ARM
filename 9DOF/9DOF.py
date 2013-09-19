#9DOF.py
# script to adquire data from a I2C 9DOF
#
# Oriol Sanchez, 9/19/2013
# 
# Changelog:
# V0 9/17/2013
# 
# Readme:
# 
# Instructions: - execute phyton 9DOF.py from the shell inside the arm
#               - visualize the data in the shell or retreive it after
#				- from the txt file created by the script
#

import smbus                          #I2C library
import time                           #Time library
import datetime                       #Timestamp library
import ctypes                         #Conversion Type library
import os

addr=0x68
maddr=0x0C
#Define a new class called Accel
class Accel():
        #Select the I2C device on /dev/i2c-0
        b=smbus.SMBus(0)
        def config(self):
                #SET Internal clock to work as z axis gyro as a reference with a phase loop lock
                self.b.write_byte_data(0x68,0x6B,0x03)
        #CONFIG THE SYSTEM
        #REGISTER 19, SAMPLE RATE
                self.b.write_byte_data(addr,0x19,0x07)
        #CONFIG REGISTER on 0x1A, data: [ExtSync][DLPF] : 0x010
                self.b.write_byte_data(addr,0x1A,0x00)
        #CONFIG GYRO on 0x1B, test disabled and scale selected 500 degrees/s
                self.b.write_byte_data(addr,0x1B,0x08)
        #CONFIG ACCEL on 0x1C, test disabled and scale +-2g without DHPF
                self.b.write_byte_data(addr,0x1C,0x00)
                #CONFIG Freefall threshold of 0mg
                #self.b.write_byte_data(addr,0x1D,0x00)
                #CONFIG Freefall duration limit of 0
                #self.b.write_byte_data(addr,0x1E,0x00)
                #CONFIG Motion threshold of 0mg
                #self.b.write_byte_data(addr,0x1F,0x00)
                #CONFIG Motion duration limit of 0
                #self.b.write_byte_data(addr,0x20,0x00)
                #CONFIG Zero Motion threshold
                #self.b.write_byte_data(addr,0x21,0x00)
                #CONFIG Zero Motion duration limit
                #self.b.write_byte_data(addr,0x22,0x00)
                #DISABLE Sensor output to FIFO buffer
                #self.b.write_byte_data(addr,0x23,0x00)
                #AUX I2C SETUP
                #self.b.write_byte_data(addr,0x24,0x00)
                #I2C SLAVES SETUP       
                #SLAVE0
                self.b.write_byte_data(addr,0x25,0x00)
                self.b.write_byte_data(addr,0x26,0x00)
                self.b.write_byte_data(addr,0x27,0x00)
                #SLAVE1
                self.b.write_byte_data(addr,0x28,0x00)
                self.b.write_byte_data(addr,0x29,0x00)
                self.b.write_byte_data(addr,0x2A,0x00)
                #SLAVE2
                self.b.write_byte_data(addr,0x2B,0x00)
                self.b.write_byte_data(addr,0x2C,0x00)
                self.b.write_byte_data(addr,0x2D,0x00)
                #SLAVE3
                self.b.write_byte_data(addr,0x2E,0x00)
                self.b.write_byte_data(addr,0x2F,0x00)
				self.b.write_byte_data(addr,0x30,0x00)
                #SLAVE4
                self.b.write_byte_data(addr,0x31,0x00)
                self.b.write_byte_data(addr,0x32,0x00)
                self.b.write_byte_data(addr,0x33,0x00)
                self.b.write_byte_data(addr,0x34,0x00)
                self.b.write_byte_data(addr,0x35,0x00)
                #INT pin
                self.b.write_byte_data(addr,0x37,0x00)
                #DATA Interrupt
                self.b.write_byte_data(addr,0x38,0x00)

                #SLAVE Out, don't care
                self.b.write_byte_data(addr,0x63,0x00)
                self.b.write_byte_data(addr,0x64,0x00)
                self.b.write_byte_data(addr,0x65,0x00)
                self.b.write_byte_data(addr,0x66,0x00)
                time.sleep(0.002)
                return 1

        def getGValue(self):
                gxh = self.b.read_byte_data(addr,0x43) #GyroxH
                gxl = self.b.read_byte_data(addr,0x44) #GyroxL
                #print gxh
                #print gxl
                gx = ((gxh << 8) | gxl)
                gyh = self.b.read_byte_data(addr,0x45) #GyroyH
                gyl = self.b.read_byte_data(addr,0x46) #GyroyL
                gy = ((gyh << 8) | gyl)
                gzh = self.b.read_byte_data(addr,0x47) #GyrozH
                gzl = self.b.read_byte_data(addr,0x48) #GyrozL
                gz = ((gzh << 8) | gzl)
                if gx>32767:
                        gx=(gx-65535)
                if gy>32767:
                        gy=(gy-65535)
                if gz>32767:
                        gz=(gz-65535)
                gx=float((gx*500)/32767)
                gy=float((gy*500)/32767)
                gz=float((gz*500)/32767)
                return (gx,gy,gz)


		
		
		def getAValue(self):
                axh = self.b.read_byte_data(addr,0x3B) #AccelH
                axl = self.b.read_byte_data(addr,0x3C) #AccelL
                #print axh
                #print axl
                ax = float((axh << 8) | axl)
                ayh = self.b.read_byte_data(addr,0x3D) #AccelH
                ayl = self.b.read_byte_data(addr,0x3E) #AccelL
                ay = float((ayh << 8) | ayl)
                azh = self.b.read_byte_data(addr,0x3F) #AccelH
                azl = self.b.read_byte_data(addr,0x40) #AccelL
                az = float((azh << 8) | azl)
                if ax>32767:
                        ax=(ax-65535)
                if ay>32767:
                        ay=(ay-65535)
                if az>32767:
                        az=(az-65535)
                ax=(ax*2)/32767
                ay=(ay*2)/32767
                az=(az*2)/32767
                return (ax,ay,az)


        def getMValue(self):

                #BYPASS MAIN I2C to Aux I2C
                self.b.write_byte_data(addr,0x37,0x02)
                #CONTROL BYTE set to single measurement mode
                self.b.write_byte_data(maddr,0x0A,0x01)
                time.sleep(0.01)
                mxh = self.b.read_byte_data(maddr,0x04) #XMagneH
                mxl = self.b.read_byte_data(maddr,0x03) #XMagneL
                myh = self.b.read_byte_data(maddr,0x06) #YMagneH
                myl = self.b.read_byte_data(maddr,0x05) #YMagneL
                mzh = self.b.read_byte_data(maddr,0x08) #ZMagneH
                mzl = self.b.read_byte_data(maddr,0x07) #ZMagneL
                #CONFIG System to acces the Fuse ROM, to get the sensitivity adjustment
#                self.b.write_byte_data(maddr,0x0A,0x0F)
#               asax= self.b.read_byte_data(maddr,0x10) #Sensitivity Adjustment
#               asay= self.b.read_byte_data(maddr,0x11) #Sensitivity Adjustment         
#               asaz= self.b.read_byte_data(maddr,0x12) #Sensitivity Adjustment
#               print asax
#               print asay
#               print asaz
                #CONFIG System again in Single measurement mode
#                self.b.write_byte_data(maddr,0x0A,0x01)
                #UNDO THE BYPASS OF  MAIN I2C to Aux I2C
#                self.b.write_byte_data(addr,0x37,0x00)
                #BUILD the 16bit data and adjust it throught the sensitivity as stated in the manual
                mx = float((mxh << 8) | mxl)
                my = float((myh << 8) | myl)
                mz = float((mzh << 8) | mzl)
				if mx>32767:
                        mx=(mx-65535)
                if my>32767:
                        my=(my-65535)
                if mz>32767:
                        mz=(mz-65535)
                mx=mx*.3
                my=my*.3
                mz=mz*.3
                return (mx,my,mz)

        def getTValue(self):

                temph = self.b.read_byte_data(addr,0x41) #TempH
                templ = self.b.read_byte_data(addr,0x42) #TempL
                temp = ((temph << 8) | templ)
                if temp>32767:
                        temp=(temp-65535)
                temp = ((float(temp)/340) +35)
                return(temp)
 
#create an accel object called mpu9150
#mpu9150 = Accel()
mpu9150=Accel()
mpu9150.config()
i=0

(gx,gy,gz)=mpu9150.getGValue()
(ax,ay,az)=mpu9150.getAValue()
(mx,my,mz)=mpu9150.getMValue()
gx3=gx2=gx1=pitch=0
gy3=gy2=gy1=roll=0
gz3=gz2=gz1=yaw=0


while 1:
       i=i+1
       #Update integration values
       gx3=gx2
       gx2=gx1
       gx1=gx
       gy3=gy2
       gy2=gy1
       gy1=gy
       gz3=gz2
       gz2=gz1
       gz1=gz
       (gx,gy,gz)=mpu9150.getGValue()
       (ax,ay,az)=mpu9150.getAValue()
       (mx,my,mz)=mpu9150.getMValue()
       tmp=mpu9150.getTValue()
       #Integrate form the angular velocity with a runge-kutta algorithm
       pitch=pitch+(gx3+(gx2*2)+(gx1*2)+gx)/6
       roll=roll+(gy3+(gy2*2)+(gy1*2)+gy)/6
       yaw=yaw+(gz3+(gz2*2)+(gz1*2)+gz)/6

	if i==1:
                i=0
                os.system('clear')
                #filename = raw_input("Give name for the file: ")
                filename="testdata.txt"
                target = open (filename, 'a') ## a will append, w will over-write
                ts=time.time()
                st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                print st
				print "Pitch: %d degrees" % (pitch)
                print "Roll: %d degrees" % (roll)
                print "Yaw: %d degrees" % (yaw)
                print "Gyroscope X:%d" % (gx)
                print "Gyroscope Y:%d" % (gy)
                print "Gyroscope Z:%d" % (gz)
                print "Accelerometer X:%d" % (ax)
                print "Accelerometer Y:%d" % (ay)
                print "Accelerometer Z:%d" % (az)
                print "Magnetometer X:%d" % (mx)
                print "Magnetometer Y:%d" % (my)
                print "Magnetometer Z:%d" % (mz)

                target.write(st)
                target.write(",")
                target.write(str(gx))
                target.write(",")
                target.write(str(gy))
                target.write(",")
                target.write(str(gz))
                target.write(",")
                target.write(str(ax))
                target.write(",")
                target.write(str(ay))
                target.write(",")
                target.write(str(az))
                target.write(",")
                target.write(str(mx))
                target.write(",")
                target.write(str(my))
                target.write(",")
                target.write(str(mz))
                target.write(",")
				target.write(str(tmp))
                target.write("\n")
                target.close()
       time.sleep(1)





