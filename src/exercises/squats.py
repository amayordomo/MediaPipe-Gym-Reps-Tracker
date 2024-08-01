import mediapipe as mp
from utils import angles
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def count_squats(results, counter, stage, left_hip_angles, left_knee_angles, right_hip_angles, right_knee_angles, last_rep_time):
    try:
        landmarks = results.pose_landmarks.landmark
        
        # Left leg
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        left_hip_angle = angles.calculate_angle(left_shoulder, left_hip, left_knee)
        left_hip_angle = angles.smooth_angle(left_hip_angle, left_hip_angles)

        left_knee_angle = angles.calculate_angle(left_hip, left_knee, left_ankle)
        left_knee_angle = angles.smooth_angle(left_knee_angle, left_knee_angles)

        # Right leg
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        right_hip_angle = angles.calculate_angle(right_shoulder, right_hip, right_knee)
        right_hip_angle = angles.smooth_angle(right_hip_angle, right_hip_angles)

        right_knee_angle = angles.calculate_angle(right_hip, right_knee, right_ankle)
        right_knee_angle = angles.smooth_angle(right_knee_angle, right_knee_angles)

        # Count reps
        if left_knee_angle < 90 and right_knee_angle < 90:
            stage = "down"
        if left_hip_angle > 170 and left_knee_angle > 170 and right_hip_angle > 170 and right_knee_angle > 170 and stage == "down":
            if last_rep_time - time.time() > 2: # 2 seconds minimum between reps
                stage = "up"
                counter += 1
                last_rep_time = time.time()

    except Exception as e:
        print(e)

    return counter, stage, last_rep_time