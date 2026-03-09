import random
import os
import sys
import pygame
import json
import math

from pygame.color import THECOLORS

try:
    with open("data.json", "r") as f:
        userdata = json.load(f)
except:
    print("ЗАПУСТИ main.py\n"*100)
    sys.exit()

user = userdata["user"]
if 1 <= userdata["userhp"] <= 150 and 2 <= userdata["userpower"] <= 8:
    hp = userdata["userhp"]
else:
    print("Стоп! Мне не приятно")
    hp = random.randint(1, 150)

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FIGHT!")

WHITE = (255, 255, 255)
GREEN = (0, 255, 75)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()
TPS = 180





square_size = 50
x, y = WIDTH // 2 - square_size // 2, HEIGHT // 2 - square_size // 2

speed = 300
enemy_speed_lerp = 2

font = pygame.font.SysFont('couriernew', 24)
nfont = pygame.font.SysFont('couriernew', 16)

enemy_x, enemy_y = 0, 0
enemy_size = 10

run = True
while run:
    dt = clock.tick(TPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    ks = pygame.key.get_pressed()
    dx, dy = 0, 0
    if ks[pygame.K_a]:
        dx -= 1
    if ks[pygame.K_d]:
        dx += 1
    if ks[pygame.K_w]:
        dy -= 1
    if ks[pygame.K_s]:
        dy += 1

    x += dx * speed * dt
    y += dy * speed * dt

    x = max(0, min(x, WIDTH - square_size))
    y = max(0, min(y, HEIGHT - square_size))

    enemy_x += (x - enemy_x) * (1 - math.exp(-enemy_speed_lerp * dt))
    enemy_y += (y - enemy_y) * (1 - math.exp(-enemy_speed_lerp * dt))

    screen.fill(WHITE)

    player_rect = pygame.Rect(x, y, square_size, square_size)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

    pygame.draw.rect(screen, WHITE, enemy_rect)
    pygame.draw.rect(screen, GREEN, player_rect)

    hp_color = BLACK
    bg_color = GREEN
    if player_rect.colliderect(enemy_rect):
        hp -= 15 * dt
        hp_color, bg_color = WHITE, RED

    if hp < 1:
        run = False

    hptext = font.render(str(max(0, round(hp))), True, hp_color, bg_color)
    ntext = nfont.render(user, True, WHITE, BLACK)

    ntext.set_alpha(128)

    screen.blit(ntext, (x, y - 20))
    screen.blit(hptext, (x, y))

    fps_display = nfont.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
    screen.blit(fps_display, (10, 10))

    pygame.mouse.set_pos(enemy_x, enemy_y)

    pygame.display.flip()

pygame.quit()

#IDE ZONE: aadddddddddddddddddddddddddddddwawwwwwwwwwwwwwwwwwwwwwwwwwd