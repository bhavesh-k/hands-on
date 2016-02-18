import collections

global alt, temp, sysCal, gyroCal, accelCal, magCal, \
        indexFingerDeg, indexKnuckleDeg, \
        middleFingerDeg, middleKnuckleDeg, \
        ringFingerDeg, ringKnuckleDeg, \
        pinkieFingerDeg, thumbDeg \
        q0, q1, q2, q3, \
        roll, pitch, yaw, \
        xAcc, yAcc, zAcc, \
        maxNumSamples = 100, \
        indexFingerDegCollect = collections.deque([0], maxNumSamples),\
        indexKnuckleDegCollect = collections.deque([0], maxNumSamples),\
        middleFingerDegCollect = collections.deque([0], maxNumSamples),\
        middleKnuckleDegCollect = collections.deque([0], maxNumSamples),\
        ringFingerDegCollect = collections.deque([0], maxNumSamples),\
        ringKnuckleDegCollect = collections.deque([0], maxNumSamples),\
        pinkieFingerDegCollect = collections.deque([0], maxNumSamples),\
        thumbDegCollect = collections.deque([0], maxNumSamples),\
        q0Collect = collections.deque([0], maxNumSamples),\
        q1Collect = collections.deque([0], maxNumSamples),\
        q2Collect = collections.deque([0], maxNumSamples),\
        q3Collect = collections.deque([0], maxNumSamples),\
        rollCollect = collections.deque([0], maxNumSamples),\
        pitchCollect = collections.deque([0], maxNumSamples),\
        yawCollect = collections.deque([0], maxNumSamples),\
        xAccCollect = collections.deque([0], maxNumSamples),\
        yAccCollect = collections.deque([0], maxNumSamples),\
        zAccCollect = collections.deque([0], maxNumSamples)
          
alt = temp = sysCal = gyroCal = accelCal = magCal = 0.0
indexFingerDeg = indexKnuckleDeg = 0.0
middleFingerDeg = middleKnuckleDeg = 0.0
ringFingerDeg = ringKnuckleDeg = 0.0
pinkieFingerDeg = 0.0
thumbDeg = 0.0
q0 = q1 = q2 = q3 = 0.0
roll = 0.0
pitch = 0.0
yaw = 0.0
xAcc = yAcc = zAcc = 0.0 

