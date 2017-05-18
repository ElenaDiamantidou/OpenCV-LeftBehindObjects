import urllib
import cv2
import numpy as np

#define url camera
url = 'http://192.168.1.17:8080/shot.jpg'

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
