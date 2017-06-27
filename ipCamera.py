import urllib
import cv2
import numpy as np


def cpu_percent():
    threading.Timer(5.0, cpu_percent).start()
    cpu_percentage = psutil.cpu_percent(interval=1)
    print "CPU : {0}".format(cpu_percentage)

def ip(ipString,
        minAreaValue,maxAreaValue,
	  	smallBufferValue, bigBufferValue,
		adaptiveValue, adaptiveModeValue,
		maxObjValue, winWidthValue, dispInputValue):

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

    	# if the video argument is None, then we are reading from webcam
    	camera = cv2.VideoCapture(img)
    	time.sleep(0.25)

    	# initialize the first frame
    	firstFrame = None

    	# Find OpenCV version
    	(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    	if int(major_ver)  < 3 :
    		fps = camera.get(cv2.cv.CV_CAP_PROP_FPS)
    	        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS):{0}".format(fps)
    	else :
    		fps = camera.get(cv2.CAP_PROP_FPS)
    	        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)

    	font = cv2.FONT_HERSHEY_SIMPLEX

    	#Variable for the counting of the frames
    	frames_counter = 0
    	adaptive_frames_counter = 0
    	adaptive = int(adaptiveValue) * 60 * fps
    	adaptive_flag = False
    	(grabbed, original_frame) = camera.read()
    	original_frame = imutils.resize(original_frame, int(winWidthValue))
    	original_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
    	original_gray = cv2.GaussianBlur(original_gray, (21, 21), 0)
    	#print original_gray[183:235,369:421]
    	#cv2.imshow("Da OG", original_frame[183:209,369:441])
    	#Lists for storing x-y coordinates of a "small" tracked object

    	log_flag = True

    	x_list = []
    	y_list = []
    	#Lists for storing x-y coordinates of a "big" tracked object
    	big_item_x_list = []
    	big_item_y_list = []
    	#list for contours
    	cnts_list = []
    	#cpu_percent()
    	start = time.time()
    	# loop over the frames of the video
		# grab the current frame and initialize the occupied/unoccupied
        (grabbed, frame) = camera.read()

		# end of the video
        if not grabbed:
        	break


        #Fps counting
        if frames_counter == 10:
        	end = time.time()
        	seconds = end - start
    		# Calculate frames per second
    		fps  = int (frames_counter / seconds)
        	#cpu_percent = psutil.cpu_percent(interval=1)
        	frames_counter = 0
        	start = time.time()

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, int(winWidthValue))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None and adaptive_flag == False:
        	firstFrame = original_gray
        	continue
        elif firstFrame is None:
        	firstFrame = gray
        	continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (thresh,cnts, _) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #print len(cnts)
        # loop over the contours
        for c in cnts:
        	# if the contour is too small, ignore it
        	if cv2.contourArea(c) < minAreaValue:
        		continue
        	elif cv2.contourArea(c) > maxAreaValue and cv2.contourArea(c) < minAreaValue:

        		(x, y, w, h) = cv2.boundingRect(c)
        		#print len(cnts)
        		if len(cnts_list) < 15:
        			cnts_list.append(len(cnts))
        			#print cnts_list
        		else:
        			#print "In else"
        			cnts_list.pop(0)
        			cnts_list.append(len(cnts))
        			#print cnts_list

        			if (max(cnts_list) - min(cnts_list) == 0 ):
        						cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #GREEN

        						adaptive_frames_counter += 1
        						adaptive_flag = True
        						#break

        		# if len(x_list) < args["small_buffer"] and len(y_list)<args["small_buffer"]:
        		# 	x_list.append(x)
        		# 	y_list.append(y)
        		# 	cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        		# 	adaptive_flag = False
        		# else:
        		# 	x_list.pop(0)
        		# 	y_list.pop(0)
        		# 	x_list.append(x)
        		# 	y_list.append(y)
        		# 	#print "X: "+str(x)+" Y: "+str(y)
        		#
        		# 	if (max(x_list) - min(x_list) > 3) and (max(y_list) - min(y_list) >3):
        		# 		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #BLUE
        		# 		adaptive_flag = False
        		# 	else:
        		# 		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #GREEN
        		# 		adaptive_flag = True
        		# 		adaptive_frames_counter += 1
        		# 		#print adaptive_frames_counter
        		# 		#logging.basicConfig(filename='example.log',level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        		# 		#logging.warning(' -> '+str(len(cnts))+' Object(s) left behind.')
        	else:
        		(x, y, w, h) = cv2.boundingRect(c)

        		#if len(big_item_x_list) < args["big_buffer"] and len(big_item_y_list)<args["big_buffer"]:
        		if len(big_item_x_list) < int(bigBufferValue) and len(big_item_y_list) < int(bigBufferValue):
        			big_item_x_list.append(x)
        			big_item_y_list.append(y)
        			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) #RED
        			adaptive_flag = False
        			adaptive_frames_counter = 0
        		else:
        			big_item_x_list.pop(0)
        			big_item_y_list.pop(0)
        			big_item_x_list.append(x)
        			big_item_y_list.append(y)

        			if (max(big_item_x_list) - min(big_item_x_list) > 3) and (max(big_item_y_list) - min(big_item_y_list) >3):
        				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) #RED
        				adaptive_flag = False
        				adaptive_frames_counter = 0
        			else:
        				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #GREEN
        				adaptive_flag = True
        				adaptive_frames_counter += 1
        				#print adaptive_frames_counter

        cv2.putText(frame, "FPS: {0}".format(fps), (int(winWidthValue)-130,30), font, 1, (255,0,0), 2, cv2.LINE_AA)
        frames_counter = frames_counter + 1

        # if args["adaptive"] == True:
        # 	#adaptive_flag = False
        # args["max_objects"] = 2
        if adaptive_frames_counter >= 100 and len(cnts) <= int(maxObjValue) and adaptive_flag == True:
        	firstFrame = None
        	adaptive_frames_counter = 0
        	#print "X: "+str(x)+" Y: "+str(y)+" h: "+str(h)+" w: "+str(w)
        	#cv2.imshow("Test", frame[(y+3):(y+h-3),(x+3):(x+w-3)])
        	#cv2.imshow("OG - Test", original_frame[(y+3):(y+h-3),(x+3):(x+w-3)])
        	frameDelta = cv2.absdiff(cv2.cvtColor(original_frame[(y+3):(y+h-3),(x+3):(x+w-3)], cv2.COLOR_BGR2GRAY), cv2.cvtColor(frame[(y+3):(y+h-3),(x+3):(x+w-3)], cv2.COLOR_BGR2GRAY))
        	if max(frameDelta.flatten()) > 20:
        		#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #GREEN
        		logging.basicConfig(filename='Security_feed.log',level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        		logging.warning(' -> '+str(len(cnts))+' Object(s) left behind.')
        	else:
        		print "No need for logging"

        		#print "I'm in"
        	# show the frame and record if the user presses a key
        	if dispInputValue == True:
        		cv2.imshow("Security Feed", frame)

        #cv2.imshow('testIPCamera', img)
        cv2.waitKey(10)
        if ord('q') == cv2.waitKey(10):
            exit(0)
