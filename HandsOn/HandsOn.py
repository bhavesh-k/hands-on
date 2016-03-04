import math
import string
import time
import serial
import collections
import share_var
import numpy as np
from sklearn import svm

#global pitch, yaw, roll

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
    """ Updates the collections.deque of all hand data (flex sensor, quaternion, euler angles, lin accel """
    share_var.indexFingerDegCollect.append(share_var.indexFingerDeg)
    share_var.indexKnuckleDegCollect.append(share_var.indexKnuckleDeg)
    share_var.middleFingerDegCollect.append(share_var.middleFingerDeg)
    share_var.middleKnuckleDegCollect.append(share_var.middleKnuckleDeg)
    share_var.ringFingerDegCollect.append(share_var.ringFingerDeg)
    share_var.ringKnuckleDegCollect.append(share_var.ringKnuckleDeg)
    share_var.pinkieFingerDegCollect.append(share_var.pinkieFingerDeg)
    share_var.thumbDegCollect.append(share_var.thumbDeg)
    share_var.q0Collect.append(share_var.q0) 
    share_var.q1Collect.append(share_var.q1) 
    share_var.q2Collect.append(share_var.q2) 
    share_var.q3Collect.append(share_var.q3) 
    share_var.rollCollect.append(share_var.roll) 
    share_var.pitchCollect.append(share_var.pitch) 
    share_var.yawCollect.append(share_var.yaw) 
    share_var.xAccCollect.append(share_var.xAcc) 
    share_var.yAccCollect.append(share_var.yAcc) 
    share_var.zAccCollect.append(share_var.zAcc) 
## end of UpdateDequeData

def FlexInstDataList():
    """ Returns the instananeuous flex sensor values in the form of a list """
    return( [ share_var.indexFingerDeg, share_var.indexKnuckleDeg, share_var.middleFingerDeg, \
                share_var.middleKnuckleDeg, share_var.ringFingerDeg, share_var.ringKnuckleDeg, \
                share_var.pinkieFingerDeg, share_var.thumbDeg ] )
## end of FlexInstDataList()

def FlexInstDataStr():
    """ Returns the instananeous Flex Sensor values in the form of a string separated by ","s """
    tmpList = [ share_var.indexFingerDeg, share_var.indexKnuckleDeg, share_var.middleFingerDeg, \
                    share_var.middleKnuckleDeg, share_var.ringFingerDeg, share_var.ringKnuckleDeg, \
                    share_var.pinkieFingerDeg, share_var.thumbDeg ]
    return( ','.join(repr(e) for e in tmpList) )
## end of FlexInstDataStr()

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

    tmpList = [ iFinger_mean, iKnuckle_mean, mFinger_mean, \
                    mKnuckle_mean, rFinger_mean, rKnuckle_mean, \
                    pFinger_mean, thumb_mean ]
    return(tmpList)
## end of FlexDataList()

def FlexDataStr():
    """ Returns the average of stored Flex Sensor values in the form of a string separated by ","s """
    # Determine average of flex sensor data in collection data
    iFinger_mean = dequeMean(share_var.indexFingerDegCollect)
    iKnuckle_mean = dequeMean(share_var.indexKnuckleDegCollect)
    mFinger_mean = dequeMean(share_var.middleFingerDegCollect)
    mKnuckle_mean = dequeMean(share_var.middleKnuckleDegCollect)
    rFinger_mean = dequeMean(share_var.ringFingerDegCollect)
    rKnuckle_mean = dequeMean(share_var.ringKnuckleDegCollect)
    pFinger_mean = dequeMean(share_var.pinkieFingerDegCollect)
    thumb_mean = dequeMean(share_var.thumbDegCollect)

    tmpList = [ iFinger_mean, iKnuckle_mean, mFinger_mean, \
                    mKnuckle_mean, rFinger_mean, rKnuckle_mean, \
                    pFinger_mean, thumb_mean ]
    return( ','.join(repr(e) for e in tmpList) )
## end of FlexDataStr()

def dequeMean(deq):
    """ Returns the mean as float of a collections.deque structure"""
    return(sum(deq)/float(len(deq)))
    
def QuatDataStr():
    """ Returns the current Quaternion Data values in the form of a string separated by ","s """
    tmpList = [ share_var.q0, share_var.q1, share_var.q2, share_var.q3 ] 
    return( ','.join(repr(e) for e in tmpList) )
## end of QuatDataStr()

def EulerDataStr():
    """ Returns the current Euler Data values in the form of a string separated by ","s """
    tmpList = [ share_var.roll, share_var.pitch, share_var.yaw] 
    return( ','.join(repr(e) for e in tmpList) )
## end of EulerDataStr()

def LinAccelDataStr():
    """ Returns the current Linear Acceleration values in the form of a string separated by ","s """
    tmpList = [ share_var.xAcc, share_var.yAcc, share_var.zAcc ] 
    return( ','.join(repr(e) for e in tmpList) )
## end of LinAccelDataStr()

## printInstHandDataToFile
def printInstHandDataToFile(fileName, str_handIdentifier):
    """ Inputs a letter/number/gesture identifying the hand animation being performed  
        Writes the identifier with the instantaneuous hand data to a file 
        Inputs:     fileName - specificy entire filename with extension (ie. 'test.csv')
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
        Inputs:     fileName - specificy entire filename with extension (ie. 'test.csv')
        Outputs:    writes to file
    """
    outFile = open(fileName,'a')
    # Obtain hand data as strings separated by "," from FlexDataStr() so that we can write to file
    strHandDataOut = str_handIdentifier + "," + FlexDataStr()
    outFile.write(strHandDataOut)
    outFile.write('\n')
    outFile.close  
## end of printHandDataToFile

def readHandDataFromFile(fileName):
    """ Reads and parses the hand data saved in a file
        Stores the identifier in numpy array "signTarget"
        Stores the hand data in numpy array "signFeatures"
        Inputs:     fileName - specificy entire filename with extension (ie. 'test.csv')
        Outputs:    signTarget - 1xn array of targets/identifiers/labels
                    signFeatures - nxm array of m features for each of the n targets
    """ 
    inFile = open(fileName,'r')
    fileList = inFile.readlines() #Each line is an item in the list
    n = len(inFile.readlines()) #Number of tagets from lines in file
    m = len(fileList[0].split(','))-1 #Number features
    signTarget = np.zeros((1,n))
    signFeatures = np.zeros((n,m))
    for i in range(0,n):
        lineList = fileList[i].split(',') # Splits line by ','
        j=0 # item iterator
        for item in lineList:
            if j==0:
                signTarget[i]= item
                j+=1
            else:
                signFeatures[i,j] = item
                j+=1
    return( signTarget, signFeatures)
## end of readHandDataFromFile
    
## Capture hand data or predict function
def pseudoMain():
    print("-------------------------------------")
    print("             HandsOn                 ")
    print("-------------------------------------")
    print("MENU:")
    print("1. Capture Hand Gesture Data to File")
    print("2. Train SVM with Hand Gesture Data From File")
    print("3. Load SVM from File")
    print("4. Predict Hand Gestures")
    print("5. Exit\n")
    
    svmFlag = False #Flag to determine if the SVM has been instantiated and fit
    
    while True:
        modeEnable = input("Enter the number corresponding to the menu option to perform: ")
        if modeEnable == 1:
            # Capture hand gesture data to file
            while True:
                gestureID = raw_input("Enter the identifier for the hand letter/number/gesture: ") # Ask for gesture identifier
                if gestureID == "\exit": ## Type \exit to exit the loop
                    break
                else:
                   printHandDataToFile("classification.csv",gestureID)
        elif modeEnable == 2:
            # Train SVM with Hand Gesture Data From File
            inFileName = raw_input("Enter the full file name with correct extension: ")
            signTarget, signFeatures = readHandDataFromFile(inFileName)
            # Instantiate the SVM object
            print("Creating the SVM and fitting the data...")
            clf = svm.SVC(C=100, kernal='rbf',gamma=0.001,probability=True) ## NEED TO OPTIMIZE THE PARAMETERS
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
                        #time.sleep(0.5)
                        svmPred = clf.predict(FlexDataList.reshape(1,-1))
                        print("Prediction: ", svmPred)
                        ## DO PROBABILITY STUFF IF REQUIRED
                        svmPredProb = clf.predict_proba(FlexDataList.reshape(1,-1))
                        print("Probability Prediction: ", svmPredProb)
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
                # Update the collection of flex sensor data
                UpdateDequeData()
            
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
