"""
HandsOn
Authors: Bhavit Patel, Bhavesh Kakwani, Tom Yang
Date Created: January 2016
Version 1

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
from sklearn import tree
#import pyttsx
from Tools import *

## Capture hand data or predict function
def pseudoMain(delay, debugFlag, ttsFlag):
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

    if ttsFlag:
        # Instantiate the text-to-speech engine
        engine = pyttsx.init()
        engine.setProperty('rate',120)

    svmFlag = False #Flag to determine if the SVM has been instantiated and fit

    while True:
        modeEnable = input("Enter the number corresponding to the menu option to perform: ")
        if modeEnable == 1:
            outFileName = raw_input("Enter the full file name with correct extension: ")
            # Capture hand gesture data to file
            while True:
                gestureID = raw_input("Enter the identifier for the hand letter/number/gesture: ") # Ask for gesture identifier
                if gestureID == "\exit": ## Type \exit to exit the loop
                    break
                else:
                   printHandDataToFile(outFileName,gestureID)
        elif modeEnable == 2:
            # Train SVM with Hand Gesture Data From File
            inFileName = raw_input("Enter the full file name with correct extension: ")
            signTarget, signFeatures = readHandDataFromFile(inFileName)
            #print "Signed Target:", signTarget
            #print "Signed Features:", signFeatures
            # Instantiate the SVM object
            print("Creating the SVM and fitting the data...")
            clf = svm.SVC(C=1, kernel='rbf',gamma=0.0001,probability=True)
            clf_tree = tree.DecisionTreeClassifier() # decision tree version of classifier

            # Train the classifiers
            clf.fit(signFeatures,signTarget)
            clf_tree.fit(signFeatures,signTarget)

            svmFlag = True
            print("SVM Fit Completed\n")
        elif modeEnable == 3:
            # Load SVM From File
            print("This feature has not yet been enabled\n")
        elif modeEnable == 4:
            # Predict Hand Gestures
            if (svmFlag != True) :
                print("SVM has not been created yet!")
            else:
                # Ctrl-C causes keyboard interrupt and allows us to exit back to the menu with try and except
                try:
                    while True:
                        print("SVM is predicting hand gestures...")
                        time.sleep(delay) # Wait time between classifications
                        #kernal_svm_time = time() #Timing how long SVM takes to classify

                        # Organize features to be used for classifier prediction
                        featureList = FlexMeanDataList() + TouchMeanBoolList() + QuatMeanDataList()
                        gest = np.asarray(featureList)
                        svmPred = clf.predict(gest.reshape(1,-1)) # change to clf_tree for decision tree classfxn
                        print("Prediction: ", svmPred)
                        if debugFlag:
                            svmPredProb = clf.predict_proba(gest.reshape(1,-1)) # change to clf_tree for decision tree classfxn
                            print("Probability Prediction: ", svmPredProb)
                        #kernal_svm_time = kernal_svm_time - time()
                        #print "Time to predict: ", kernal_svm_time
                        if ttsFlag:
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

def parseSerialHandData(ser):
    """ Parses serial data and assigns to appropriate global variables """
    while True:
        line = ser.readline() #Read line until \n
        #print(line)
        parseLineData(line)
## end of parseSerialHandData

def parseLineData(line):
    lineList = line.split()
    if len(lineList) > 1:
        if lineList[0] == b"Alt:":
            share_var.alt = float(lineList[1])
        elif lineList[0] == b"Temp:":
            share_var.temp = float(lineList[1])
        #Calibration Values
        elif lineList[0] == b"System:":
            share_var.sysCal   = int(lineList[1])
            share_var.gyroCal  = int(lineList[3])
            share_var.accelCal = int(lineList[5])
            share_var.magCal   = int(lineList[7])
        # Fingers Part 1
        elif lineList[0] == b"FingerDegrees:":
            share_var.flexIndexFinger = float(lineList[1])
            share_var.flexMiddleFinger = float(lineList[2])
            share_var.flexRingFinger = float(lineList[3])
            share_var.flexPinkyFinger = float(lineList[4])
            share_var.flexThumb = float(lineList[5])
        # Fingers Part 2
        elif lineList[0] == b"KnuckleDegrees:":
            share_var.flexIndexKnuckle = float(lineList[1])
            share_var.flexMiddleKnuckle = float(lineList[2])
            share_var.flexRingKnuckle = float(lineList[3])
            share_var.flexThumbKnuckle = float(lineList[4])
        # Quaternions
        elif lineList[0] == b"Quaternions":
            share_var.qW = float(lineList[1])/100.0
            share_var.qX = float(lineList[2])/100.0
            share_var.qY = float(lineList[3])/100.0
            share_var.qZ = float(lineList[4])/100.0
            [r,p,y] = QuatToEuler(share_var.qW,share_var.qX,share_var.qY,share_var.qZ)
            share_var.pitch = -math.degrees(p)
            share_var.roll = -math.degrees(r)
            share_var.yaw = math.degrees(y)
            #share_var.direction = EulerToDir(share_var.roll,share_var.pitch,share_var.yaw)
            share_var.direction = QuatToDir(share_var.qW, share_var.qX, share_var.qY, share_var.qZ)
        #Linear Acceleration
        elif lineList[0] == b"Acceleration":
            share_var.accelX = float(lineList[1])
            share_var.accelY = float(lineList[2])
            share_var.accelZ = float(lineList[3])
        # Touch Sensors
        elif lineList[0] == b"TouchSensors:":
            share_var.touchIndSide = int(lineList[1])
            share_var.touchIndTop = int(lineList[2])
            share_var.touchMidTop = int(lineList[3])
            share_var.touchMidSide = int(lineList[4])
            share_var.touchRing = int(lineList[5])
            share_var.touchPinkySide = int(lineList[6])
            share_var.touchPinkyTop = int(lineList[7])
            # This line is the last one of the current serial data block so...
            # Update the moving window deque structure with new sensor values
            UpdateDequeData()
## end of parseLineData(line)
