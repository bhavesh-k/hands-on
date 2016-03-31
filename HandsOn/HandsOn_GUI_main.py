import sys 
from PyQt5 import QtCore, QtGui, QtWidgets # Import Qt main modules
import HandsOn_GUI_Layout # Imports our designed .ui layout that was converted to .py

class DevApp(QtWidgets.QMainWindow, HandsOn_GUI_Layout.Ui_MainWindow):
    
 
    def __init__(self):
        # Super to access variables, methods, etc in HandsOn_GUI_Layout.py
        super(self.__class__, self).__init__()
        self.setupUi(self)  # Defined in HandsOn_GUI_Layout.py automatically. Sets up layout and widgets that are defined
        self.btnFileOut.clicked.connect(self.SetOutFile)
        self.btnTrainFile.clicked.connect(self.SetTrainFile)


    def SetOutFile(self):
        outFileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open/Create File")
        self.lineEditFileOut.setText(str(outFileName[0]))
        self.lineEditFileOut.setReadOnly(True)
        if outFileName[0]:
            outFile = open(str(outFileName[0]), 'r')
            with outFile:
                data = outFile.read()
                self.plainTextEditFileOut.setPlainText(data)
        outFile.close()
    
    def SetTrainFile(self):
        inFileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open/Create File")
        self.lineEditTrainFile.setText(str(inFileName[0]))
        self.lineEditTrainFile.setReadOnly(True)
        if inFileName[0]:
            inFile = open(str(inFileName[0]), 'r')
            with inFile:
                data = inFile.read()
                self.plainTextEditTrainFile.setPlainText(data)
            inFile.close()

def main():
    app = QtWidgets.QApplication(sys.argv)    # New instance of QApplication
    form = DevApp()                 # We set the form to be our DevApp
    form.show()                     # Show the form
    app.exec_()                     # and execute the app

# If we're running the file directly and not importing, run the main function
if __name__ == '__main__':
    main()

