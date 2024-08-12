import cv2              # main module in OpenCV that provides developers with an easy-to-use interface for working with image and video processing functions
import time
import mediapipe as mp
from log_config import get_logger
from exercises import curls, squats
from utils import render_rep_counter, user_input
from calibration import sample_calibration_data

# MediaPipe and logging setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
logger = get_logger(__name__)

# Extract camera matrix and distortion coefficients from calibration data
camera_matrix = sample_calibration_data.calibration_data['camera_matrix']
dist_coeffs = sample_calibration_data.calibration_data['dist_coeffs']

def main():
    logger.info("Main function started")

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
                logger.log("Can't receive frame (stream end?). Exiting ...")
                break

            # Check frame validity - if not valid, skip current iteration and try to read next frame
            if frame is None or frame.size==0:
                continue

            # Undistort the frame using the camera matrix and distortion coefficients
            h, w = frame.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
            frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, newcameramtx)
            x, y, w, h = roi
            frame = frame[y:y+h, x:x+w]

            # Convert frame to RGB
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
    cv2.destroyAllWindows()
    logger.info("Main function ended")

if __name__ == "__main__":
    logger.info("Program started")
    main()
    logger.info("Program ended")
