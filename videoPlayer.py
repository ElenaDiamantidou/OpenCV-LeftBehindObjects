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
class VideoWidgetSurface(QAbstractVideoSurface):

    def __init__(self, widget, parent=None):
        super(VideoWidgetSurface, self).__init__(parent)
        self.widget = widget
        self.imageFormat = QImage.Format_Invalid
        global frameCounter
        frameCounter = 0 #Frame Counter initialize

    def supportedPixelFormats(self, handleType=QAbstractVideoBuffer.NoHandle):
        formats = [QVideoFrame.PixelFormat()]
        if (handleType == QAbstractVideoBuffer.NoHandle):
            for f in [QVideoFrame.Format_RGB32, QVideoFrame.Format_ARGB32, QVideoFrame.Format_ARGB32_Premultiplied, QVideoFrame.Format_RGB565, QVideoFrame.Format_RGB555,QVideoFrame.Format_BGR24,QVideoFrame.Format_RGB24]:
                formats.append(f)
        return formats

    def isFormatSupported(self, _format):
        imageFormat = QVideoFrame.imageFormatFromPixelFormat(_format.pixelFormat())
        size = _format.frameSize()
        _bool = False
        if (imageFormat != QImage.Format_Invalid and not size.isEmpty() and _format.handleType() == QAbstractVideoBuffer.NoHandle):
            _bool = True
        return _bool

    def start(self, _format):
        imageFormat = QVideoFrame.imageFormatFromPixelFormat(_format.pixelFormat())
        size = _format.frameSize()
        #frameCounter = 0 #Frame Counter initialize
        if (imageFormat != QImage.Format_Invalid and not size.isEmpty()):
            self.imageFormat = imageFormat
            self.imageSize = size
            self.sourceRect = _format.viewport()
            QAbstractVideoSurface.start(self, _format)
            self.widget.updateGeometry()
            self.updateVideoRect()
            return True
        else:
            return False

    def stop(self):
        self.currentFrame = QVideoFrame()
        self.targetRect = QRect()
        QAbstractVideoSurface.stop(self)

        self.widget.update()

    def present(self, frame):
        global frameCounter,removeBool
        if (self.surfaceFormat().pixelFormat() != frame.pixelFormat() or self.surfaceFormat().frameSize() != frame.size()):
            self.setError(QAbstractVideoSurface.IncorrectFormatError)
            self.stop()
            return False
        else:
            self.currentFrame = frame
            frameCounter += 1
            removeBool = True #Removes the boxes on current frame
            self.widget.repaint(self.targetRect)
            return True

    def videoRect(self):
        return self.targetRect

    def updateVideoRect(self):
        size = self.surfaceFormat().sizeHint()
        size.scale(self.widget.size().boundedTo(size), Qt.KeepAspectRatio)
        self.targetRect = QRect(QPoint(0, 0), size);
        self.targetRect.moveCenter(self.widget.rect().center())

    def paint(self, painter):
        if (self.currentFrame.map(QAbstractVideoBuffer.ReadOnly)):
            oldTransform = painter.transform()
            if (self.surfaceFormat().scanLineDirection() == QVideoSurfaceFormat.BottomToTop):
                painter.scale(1, -1);
                painter.translate(0, -self.widget.height())

            image = QImage(self.currentFrame.bits(),
                    self.currentFrame.width(),
                    self.currentFrame.height(),
                    self.currentFrame.bytesPerLine(),
                    self.imageFormat
            )

            painter.drawImage(self.targetRect, image, self.sourceRect)
            painter.setTransform(oldTransform)

            self.currentFrame.unmap()

class VideoWidget(QWidget):

    def __init__(self, parent=None):
        global classLabels, imageBuffer
        super(VideoWidget, self).__init__(parent)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        palette = self.palette()
        palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(palette)
        self.setSizePolicy(QSizePolicy.MinimumExpanding ,
        QSizePolicy.MinimumExpanding)
        self.surface = VideoWidgetSurface(self)

        classLabels = []
        highLabels = []
        imageBuffer = []

    def videoSurface(self):
        return self.surface


class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        #initialize video player window
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        try:
            #DEFINE PLAYER-PLAYLIST
            #----------------------
            pass
        except:
            pass
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("/home/ediamant/Documents/myProjects/OpenCV-LeftBehindObjects/5.MOV")))
        self.videoWidget = VideoWidget()
        self.videoWidget.setFixedSize(640, 480)

        #player buttons
        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        #video slider
        self.positionSlider = QSlider(Qt.Horizontal)
        #self.positionSlider.setRange(0,x)
        self.positionSlider.setMinimum(0)
        #self.positionSlider.setMaximum()
        self.positionSlider.setTickInterval(1)
        #self.positionSlider.sliderMoved.connect(self.setPosition)

        self.controlLayout = QHBoxLayout()
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)
        self.controlLayout.setAlignment(Qt.AlignLeft)
        #self.controlLayout.addStretch(1)

        videoLayout = QVBoxLayout()
        #videoLayout.addStretch(1)
        videoLayout.addWidget(self.videoWidget)
        videoLayout.addLayout(self.controlLayout)
        self.setLayout(videoLayout)

        self.mediaPlayer.setVideoOutput(self.videoWidget.videoSurface())
        self.setWindowTitle("Player")
        self.show()

    def play(self):
        print 'play'
        self.time_ = self.mediaPlayer.position()
        self.mediaPlayer.play()
        '''
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.videoPosition()
            self.mediaPlayer.pause()
            self.time_ = self.positionSlider

        else:
            pass
        '''
    def mediaStateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    #initialize main window
    player = VideoPlayer()

    sys.exit(app.exec_())
