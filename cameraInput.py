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
        self.textbox.setPlaceholderText('Enter Link...')
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
        self.cameraChoice = QComboBox()
        self.cameraChoice.addItem("PC WebCam (0)")
        self.cameraChoice.addItem("External WebCam(1)")
        #add connections to items
        self.cameraChoice.setEnabled(False)

        buttonLayout1 = QHBoxLayout()
        buttonLayout1.addWidget(self.checkBox2)
        buttonLayout1.addWidget(self.videoButton)

        buttonLayout2 = QHBoxLayout()
        #buttonLayout2.addStretch(1)
        buttonLayout2.addWidget(self.checkBox1)
        buttonLayout2.addWidget(self.textbox)
        buttonLayout2.addWidget(self.ipButton)

        buttonLayout3 = QHBoxLayout()
        #buttonLayout3.addStretch(1)
        buttonLayout3.addWidget(self.checkBox3)
        buttonLayout3.addWidget(self.cameraChoice)
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

    def ipConnect(self):
        pass

    def link(self, text):
        print text



if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    #initialize main window
    window = cameraInput()

    sys.exit(app.exec_())
