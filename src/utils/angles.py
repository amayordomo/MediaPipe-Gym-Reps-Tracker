import numpy as np      # helps with trig 

def calculate_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    # max angle of arm is 180, not 360
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def smooth_angle(angle, prev_angles, window_size=5):
    # Add the current angle to the list of previous angles
    prev_angles.append(angle)
    
    # If the list of previous angles exceeds the window size, remove the oldest angle
    if len(prev_angles) > window_size:
        prev_angles.pop(0)
    
    # Calculate the average of the angles in the list to get the smoothed angle
    # Smooth only the angle values
    return np.mean([a[0] for a in prev_angles])