import random
import os
import sys
import pygame
import json
import math
from pygame.color import THECOLORS

points = 0

if getattr(pygame, "IS_CE", False) == False:
    print("Поставь Pygame Community Edition (pip install pygame-ce)\n"*10)

try:
    with open("data.json", "r") as f:
        userdata = json.load(f)
except:
    print("ЗАПУСТИ main.py\n" * 100)
    sys.exit()

user = userdata["user"]
if 1 <= userdata["userhp"] <= 150 and 2 <= userdata["userpower"] <= 8:
    HP = userdata["userhp"]
else:
    print("Стоп! Мне не приятно")
    HP = random.randint(1, 150)
    userdata["userpower"] = random.randint(2, 8)

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FIGHT!")

btn_w, btn_h = 150, 50
button_rect = pygame.Rect(10*int(userdata["userpower"]), 10*int(userdata["userpower"]), 10*int(userdata["userpower"]), 10*int(userdata["userpower"]))
button_rect.center = (WIDTH//2, HEIGHT//2)
color_idle = (70, 70, 70)
color_hover = (100, 100, 100)

WHITE = (255, 255, 255)
GREEN = (0, 255, 75)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()
TPS = 240

START = False

square_size = 50
x, y = WIDTH // 2 - square_size // 2, HEIGHT // 2 - square_size // 2

speed = 300
enemy_speed_lerp = 2

enemy_x, enemy_y = 0, 0
enemy_size = 10

font = pygame.font.SysFont('couriernew', 24)
nfont = pygame.font.SysFont('couriernew', 16)


run = True

while run:
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_rect.collidepoint(mouse_pos)
    if pygame.mouse.get_pressed()[0]:
        START = True
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    dt = clock.tick(TPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if is_hovered and START:
                new_x = random.randint(0, WIDTH - btn_w)
                new_y = random.randint(0, HEIGHT - btn_h)
                button_rect.topleft = (new_x, new_y)
                points += 1
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
    if START:
        x += dx * speed * dt
        y += dy * speed * dt

        x = max(0, min(x, WIDTH - square_size))
        y = max(0, min(y, HEIGHT - square_size))

        enemy_x += (x + 25 - enemy_x) * (1 - math.exp(-enemy_speed_lerp * dt))
        enemy_y += (y + 25 - enemy_y) * (1 - math.exp(-enemy_speed_lerp * dt))

    screen.fill(WHITE)
    if START:
        player_rect = pygame.Rect(x, y, square_size, square_size)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
        pygame.draw.rect(screen, WHITE, enemy_rect)
        pygame.draw.rect(screen, color_hover if is_hovered else color_idle, button_rect, border_radius=10)
        pygame.draw.rect(screen, GREEN, player_rect)
        if player_rect.colliderect(enemy_rect):
            HP -= 15 * dt

    hp_color = BLACK
    bg_color = GREEN
    if HP < 1:
        run = False
    if not START:
        text = font.render("ЛКМ ДЛЯ НАЧАЛА", True, THECOLORS['blue'])
        screen.blit(text, (100, 100))
    hptext = font.render(str(max(0, round(HP))), True, hp_color, bg_color)
    ntext = nfont.render(user, True, WHITE, BLACK)

    ntext.set_alpha(128)
    if START:
        screen.blit(ntext, (x, y - 20))
        screen.blit(hptext, (x, y))
        pygame.mouse.set_pos(enemy_x, enemy_y)

    fps_display = nfont.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
    screen.blit(fps_display, (10, 10))
    p_display = nfont.render(f"Очки: {points}", True, BLACK)
    screen.blit(p_display, (10, 25))

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if is_hovered else pygame.SYSTEM_CURSOR_ARROW)

    pygame.display.flip()

pygame.quit()
