import math
import string
import time
import serial

import share_var

#global pitch, yaw, roll

## Function to parse the serial data and assign them
## to the appropriate global variables
# class serialThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.daemon = True
#         ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5) #Open serial port
#         self.start()
        
def parseSerialHandData(ser):
        
    while True: 
        line = ser.readline() #Read line until \n 
        print line      
        lineList = line.split()
        if len(lineList) > 1:
            #print(lineList) # Testing Purposes
            if lineList[0] == "Alt:":
                share_var.alt = float(lineList[1])
            elif lineList[0] == "Temp:":
                share_var.temp = float(lineList[1])
            #Calibration Values
            elif lineList[0] == "System:":
                share_var.sysCal   = int(lineList[1])
                share_var.gyroCal  = int(lineList[3])
                share_var.accelCal = int(lineList[5])
                share_var.magCal   = int(lineList[7])
    
            # Fingers Part 1
            elif lineList[0] == "Index:":
                share_var.indexFingerDeg = float(lineList[1])
                share_var.middleFingerDeg = float(lineList[3])
                share_var.ringFingerDeg = float(lineList[5])
                share_var.pinkieFingerDeg = float(lineList[7])
    
            # Fingers Part 2
            elif lineList[0] == "IndexKnuckle:":
                share_var.indexKnuckleDeg = float(lineList[1])
                share_var.middleKnuckleDeg = float(lineList[3])
                share_var.ringKnuckleDeg = float(lineList[5])
    
            # Quaternions
            elif lineList[0] == "qW:":
                q0 = share_var.q0 = float(lineList[1])
                q1 = share_var.q1 = float(lineList[3])
                q2 = share_var.q2 = float(lineList[5])
                q3 = share_var.q3 = float(lineList[7])
    
                # Angle calculation from quaternions
                if (abs(q1*q2+q0*q3)!=0.5):
                    share_var.pitch = math.atan2(2*q2*q0-2*q1*q3,1-2*q2*q2-2*q3*q3)
                    share_var.yaw = math.asin(2*q1*q2+2*q3*q0)
                    share_var.roll = math.atan2(2*q1*q0-2*q2*q3,1-2*q1*q1-2*q3*q3)
                elif (q1*q2+q0*q3 > 0):
                    share_var.pitch = 2*math.atan2(q1,q0)
                    share_var.roll = 0.0
                else:
                    share_var.pitch = -2*math.atan2(q1,q0)
                    share_var.roll = 0.0
                
                share_var.pitch = -math.degrees(share_var.pitch)
                share_var.roll = -math.degrees(share_var.roll)
                share_var.yaw = math.degrees(share_var.yaw)
    
            #Linear Acceleration
            elif lineList[0] == "aX:":
                share_var.xacc = float(lineList[1])
                share_var.yacc = float(lineList[3])
                share_var.zacc = float(lineList[5])
                
     ## Parsing serial hand data function end