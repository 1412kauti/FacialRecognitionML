import numpy as np
import cv2

cap = cv2.VideoCapture('rtsp://admin:admin@192.168.8.220:1935/')

def videofeed():

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        #gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            videoCaptureObject = cv2.VideoCapture(0)
            frame = videoCaptureObject.read()
            cv2.imwrite("NewPicture.jpg", frame)
            videoCaptureObject.release()




# When everything done, release the capture
videofeed()
cap.release()
cv2.destroyAllWindows()
