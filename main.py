# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import time
import threading
import psutil
import sys
import logging

#Calculates the CPU usage using a thread, the thread needs to be handled when closing
#Not in use for now
def cpu_percent():
	threading.Timer(5.0, cpu_percent).start()
	cpu_percentage = psutil.cpu_percent(interval=1)
	print "CPU : {0}".format(cpu_percentage)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-min", "--min-area", type=int, default=2000, help="minimum area size")
ap.add_argument("-max", "--max-area", type=int, default=4800, help="maximum area size")
ap.add_argument("-small", "--small-buffer", type=int, default=20, help="buffer for small objects")
ap.add_argument("-big", "--big-buffer", type=int, default=100, help="buffer for big objects")
ap.add_argument("-ad", "--adaptive", type=int, default=0, help="minutes after adaptive")
ap.add_argument("-max-obj", "--max-objects", type=int, default=2, help="maximum number of objects in frame to be adapted")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	# camera = cv2.VideoCapture("http://axilleas:79c87afa55@83.212.104.135:8080/4.MOV")
	#camera = cv2.VideoCapture("http://::192.168.2.2:8080/")
	time.sleep(0.25)

# we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

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
adaptive = args["adaptive"] * 60 * fps
adaptive_flag = False

#Lists for storing x-y coordinates of a "small" tracked object
x_list = []
y_list = []
#Lists for storing x-y coordinates of a "big" tracked object
big_item_x_list = []
big_item_y_list = []
#list for contours
cnts_list = []
#cpu_percent()
start = time.time()
width = 500
# loop over the frames of the video
while True:
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
	frame = imutils.resize(frame, width)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
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
		if cv2.contourArea(c) < args["min_area"]:
			continue
		elif cv2.contourArea(c) > args["min_area"] and cv2.contourArea(c) < args["max_area"]:

			(x, y, w, h) = cv2.boundingRect(c)
			#print len(cnts)
			if len(cnts_list) < 10:
				cnts_list.append(len(cnts))
				#print cnts_list
			else:
				#print "In else"
				cnts_list.pop(0)
				cnts_list.append(len(cnts))
				#print cnts_list

				if (max(cnts_list) - min(cnts_list) == 0 ):
							cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #GREEN
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

			if len(big_item_x_list) < args["big_buffer"] and len(big_item_y_list)<args["big_buffer"]:
				big_item_x_list.append(x)
				big_item_y_list.append(y)
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) #RED
				adaptive_flag = False
			else:
				big_item_x_list.pop(0)
				big_item_y_list.pop(0)
				big_item_x_list.append(x)
				big_item_y_list.append(y)

				if (max(big_item_x_list) - min(big_item_x_list) > 3) and (max(big_item_y_list) - min(big_item_y_list) >3):
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) #RED
					adaptive_flag = False
				else:
					cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #GREEN
					adaptive_flag = True
					adaptive_frames_counter += 1
					#print adaptive_frames_counter


	cv2.putText(frame, "FPS: {0}".format(fps), (width-130,30), font, 1, (255,0,0), 2, cv2.LINE_AA)
	frames_counter = frames_counter + 1

	adaptive_flag = False
	if adaptive_frames_counter >= 100 and len(cnts) <= args["max_objects"] and adaptive_flag == True:
		firstFrame = None
		adaptive_frames_counter = 0
		#print "I'm in"
	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	#cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
#sys.exit(qApp.exec_())
