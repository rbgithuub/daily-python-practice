# game.py
import cv2
import pygame
import random
import time
import math
from hand_tracker import HandTracker

# Initialize camera
cap = cv2.VideoCapture(0)

# Pygame setup
pygame.init()
bubble_pop_sound = pygame.mixer.Sound("pop.wav")  # Make sure pop.wav exists
font = pygame.font.Font(None, 48)

# Create overlay screen
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bubble Burst Game")

# Bubble class
class Bubble:
    def __init__(self):
        self.x = random.randint(50, width - 50)
        self.y = random.randint(50, height - 50)
        self.radius = random.randint(25, 40)
        self.color = random.choice([
            (255, 0, 0),   # Red
            (0, 255, 0),   # Green
            (0, 0, 255),   # Blue
            (255, 255, 0), # Yellow
            (255, 0, 255), # Magenta
            (0, 255, 255)  # Cyan
        ])
        self.dx = random.uniform(-1.5, 1.5)
        self.dy = random.uniform(-1.5, 1.5)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x <= self.radius or self.x >= width - self.radius:
            self.dx *= -1
        if self.y <= self.radius or self.y >= height - self.radius:
            self.dy *= -1

    def draw(self):
        # Simulate 3D effect by creating a shiny spot
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x - self.radius//3), int(self.y - self.radius//3)), self.radius // 4)

    def is_burst(self, finger_x, finger_y):
        dist = math.hypot(self.x - finger_x, self.y - finger_y)
        return dist <= self.radius

# Game variables
bubbles = [Bubble() for _ in range(10)]
score = 0
hand_tracker = HandTracker()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))

    screen.blit(frame_surface, (0, 0))

    # Get hand landmarks
    hand_landmarks = hand_tracker.get_hand_landmarks(frame)

    index_finger_tip = None
    if hand_landmarks:
        h, w, _ = frame.shape
        index_tip = hand_landmarks.landmark[8]  # Index finger tip
        index_finger_tip = (int(index_tip.x * w), int(index_tip.y * h))
        pygame.draw.circle(screen, (255, 255, 255), index_finger_tip, 10)

    # Update and draw bubbles
    for bubble in bubbles[:]:
        bubble.move()
        bubble.draw()
        if index_finger_tip and bubble.is_burst(*index_finger_tip):
            bubbles.remove(bubble)
            score += 1
            bubble_pop_sound.play()
            bubbles.append(Bubble())

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(30)

cap.release()
pygame.quit()
cv2.destroyAllWindows()
