
# cam.py
# script to take photos from the linksprite LS-Y201 camera
#
# Oriol Sanchez, 9/19/2013
# 
# Changelog:
# V0 9/19/2013
# 
# Readme:
# Freely based on the code linksprite_grab.py of Jon Klein (kleinjt@ieee.org)
# It takes a photo and stores it inside an embedded ARM board,
# in this case the Fox_Board from Acme Systems. Take into account that a relay
# was used to interface the camera with the embedded system, that is why 
# GPIO is used.
#
# Instructions: - execute phyton cam.py from the shell inside the arm
#               - retrieve the picture from the test folder
#
# Advice: my LS-Y201 camera didn't work correctly outdoors, maybe it is only my cam
# or it is all the cams as the linksprite LS-Y201 cam seems to be a PUTAL PTC08 cam
# from china as their control messages seems to be the same and so its specs. Anyway
# light exposure seem to be too long to withstand sunny day conditions.

import serial                         #Serial library, required to comunicate with the cam
import time                           #Time library
import datetime                       #Timestamp library
import ctypes                         #Conversion Type library
import fox                            #Fox board library, needed for the GPIO ports
import os


#Define an array of hex strings
def a2s(arr):
        return ''.join(chr(b) for b in arr)

#Define Camera Messages, send and answer
#Reset
CAM_RST                 = a2s([0x56, 0x00, 0x26, 0x00])
CAM_RST_RET             = a2s([0x76, 0x00, 0x26, 0x00, 0x00])#Additional 0x00 not specified in the instructions
#Take picture
CAM_GO                  = a2s([0x56, 0x00, 0x36, 0x01, 0x00])
CAM_GO_RET              = a2s([0x76, 0x00, 0x36, 0x00, 0x00])
#Read Jpeg file size
CAM_SIZE                = a2s([0x56, 0x00, 0x34, 0x01, 0x00])
CAM_SIZE_RET            = a2s([0x76, 0x00, 0x34, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00]) # then XH XL (filesize MSB , LSB)
#Read Jpeg
CAM_READ                = [0x56, 0x00, 0x32, 0x0C, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]; �
CAM_INT_TIME            = [0x00, 0x0A] # .1 ms, as stated in the manual
CAM_READ_RET            = a2s([0x76, 0x00, 0x32, 0x00, 0x00])
#After receiving the READ_Ret the JPEG image will be contained between the File_start and the File_end
FILE_START              = a2s([0xFF, 0xD8])
FILE_END                = a2s([0xFF, 0xD9])
#Stop taking pictures
CAM_STOP                = a2s([0x56, 0x00, 0x36, 0x01, 0x03])
CAM_STOP_RET            = a2s([0x76, 0x00, 0x36, 0x00, 0x00])


#Define the serial comunication
def init_serial():
        return serial.Serial(
        port='/dev/ttyS2',
        baudrate=38400,
        timeout=1,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
#All the orders to the cam require a serial port, therefore the functions are defined with it as an input
#Define Cam Reset Procedure
def cam_reset(s):
        s.flushInput()
        s.write(CAM_RST)
        read = s.read(len(CAM_RST_RET)) #Read as much bytes as are inside the CAM_RST_RET
        if(read != CAM_RST_RET): #Compare the answer to the expected message
                print "Failed to reset the camera"
        time.sleep(.5)
#Define Order to take a Photo
def cam_shoot(s):
        s.flushInput()
        s.write(CAM_GO)
        read = s.read(len(CAM_GO_RET))
        if(read != CAM_GO_RET):
                print "Failed to shoot a photo"
        time.sleep(.1)

#Check File size
def cam_psize(s):
        s.flushInput()
        s.write(CAM_SIZE)
        read = s.read(len(CAM_SIZE_RET))
        return [ord(read[-2]),ord(read[-1])]

#Define Order to retrieve a Photo
def cam_rfile(s,size):
        s.flushInput()
        s.write(a2s(CAM_READ + size + CAM_INT_TIME))
        read=s.read(len(CAM_READ_RET))
        if(read != CAM_READ_RET):
                print "Failed to read photo"
        #Read two words
        photo=s.read(2)
        if(photo != FILE_START):
                print "Photo seems to be corrupted"
        #If head is ok, keep reading until you reach the end
        while (photo[-2:] != FILE_END):
                photo=photo+s.read(2);
        #Return the data into
        return photo

		
#Main script


#Main script
def main():
        #Enable Cam Relay with a GPIO pin of the FoxBoard
        camen = fox.Pin('J6.26','high')
        camen.on()
        time.sleep(1)
        #Init the serial port
        ser=init_serial()
        #Reset the camera
        cam_reset(ser)
        #Shoot a picture
        cam_shoot(ser)
        #Check the filesize     
        size=cam_psize(ser)
        #Retrieve the data
        photo=cam_rfile(ser,size)
        ts=time.time()
        st=datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H_%M_%S')
        print st
        #Create a file
        if os.path.exists("/home/cam_out") == False:
                os.mkdir("/home/cam_out")
        filename= '/home/cam_out/' + st +'.jpg'
        print filename
        filename = open(filename,'wb')
        filename.write(photo)
        filename.close()
        #Turn off Serial and Camera Relay
        ser.close()
        camen.off()


if __name__ == "__main__":
    main()



