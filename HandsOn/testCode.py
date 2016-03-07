import HandsOn
import share_var
import numpy as np
import pyttsx


def main():
    """ For testing HandsOn without the data glove """
    engine = pyttsx.init()
    engine.say('Sally sells seashells by the seashore.')
    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()
    # Text-to-Speech randomly works sometimes and othertimes gives errors?

    for i in range(0,100):
        share_var.indexFingerDegCollect.append(3)
        share_var.indexKnuckleDegCollect.append(3)
        share_var.middleFingerDegCollect.append(3)
        share_var.middleKnuckleDegCollect.append(3)
        share_var.ringFingerDegCollect.append(3)
        share_var.ringKnuckleDegCollect.append(3)
        share_var.pinkieFingerDegCollect.append(3)
        share_var.thumbDegCollect.append(3)
    
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
        
