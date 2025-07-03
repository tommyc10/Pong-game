import pygame
import sys
import random
import random
# this is a test code seeing changes
def biased_sample(diff):
    """
    Returns a float in [-5, 5], skewed toward 5 as diff increases.
    """
    # Convert diff (1–10) to a weight for the mean (0 to 1)
    difficulty_scale = diff / 10

    # Mean shifts from 0 to 5
    mean = 5 * difficulty_scale

    # Stddev shrinks slightly with higher difficulty (tighter around mean)
    stddev = 2.5 * (1 - difficulty_scale) + 0.2  # Min 0.2 at diff=10

    # Sample from normal distribution
    sample = random.gauss(mean, stddev)

    # Clamp to [-5, 5]
    return max(-5, min(5, sample))


# Ask for game mode
mode = input("Choose mode (1 = Single Player, 2 = Two Player): ")
single_player = mode.strip() == "1"

DIFF=1

print()

while True:
    try:
        DIFF = int( input("How difficult? (1-10) "))
        break
    except:
        print("Please enter a value 1-10")
        continue


# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 10

# Default ball speed settings
OG_BALL_SPEED = 3
DEFAULT_BALL_SPEED = 3
MAX_SPEED = 12

# Paddle positions
paddle_a = pygame.Rect(50, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball settings
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_dx = DEFAULT_BALL_SPEED
ball_dy = DEFAULT_BALL_SPEED

# Clock
clock = pygame.time.Clock()

# Main loop
while True:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_a.top > 0:
        paddle_a.y -= 6
    if keys[pygame.K_s] and paddle_a.bottom < HEIGHT:
        paddle_a.y += 6

    if single_player:
        # Simple AI: follow the ball
        if paddle_b.centery < ball.centery and paddle_b.bottom < HEIGHT:
            paddle_b.y += biased_sample(DIFF)
        elif paddle_b.centery > ball.centery and paddle_b.top > 0:
            paddle_b.y -= biased_sample(DIFF)
    else:
        if keys[pygame.K_UP] and paddle_b.top > 0:
            paddle_b.y -= 6
        if keys[pygame.K_DOWN] and paddle_b.bottom < HEIGHT:
            paddle_b.y += 6


    # Ball movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Collision with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    # Paddle A collision
    if ball.colliderect(paddle_a):
        offset = abs((ball.centery - paddle_a.centery) / (PADDLE_HEIGHT / 2))
        ball.left = paddle_a.right
        ball_dx = DEFAULT_BALL_SPEED
        if keys[pygame.K_SPACE]:
            boost=int(offset*4) + 1
            ball_dx = min(ball_dx + boost, MAX_SPEED)
            print("🔥 Paddle A power hit!")
        else:
            ball_dx = abs(ball_dx)
        #ball_dx *= -1  # Bounce right
        DEFAULT_BALL_SPEED += .2

    # Paddle B collision
    if ball.colliderect(paddle_b):
        offset = abs((ball.centery - paddle_b.centery) / (PADDLE_HEIGHT / 2))
        ball.right = paddle_b.left
        ball_dx = DEFAULT_BALL_SPEED
        if keys[pygame.K_SPACE]:
            boost=int(offset*4) + 1
            ball_dx = min(ball_dx + boost, MAX_SPEED)
            print("🔥 Paddle B power hit!")
        else:
            ball_dx = abs(ball_dx)
        ball_dx *= -1  # Bounce left
        DEFAULT_BALL_SPEED += .2

    # Reset if ball goes out
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.center = (WIDTH // 2, HEIGHT // 2)
        DEFAULT_BALL_SPEED = OG_BALL_SPEED
        ball_dx = DEFAULT_BALL_SPEED * (-1 if ball_dx > 0 else 1)
        ball_dy = DEFAULT_BALL_SPEED

    # Draw everything
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    pygame.display.flip()
    clock.tick(60)
 

 
