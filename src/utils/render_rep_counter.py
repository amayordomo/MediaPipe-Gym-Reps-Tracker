import cv2

def render_counter(image, left_counter, right_counter, left_stage, right_stage):
    try:
        # Setup status boxes
        cv2.rectangle(image, (0, 0), (225, 100), (245, 117, 16), -1)  # Left status box
        cv2.rectangle(image, (image.shape[1] - 225, 0), (image.shape[1], 100), (245, 117, 16), -1)  # Right status box

        # Left Rep data
        cv2.putText(image, 'LEFT REPS', (15, 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(left_counter), 
                    (15, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Left Stage data
        cv2.putText(image, 'LEFT STAGE', (15, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, left_stage if left_stage else "", 
                    (15, 140), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Right Rep data
        cv2.putText(image, 'RIGHT REPS', (image.shape[1] - 210, 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(right_counter), 
                    (image.shape[1] - 210, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Right Stage data
        cv2.putText(image, 'RIGHT STAGE', (image.shape[1] - 210, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, right_stage if right_stage else "", 
                    (image.shape[1] - 210, 140), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        
    except Exception as e:
        print(e)
