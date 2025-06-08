import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (107, 114, 128)
FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 8
PADDLE_SPEED = 6
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Set up the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - 2 Player")

# Load font
score_font = pygame.font.SysFont("Arial", 36, bold=True)

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, border_radius=5)

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def draw(self, surface):
        pygame.draw.ellipse(surface, BLACK, self.rect)

    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speed_x *= -1  # Switch direction
        self.speed_y = BALL_SPEED_Y if self.speed_y > 0 else -BALL_SPEED_Y

# Game variables
left_paddle = Paddle(20, HEIGHT//2 - PADDLE_HEIGHT//2)
right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
ball = Ball()

left_score = 0
right_score = 0

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key states
    keys = pygame.key.get_pressed()

    # Left paddle controls - W and S
    if keys[pygame.K_w]:
        left_paddle.move_up()
    if keys[pygame.K_s]:
        left_paddle.move_down()

    # Right paddle controls - UP and DOWN arrows
    if keys[pygame.K_UP]:
        right_paddle.move_up()
    if keys[pygame.K_DOWN]:
        right_paddle.move_down()

    # Move ball
    ball.move()

    # Ball collision with paddles
    if ball.rect.colliderect(left_paddle.rect):
        ball.speed_x = abs(ball.speed_x)
    if ball.rect.colliderect(right_paddle.rect):
        ball.speed_x = -abs(ball.speed_x)

    # Check scoring
    if ball.rect.left <= 0:
        right_score += 1
        ball.reset()
    if ball.rect.right >= WIDTH:
        left_score += 1
        ball.reset()

    # Draw paddles and ball
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    ball.draw(screen)

    # Draw scores
    left_score_text = score_font.render(str(left_score), True, GRAY)
    right_score_text = score_font.render(str(right_score), True, GRAY)
    screen.blit(left_score_text, (WIDTH // 4, 20))
    screen.blit(right_score_text, (WIDTH * 3 // 4, 20))

    # Draw center line
    for y in range(10, HEIGHT, 30):
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 1, y, 2, 20), border_radius=1)

    pygame.display.flip()

