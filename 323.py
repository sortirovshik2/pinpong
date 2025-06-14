import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (107, 114, 128)
FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 40
PADDLE_SPEED = 6
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - 2 Player")

score_font = pygame.font.SysFont("Arial", 36, bold=True)
game_over_font = pygame.font.SysFont("Arial", 72, bold=True)

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

class Ball:
    def __init__(self):
        self.image = pygame.image.load("cartin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 10, self.image.get_height() // 10))
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speed_x *= -1
        self.speed_y = BALL_SPEED_Y if self.speed_y > 0 else -BALL_SPEED_Y

left_paddle = Paddle(20, HEIGHT//2 - PADDLE_HEIGHT//2)
right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
ball = Ball()

left_score = 0
right_score = 0

clock = pygame.time.Clock()

game_over = False

running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    if game_over:
        game_over_text = game_over_font.render("Game Over", True, BLACK)
        text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(game_over_text, text_rect)

        keys = pygame.key.get_pressed()
        if any(keys):
            running = False
            break
    else:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            left_paddle.move_up()
        if keys[pygame.K_s]:
            left_paddle.move_down()

        if keys[pygame.K_UP]:
            right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            right_paddle.move_down()

        ball.move()

        if ball.rect.colliderect(left_paddle.rect):
            ball.speed_x = abs(ball.speed_x)
        if ball.rect.colliderect(right_paddle.rect):
            ball.speed_x = -abs(ball.speed_x)

        if ball.rect.left <= 0:
            right_score += 1
            game_over = True
            ball.reset()
        if ball.rect.right >= WIDTH:
            left_score += 1
            game_over = True
            ball.reset()

        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        left_score_text = score_font.render(str(left_score), True, GRAY)
        right_score_text = score_font.render(str(right_score), True, GRAY)


        screen.blit(left_score_text, (WIDTH // 4, 20))
        screen.blit(right_score_text, (WIDTH * 3 // 4, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
