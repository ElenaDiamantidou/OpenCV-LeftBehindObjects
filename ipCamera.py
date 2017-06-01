import urllib
import cv2
import numpy as np

def ip(ipString):
    print ipString
    #define url camera
    url = 'http://' + ipString + '/shot.jpg'
    #url = 'http://192.168.1.13:8080/shot.jpg'
    print url

    #refresh image using while loop
    while True:
        #open url image
        imgUrl = urllib.urlopen(url)
        #convert to numpy
        imgNp = np.array(bytearray(imgUrl.read()),dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        print img
        cv2.imshow('testIPCamera', img)
        cv2.waitKey(10)
        if ord('q') == cv2.waitKey(10):
            exit(0)
