import cv2
import mediapipe as mp
import pygame
import random
import numpy as np
import os

# Initialize Pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Burst Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load font and sound
font = pygame.font.SysFont("Arial", 36)
burst_sound = pygame.mixer.Sound(os.path.join("assets", "pop.wav"))

# Mediapipe for hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize camera
cap = cv2.VideoCapture(0)

# Bubble class
class Bubble:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT + random.randint(0, 100)
        self.radius = random.randint(20, 40)
        self.speed = random.uniform(1.0, 3.0)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def move(self):
        self.y -= self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        return self.y + self.radius < 0

    def check_collision(self, hand_x, hand_y):
        dist = np.sqrt((self.x - hand_x) ** 2 + (self.y - hand_y) ** 2)
        return dist < self.radius

# Bubble list
bubbles = []
bubble_timer = 0

# Score
score = 0

# Main game loop
running = True
while running:
    success, frame = cap.read()
    if not success:
        continue

    # Flip and convert for Mediapipe
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    # Fill screen black
    screen.fill((0, 0, 0))

    # Hand tracking
    hand_x, hand_y = None, None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark[8]  # Index finger tip
            hand_x = int(lm.x * WIDTH)
            hand_y = int(lm.y * HEIGHT)
            pygame.draw.circle(screen, (255, 255, 255), (hand_x, hand_y), 10)

    # Bubble generation
    bubble_timer += 1
    if bubble_timer > 30:
        bubbles.append(Bubble())
        bubble_timer = 0

    # Update and draw bubbles
    for bubble in bubbles[:]:
        bubble.move()
        bubble.draw(screen)

        if hand_x is not None and hand_y is not None and bubble.check_collision(hand_x, hand_y):
            bubbles.remove(bubble)
            score += 1
            burst_sound.play()

        elif bubble.is_off_screen():
            bubbles.remove(bubble)

    # Render score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update screen
    pygame.display.flip()
    clock.tick(30)

# Cleanup
cap.release()
pygame.quit()
