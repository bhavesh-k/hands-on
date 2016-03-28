"""
testCode
Authors: Bhavit Patel
Date Created: March 2016
Version 1

Allows testing of various modules and functions in HandsOn 
without the data glove to ensure proper functionality
"""

import HandsOn
import share_var
import numpy as np
import pyttsx

def main():
    """ For testing HandsOn features without the data glove """

    # Text to speech testing
    engine = pyttsx.init()
    engine.say('Sally sells seashells by the seashore.')
    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()

    testVal = 3
    for i in range(0,100):
        share_var.indexFingerDegCollect.append(testVal)
        share_var.indexKnuckleDegCollect.append(testVal)
        share_var.middleFingerDegCollect.append(testVal)
        share_var.middleKnuckleDegCollect.append(testVal)
        share_var.ringFingerDegCollect.append(testVal)
        share_var.ringKnuckleDegCollect.append(testVal)
        share_var.pinkieFingerDegCollect.append(testVal)
        share_var.thumbDegCollect.append(testVal)
    
    # Test some functions
    dataListTest = HandsOn.FlexDataList()
    print "Output from FlexDataList(): ", dataListTest
    print np.asarray(dataListTest)
    dataStrTest = HandsOn.FlexDataStr()
    print "Output from FlexDataStr(): ", dataStrTest
    
    # Test reading file
    signTargetTest, signFeaturesTest = HandsOn.readHandDataFromFile('testClf.csv')
    print "Sign Target Test:", signTargetTest
    print "Sign Features Test:", signFeaturesTest[2]
   
    #Test menu
    HandsOn.pseudoMain()

    return 0
        
if __name__ == "__main__":
    main()
        
