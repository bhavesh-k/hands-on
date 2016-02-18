import math
import string
import time
import serial
import statistics
import collections

import share_var

#global pitch, yaw, roll

def QuatToEuler(q0, q1, q2, q3):
    ## Euler Angle calculation from quaternions
    if (abs(q1*q2+q0*q3)!=0.5):
        pitch = math.atan2(2*q2*q0-2*q1*q3,1-2*q2*q2-2*q3*q3)
        yaw = math.asin(2*q1*q2+2*q3*q0)
        roll = math.atan2(2*q1*q0-2*q2*q3,1-2*q1*q1-2*q3*q3)
    elif (self.q1*q2+q0*q3 > 0):
        pitch = 2*math.atan2(q1,q0)
        roll = 0.0
    else:
        pitch = -2*math.atan2(q1,q0)
        roll = 0.0
    return([roll, pitch, yaw])
## end of QuatToEuler(...)

def UpdateFlexCollectData():
    ## Updates the collection of flex sensor data
    share_var.indexFingerDegCollect.append(share_var.indexFingerDeg)
    share_var.indexKnuckleDegCollect.append(share_var.indexKnuckleDeg)
    share_var.middleFingerDegCollect.append(share_var.middleFingerDeg)
    share_var.middleKnuckleDegCollect.append(share_var.middleKnuckleDeg)
    share_var.ringFingerDegCollect.append(share_var.ringFingerDeg)
    share_var.ringKnuckleDegCollect.append(share_var.ringKnuckleDeg)
    share_var.pinkieFingerDegCollect.append(share_var.pinkieFingerDeg)
    share_var.thumbDegCollect.append(share_var.thumbDeg)
## end of UpdateFlexCollectData

def FlexDataList():
    # Returns the current flex sensor values in the form of a list
    return( [ share_var.indexFingerDeg, share_var.indexKnuckleDeg, share_var.middleFingerDeg, \
                share_var.middleKnuckleDeg, share_var.ringFingerDeg, share_var.ringKnuckleDeg, \
                share_var.pinkieFingerDeg, share_var.thumbDeg ] )
## end of FlexDataList()

def FlexDataStr():
    # Returns the current Flex Sensor values in the form of a string separated by ","s
    tmpList = [ share_var.indexFingerDeg, share_var.indexKnuckleDeg, share_var.middleFingerDeg, \
                    share_var.middleKnuckleDeg, share_var.ringFingerDeg, share_var.ringKnuckleDeg, \
                    share_var.pinkieFingerDeg, share_var.thumbDeg ]
    return( ','.join(repr(e) for e in tmpList) )
## end of FlexDataStr()
    
def QuatDataStr():
    ## Returns the current Quaternion Data values in the form of a string separated by ","s
    tmpList = [ share_var.q0, share_var.q1, share_var.q2, share_var.q3 ] 
    return( ','.join(repr(e) for e in tmpList) )
## end of QuatDataStr()

def EulerDataStr():
    ## Returns the current Euler Data values in the form of a string separated by ","s
    tmpList = [ share_var.roll, share_var.pitch, share_var.yaw] 
    return( ','.join(repr(e) for e in tmpList) )
## end of EulerDataStr()

def LinAccelDataStr():
    ## Returns the current Linear Acceleration values in the form of a string separated by ","s
    tmpList = [ share_var.xAcc, share_var.yAcc, share_var.zAcc ] 
    return( ','.join(repr(e) for e in tmpList) )
## end of LinAccelDataStr()

## printHandDataToFile
# Inputs a letter/number/gesture identifying the hand animation being performed  
# Writes the identifier with the corresponding hand data to a file
def printHandDataToFile(str_handIdentifier):
    outFile = open("classification.txt",'a')
    # Obtain hand data as strings separated by "," so that we can write to file
    strHandDataOut = str_handIdentifier + "," + FlexDataStr() + "," + QuatDataStr() + "," + EulerDataStr() + "," + LinAccelDataStr()
    outFile.write(strHandDataOut)
    outFile.write('\n')
    outFile.close  
## end of printHandDataToFile

    # IGNORE THIS STUFF FOR NOW
        #printHandDataToFile('test', handInst)
        #enableWriteHandData = input("Would you like to write the hand data for a gesture to a file? (Y/N): ")
        #if (enableWriteHandData.upper() == "Y"):
        #    gestureID = input("Enter the identifier for the hand letter/number/gesture: ") # Ask for gesture identifier
        #    # Write all hand data to formatted file or average of all collected? or average of all flex sensors + all movement data
        #    printHandDataToFile(gestureID, handInst)


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

            # Update the collection of flex sensor data
            UpdateFlexCollectData()
            
            # Quaternions
            elif lineList[0] == "qW:":
                q0 = share_var.q0 = float(lineList[1])
                q1 = share_var.q1 = float(lineList[3])
                q2 = share_var.q2 = float(lineList[5])
                q3 = share_var.q3 = float(lineList[7])
                # Angle calculation from quaternions
##                if (abs(q1*q2+q0*q3)!=0.5):
##                    share_var.pitch = math.atan2(2*q2*q0-2*q1*q3,1-2*q2*q2-2*q3*q3)
##                    share_var.yaw = math.asin(2*q1*q2+2*q3*q0)
##                    share_var.roll = math.atan2(2*q1*q0-2*q2*q3,1-2*q1*q1-2*q3*q3)
##                elif (q1*q2+q0*q3 > 0):
##                    share_var.pitch = 2*math.atan2(q1,q0)
##                    share_var.roll = 0.0
##                else:
##                    share_var.pitch = -2*math.atan2(q1,q0)
##                    share_var.roll = 0.0
                [r,p,y] = QuatToEuler(share_var.q0,share_var.q1,share_var.q2,share_var.q3)
                share_var.pitch = -math.degrees(p)
                share_var.roll = -math.degrees(r)
                share_var.yaw = math.degrees(y)
    
            #Linear Acceleration
            elif lineList[0] == "aX:":
                share_var.xAcc = float(lineList[1])
                share_var.yAcc = float(lineList[3])
                share_var.zAcc = float(lineList[5])
## end of parseSerialHandData
