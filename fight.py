import random, os, sys, pygame, json, math, socket, pickle, subprocess
from pygame.color import THECOLORS

# ================== CONSTANTS ==================
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

WIDTH, HEIGHT = 1280, 720

BTN_W, BTN_H = 150, 50

BTN_BASE_MULT = 10  # множитель userpower

COLOR_IDLE = (70, 70, 70)
COLOR_HOVER = (100, 100, 100)

WHITE = (255, 255, 255)
GREEN = (0, 255, 75)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

TPS = 2000

SQUARE_SIZE = 50
ENEMY_SIZE = 10

PLAYER_SPEED = 300
ENEMY_SPEED_LERP = 2

DAMAGE_PER_SEC = 15

HP_BAR_X = 10
HP_BAR_Y = 680
HP_BAR_W = 200
HP_BAR_H = 20

FONT_MAIN = ('couriernew', 20)
FONT_SMALL = ('couriernew', 16)

# подключение к серваку
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    my_id = pickle.loads(client.recv(2048))
    all_players = {}
except:
    subprocess.Popen(["python", "server/fserver.py"])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    my_id = pickle.loads(client.recv(2048))
    all_players = {}

points = 0

if not getattr(pygame, "IS_CE", False):
    print("Поставь Pygame Community Edition (pip install pygame-ce)\n"*10)

try:
    with open("data/data.json", "r") as f:
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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FIGHT!")

button_rect = pygame.Rect(
    BTN_BASE_MULT * int(userdata["userpower"]),
    BTN_BASE_MULT * int(userdata["userpower"]),
    BTN_BASE_MULT * int(userdata["userpower"]),
    BTN_BASE_MULT * int(userdata["userpower"])
)
button_rect.center = (WIDTH//2, HEIGHT//2)

clicksound = pygame.mixer.Sound("assets/click.wav")

nclp = False

clock = pygame.time.Clock()

start = False

x, y = WIDTH // 2 - SQUARE_SIZE // 2, HEIGHT // 2 - SQUARE_SIZE // 2

enemy_x, enemy_y = 0, 0

font = pygame.font.SysFont(*FONT_MAIN)
nfont = pygame.font.SysFont(*FONT_SMALL)

hp_color = BLACK
bg_color = GREEN

run = True

while run:
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_rect.collidepoint(mouse_pos)

    if pygame.mouse.get_pressed()[0]:
        start = True
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    dt = clock.tick(TPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if is_hovered and start:
                new_x = random.randint(0, WIDTH-20 - BTN_W)
                new_y = random.randint(0, HEIGHT-20 - BTN_H)
                print(new_x, new_y)
                button_rect.topleft = (new_x, new_y)
                points += 1
                clicksound.play()

        if event.type == pygame.QUIT:
            run = False

    ks = pygame.key.get_pressed()
    dx, dy = 0, 0

    if ks[pygame.K_a]: dx -= 1
    if ks[pygame.K_d]: dx += 1
    if ks[pygame.K_w]: dy -= 1
    if ks[pygame.K_s]: dy += 1

    if ks[pygame.K_ESCAPE]:
        start = False

    if ks[pygame.K_n] and ks[pygame.K_c] and ks[pygame.K_l] and ks[pygame.K_p]:
        nclp = True

    screen.fill(WHITE)

    if not start:
        text = font.render(
            "Кликай по кнопке (ЛКМ), \nуклоняйся от курсора-врага (WASD), \nне дай HP упасть до 0. Hitbox 2–8 влияет на размер цели. ЛКМ ДЛЯ НАЧАЛА",
            True,
            THECOLORS['blue']
        )
        screen.blit(text, (100, 100))
        pygame.display.flip()

    else:
        hptext = font.render(str(max(0, round(HP))), True, hp_color)

        fps_display = nfont.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
        p_display = nfont.render(f"Очки: {points}", True, BLACK)

        x += dx * PLAYER_SPEED * dt
        y += dy * PLAYER_SPEED * dt

        x = max(0, min(x, WIDTH - SQUARE_SIZE))
        y = max(0, min(y, HEIGHT - SQUARE_SIZE))

        enemy_x += (x + 25 - enemy_x) * (1 - math.exp(-ENEMY_SPEED_LERP * dt))
        enemy_y += (y + 25 - enemy_y) * (1 - math.exp(-ENEMY_SPEED_LERP * dt))

        pygame.mouse.set_pos(enemy_x, enemy_y)

        player_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)

        pygame.draw.rect(screen, WHITE, enemy_rect)
        pygame.draw.rect(screen, COLOR_HOVER if is_hovered else COLOR_IDLE, button_rect, border_radius=10)

        try:
            client.send(pickle.dumps({
                "x": x, "y": y,
                "points": points,
                "user": user,
                "hp": HP,
                "ex": enemy_x, "ey": enemy_y
            }))
            all_players = pickle.loads(client.recv(4096))
        except:
            print("Потеряно соединение с сервером")
            run = False

        for p_id, p_data in all_players.items():
            if p_id != my_id:
                other_rect = pygame.Rect(p_data["x"], p_data["y"], SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, (0, 100, 255), other_rect)

                other_e = pygame.Rect(p_data["ex"], p_data["ey"], ENEMY_SIZE, ENEMY_SIZE)
                pygame.draw.rect(screen, (0, 0, 0), other_e)

                other_name = nfont.render(p_data["user"], True, BLACK)
                screen.blit(other_name, (p_data["x"], p_data["y"] - 20))

        pygame.draw.rect(screen, GREEN, player_rect)

        ntext = nfont.render(user, True, WHITE, BLACK)
        ntext.set_alpha(128)
        screen.blit(ntext, (x, y - 20))

        if player_rect.colliderect(enemy_rect) and not nclp:
            HP -= DAMAGE_PER_SEC * dt

        pygame.draw.rect(screen, RED, (HP_BAR_X, HP_BAR_Y, HP_BAR_W, HP_BAR_H))
        pygame.draw.rect(screen, GREEN, (HP_BAR_X, HP_BAR_Y, max(0, HP / int(userdata["userhp"]) * HP_BAR_W), HP_BAR_H))
        screen.blit(hptext, (HP_BAR_X, HP_BAR_Y))

        if HP < 1:
            run = False

        screen.blit(fps_display, (10, 10))
        screen.blit(p_display, (10, 25))

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if is_hovered else pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()

pygame.quit()