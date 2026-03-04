import pygame
import sys
from pygame.color import THECOLORS

hp = 100
pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FIGHT!")

WHITE = (255, 255, 255)
GREEN = (0, 255, 75)

TPS = 60

square_size = 50
x = WIDTH // 2 - square_size // 2
y = HEIGHT // 2 - square_size // 2
speed = 5

font = pygame.font.SysFont('couriernew', 40)

enemy_x, enemy_y = 0, 0
enemy_size = 40
enemy_speed_factor = 0.01



run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    ks = pygame.key.get_pressed()
    if ks[pygame.K_a]:
        x -= speed
    if ks[pygame.K_d]:
        x += speed
    if ks[pygame.K_w]:
        y -= speed
    if ks[pygame.K_s]:
        y += speed

    x = max(0, min(x, WIDTH - square_size))
    y = max(0, min(y, HEIGHT - square_size))
    enemy_x += (x - enemy_x) * enemy_speed_factor
    enemy_y += (y - enemy_y) * enemy_speed_factor

    screen.fill(WHITE)

    player_rect = pygame.Rect(x, y, square_size, square_size)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

    pygame.draw.rect(screen, (255, 0, 0), enemy_rect)
    pygame.draw.rect(screen, GREEN, player_rect)

    text = font.render(str(hp), True, THECOLORS['black'])
    if player_rect.colliderect(enemy_rect):

        hp = hp-1

    if hp == 0:
        run = False

    screen.blit(text, (50, 50))

    pygame.display.flip()

    pygame.time.Clock().tick(TPS)

