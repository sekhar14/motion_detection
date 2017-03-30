import argparse 
import datetime
import imutils
import time
import cv2


#print "all setup"

camera = cv2.VideoCapture(0)
time.sleep(0.30)

firstFrame = None

while True:
	g,frame = camera.read()
	text = "Motion detected"

	if not g:
		print("can't get hold of camera")
		break

	frame = imutils.resize(frame,width=500)
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(21,21),0)

	
	if firstFrame is None:
		firstFrame = gray
		continue

	diff = cv2.absdiff(firstFrame,gray)
	thresh_hold = cv2.threshold(diff,25,255,cv2.THRESH_BINARY)[1]

	thresh_hold = cv2.dilate(thresh_hold,None,iterations=2)
	_ ,cnts, _ = cv2.findContours(thresh_hold.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	for c in cnts:
		x,y,w,h = cv2.boundingRect(c)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
		print("rect drawn")
		cv2.putText(frame,"motion",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
		print("text drawn")
		cv2.imshow("detection window",frame)
		#cv2.imshow("Thresh",thresh_hold)
		#cv2.imshow("delt")
		key = cv2.waitKey(1) 
		if key == ord('q'):
			break
