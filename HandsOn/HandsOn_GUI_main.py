"""
HandsOn_GUI_main
Authors: Bhavit Patel, Bhavesh Kakwani, Tom Yang
Date Created: March 2016
Developer GUI Application using multi-threading to capture gestures; setup machine learning as gesture classifier; perform real-time gesture classification
while parsing serial data from an HCI glove. Also plots all input signals and displays a hand animation using OpenGL in separate threads
"""

import sys
import math
import string
import time

import serial
import numpy as np
import collections
from sklearn import svm
from sklearn import tree
import pyttsx
#from espeak import espeak

from PyQt5 import QtCore, QtGui, QtWidgets # Import Qt main modules
import HandsOn_GUI_Layout # Imports our designed .ui layout that was converted to .py

import share_var
import Tools
import HandsOn
import Animation

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GL.VERSION.GL_1_0 import glTranslatef


class DevApp(QtWidgets.QMainWindow, HandsOn_GUI_Layout.Ui_MainWindow, QtCore.QObject):
    """ HandsOn Developer GUI Application """

    def __init__(self):
        ## Super to access variables, methods, etc in HandsOn_GUI_Layout.py
        super(self.__class__, self).__init__()

        self.setupUi(self)  # Defined in HandsOn_GUI_Layout.py automatically. Sets up layout and widgets that are defined
        self._initButtons() # Initilize all button connections

        ## Instance variables for file names
        self.gestFileName = ""
        self.trainFileName = ""

        ## Log File Iterator to prevent overwriting log files on same day
        self.logFileIterator = 1

        ## Set default delay for classifier
        self.lineEditClassRtDelay.setText("4")

        ## Multidimensional List for sensor display line edits for easy updating
        self.sensorLineEdits = [ [self.indexLineEdit, self.indexKnuckleLineEdit, self.middleLineEdit, self.middleKnuckleLineEdit, self.ringLineEdit, self.ringKnuckleLineEdit,  self.pinkyLineEdit, self.thumbLineEdit, self.thumbKnuckeLineEdit], \
                                [self.indexSideLineEdit, self.indexTopLineEdit, self.middleTopLineEdit, self.middleSideLineEdit, self.ringSideLineEdit, self.pinkySideLineEdit, self.pinkyTopLineEdit], \
                                [self.accelXLineEdit, self.accelYLineEdit, self.accelZLineEdit], \
                                [self.quatWLineEdit, self.quatXLineEdit, self.quatYLineEdit, self.quatZLineEdit], [self.rollLineEdit, self.pitchLineEdit, self.yawLineEdit] ]

    def _initButtons(self):
        # Capture Gesture
        self.btnFileOut.clicked.connect(self.SetGestOutFile)
        self.btnGestCap.clicked.connect(self.CaptureGesture)
        self.btnGestCap.setEnabled(False)
        # Train Classifier
        self.btnTrainFile.clicked.connect(self.SetTrainFile)
        self.btnTrainClassifier.clicked.connect(self.TrainClassifier)
        self.btnTrainClassifier.setEnabled(False)
        # Realtime Classification
        self.btnClassifyStart.clicked.connect(self.StartClassifyThread)
        self.btnClassifyStop.clicked.connect(self.EndClassifyThread)
        self.btnClassifyStart.setEnabled(False)
        self.btnClassifyStop.setEnabled(False)
        # Serial Parse
        self.btnSerialParseStart.clicked.connect(self.StartSerialParseThread)
        self.btnSerialParseStop.clicked.connect(self.EndSerialParseThread)
        self.btnSerialParseStop.setEnabled(False)
        # Hand Animation
        self.btnHandAnimateStart.clicked.connect(self.StartAnimateThread)
        self.btnHandAnimateStop.clicked.connect(self.EndAnimateThread)
        self.btnHandAnimateStop.setEnabled(False)
        # Plot Signals
        self.btnPlotSignalsStart.clicked.connect(self.StartPlotThread)
        self.btnPlotSignalsStop.clicked.connect(self.EndPlotThread)
        self.btnPlotSignalsStop.setEnabled(False)
    ## end of _initButtons

    def SetGestOutFile(self):
        """ Sets file name and opens a file used to save gesture data with a user-input gesture label. Outputs contents of file in GUI"""
        outFileName = self.lineEditFileOut.text()
        if outFileName == "":
            # Open QFileDialog to let user select a file if they did not type one in
            outFileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open/Create File")
            outFileName = outFileName[0]
        if outFileName:
            self.gestFileName = str(outFileName)
            self.lineEditFileOut.setText(self.gestFileName) #Show file name in GUI
            self.btnGestCap.setEnabled(True) # Enable Capture Gesture button
            # Display file contents
            outFile = open(self.gestFileName, 'r')
            with outFile:
                data = outFile.read()
                self.plainTextEditFileOut.setPlainText(data)
            outFile.close()
            QtWidgets.QMessageBox.information(self, "Gesture File", "Successfully created/loaded file to save gestures!")
    ## end of SetGestOutFile

    def CaptureGesture(self):
        """ Captures gesture to file with a user-input gesture identifier and flex, touch, quaternion sensor data """
        Tools.printHandDataToFile(self.gestFileName,self.lineEditGestCap.text())
    ## end of CaptureGesture

    def SetTrainFile(self):
        """ Sets file name and opens a file used to train machine learning classifiers. Outputs contents of file in GUI """
        inFileName = self.lineEditTrainFile.text()
        if inFileName == "":
            # Open QFileDialog to let user select a file if they did not type one in
            inFileName = QtWidgets.QFileDialog.getOpenFileName(self, "Load File")
            inFileName = inFileName[0]
        if inFileName:
            self.trainFileName = str(inFileName)
            self.lineEditTrainFile.setText(self.trainFileName) #Show file name in GUI
            self.btnTrainClassifier.setEnabled(True) #Enable Train Classifier Button
            self.lineEditTrainStatus.setText("Not Trained") #Show the classifier status
            # Display file contents
            inFile = open(self.trainFileName, 'r')
            with inFile:
                data = inFile.read()
                self.plainTextEditTrainFile.setPlainText(data)
            inFile.close()
            QtWidgets.QMessageBox.information(self, "Train File", "Successfully loaded file to train classifiers!")
    ## end of SetTrainFile

    def TrainClassifier(self):
        """ Trains the classifier using the training examples in "self.trainFileName" """
        signTarget, signFeatures = Tools.readHandDataFromFile(self.trainFileName)
        # Instantiate the SVM object
        self.clf = svm.SVC(C=1, kernel='rbf',gamma=0.0001,probability=True)
        self.clf_tree = tree.DecisionTreeClassifier() # decision tree version of classifier
        # Train the classifiers
        self.clf.fit(signFeatures,signTarget)
        self.clf_tree.fit(signFeatures,signTarget)
        self.lineEditTrainStatus.setText("Trained") #Show the classifier status
        self.btnClassifyStart.setEnabled(True) #Set the Classify Start button to enabled
        QtWidgets.QMessageBox.information(self, "Classifier", "Successfully trained classifier!")
    ## end of TrainClassifier

    def StartClassifyThread(self):
        """ Instantiates and runs a QThread class to perform the gesture classification continuously in real time """
        self.btnClassifyStart.setEnabled(False)
        self.btnClassifyStop.setEnabled(True)
        self.logFileIterator += 1
        delayClassifer = eval(self.lineEditClassRtDelay.text())
        debugFlag = self.checkBoxClassRTdebug.isChecked()
        ttsFlag = self.checkBoxTtoS.isChecked()
        # Instantiate QThread ClassifyThread object and pass trained SVM by reference???
        self.classifyThread = ClassifyRealTime(self.clf, delayClassifer, debugFlag, ttsFlag)
        # Connect signal sig_PredictedGest from ClassifyThread to UpdatePredictionDisplay
        self.classifyThread.sig_PredictedGest.connect(self.UpdatePredictionDisplay)
        self.classifyThread.start()
    ## end of StartClassifyThread

    def EndClassifyThread(self):
        """ Terminates Classify thread """
        self.classifyThread.terminate()
        self.btnClassifyStart.setEnabled(True)
        self.btnClassifyStop.setEnabled(False)
    ## end of EndClassifyThread

    def UpdatePredictionDisplay(self, predList):
        """ Updates GUI display after signal emitted by ClassifyRealTime thread indicating that a gesture has been predicted """
        if len(predList) == 1:
            # Only contains predicted label and no debug statistics
            self.plainTextEditClassRT.appendPlainText(predList[0])
        else:
            self.plainTextEditClassRT.appendPlainText(predList[0] + Tools.ListToCSstr(predList[1]))
        # Update log file
        self.LogSession(predList)
    ## end of UpdatePredictionDisplay

    def LogSession(self, predList):
        currentTime = time.strftime("%Y-%m-%d", time.localtime())
        logFileName = "Logs/" + currentTime + "-LogFile" + str(self.logFileIterator) + ".txt"
        outFile = open(logFileName, 'a+') #Open in append and create file if it does not exist
        outFile.seek(0) # Start of file
        if outFile.read() == "":
            outFile.write(time.asctime())
            outFile.write("\n")
            outFile.write("Classifier Training File: ")
            outFile.write(self.lineEditTrainFile.text())
            outFile.write("\n")
            outFile.write("Session Real-time Classification Log: \n")
        outFile.seek(2) # End of file
        featureStr = Tools.FlexMeanDataStr() + "," + Tools.TouchMeanBoolStr() + "," + Tools.QuatMeanDataStr()
        outFile.write("Feature Input: ")
        outFile.write(featureStr)
        outFile.write("\nPrediction: ")
        outFile.write(predList[0])
        if (len(predList) > 1):
            outFile.write("\nPrediction Probablity: ")
            outFile.write(Tools.ListToCSstr(predList[1]))
        outFile.write("\n")
        outFile.close
    ## end of LogSession

    def StartSerialParseThread(self):
        """ Instantiates and runs a QThread class to perform the serial data parsing continuously """
        self.btnSerialParseStart.setEnabled(False)
        self.btnSerialParseStop.setEnabled(True)
        # instanitate QThread SerialParseThread object
        self.serialParseThread = SerialParse()
        # Connect signal sig_UpdateData from SerialParse class thread to UpdateSensorDisplay method below
        self.serialParseThread.sig_UpdateData.connect(self.UpdateSensorDisplay)
        self.serialParseThread.start()
    ## end of StartSerialParseThread

    def EndSerialParseThread(self):
        """ Terminates SerialParse thread """
        # terminate thread
        self.serialParseThread.terminate()
        # enable start button and disable stop
        self.btnSerialParseStart.setEnabled(True)
        self.btnSerialParseStop.setEnabled(False)
    ## end of EndSerialParseThread

    def UpdateSensorDisplay(self):
        """ Updates GUI display after signal emitted by ParseSerial thread indiciating sensor values have been updated """
        # If box is checked, display the average of the moving window rather than instantaneuous values
        dataOutAvgFlag = self.checkBoxDataOutAvg.isChecked()
        for i in range(0,len(share_var.sensorCollectList)):
            for j in range(0, len(share_var.sensorCollectList[i])):
                if dataOutAvgFlag:
                    # Display mean of moving average stored in deques
                    mean = Tools.DequeMean(share_var.sensorCollectList[i][j])
                    self.sensorLineEdits[i][j].setText(str(mean))
                else:
                    # Display instataneuous values
                    self.sensorLineEdits[i][j].setText(str(share_var.sensorCollectList[i][j][-1]))
    ## end of UpdateSensorDisplay

    def StartAnimateThread(self):
        """ Instantiates and runs a QThread class to perform the hand animation """
        self.btnHandAnimateStart.setEnabled(False)
        self.btnHandAnimateStop.setEnabled(True)
        # Instanitate QThread animateHandThread object
        self.animateHandThread = HandAnimation()
        self.animateHandThread.start()
    ## end of StartAnimateThread

    def EndAnimateThread(self):
        """ Terminates Hand Animation Thread """
        # terminate thread
        self.animateHandThread.terminate()
        # enable start button and disable stop
        self.btnHandAnimateStart.setEnabled(True)
        self.btnHandAnimateStop.setEnabled(False)
    ## end of EndAnimateThread

    def StartPlotThread(self):
        """ Instantiates and runs a QThread class to perform real-time plotting of hand sensor signals """
        x=0
    ## end of StartPlotThread

    def EndPlotThread(self):
        """ Terminates Signal Plotting Thread """
        x=0
    ## end of StopPlotThread

## end of DevApp class


class SerialParse(QtCore.QThread):
    """ Threading class using QThread to perform parsing of serial data containing flex sensor, touch sensor, and IMU data """
    # Signal to communicate with main program class. signal will emit and run a method we connect it to in the main program class
    sig_UpdateData = QtCore.pyqtSignal()

    def __init__(self):
        super(SerialParse, self).__init__()

    def __del__(self):
        self.wait()

    ## rename "runTest" to "run" and rename "run" to "run1" in order to use the runTest method
    def runTest(self):
        """ Simple test for SerialParse threading, multidimensional lists of deque objects, and updating GUI without glove data """
        i = 0
        while True:
            for deq in share_var.flexCollectList:
                deq.append(i)
            for deq in share_var.touchCollectList:
                deq.append(2*i)
            for deq in share_var.accelCollectList:
                deq.append(3*i)
            for deq in share_var.quatCollectList:
                deq.append(4*i)
            for deq in share_var.eulerCollectList:
                deq.append(5*i)
            self.sig_UpdateData.emit()
            i += 1
            self.sleep(1)

    def run(self):
        """ Opens serial port and parses data. Emits signal to update GUI sensor display values after sensor data in share_var has been updated """
        ser = serial.Serial('COM3', 9600) # Bhavit's PORT
        #ser = serial.Serial('/dev/ttyACM0', 9600) #Bhavesh's PORT
        while True:
            line = ser.readline() #Read line until \n
            #print(line)
            HandsOn.parseLineData(line)
            self.sig_UpdateData.emit()
## end of SerialParse class


class ClassifyRealTime(QtCore.QThread):
    """ Threading class using QThread to perform real-time classification of hand gestures """
    # Signal to communicate with main program class. signal will emit and run a method we connect it to in the main program class
    sig_PredictedGest = QtCore.pyqtSignal(list)

    def __init__(self, trainedClassifier, delay, debugFlag, ttsFlag):
        super(ClassifyRealTime, self).__init__()
        self.clf = trainedClassifier
        self.delay = delay
        self.debugFlag = debugFlag
        self.ttsFlag = ttsFlag
        self._initTTS()

    def _initTTS(self):
        if self.ttsFlag:
            # Instantiate the text-to-speech engine
            self.engine = pyttsx.init()
            #espeak.set_voice('english-us','en-us') # 'Murica!
            #espeak.set_parameter(espeak.Parameter.Pitch,50) # medium pitch
            #espeak.set_parameter(espeak.Parameter.Rate,120) # decent speed

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            while Tools.isMoving():
                time.sleep(0.02)
            time.sleep(self.delay)
            # Organize features to be used for classifier prediction
            test = Tools.QuatMeanDataList()
            l = [x * 100 for x in test]
            featureList = Tools.FlexMeanDataList() + Tools.TouchMeanBoolList() + l
            #featureList = Tools.FlexMeanDataList() + Tools.TouchMeanBoolList() + Tools.QuatMeanDataList()
            gest = np.asarray(featureList)
            predictedGest = self.clf.predict(gest.reshape(1,-1)) # change to clf_tree for decision tree classfxn
            predictedGest = [predictedGest[0]] #convert from numpy array to list
            if self.debugFlag:
                predictedGestProba = self.clf.predict_proba(gest.reshape(1,-1)) # change to clf_tree for decision tree classfxn
                predictedGest = [predictedGest[0], predictedGestProba]
            self.sig_PredictedGest.emit(predictedGest) # Emit the predicted results to be displayed in GUI
            if self.ttsFlag:
                # Text to speech of output using espeak
                #espeak.synth(predictedGest[0])
                self.engine.say(predictedGest[0])
                #self.engine.setProperty('rate',150)
                self.engine.runAndWait()
## end of ClassifyRealTime class


class HandAnimation(QtCore.QThread):
    """ Threading class using QThread to perform hand animation using OpenGL """

    def __init__(self):
        super(HandAnimation, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        pygame.init()
        display = (800,800)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        # view angle, aspect ratio, z_near, z_far (z's are clipping planes)
        gluPerspective(90, 1, 1.0, 50.0)
        glTranslatef(0.0, 0.0, -20) # move cube away from screen (zoom out)
        glRotatef(0, 0, 0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # clear GL frame
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            # draw 3D hand
            Animation.drawHand()
            # refresh the frame
            pygame.display.flip()
## end of HandAnimation class

def main():
    app = QtWidgets.QApplication(sys.argv)    # New instance of QApplication
    form = DevApp()                 # We set the form to be our DevApp
    form.show()                     # Show the form
    app.exec_()                     # and execute the app

# If we're running the file directly and not importing, run the main function
if __name__ == '__main__':
    main()
