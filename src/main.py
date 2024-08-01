import cv2              # main module in OpenCV that provides developers with an easy-to-use interface for working with image and video processing functions
import mediapipe as mp
from exercises import curls, squats
from utils import render_rep_counter, user_input
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def main():
    # Get user input for exercise type and target rep count
    exercise = user_input.get_valid_exercise()
    target_reps = user_input.get_valid_reps()

    # video feed
    cap = cv2.VideoCapture(1)

    # handle unopened camera
    if not cap.isOpened():
        print("Cannot open webcam")
        exit()

    # Counter variables
    left_counter, right_counter = 0 , 0 
    left_stage, right_stage = None, None
    left_angles_0, left_angles_1, right_angles_0, right_angles_1 = [], [], [], []
    last_left_rep_time, last_right_rep_time = time.time()-10, time.time()-10

    # setup mediapipe instance
    with mp_pose.Pose() as pose:

        # main loop to read and display frames
        while cap.isOpened():

            # get current read from webcam // ret = return variable, frame = image from webcam
            ret, frame = cap.read() 

            # check camera availability
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Check frame validity - if not valid, skip current iteration and try to read next frame
            if frame is None or frame.size==0:
                continue

            # Detect stuff and render
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Recolor image - when pass image to mediapipe, need it in RGB as opposed to CV2's default BGR
            image.flags.writeable = False                   # Helps save memory   
            results = pose.process(image)                   # Make detection
            image.flags.writeable = True                    
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Recolor back to BGR so can render

            # Select user's exercise
            if exercise == "curls":
                left_counter, right_counter, left_stage, right_stage, last_left_rep_time, last_right_rep_time = curls.count_bilateral_curls(
                    results, left_counter, right_counter, left_stage, right_stage, left_angles_0, right_angles_0, last_left_rep_time, last_right_rep_time)
            elif exercise == "squats":
                left_counter, left_stage, last_left_rep_time = squats.count_squats(results, left_counter, left_stage, left_angles_0, left_angles_1, right_angles_0, right_angles_1, last_left_rep_time)

            # Render counter
            render_rep_counter.render_counter(image, left_counter, right_counter, left_stage, right_stage)

            # Render pose detections
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


if __name__ == "__main__":
    main()