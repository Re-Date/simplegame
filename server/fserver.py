import socket
import threading
import pickle
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import sys
import os


# --- СЕРВЕРНАЯ ЛОГИКА ---
players = {}


def handle_client(conn, p_id):
    conn.send(pickle.dumps(p_id))
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            players[p_id] = data
            conn.sendall(pickle.dumps(players))
        except:
            break
    if p_id in players:
        del players[p_id]
    conn.close()


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Позволяет повторно использовать порт после перезапуска
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5555))
    server.listen()

    count = 0
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, count), daemon=True).start()
        count += 1


# --- ЛОГИКА ТРЕЯ ---
def create_image():
    # Создаем простую иконку (красный круг)
    image = Image.new('RGB', (64, 64), color='white')
    dc = ImageDraw.Draw(image)
    dc.ellipse((10, 10, 54, 54), fill='red')
    return image


def on_quit(icon, item):
    icon.stop()
    # Жесткое завершение процесса, чтобы закрыть поток сервера
    os._exit(0)


# Запуск сервера в фоновом потоке
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Настройка и запуск трея
menu = Menu(MenuItem('Остановить сервер и выйти', on_quit))
icon = Icon("ServerIcon", create_image(), "Игровой сервер", menu)

print("Сервер запущен. Управление через трей.")
icon.run()
