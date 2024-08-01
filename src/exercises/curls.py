import mediapipe as mp
from utils import angles
import numpy as np
import time

DOWN_ANGLE_THRESHOLD = 160  # Angle for the "down" stage (arm extended)
UP_ANGLE_THRESHOLD = 30     # Angle for the "up" stage (arm flexed)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Bilateral curls counter
def count_bilateral_curls(results, left_counter, right_counter, left_stage, right_stage, left_angles, right_angles, last_left_rep_time, last_right_rep_time, stability_threshold=0.25):
    try:
        landmarks = results.pose_landmarks.landmark

        # Left arm
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        left_angle = angles.calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_angle = angles.smooth_angle((left_angle, left_shoulder), left_angles)

        # Check shoulder stability
        if left_angles:
            left_shoulder_movement = np.linalg.norm(np.array(left_shoulder) - np.array(left_angles[-1][1]))
            if left_shoulder_movement > stability_threshold:
                return left_counter, right_counter, left_stage, right_stage
        else:
            left_shoulder_movement = 0

        # Count rep given correct angle(s)
        if left_angle > DOWN_ANGLE_THRESHOLD:
            left_stage = "down"
        if left_angle < UP_ANGLE_THRESHOLD and left_stage == "down":
            if time.time() - last_left_rep_time > 1.25: # 1.25 s minium between reps
                left_stage = "up"
                left_counter += 1
                last_left_rep_time = time.time()

        # Right arm
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        right_angle = angles.calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_angle = angles.smooth_angle((right_angle, right_shoulder), right_angles)

        # Check shoulder stability
        if right_angles:
            right_shoulder_movement = np.linalg.norm(np.array(right_shoulder) - np.array(right_angles[-1][1]))
            if right_shoulder_movement > stability_threshold:
                return left_counter, right_counter, left_stage, right_stage
        else:
            right_shoulder_movement = 0

        # Count rep given correct angle(s)
        if right_angle > 160:
            right_stage = "down"
        if right_angle < 30 and right_stage == "down":
            if time.time() - last_right_rep_time > 1.25: # 1.25 s minimum between reps
                right_stage = "up"
                right_counter += 1
                last_right_rep_time = time.time()

    except Exception as e:
        print(e)

    return left_counter, right_counter, left_stage, right_stage, last_left_rep_time, last_right_rep_time