import pygame
import random
import sys

# Initialize pygame
pygame.init()
game_over_font = pygame.font.Font(None, 72)

# Load the highest score from file
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Basket settings
BASKET_WIDTH, BASKET_HEIGHT = 80, 20
basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
basket_y = SCREEN_HEIGHT - BASKET_HEIGHT - 10
basket_speed = 15

# Object settings
OBJECT_WIDTH, OBJECT_HEIGHT = 20, 20
object_x = random.randint(0, SCREEN_WIDTH - OBJECT_WIDTH)
object_y = -OBJECT_HEIGHT
object_speed = 5

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))
            pygame.quit()
            sys.exit()

    if score < 0:
        screen.fill(WHITE)
        game_over_text = game_over_font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))
        pygame.quit()
        sys.exit()

    # Basket movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - BASKET_WIDTH:
        basket_x += basket_speed

    # Object falling
    object_y += object_speed
    if object_y > SCREEN_HEIGHT:
        object_y = -OBJECT_HEIGHT
        object_x = random.randint(0, SCREEN_WIDTH - OBJECT_WIDTH)
        score -= 1  # Decrease score if missed

    # Check for collision
    if (basket_x < object_x < basket_x + BASKET_WIDTH or basket_x < object_x + OBJECT_WIDTH < basket_x + BASKET_WIDTH) and \
       (basket_y < object_y + OBJECT_HEIGHT < basket_y + BASKET_HEIGHT):
        score += 1
        object_y = -OBJECT_HEIGHT
        object_x = random.randint(0, SCREEN_WIDTH - OBJECT_WIDTH)
        object_speed += 0.5  # Increase speed each time you catch an object

    # Draw basket and object with rounded corners
    pygame.draw.rect(screen, BLUE, (basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT), border_radius=10)
    pygame.draw.ellipse(screen, RED, (object_x, object_y, OBJECT_WIDTH, OBJECT_HEIGHT))

    # Display score and high score
    if score > high_score:
        high_score = score
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(30)  # Control the frame rate