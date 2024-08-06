import socket
import threading
import json
import random

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        self.accept_clients()

    def accept_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        client_id = client_socket.getpeername()
        self.clients[client_id] = {'socket': client_socket, 'x': random.uniform(-50, 50), 'y': random.uniform(-50, 50), 'z': random.uniform(-50, 50)}
        self.send_initial_position(client_socket, client_id)

        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    command = json.loads(data)
                    self.update_position(client_id, command)
                    self.broadcast_positions()
                else:
                    break
            except:
                break
        self.remove_client(client_id)
        client_socket.close()

    def send_initial_position(self, client_socket, client_id):
        init_data = json.dumps({'type': 'INIT', 'x': self.clients[client_id]['x'], 'y': self.clients[client_id]['y'], 'z': self.clients[client_id]['z']})
        client_socket.send(init_data.encode('utf-8'))

    def update_position(self, client_id, command):
        with self.lock:
            self.clients[client_id]['x'] += command.get('dx', 0)
            self.clients[client_id]['y'] += command.get('dy', 0)
            self.clients[client_id]['z'] += command.get('dz', 0)

    def broadcast_positions(self):
        with self.lock:
            positions = [{'id': f"{client_id[0]}:{client_id[1]}", 'x': info['x'], 'y': info['y'], 'z': info['z']} for client_id, info in self.clients.items()]
            message = json.dumps({'type': 'POS', 'positions': positions})
            for client_id in self.clients:
                self.clients[client_id]['socket'].send(message.encode('utf-8'))

    def remove_client(self, client_id):
        with self.lock:
            if client_id in self.clients:
                del self.clients[client_id]
                self.broadcast_positions()

if __name__ == "__main__":
    server = GameServer()
    server.start()
