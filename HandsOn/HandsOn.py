import math
import string
import time
import serial

## Function to parse the serial data and assign them
## to the appropriate global variables
def parseSerialHandData( line ):
    # Define as global variables in each function that WRITES to them
    global alt, temp, sysCal, gyroCal, accelCal, magCal, \
            indexFingerDeg, indexKnuckleDeg, \
            middleFingerDeg, middleKnuckleDeg, \
            ringFingerDeg, ringKnuckleDeg, \
            pinkieFingerDeg, \
            q0, q1, q2, q3, \
            roll, pitch, yaw, \
            xacc, yacc, zacc
    lineList = line.split()
    if len(lineList) > 1:
        #print(lineList) # Testing Purposes
        if lineList[0] == "Alt:": 
            alt = float(lineList[1])
        elif lineList[0] == "Temp:":
            temp = float(lineList[1])
        #Calibration Values
        elif lineList[0] == "System:":
            sysCal   = int(lineList[1])
            gyroCal  = int(lineList[3])
            accelCal = int(lineList[5])
            magCal   = int(lineList[7])
      
        # Fingers Part 1
        elif lineList[0] == "Index:":
            indexFingerDeg = float(lineList[1])
            middleFingerDeg = float(lineList[3])
            ringFingerDeg = float(lineList[5])
            pinkieFingerDeg = float(lineList[7])

        # Fingers Part 2
        elif lineList[0] == "IndexKnuckle:":
            indexKnuckleDeg = float(lineList[1])
            middleKnuckleDeg = float(lineList[3])
            ringKnuckleDeg = float(lineList[5])

        # Quaternions
        elif lineList[0] == "qW:":
            q0 = float(lineList[1]) + q0off
            q1 = float(lineList[3]) + q1off
            q2 = float(lineList[5]) + q2off
            q3 = float(lineList[7]) + q3off
        
            # Angle calculation from quaternions
            if (!(abs(q1*q2+q0*q3)==0.5)):
                pitch = atan2(2*q2*q0-2*q1*q3,1-2*q2*q2-2*q3*q3)
                yaw = asin(2*q1*q2+2*q3*q0)
                roll = atan2(2*q1*q0-2*q2*q3,1-2*q1*q1-2*q3*q3)
            elif (q1*q2+q0*q3 > 0):        
                pitch = 2*atan2(q1,q0)
                roll = 0.0
            else:
                pitch = -2*atan2(q1,q0)
                roll = 0.0     

        #Linear Acceleration
        elif lineList[0] == "aX:":
            xacc = float(lineList[1])
            yacc = float(lineList[3])
            zacc = float(lineList[5])
 ## Parsing serial hand data function end

def main():
    print('    Teensy Serial Read Starting ')
    ser = serial.Serial('COM3', 9600, timeout=5) #Open serial port
    print('    Waiting 5 seconds to establish connection to Teensy...')
    time.sleep(5) # Sleep for 5 seconds while teensy to sets up
    print('Serial Name: ', ser.name)
    print('\n')
    print('Serial Read: ')
    line = ser.readline #Read line until \n
    print(line) 
    parseSerialHandData(line)    

    ser.close()
## main() end

if __name__ == "__main__":
    main()