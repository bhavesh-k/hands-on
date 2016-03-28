"""
share_var
Authors: Bhavit Patel, Bhavesh Kakwani, Tom Yang
Date Created: 2016

Instantiation of variables for instantaneuous hand data
and collections.deque structures for storing moving window of data
"""

import collections

global alt, temp, sysCal, gyroCal, accelCal, magCal, \
        indexFingerDeg, indexKnuckleDeg, \
        middleFingerDeg, middleKnuckleDeg, \
        ringFingerDeg, ringKnuckleDeg, \
        pinkieFingerDeg, thumbDeg, thumbKnuckleDeg, \
        touch1, touch2, touch3, touch4, \
        touch5, touch6, touch7, \
        q0, q1, q2, q3, \
        roll, pitch, yaw, \
        xAcc, yAcc, zAcc
        
maxNumSamples = 100 #Set moving window length
# Flex Sensors
indexFingerDegCollect = collections.deque([0], maxNumSamples)
indexKnuckleDegCollect = collections.deque([0], maxNumSamples)
middleFingerDegCollect = collections.deque([0], maxNumSamples)
middleKnuckleDegCollect = collections.deque([0], maxNumSamples)
ringFingerDegCollect = collections.deque([0], maxNumSamples)
ringKnuckleDegCollect = collections.deque([0], maxNumSamples)
pinkieFingerDegCollect = collections.deque([0], maxNumSamples)
thumbDegCollect = collections.deque([0], maxNumSamples)
thumbKnuckleDegCollect = collections.deque([0], maxNumSamples)
# Touch Capacitive Sensors
touch1Collect = collections.deque([0], maxNumSamples)
touch2Collect = collections.deque([0], maxNumSamples)
touch3Collect = collections.deque([0], maxNumSamples)
touch4Collect = collections.deque([0], maxNumSamples)
touch5Collect = collections.deque([0], maxNumSamples)
touch6Collect = collections.deque([0], maxNumSamples)
touch7Collect = collections.deque([0], maxNumSamples)
# Quaternions
q0Collect = collections.deque([0], maxNumSamples)
q1Collect = collections.deque([0], maxNumSamples)
q2Collect = collections.deque([0], maxNumSamples)
q3Collect = collections.deque([0], maxNumSamples)
# Eurler Angles
rollCollect = collections.deque([0], maxNumSamples)
pitchCollect = collections.deque([0], maxNumSamples)
yawCollect = collections.deque([0], maxNumSamples)
# Linear Acceleration
xAccCollect = collections.deque([0], maxNumSamples)
yAccCollect = collections.deque([0], maxNumSamples)
zAccCollect = collections.deque([0], maxNumSamples)

# Current Values          
alt = temp = sysCal = gyroCal = accelCal = magCal = 0.0
indexFingerDeg = indexKnuckleDeg = 0.0
middleFingerDeg = middleKnuckleDeg = 0.0
ringFingerDeg = ringKnuckleDeg = 0.0
pinkieFingerDeg = 0.0
thumbDeg = thumbKnuckleDeg = 0.0
touch1 = touch2 = touch3 = touch4 = touch5 = touch6 = touch7 = 0.0
q0 = q1 = q2 = q3 = 0.0
roll = 0.0
pitch = 0.0
yaw = 0.0
xAcc = yAcc = zAcc = 0.0 

