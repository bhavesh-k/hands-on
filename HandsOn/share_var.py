"""
share_var
Authors: Bhavit Patel, Bhavesh Kakwani, Tom Yang
Date Created: 2016

Variables for instantaneuous hand sensor data and collections.deque objects for storing real-time moving window of sensor data
Global to allow usage by multiple functions. Deques are thread-safe allowing multi-threading with GUI, serial parsing, and animation
"""
import collections

## Global variables to be used by various functions
global alt, temp, sysCal, gyroCal, accelCal, magCal, \
        flexIndexFinger, flexIndexKnuckle, \
        flexMiddleFinger, flexMiddleKnuckle, \
        flexRingFinger, flexRingKnuckle, \
        flexPinkyFinger, flexThumb, flexThumbKnuckle, \
        touchIndSide, touchIndTop, touchMidSide, touchMidTop, \
        touchRing, touchPinkySide, touchPinkyTop, \
        qW, qX, qY, qZ, \
        roll, pitch, yaw, direction, \
        accelX, accelY, accelZ
# Initialize Current Values
alt = temp = sysCal = gyroCal = accelCal = magCal = 0.0
flexIndexFinger = flexIndexKnuckle = 0.0
flexMiddleFinger = flexMiddleKnuckle = 0.0
flexRingFinger = flexRingKnuckle = 0.0
flexPinkyFinger = 0.0
flexThumb = flexThumbKnuckle = 0.0
touchIndSide = touchIndTop = touchMidSide = touchMidTop = touchRing = touchPinkySide = touchPinkyTop = 0.0
qW = qX = qY = qZ = 0.0
roll = 0.0
pitch = 0.0
yaw = 0.0
direction = 0
accelX = accelY = accelZ = 0.0

## Deque objects for fast and efficient real-time data collection. Also thread-safe to allow usage with GUI, animation, and various functions
maxNumSamples = 25 #Set moving window length
# Flex Sensors
flexIndexFingerCollect = collections.deque([0], maxNumSamples)
flexIndexKnuckleCollect = collections.deque([0], maxNumSamples)
flexMiddleFingerCollect = collections.deque([0], maxNumSamples)
flexMiddleKnuckleCollect = collections.deque([0], maxNumSamples)
flexRingFingerCollect = collections.deque([0], maxNumSamples)
flexRingKnuckleCollect = collections.deque([0], maxNumSamples)
flexPinkyFingerCollect = collections.deque([0], maxNumSamples)
flexThumbCollect = collections.deque([0], maxNumSamples)
flexThumbKnuckleCollect = collections.deque([0], maxNumSamples)
flexCollectList = [flexIndexFingerCollect, flexIndexKnuckleCollect, flexMiddleFingerCollect, \
                        flexMiddleKnuckleCollect, flexRingFingerCollect, flexRingKnuckleCollect, \
                        flexPinkyFingerCollect, flexThumbCollect, flexThumbKnuckleCollect]
# Touch Capacitive Sensors
touchIndSideCollect = collections.deque([0], maxNumSamples)
touchIndTopCollect = collections.deque([0], maxNumSamples)
touchMidSideCollect = collections.deque([0], maxNumSamples)
touchMidTopCollect = collections.deque([0], maxNumSamples)
touchRingCollect = collections.deque([0], maxNumSamples)
touchPinkySideCollect = collections.deque([0], maxNumSamples)
touchPinkyTopCollect = collections.deque([0], maxNumSamples)
touchCollectList = [touchIndSideCollect, touchIndTopCollect, touchMidTopCollect, touchMidSideCollect, \
                    touchRingCollect, touchPinkySideCollect, touchPinkyTopCollect]
# Linear Acceleration
accelXCollect = collections.deque([0], maxNumSamples)
accelYCollect = collections.deque([0], maxNumSamples)
accelZCollect = collections.deque([0], maxNumSamples)
accelCollectList = [accelXCollect, accelYCollect, accelZCollect]
# Quaternions
qWCollect = collections.deque([0], maxNumSamples)
qXCollect = collections.deque([0], maxNumSamples)
qYCollect = collections.deque([0], maxNumSamples)
qZCollect = collections.deque([0], maxNumSamples)
quatCollectList = [qWCollect, qXCollect, qYCollect, qZCollect]
# Euler Angles
rollCollect = collections.deque([0], maxNumSamples)
pitchCollect = collections.deque([0], maxNumSamples)
yawCollect = collections.deque([0], maxNumSamples)
eulerCollectList = [rollCollect, pitchCollect, yawCollect]
# Multidimensional list containing all deque objects for easier processing
sensorCollectList = [ flexCollectList, touchCollectList, accelCollectList, quatCollectList, eulerCollectList ]
