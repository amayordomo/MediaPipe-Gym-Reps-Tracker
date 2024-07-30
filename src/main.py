import cv2              # main module in OpenCV that provides developers with an easy-to-use interface for working with image and video processing functions
import mediapipe as mp
import numpy            # helps with trig later


mp_drawing = mp.solutions.drawing_utils # drawing utilities
mp_pose = mp.solutions.pose             # import pose estimation module (as opposed to face detection, iris, hands, etc.)


# video feed
cap = cv2.VideoCapture(1)   # set up video capture device - 0 indicates webcam, this may be different for different devices

# handle unopened camera
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

# main loop to read and display frames
while cap.isOpened():
    ret, frame = cap.read() # get current read from webcam // ret = return variable, frame = image from webcam

    # check camera availability
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # check frame validity - if not valid, skip current iteration and try to read next frame
    if frame is None or frame.size==0:
        continue

    # display frame
    cv2.imshow('Mediapipe Feed', frame) 

    # exit loop if 'q' pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() # close video feed

