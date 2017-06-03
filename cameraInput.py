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
import main

class cameraInput(QWidget):
    def __init__(self, parent=None):
        super(cameraInput, self).__init__(parent)


        #first UI
        #initialize video choices
        self.checkBox1 = QRadioButton("IP Camera")
        self.checkBox1.setChecked(False)
        self.checkBox1.toggled.connect(lambda:self.btnstate(self.checkBox1))
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
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
        #add arguments for streaming
        self.minArea = QLabel("min-area", self)
        self.minAreaInput = QLineEdit(self)
        #self.minAreaInput.resize(280,40)
        self.minAreaInput.setEnabled(False)
        self.minAreaInput.setPlaceholderText('2000')
        #ap.add_argument("-min", "--min-area", type=int, default=2000, help="minimum area size")
    	#ap.add_argument("-max", "--max-area", type=int, default=4800, help="maximum area size")
    	#ap.add_argument("-small", "--small-buffer", type=int, default=20, help="buffer for small objects")
    	#ap.add_argument("-big", "--big-buffer", type=int, default=100, help="buffer for big objects")
    	#ap.add_argument("-ad", "--adaptive", type=int, default=0, help="minutes after adaptive")
    	#ap.add_argument("-am", "--adaptive-mode", type=bool, default=0, help="adaptive mod ON/OFF")
    	#ap.add_argument("-max-obj", "--max-objects", type=int, default=2, help="maximum number of objects in frame to be adapted")
    	#ap.add_argument("-w", "--win-width", type=int, default=500, help="maximum window width")
    	#ap.add_argument("-disp", "--display", default="y", help="Display window"

        buttonLayout1 = QHBoxLayout()
        buttonLayout1.addWidget(self.checkBox2)
        buttonLayout1.addWidget(self.videoButton)

        buttonLayout2 = QHBoxLayout()
        #buttonLayout2.addStretch(1)
        buttonLayout2.addWidget(self.checkBox1)
        buttonLayout2.addWidget(self.textbox)
        buttonLayout2.addWidget(self.ipButton)


        buttonLayout3MinArea = QHBoxLayout()
        buttonLayout3MinArea.addWidget(self.minArea)
        buttonLayout3MinArea.addWidget(self.minAreaInput)

        buttonLayout3OpenCam = QHBoxLayout()
        buttonLayout3OpenCam.addWidget(self.checkBox3)
        buttonLayout3OpenCam.addWidget(self.cameraChoice)


        buttonLayout3 = QVBoxLayout()
        buttonLayout3.addLayout(buttonLayout3OpenCam)
        buttonLayout3.addLayout(buttonLayout3MinArea)
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
        self.input.addLayout(buttonLayout1)
        self.input.addLayout(buttonLayout2)
        self.input.addLayout(buttonLayout3)

        self.setLayout(self.input)
        self.setWindowTitle("initialize Camera")
        self.show()

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
        main.main(self.fileName)


    def ipConnect(self):
        ipCamera.ip(self.ipWebcam)

    def link(self, text):
        #enable ipButton for connection with ip webacam
        self.ipButton.setEnabled(True)
        self.ipWebcam = text

    def cameraStream(self):
        #open pc webcam for streaming
        streamDisp.main()



if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    #initialize main window
    window = cameraInput()

    sys.exit(app.exec_())
