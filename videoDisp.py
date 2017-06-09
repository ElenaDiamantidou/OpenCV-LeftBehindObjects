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

def main(video,
		minAreaValue,maxAreaValue,
	  	smallBufferValue, bigBufferValue,
		adaptiveValue, adaptiveModeValue,
		maxObjValue, winWidthValue, dispInputValue):

	camera = cv2.VideoCapture(video)

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
	#adaptive = args["adaptive"] * 60 * fps
	adaptive = 0
	adaptive_flag = False
	(grabbed, original_frame) = camera.read()
	original_frame = imutils.resize(original_frame, 500) #args["win_width"]
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
		frame = imutils.resize(frame, 500) #args["win_width"])
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
			if cv2.contourArea(c) < 2000: #args["min_area"]:
				continue
			elif cv2.contourArea(c) > 2000 and cv2.contourArea(c) < 4800:#args["min_area"] and cv2.contourArea(c) < args["max_area"]:

				(x, y, w, h) = cv2.boundingRect(c)
				#print len(cnts)
				if len(cnts_list) < 20:
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
				if len(big_item_x_list) < 100 and len(big_item_y_list) < 100:
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

		#args["win_width"] = 500
		cv2.putText(frame, "FPS: {0}".format(fps), (500-130,30), font, 1, (255,0,0), 2, cv2.LINE_AA)
		frames_counter = frames_counter + 1

		# if args["adaptive"] == True:
		# 	#adaptive_flag = False
		# args["max_objects"] = 2
		if adaptive_frames_counter >= 100 and len(cnts) <= 2 and adaptive_flag == True:
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
		#if args["display"] == "y":
		cv2.imshow("Security Feed", frame)

		#cv2.imshow("Thresh", thresh)
		#cv2.imshow("Frame Delta", frameDelta)
		#cv2.imshow("Da OG", original_frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break

		time.sleep(0.009)

	# cleanup the camera and close any open windows
	camera.release()
	cv2.destroyAllWindows()
	#sys.exit(qApp.exec_())

	# import numpy as np
	# import cv2
	# import Tkinter as tk
	# from PIL import Image, ImageTk
	#
	# #Set up GUI
	# window = tk.Tk()  #Makes main window
	# window.wm_title("Digital Microscope")
	# window.config(background="#FFFFFF")
	#
	# #Graphics window
	# imageFrame = tk.Frame(window, width=600, height=500)
	# imageFrame.grid(row=0, column=0, padx=10, pady=2)
	#
	# #Capture video frames
	#
	# #cap = cv2.VideoCapture(0)
	# cap = cv2.VideoCapture("~/Documents/Vm\ Shared/5.MOV")
	#
	# def show_frame():
	#     _, frame = cap.read()
	#     frame = cv2.flip(frame, 1)
	#     #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	#     img = Image.fromarray(frame)
	#     imgtk = ImageTk.PhotoImage(image=img)
	#     display1.imgtk = imgtk #Shows frame for display 1
	#     display1.configure(image=imgtk)
	#     #display2.imgtk = imgtk #Shows frame for display 2
	#     #display2.configure(image=imgtk)
	#     window.after(10, show_frame)
	#
	# display1 = tk.Label(imageFrame)
	# display1.grid(row=1, column=0, padx=10, pady=2)  #Display 1
	# #display2 = tk.Label(imageFrame)
	# #display2.grid(row=0, column=0) #Display 2
	#
	# #Slider window (slider controls stage position)
	# sliderFrame = tk.Frame(window, width=600, height=100)
	# sliderFrame.grid(row = 600, column=0, padx=10, pady=2)
	#
	#
	# show_frame() #Display
	# window.mainloop()  #Starts GUI
