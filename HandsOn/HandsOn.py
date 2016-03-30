"""
HandsOn
Authors: Bhavit Patel, Bhavesh Kakwani, Tom Yang
Date Created: January 2016
Version 1

Contains multiple modules and functions for processing data from serial output
Also contains pseudoMain() which is a console application to save gesture data to file,
train SVM from data in a file, and classify gestures in real time (also with text-to-speech output).
"""
import math
import string
import time
import serial
import share_var
import numpy as np
from sklearn import svm
import pyttsx


def QuatToEuler(q0, q1, q2, q3):
    """ Euler Angle calculation from quaternions """
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

def UpdateDequeData():
    """ Updates the collections.deque of all hand data (flex sensor, touch sensors, quaternion, euler angles, lin accel """
    # Flex Sensors
    share_var.indexFingerDegCollect.append(share_var.indexFingerDeg)
    share_var.indexKnuckleDegCollect.append(share_var.indexKnuckleDeg)
    share_var.middleFingerDegCollect.append(share_var.middleFingerDeg)
    share_var.middleKnuckleDegCollect.append(share_var.middleKnuckleDeg)
    share_var.ringFingerDegCollect.append(share_var.ringFingerDeg)
    share_var.ringKnuckleDegCollect.append(share_var.ringKnuckleDeg)
    share_var.pinkieFingerDegCollect.append(share_var.pinkieFingerDeg)
    share_var.thumbDegCollect.append(share_var.thumbDeg)
    share_var.thumbKnuckleDegCollect.append(share_var.thumbKnuckleDeg)
    # Touch Sensors
    share_var.touch1Collect.append(share_var.touch1)
    share_var.touch2Collect.append(share_var.touch2)
    share_var.touch3Collect.append(share_var.touch3)
    share_var.touch4Collect.append(share_var.touch4)
    share_var.touch5Collect.append(share_var.touch5)
    share_var.touch6Collect.append(share_var.touch6)
    share_var.touch7Collect.append(share_var.touch7)
    # Quaternions
    share_var.q0Collect.append(share_var.q0)
    share_var.q1Collect.append(share_var.q1)
    share_var.q2Collect.append(share_var.q2)
    share_var.q3Collect.append(share_var.q3)
    # Euler Angles
    share_var.rollCollect.append(share_var.roll)
    share_var.pitchCollect.append(share_var.pitch)
    share_var.yawCollect.append(share_var.yaw)
    # Linear Acceleration
    share_var.xAccCollect.append(share_var.xAcc)
    share_var.yAccCollect.append(share_var.yAcc)
    share_var.zAccCollect.append(share_var.zAcc)
## end of UpdateDequeData

def dequeMean(deq):
    """ Returns the mean as float of a collections.deque structure"""
    return(sum(deq)/float(len(deq)))
## end of dequeMean(deq)

def FlexCurrDataList():
    """ Returns the current instananeuous flex sensor values in the form of a list """
    return( [ share_var.indexFingerDeg, share_var.indexKnuckleDeg, share_var.middleFingerDeg, \
                share_var.middleKnuckleDeg, share_var.ringFingerDeg, share_var.ringKnuckleDeg, \
                share_var.pinkieFingerDeg, share_var.thumbDeg, share_var.thumbKnuckleDeg ] )
## end of FlexCurrDataList()

def FlexCurrDataStr():
    """ Returns the instananeous Flex Sensor values in the form of a string separated by ","s """
    tmpList = [ share_var.indexFingerDeg, share_var.indexKnuckleDeg, share_var.middleFingerDeg, \
                    share_var.middleKnuckleDeg, share_var.ringFingerDeg, share_var.ringKnuckleDeg, \
                    share_var.pinkieFingerDeg, share_var.thumbDeg, share_var.thumbKnuckleDeg ]
    return( ','.join(repr(e) for e in tmpList) )
## end of FlexCurrDataStr()

def FlexDataList():
    """ Returns the average of stored Flex Sensor values as a list"""
    # Determine average of flex sensor data in collection data
    iFinger_mean = dequeMean(share_var.indexFingerDegCollect)
    iKnuckle_mean = dequeMean(share_var.indexKnuckleDegCollect)
    mFinger_mean = dequeMean(share_var.middleFingerDegCollect)
    mKnuckle_mean = dequeMean(share_var.middleKnuckleDegCollect)
    rFinger_mean = dequeMean(share_var.ringFingerDegCollect)
    rKnuckle_mean = dequeMean(share_var.ringKnuckleDegCollect)
    pFinger_mean = dequeMean(share_var.pinkieFingerDegCollect)
    thumb_mean = dequeMean(share_var.thumbDegCollect)
    tKnuckle_mean = dequeMean(share_var.thumbKnuckleDegCollect)

    tmpList = [ iFinger_mean, iKnuckle_mean, mFinger_mean, \
                    mKnuckle_mean, rFinger_mean, rKnuckle_mean, \
                    pFinger_mean, thumb_mean, tKnuckle_mean ]
    return(tmpList)
## end of FlexDataList()

def FlexDataStr():
    """ Returns the average of stored Flex Sensor values in the form of a string separated by ","s """
    # Determine average of flex sensor data in collection data
    tmpList = FlexDataList()
    return( ','.join(repr(e) for e in tmpList) )
## end of FlexDataStr()

def TouchDataList():
    """ Returns the average of stored Touch Sensor values in the form of a list """
    # Determine average of touch sensor data in collection data
    touch1_mean = dequeMean(share_var.touch1Collect)
    touch2_mean = dequeMean(share_var.touch2Collect)
    touch3_mean = dequeMean(share_var.touch3Collect)
    touch4_mean = dequeMean(share_var.touch4Collect)
    touch5_mean = dequeMean(share_var.touch5Collect)
    touch6_mean = dequeMean(share_var.touch6Collect)
    touch7_mean = dequeMean(share_var.touch7Collect)

    tmpList = [ touch1_mean, touch2_mean, touch3_mean, \
                    touch4_mean, touch5_mean, touch6_mean, \
                    touch7_mean ]
    return (tmpList)
## end of TouchDataList()

def TouchDataStr():
    """ Returns the average of stored Touch Sensor values in the form of a string separated by ","s """
    tmpList = TouchDataList()
    return( ','.join(repr(e) for e in tmpList) )
## end of TouchDataStr()

def TouchBoolList():
    """ Returns a boolean int (0 or 1) from average of stored Touch Sensor Data in the form of a list """
    # Threshold value for indicated the fingers have touched
    touchThres = 4000;
    # Determine average of touch sensor data in collection data and use threshold for boolean (touched or not touched)
    touch1_bool = 1 if (dequeMean(share_var.touch1Collect) > touchThres) else 0
    touch2_bool = 1 if (dequeMean(share_var.touch2Collect) > touchThres) else 0
    touch3_bool = 1 if (dequeMean(share_var.touch3Collect) > touchThres) else 0
    touch4_bool = 1 if (dequeMean(share_var.touch4Collect) > touchThres) else 0
    touch5_bool = 1 if (dequeMean(share_var.touch5Collect) > touchThres) else 0
    touch6_bool = 1 if (dequeMean(share_var.touch6Collect) > touchThres) else 0
    touch7_bool = 1 if (dequeMean(share_var.touch7Collect) > touchThres) else 0

    tmpList = [ touch1_bool, touch2_bool, touch3_bool, \
                    touch4_bool, touch5_bool, touch6_bool, \
                    touch7_bool ]
    return( tmpList )
## end of TouchBoolList()

def TouchBoolStr():
    """ Returns a boolean int (0 or 1) from average of stored Touch Sensor Data in the form of a string separated by ","s """
    tmpList = TouchBoolList()
    return( ','.join(repr(e) for e in tmpList) )
## end of TouchBoolStr()

def QuatDataList():
    """ Returns the average of stored Quaternion values in the form of a list """
    # Determine average of quaternion data in collection data
    q0_mean = dequeMean(share_var.q0Collect)
    q1_mean = dequeMean(share_var.q1Collect)
    q2_mean = dequeMean(share_var.q2Collect)
    q3_mean = dequeMean(share_var.q3Collect)

    tmpList = [ q0_mean, q1_mean, q2_mean, q3_mean ]
    return(tmpList)
## end of QuatDataList()

def QuatDataStr():
    """ Returns the average of stored Quaternion values in the form of a string separated by ","s """
    tmpList = QuatDataList()
    return( ','.join(repr(e) for e in tmpList) )
## end of QuatDataStr()

def QuatCurrDataStr():
    """ Returns the current Quaternion Data values in the form of a string separated by ","s """
    tmpList = [ share_var.q0, share_var.q1, share_var.q2, share_var.q3 ]
    return( ','.join(repr(e) for e in tmpList) )
## end of QuatCurrDataStr()

def EulerCurrDataStr():
    """ Returns the current Euler Data values in the form of a string separated by ","s """
    tmpList = [ share_var.roll, share_var.pitch, share_var.yaw]
    return( ','.join(repr(e) for e in tmpList) )
## end of EulerCurrDataStr()

def LinAccelCurrDataStr():
    """ Returns the current Linear Acceleration values in the form of a string separated by ","s """
    tmpList = [ share_var.xAcc, share_var.yAcc, share_var.zAcc ]
    return( ','.join(repr(e) for e in tmpList) )
## end of LinAccelCurrDataStr()

## printInstHandDataToFile
def printInstHandDataToFile(fileName, str_handIdentifier):
    """ Inputs a letter/number/gesture identifying the hand animation being performed
        Writes the identifier with the instantaneuous hand data to a file
        Inputs:     fileName - specify entire filename with extension (ie. 'test.csv')
        Outputs:    writes to file
    """
    outFile = open(fileName,'a')
    # Obtain hand data as strings separated by "," so that we can write to file
    strHandDataOut = str_handIdentifier + "," + FlexDataStr() + "," + QuatDataStr() + "," + EulerDataStr() + "," + LinAccelDataStr()
    outFile.write(strHandDataOut)
    outFile.write('\n')
    outFile.close
## end of printInstHandDataToFile

## printHandDataToFile
def printHandDataToFile(fileName, str_handIdentifier):
    """ Inputs a letter/number/gesture identifying the hand animation being performed
        Writes the identifier with the appropriate hand data to the file specified
        Inputs:     fileName - specify entire filename with extension (ie. 'test.csv')
        Outputs:    writes to file
    """
    outFile = open(fileName,'a') # append mode
    # Obtain hand data as strings separated by "," from XDataStr() so that we can write to file
    strHandDataOut = str_handIdentifier + "," + FlexDataStr() + ',' + TouchBoolStr() + ',' + QuatDataStr()
    outFile.write(strHandDataOut)
    outFile.write('\n')
    outFile.close
## end of printHandDataToFile

def readHandDataFromFile(fileName):
    """ Reads and parses the hand data saved in a file
        Stores the identifier in numpy array "signTarget"
        Stores the hand data in numpy array "signFeatures"
        Inputs:     fileName - specify entire filename with extension (ie. 'test.csv')
        Outputs:    signTarget - nx1 array of targets/identifiers/labels
                    signFeatures - nxm array of m features for each of the n targets
    """
    inFile = open(fileName,'r')
    fileList = inFile.readlines() #Each line is an item in the list
    # print (fileList) #For testing
    n = len(fileList) #Number of targets from lines in file
    m = len(fileList[0].split(','))-1 #Number of features
    # print ('n,m=',n,m) #For testing
    signTarget = np.empty((n),dtype='a16') #Empty nx1 array of 16 char max strings
    signFeatures = np.zeros((n,m))
    for i in range(0,n):
        lineList = fileList[i].split(',') # Splits line by ','
        j=0 # item iterator
        for item in lineList:
            if j==0:
                signTarget[i]= item
                j+=1
            else:
                signFeatures[i,j-1] = item
                j+=1
    inFile.close
    return( signTarget, signFeatures )
## end of readHandDataFromFile

## Capture hand data or predict function
def pseudoMain():
    """ Console menu application for capturing hand gestures, training SVM, and classifying gestures """
    print("--------------------------------------------------")
    print("                     HandsOn                      ")
    print("--------------------------------------------------")
    print("MENU:")
    print("1. Capture Hand Gesture Data to File")
    print("2. Train SVM with Hand Gesture Data From File")
    print("3. Load SVM from File")
    print("4. Predict Hand Gestures")
    print("5. Exit\n")

    # Instantiate the text-to-speech engine
    engine = pyttsx.init()

    svmFlag = False #Flag to determine if the SVM has been instantiated and fit

    while True:
        modeEnable = input("Enter the number corresponding to the menu option to perform: ")
        if modeEnable == 1:
            inFileName = raw_input("Enter the full file name with correct extension: ")
            # Capture hand gesture data to file
            while True:
                gestureID = raw_input("Enter the identifier for the hand letter/number/gesture: ") # Ask for gesture identifier
                if gestureID == "\exit": ## Type \exit to exit the loop
                    break
                else:
                   printHandDataToFile(inFileName,gestureID)
        elif modeEnable == 2:
            # Train SVM with Hand Gesture Data From File
            inFileName = raw_input("Enter the full file name with correct extension: ")
            signTarget, signFeatures = readHandDataFromFile(inFileName)
            #print "Signed Target:", signTarget
            #print "Signed Features:", signFeatures
            # Instantiate the SVM object
            print("Creating the SVM and fitting the data...")
            clf = svm.SVC(C=1, kernel='rbf',gamma=0.0001,probability=True) ## NEED TO OPTIMIZE THE PARAMETERS
            clf.fit(signFeatures,signTarget)
            svmFlag = True
            print("SVM Fit Completed\n")
        elif modeEnable == 3:
            # Load SVM From File
            x = 0 # placeholder to remove IDE errors shown
        elif modeEnable == 4:
            # Predict Hand Gestures
            if (svmFlag != True) :
                print("SVM has not been created yet!")
            else:
                # Ctrl-C causes keyboard interrupt and allows us to exit back to the menu with try and except
                try:
                    while True:
                        print("SVM is predicting hand gestures...")
                        time.sleep(4) # Wait time between classifications
                        #kernal_svm_time = time() #Timing how long SVM takes to classify
                        gest = np.asarray(FlexDataList()+TouchBoolList()+QuatDataList()) #avg of last 2 seconds
                        svmPred = clf.predict(gest.reshape(1,-1))
                        print "Prediction: ", svmPred
                        ## DO PROBABILITY STUFF IF REQUIRED
                        svmPredProb = clf.predict_proba(gest.reshape(1,-1))
                        print "Probability Prediction: ", svmPredProb
                        #kernal_svm_time = kernal_svm_time - time()
                        #print "Time to predict: ", kernal_svm_time

                        # Text to speech of output
                        engine.say(svmPred[0])
                        engine.runAndWait()
                except KeyboardInterrupt:
                    pass
        elif modeEnable == 5:
            print("Exiting...\n")
            break # Exit while loop and terminate
        else:
            print("Not a valid input")
            print("Returning to Menu\n")
    return 0
## end of pseudoMain


## Function to parse the serial data and assign them
## to the appropriate global variables
# class serialThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.daemon = True
#         ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5) #Open serial port
#         self.start()

def parseSerialHandData(ser):
    """ Parses serial data and assigns to appropriate global variables """
    while True:
        line = ser.readline() #Read line until \n
        #print(line)
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
                share_var.thumbDeg = float(lineList[7])
                share_var.thumbKnuckleDeg = float(lineList[9])

            # Touch Sensors Part 1
            elif lineList[0] == "IndexSide:":
                share_var.touch1 = int(lineList[1])
                share_var.touch2 = int(lineList[3])
                share_var.touch3 = int(lineList[5])
                share_var.touch4 = int(lineList[7])

            # Touch Sensors Part 2
            elif lineList[0] == "RingSide:":
                share_var.touch5 = int(lineList[1])
                share_var.touch6 = int(lineList[3])
                share_var.touch7 = int(lineList[5])
                # This line is the last one of the current serial data block so...
                # Update the moving window deque structure with new sensor values
                UpdateDequeData()

            # Quaternions
            elif lineList[0] == "qW:":
                q0 = share_var.q0 = float(lineList[1])
                q1 = share_var.q1 = float(lineList[3])
                q2 = share_var.q2 = float(lineList[5])
                q3 = share_var.q3 = float(lineList[7])
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
