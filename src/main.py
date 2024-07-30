import cv2              # main module in OpenCV that provides developers with an easy-to-use interface for working with image and video processing functions
import mediapipe as mp
from trig_calcs import calculate_angle
import numpy as np


mp_drawing = mp.solutions.drawing_utils # drawing utilities
mp_pose = mp.solutions.pose             # import pose estimation module (as opposed to face detection, iris, hands, etc.)


# video feed
cap = cv2.VideoCapture(1)   # set up video capture device - 0 indicates webcam, this may be different for different devices

# Curl counter variables
counter = 0 
stage = None

# handle unopened camera
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

# setup mediapipe instance
with mp_pose.Pose() as pose:

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

        # Detect stuff and render
        #   Recolor image - when pass image to mediapipe, need it in RGB as opposed to CV2's default BGR
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False     # helps save memory   
       
        #   Make detection
        results = pose.process(image)

        #   Recolor back to BGR so can render
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #   Extract landmarks if detections made

        '''
        # lists all 33 landmarks captured by MediaPipe Pose LandMarker
        for lndmrk in mp_pose.PoseLandmark:
            print(lndmrk)
        '''

        try:
            landmarks = results.pose_landmarks.landmark
            
            # get left arm coordinates to calculate angle as lists of format [body_part_x_coordinate, body_part_y_coordinate]
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            angle = calculate_angle(shoulder, elbow, wrist)

            # Curl counter logic
            if angle > 160:
                stage = "down"
            if angle < 30 and stage =="down":
                stage="up"
                counter +=1
                print(counter)

        except:
            pass

        # Render curl counter
        #   Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        #   Rep data
        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        #   Stage data
        cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        

        # Render detections
        dot_formatting = mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2)
        line_formatting = mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, dot_formatting, line_formatting)

        # display frame
        cv2.imshow('Mediapipe Feed', image) 

        # exit loop if 'q' pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows() # close video feed


