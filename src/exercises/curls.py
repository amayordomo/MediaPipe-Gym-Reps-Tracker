import mediapipe as mp
from utils import trig_calcs

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Bilateral curls counter
def count_bilateral_curls(results, left_counter, right_counter, left_stage, right_stage):
    try:
        landmarks = results.pose_landmarks.landmark

        # Left arm
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        left_angle = trig_calcs.calculate_angle(left_shoulder, left_elbow, left_wrist)

        if left_angle > 160:
            left_stage = "down"
        if left_angle < 30 and left_stage == "down":
            left_stage = "up"
            left_counter += 1

        # Right arm
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        right_angle = trig_calcs.calculate_angle(right_shoulder, right_elbow, right_wrist)

        if right_angle > 160:
            right_stage = "down"
        if right_angle < 30 and right_stage == "down":
            right_stage = "up"
            right_counter += 1

    except Exception as e:
        print(e)

    return left_counter, right_counter, left_stage, right_stage