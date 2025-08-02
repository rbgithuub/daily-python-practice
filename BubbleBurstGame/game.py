import cv2
import pygame
import random
import numpy as np
import mediapipe as mp
import sys

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize PyGame
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bubble Burst Game")
clock = pygame.time.Clock()

# Colors and fonts
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
font = pygame.font.SysFont("Arial", 36)

# Bubble class
class Bubble:
    def __init__(self):
        self.x = random.randint(50, width - 50)
        self.y = height + random.randint(0, 300)
        self.radius = random.randint(30, 50)
        self.speed = random.uniform(2, 5)
        self.color = BLUE

    def move(self):
        self.y -= self.speed
        if self.y < -self.radius:
            self.reset()

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius, 2)

    def reset(self):
        self.__init__()

    def is_hit(self, fx, fy):
        return (self.x - fx) ** 2 + (self.y - fy) ** 2 <= self.radius ** 2

# Webcam setup
cap = cv2.VideoCapture(0)

# Game variables
bubbles = [Bubble() for _ in range(10)]
score = 0

# Game loop
running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and process frame
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    fingertip_x, fingertip_y = None, None

    # Get index fingertip coordinates
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            fingertip_x = int(index_tip.x * width)
            fingertip_y = int(index_tip.y * height)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Clear screen
    screen.fill(WHITE)

    # Update and draw bubbles
    for bubble in bubbles:
        bubble.move()
        if fingertip_x and fingertip_y and bubble.is_hit(fingertip_x, fingertip_y):
            bubbles.remove(bubble)
            bubbles.append(Bubble())
            score += 1
        else:
            bubble.draw(screen)

    # Draw fingertip pointer
    if fingertip_x and fingertip_y:
        pygame.draw.circle(screen, RED, (fingertip_x, fingertip_y), 15)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game display
    pygame.display.flip()
    clock.tick(30)

    # Optional: show hand tracking in OpenCV window (for debugging)
    # cv2.imshow("Hand Tracking", frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Clean up
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
