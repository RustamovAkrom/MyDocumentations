import pygame
import socket
import threading
import json
import sys

class GameClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.positions = {}
        self.x = 0
        self.y = 0
        self.z = 0
        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        threading.Thread(target=self.listen_to_server).start()
        self.game_loop()

    def listen_to_server(self):
        while self.running:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data:
                    self.handle_server_message(data)
            except:
                self.running = False

    def handle_server_message(self, message):
        data = json.loads(message)
        if data['type'] == 'INIT':
            self.x = data['x']
            self.y = data['y']
            self.z = data['z']
        elif data['type'] == 'POS':
            self.positions = {pos['id']: (pos['x'], pos['y'], pos['z']) for pos in data['positions']}
        self.render()

    def render(self):
        self.screen.fill((0, 0, 0))
        for (x, y, z) in self.positions.values():
            pygame.draw.circle(self.screen, (255, 0, 0), (int(x) + 400, int(y) + 300), 5)
        pygame.display.flip()

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            dx = dy = dz = 0
            if keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_RIGHT]:
                dx += 1
            if keys[pygame.K_UP]:
                dy -= 1
            if keys[pygame.K_DOWN]:
                dy += 1
            if keys[pygame.K_PAGEUP]:
                dz += 1
            if keys[pygame.K_PAGEDOWN]:
                dz -= 1

            if dx or dy or dz:
                command = json.dumps({'dx': dx, 'dy': dy, 'dz': dz})
                self.client_socket.send(command.encode('utf-8'))

            self.clock.tick(30)

        pygame.quit()
        self.client_socket.close()

if __name__ == "__main__":
    client = GameClient()
    client.connect()
