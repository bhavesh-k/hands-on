"""
Tools
Authors: Bhavit Patel, Bhavesh Kakwani, Tom Yang
Date Created: March 2016

Contains multiple functions and tools for processing hand sensor data obtained 
from parseSerialData() and stored in global variables or deque objects in share_var
"""
import share_var
import string
import math
import numpy as np

def UpdateDequeData():
    """ Updates the collections.deque instances of all hand sensor data (flex sensor, touch sensors, quaternion, euler angles, lin accel) """
    # Flex Sensors
    share_var.flexIndexFingerCollect.append(share_var.flexIndexFinger)
    share_var.flexIndexKnuckleCollect.append(share_var.flexIndexKnuckle)
    share_var.flexMiddleFingerCollect.append(share_var.flexMiddleFinger)
    share_var.flexMiddleKnuckleCollect.append(share_var.flexMiddleKnuckle)
    share_var.flexRingFingerCollect.append(share_var.flexRingFinger)
    share_var.flexRingKnuckleCollect.append(share_var.flexRingKnuckle)
    share_var.flexPinkyFingerCollect.append(share_var.flexPinkyFinger)
    share_var.flexThumbCollect.append(share_var.flexThumb)
    share_var.flexThumbKnuckleCollect.append(share_var.flexThumbKnuckle)
    # Touch Sensors
    share_var.touchIndSideCollect.append(share_var.touchIndSide)
    share_var.touchIndTopCollect.append(share_var.touchIndTop)
    share_var.touchMidTopCollect.append(share_var.touchMidTop)
    share_var.touchMidSideCollect.append(share_var.touchMidSide)
    share_var.touchRingCollect.append(share_var.touchRing)
    share_var.touchPinkySideCollect.append(share_var.touchPinkySide)
    share_var.touchPinkyTopCollect.append(share_var.touchPinkyTop)
    # Quaternions
    share_var.qWCollect.append(share_var.qW)
    share_var.qXCollect.append(share_var.qX)
    share_var.qYCollect.append(share_var.qY)
    share_var.qZCollect.append(share_var.qZ)
    # Euler Angles
    share_var.rollCollect.append(share_var.roll)
    share_var.pitchCollect.append(share_var.pitch)
    share_var.yawCollect.append(share_var.yaw)
    # Linear Acceleration
    share_var.accelXCollect.append(share_var.accelX)
    share_var.accelYCollect.append(share_var.accelY)
    share_var.accelZCollect.append(share_var.accelZ)
## end of UpdateDequeData

def DequeMean(deq):
    """ Returns the mean as a float of a collections.deque instance
        Input: deq - collections.deque instance (ex. flexIndexFingerCollect, qWCollect, etc.)
        Output: meanList - list of current means for the collections.deque instances  """
    return(sum(deq)/float(len(deq)))
## end of DequeMean(deq)

def DequeMeanList(deqList):
    """ Returns the means for a list of collections.deque instances
        Input: deqList - list of collections.deque instances (ex. flexCollectList, touchCollectList, etc.)
        Output: meanList - list of current means for the collections.deque instances  """
    # Initialize meanList to be all 0s and length of deqList
    meanList = [0]*len(deqList)
    i = 0
    for deq in deqList:
        meanList[i] = DequeMean(deq)
        i += 1 #increment
    return meanList
## end of DequeMeanList(deqList)
    
def ListToCSstr(list):
    """ Returns a comma separated string consisting of values in input list """
    return(','.join(repr(e) for e in list))
## end of ListToCSstr(list)

def FlexCurrDataList():
    """ Returns the current instananeuous flex sensor values in the form of a list """
    return( [ share_var.flexIndexFinger, share_var.flexIndexKnuckle, share_var.flexMiddleFinger, \
                share_var.flexMiddleKnuckle, share_var.flexRingFinger, share_var.flexRingKnuckle, \
                share_var.flexPinkyFinger, share_var.flexThumb, share_var.flexThumbKnuckle ] )
## end of FlexCurrDataList()

def FlexCurrDataStr():
    """ Returns the instananeous Flex Sensor values in the form of a string separated by ","s """
    tmpList = FlexCurrDataList()
    return( ListToCSstr(tmpList) )
## end of FlexCurrDataStr()

def FlexMeanDataList():
    """ Returns the mean of collected Flex Sensor data as a list """
    return (DequeMeanList(share_var.flexCollectList))
## end of FlexMeanDataList()

def FlexMeanDataStr():
    """ Returns the mean of collected Flex Sensor data in the form of a string separated by ","s """
    meanList = DequeMeanList(share_var.flexCollectList)
    return( ListToCSstr(meanList) )
## end of FlexMeanDataStr()

def TouchMeanDataList():
    """ Returns the mean of collected Touch Sensor data as a list """
    return (DequeMeanList(share_var.touchCollectList))
## end of TouchMeanDataList()

def TouchMeanDataStr():
    """ Returns the mean of collected Touch Sensor data in the form of a string separated by ","s """
    meanList = DequeMeanList(share_var.touchCollectList)
    return( ListToCSstr(meanList) )
## end of TouchMeanDataStr()

def TouchMeanBoolList():
    """ Returns a boolean int (0 or 1) from the means of collected Touch Sensor data as a list
        0 if TouchMean < threshold (ie. touch sensor has not been touched)
        1 if TouchMean > threshold (ie. touch sensor has been touched) """
    # Threshold value for indicated the fingers have touched
    touchThres = 2000;
    meanList = DequeMeanList(share_var.touchCollectList)
    # replace means with boolean int (0 or 1)
    for i in range(0,len(meanList)):
        meanList[i] = 100 if (meanList[i] > touchThres) else 0
    return( meanList )
## end of TouchMeanBoolList()

def TouchMeanBoolStr():
    """ Returns a boolean int (0 or 1) from the means of collected Touch Sensor data in the form of a string separated by ","s
        0 if TouchMean < threshold (ie. touch sensor has not been touched)
        1 if TouchMean > threshold (ie. touch sensor has been touched) """
    meanList = TouchMeanBoolList()    
    return( ListToCSstr(meanList) )
## end of TouchMeanBoolStr()

def QuatMeanDataList():
    """ Returns the mean of collected Quaternion data as a list """
    return (DequeMeanList(share_var.quatCollectList))
## end of QuatMeanDataList()

def QuatMeanDataStr():
    """ Returns the mean of collected Quaternion data in the form of a string separated by ","s """
    meanList = DequeMeanList(share_var.quatCollectList)
    return( ListToCSstr(meanList) )
## end of QuatMeanDataStr()

def QuatCurrDataStr():
    """ Returns the current Quaternion data in the form of a string separated by ","s """
    tmpList = [ share_var.qW, share_var.qX, share_var.qY, share_var.qZ ]
    return( ListToCSstr(tmpList) )
## end of QuatCurrDataStr()

def EulerCurrDataStr():
    """ Returns the current Euler Angle values in the form of a string separated by ","s """
    tmpList = [ share_var.roll, share_var.pitch, share_var.yaw]
    return( ListToCSstr(tmpList) )
## end of EulerCurrDataStr()

def LinAccelCurrDataStr():
    """ Returns the current Linear Acceleration values in the form of a string separated by ","s """
    tmpList = [ share_var.accelX, share_var.accelY, share_var.accelZ ]
    return( ListToCSstr(tmpList) )
## end of LinAccelCurrDataStr()

def LinAccelMeanDataList():
    """ Returns the mean of collected Linear Accelreation data as a list """
    return (DequeMeanList(share_var.accelCollectList))
## end of LinAccelMeanDataList()

def LinAccelMeanDataStr():
    """ Returns the mean of collected Linear Acceleration data in the form of a string separated by ","s """
    meanList = DequeMeanList(share_var.accelCollectList)
    return( ListToCSstr(meanList) )
## end of FlexMeanDataStr()

def LinAccelMoving():
    numPreviousSamples = 5
    movingList = [0]*3
    i = 0
    for deq in share_var.accelCollectList:
        sum = 0
        for j in range(1,numPreviousSamples+1):
            sum = sum + abs(deq(-j))
            meanAbs = sum/numPreviousSamples
            movingList[i]= meanAbs
        i += 1
    return (movingList)
## end of LinAccelMoving

def isMoving():
    """ Returns a boolean if the user is moving determined wtih the collected linear acceleration """
    movingList = LinAccelMoving()
    moveFlag = False;
    linAccelThres = 0.5
    for direction in movingList:
        if direction > linAccelThres:
            moveFlag = True;
    return moveFlag
## end of isMoving

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


def printInstHandDataToFile(fileName, str_handIdentifier):
    """ Inputs a letter/number/gesture identifying the hand animation being performed
        Writes the identifier with the instantaneuous hand data to a file
        Inputs:     fileName - specify entire filename with extension (ie. 'test.csv')
        Outputs:    writes to file
    """
    outFile = open(fileName,'a')
    # Obtain hand data as strings separated by "," so that we can write to file
    strHandDataOut = str_handIdentifier + "," + FlexCurrDataStr() + "," + QuatCurrDataStr() + "," + EulerCurrDataStr() + "," + LinAccelCurrDataStr()
    outFile.write(strHandDataOut)
    outFile.write('\n')
    outFile.close
## end of printInstHandDataToFile

def printHandDataToFile(fileName, str_handIdentifier):
    """ Inputs a letter/number/gesture identifying the hand animation being performed
        Writes the identifier with the appropriate hand data to the file specified
        Inputs:     fileName - specify entire filename with extension (ie. 'test.csv')
        Outputs:    writes to file
    """
    outFile = open(fileName,'a') # append mode
    # Obtain mean of collected hand data as strings separated by "," from XDataStr() so that we can write to file
    strHandDataOut = str_handIdentifier + "," + FlexMeanDataStr() + ',' + TouchMeanBoolStr() + ',' + QuatMeanDataStr()
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
