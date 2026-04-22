import socket
import threading
import pickle

# Хранилище данных: {id: {"x": x, "y": y, "points": p, "user": name}}
players = {}

def handle_client(conn, p_id):
    conn.send(pickle.dumps(p_id)) # Отправляем клиенту его ID
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            players[p_id] = data
            conn.sendall(pickle.dumps(players))
        except:
            break
    del players[p_id]
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()
print("Сервер запущен...")

count = 0
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, count)).start()
    count += 1
