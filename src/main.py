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

# setup mediapipe instance
with mp_pose.Pose() as pose:
    i = 0
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

        #   Render detections
        dot_formatting = mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2)
        line_formatting = mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, dot_formatting, line_formatting)
        
        if i==10:
            print(results.pose_landmarks)
        i+=1

        # display frame
        cv2.imshow('Mediapipe Feed', image) 

        # exit loop if 'q' pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows() # close video feed


