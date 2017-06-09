#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import imutils

#PyQT5 Libraries
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

#OpenCV Libraries
import cv2

#python files
import ipCamera
import streamDisp
import videoDisp

class cameraInput(QWidget):
    def __init__(self, parent=None):
        super(cameraInput, self).__init__(parent)
        self.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.center()
        #first UI
        #initialize video choices
        self.checkBox1 = QRadioButton("IP Camera")
        self.checkBox1.setChecked(False)
        self.checkBox1.toggled.connect(lambda:self.btnstate(self.checkBox1))
        self.textbox = QLineEdit(self)
        self.textbox.setEnabled(False)
        self.textbox.setPlaceholderText('Enter IP...')
        self.textbox.textChanged.connect(self.link)
        self.ipButton = QPushButton("Connect IP")
        self.ipButton.clicked.connect(self.ipConnect)
        self.ipButton.setEnabled(False)

        #default enadle video input
        self.checkBox2 = QRadioButton("Video")
        self.checkBox2.setChecked(True)
        self.checkBox2.toggled.connect(lambda:self.btnstate(self.checkBox2))
        self.videoButton = QPushButton("Browse Video...")
        self.videoButton.clicked.connect(self.browse)

        self.checkBox3 = QRadioButton("Camera")
        self.checkBox3.setChecked(False)
        self.checkBox3.toggled.connect(lambda:self.btnstate(self.checkBox3))
        self.cameraChoice = QPushButton("Open PC Camera")
        self.cameraChoice.clicked.connect(self.cameraStream)
        self.cameraChoice.setEnabled(False)

        #Horizontal Line for split
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setLineWidth(3)

        #add arguments for streaming
        #minimum area size
        self.minArea = QLabel("min-area", self)
        self.minAreaInput = QLineEdit(self)
        self.minAreaInput.resize(20,20)
        self.minAreaInput.setText('2000')
        self.minAreaValue = self.minAreaInput.text()
        self.minAreaInput.textChanged.connect(self.minAreaInputChange)
        #maximum area size
        self.maxArea = QLabel("max-area", self)
        self.maxAreaInput = QLineEdit(self)
        self.maxAreaInput.setText('4800')
        self.maxAreaValue = self.maxAreaInput.text()
        self.maxAreaInput.textChanged.connect(self.maxAreaInputChange)
        #buffer for small objects
        self.smalBuffer = QLabel("small-buffer", self)
        self.smallBufferInput = QLineEdit(self)
        self.smallBufferInput.setText('20')
        self.smallBufferValue = self.smallBufferInput.text()
        self.smallBufferInput.textChanged.connect(self.smallBufferInputChange)
        #buffer for big objects
        self.bigBuffer = QLabel("big-buffer", self)
        self.bigBufferInput = QLineEdit(self)
        self.bigBufferInput.setText('100')
        self.bigBufferValue = self.bigBufferInput.text()
        self.bigBufferInput.textChanged.connect(self.bigBufferInputChange)
        #minutes after adaptive
        self.adaptive = QLabel("adaptive", self)
        self.adaptiveInput = QLineEdit(self)
        self.adaptiveInput.setText('0')
        self.adaptiveValue = self.adaptiveInput.text()
        self.adaptiveInput.textChanged.connect(self.adaptiveInputChange)
        #adaptive mod ON/OFF
        self.adaptiveMode = QLabel("adaptive-mode", self)
        self.adaptiveModeInput = QCheckBox(self)
        self.adaptiveModeInput.setChecked(True)
        self.adaptiveModeValue = True
        self.adaptiveModeInput.stateChanged.connect(self.adaptiveModeChange)
        #maximum number of objects in frame to be adapted
        self.maxObj = QLabel("max-obj", self)
        self.maxObjInput = QLineEdit(self)
        self.maxObjInput.setText('2')
        self.maxObjValue = self.maxObjInput.text()
        self.maxObjInput.textChanged.connect(self.maxObjInputChange)
        #maximum window width
        self.winWidth = QLabel("window-width", self)
        self.winWidthInput = QLineEdit(self)
        self.winWidthInput.setText('500')
        self.winWidthValue = self.winWidthInput.text()
        self.winWidthInput.textChanged.connect(self.winWidthInputChange)
        #Display window
        self.disp = QLabel("display-window", self)
        self.dispInput = QCheckBox(self)
        self.dispInput.setChecked(True)
        self.dispInputValue = True
        self.dispInput.stateChanged.connect(self.dispInputChange)

    	#ap.add_argument("-w", "--win-width", type=int, default=500, help="maximum window width")
    	#ap.add_argument("-disp", "--display", default="y", help="Display window"

        buttonLayout1 = QHBoxLayout()
        buttonLayout1.addWidget(self.checkBox2)
        buttonLayout1.addWidget(self.videoButton)

        buttonLayout2 = QHBoxLayout()
        buttonLayout2.addWidget(self.checkBox1)
        buttonLayout2.addWidget(self.textbox)
        buttonLayout2.addWidget(self.ipButton)


        buttonLayout3Area = QHBoxLayout()
        #buttonLayout3Area..setAlignment(Qt.AlignCenter)
        buttonLayout3Area.addWidget(self.minArea)
        buttonLayout3Area.addWidget(self.minAreaInput)
        buttonLayout3Area.addWidget(self.maxArea)
        buttonLayout3Area.addWidget(self.maxAreaInput)

        buttonLayout3Buffer = QHBoxLayout()
        buttonLayout3Buffer.addWidget(self.smalBuffer)
        buttonLayout3Buffer.addWidget(self.smallBufferInput)
        buttonLayout3Buffer.addWidget(self.bigBuffer)
        buttonLayout3Buffer.addWidget(self.bigBufferInput)

        buttonLayout3Adaptive = QHBoxLayout()
        buttonLayout3Adaptive.addWidget(self.adaptive)
        buttonLayout3Adaptive.addWidget(self.adaptiveInput)

        buttonLayout3CheckBox = QHBoxLayout()
        buttonLayout3CheckBox.addWidget(self.adaptiveMode)
        buttonLayout3CheckBox.addWidget(self.adaptiveModeInput)
        buttonLayout3CheckBox.addWidget(self.disp)
        buttonLayout3CheckBox.addWidget(self.dispInput)

        buttonLayout3Objects = QHBoxLayout()
        buttonLayout3Objects.addWidget(self.maxObj)
        buttonLayout3Objects.addWidget(self.maxObjInput)
        buttonLayout3Objects.addWidget(self.winWidth)
        buttonLayout3Objects.addWidget(self.winWidthInput)


        buttonLayout3OpenCam = QHBoxLayout()
        buttonLayout3OpenCam.addWidget(self.checkBox3)
        buttonLayout3OpenCam.addWidget(self.cameraChoice)


        buttonLayout3 = QVBoxLayout()
        buttonLayout3.addLayout(buttonLayout3OpenCam)
        buttonLayout3.addWidget(self.line)
        buttonLayout3.addLayout(buttonLayout3Area)
        buttonLayout3.addLayout(buttonLayout3Buffer)
        buttonLayout3.addLayout(buttonLayout3Adaptive)
        buttonLayout3.addLayout(buttonLayout3CheckBox)
        buttonLayout3.addLayout(buttonLayout3Objects)
        #buttonLayout3.addLayout(buttonLayout3Main)
        #buttonLayout3.addLayout(buttonLayout3Modify)

        '''
        self.choice = QButtonGroup()
        self.choice.setExclusive(True)
        self.choice.addButton(self.checkBox1)
        self.choice.addButton(self.checkBox2)
        self.choice.addButton(self.checkBox3)
        '''

        self.input = QVBoxLayout()
        self.input.setAlignment(Qt.AlignCenter)
        self.input.addLayout(buttonLayout1)
        self.input.addLayout(buttonLayout2)
        self.input.addLayout(buttonLayout3)

        self.setLayout(self.input)
        self.setWindowTitle("initialize Camera")
        self.show()

    ### Values Change in arguments _ Handle Connections ###
    def minAreaInputChange(self, text):
        self.minAreaValue = text

    def maxAreaInputChange(self, text):
        self.maxAreaValue = text

    def smallBufferInputChange(self, text):
        self.smallBufferValue = text

    def bigBufferInputChange(self, text):
        self.bigBufferValue = text

    def adaptiveInputChange(self, text):
        self.adaptiveValue = text

    def adaptiveModeChange(self):
        if self.adaptiveModeInput.isChecked():
            self.adaptiveModeValue = True
        else:
            self.adaptiveModeValue = False

    def maxObjInputChange(self, text):
        self.maxObjValue = text

    def winWidthInputChange(self, text):
        self.winWidthValue = text

    def dispInputChange(self):
        if self.dispInput.isChecked():
            self.dispInputValue = True
        else:
            self.dispInputValue = False

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btnstate(self,b):
        if b.text() == "Video":
            #Enable Video input
            self.videoButton.setEnabled(True)
            self.cameraChoice.setEnabled(False)
            self.textbox.setEnabled(False)
            self.ipButton.setEnabled(False)

        if b.text() == "Camera":
            #Enable Camera input
            self.videoButton.setEnabled(False)
            self.cameraChoice.setEnabled(True)
            self.textbox.setEnabled(False)
            self.ipButton.setEnabled(False)

            '''
            cap = cv2.VideoCapture(0)

            while(True):
                # Capture frame-by-frame
                ret, frame = cap.read()

                # Our operations on the frame come here
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Display the resulting frame
                cv2.imshow('frame',gray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()
            '''

        if b.text() == "IP Camera":

            #Enable IP Camera/Video input
            self.videoButton.setEnabled(False)
            self.cameraChoice.setEnabled(False)
            self.textbox.setEnabled(True)
            self.ipButton.setEnabled(False)


    ''' BTN CONNECTIONS '''
    def browse(self):
        #"(*.avi) for browse filter"
        fileName,_ =  QFileDialog.getOpenFileName(self, "Open Video File ", QDir.currentPath())
        print fileName
        self.fileName = fileName
        #open main with vieo input
        videoDisp.main(self.fileName,
                  self.minAreaValue, self.maxAreaValue,
                  self.smallBufferValue, self.bigBufferValue,
                  self.adaptiveValue, self.adaptiveModeValue,
                  self.maxObjValue, self.winWidthValue, self.dispInputValue)


    def ipConnect(self):
        ipCamera.ip(self.ipWebcam,
                    self.minAreaValue, self.maxAreaValue,
                    self.smallBufferValue, self.bigBufferValue,
                    self.adaptiveValue, self.adaptiveModeValue,
                    self.maxObjValue, self.winWidthValue, self.dispInputValue)

    def link(self, text):
        #enable ipButton for connection with ip webacam
        self.ipButton.setEnabled(True)
        self.ipWebcam = text

    def cameraStream(self):
        #open pc webcam for streaming
        streamDisp.main(self.minAreaValue, self.maxAreaValue,
                        self.smallBufferValue, self.bigBufferValue,
                        self.adaptiveValue, self.adaptiveModeValue,
                        self.maxObjValue, self.winWidthValue, self.dispInputValue)
        #print self.minAreaValue, self.maxAreaValue, self.smallBufferValue, self.bigBufferValue
        #print self.adaptiveModeValue



if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    #initialize main window
    window = cameraInput()

    sys.exit(app.exec_())
