import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1100, 700
BASKET_WIDTH, BASKET_HEIGHT = 100, 20
OBJECT_WIDTH, OBJECT_HEIGHT = 30, 30
BASKET_SPEED = 15
OBJECT_SPEED = 5
OBJECT_SPAWN_DELAY = 1000  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Load high score
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Fonts
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
title_font = pygame.font.Font(None, 100)

# Basket position
basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
basket_y = SCREEN_HEIGHT - BASKET_HEIGHT - 10

# Game variables
objects = []
score = 10
game_state = "START"
clock = pygame.time.Clock()
last_object_spawn = pygame.time.get_ticks()

# Functions
def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]
    pygame.draw.rect(screen, hover_color if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height else color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return clicked and x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height

def draw_text(text, font, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

def spawn_object():
    obj_type = random.choice(["red", "green", "yellow"])
    objects.append({"type": obj_type, "x": random.randint(0, SCREEN_WIDTH - OBJECT_WIDTH), "y": -OBJECT_HEIGHT})

def draw_basket():
    pygame.draw.rect(screen, BLUE, (basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT), border_radius=10)

def draw_objects():
    for obj in objects:
        color = RED if obj["type"] == "red" else GREEN if obj["type"] == "green" else YELLOW
        pygame.draw.ellipse(screen, color, (obj["x"], obj["y"], OBJECT_WIDTH, OBJECT_HEIGHT))

def check_collision():
    global score
    caught_objects = []
    for obj in objects:
        if basket_x < obj["x"] + OBJECT_WIDTH / 2 < basket_x + BASKET_WIDTH and basket_y < obj["y"] + OBJECT_HEIGHT < basket_y + BASKET_HEIGHT:
            caught_objects.append(obj)
            if obj["type"] == "red":
                score += 1
            elif obj["type"] == "green":
                score += 2
            elif obj["type"] == "yellow":
                score += 3
    for obj in caught_objects:
        objects.remove(obj)

def game_loop():
    global basket_x, game_state, last_object_spawn, score, high_score
    running = True
    while running:
        screen.fill(BLACK if game_state == "START" else WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if game_state == "START":
            if draw_button("Start", SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT//2 - 50, 150, 50, GRAY, BLUE):
                pygame.time.delay(200)  # Prevent accidental double-click
                game_state = "PLAYING"
            pygame.display.flip()
        elif game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            basket_x += (-BASKET_SPEED if keys[pygame.K_LEFT] and basket_x > 0 else BASKET_SPEED if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - BASKET_WIDTH else 0)
            if pygame.time.get_ticks() - last_object_spawn > OBJECT_SPAWN_DELAY:
                spawn_object()
                last_object_spawn = pygame.time.get_ticks()
            for obj in objects:
                obj["y"] += OBJECT_SPEED
            check_collision()
            # Remove objects that fall off the screen and decrement score if not caught
            for obj in objects:
                if obj["y"] > SCREEN_HEIGHT:
                    objects.remove(obj)
                    score = max(0, score - 1)  # Decrement score only if the object was not caught
            if score == 0:
                game_state = "GAME_OVER"
            draw_basket()
            draw_objects()
            if score > high_score:
                high_score = score
            draw_text(f"Score: {score}", font, BLACK, 10, 10)
            draw_text(f"High Score: {high_score}", font, BLACK, 10, 50)
            pygame.display.flip()
            clock.tick(30)
        elif game_state == "GAME_OVER":
            draw_text(f"Game Over! High Score: {high_score}", game_over_font, BLACK, SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 100)
            if draw_button("Restart", SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT//2, 150, 50, GRAY, BLUE):
                pygame.time.delay(200)
                score = 10
                objects.clear()
                game_state = "START"
            if draw_button("Quit", SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT//2 + 80, 150, 50, GRAY, RED):
                running = False
            pygame.display.flip()
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))
    pygame.quit()
    sys.exit()

game_loop()