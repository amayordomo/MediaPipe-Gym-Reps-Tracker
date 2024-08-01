import mediapipe as mp
from utils import trig_calcs

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def count_squats(results, counter, stage):
    try:
        landmarks = results.pose_landmarks.landmark
        
        # Left leg
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        left_hip_angle = trig_calcs.calculate_angle(left_shoulder, left_hip, left_knee)
        left_knee_angle = trig_calcs.calculate_angle(left_hip, left_knee, left_ankle)

        # Right leg
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        right_hip_angle = trig_calcs.calculate_angle(right_shoulder, right_hip, right_knee)
        right_knee_angle = trig_calcs.calculate_angle(right_hip, right_knee, right_ankle)

        # Count reps
        if left_knee_angle < 90 and right_knee_angle < 90:
            stage = "down"
        if left_hip_angle > 170 and left_knee_angle > 170 and right_hip_angle > 170 and right_knee_angle > 170 and stage == "down":
            stage = "up"
            counter += 1

    except Exception as e:
        print(e)

    return counter, stage