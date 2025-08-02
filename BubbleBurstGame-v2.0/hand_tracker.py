import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.drawing = mp.solutions.drawing_utils

    def get_hand_position(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        hand_x, hand_y = 320, 240  # default center
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Using index finger tip
                x = hand_landmarks.landmark[8].x
                y = hand_landmarks.landmark[8].y
                h, w, _ = frame.shape
                hand_x = int(x * w)
                hand_y = int(y * h)
                self.drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                break

        return (hand_x, hand_y), frame
