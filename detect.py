import datetime
import imutils
import time
import cv2



camera =  cv2.VideoCapture(0)
time.sleep(0.25)

first_frame = None

print("good")

while True:
	(grabbed, frame) = camera.read()
	text = "Unoccupied"
	'''
	if not grabbed:
		print("this case")
		break
	'''

	frame = imutils.resize(frame, width = 500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21,21), 0)


	if first_frame is None:
		first_frame = gray
		continue

	frame_delta = cv2.absdiff(first_frame, gray)
	thresh =  cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

	thresh = cv2.dilate(thresh, None, iteration=2)
	_,cnts,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in cnts:
		if cv2.contourArea(c) < 500:
			continue

		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

		cv2.putText(frame, "Room Status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		cv2.imshow("Security feed", frame)
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame delta", frame_delta)

		key = cv2.waitKey(1) & 0xFF

		if key == ord('q'):
			break

#camera.release()
#cv2.destroyAllWindows()