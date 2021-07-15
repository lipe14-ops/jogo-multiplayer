import socket
import random
from threading import Thread

class Server:
    def __init__(self):
        self.state = {'fruits':[{'x':random.randint(0,580), 'y':random.randint(0,580)}], 'players':[]}
        self.clients = []
        self.OBJ_SIZE = 20
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('192.168.1.67', 12010))
        self.server.listen(5)
    
    def _players_management(self, data):
        for index, users in enumerate(self.state['players']):
            if data['id'] in users['id']:
                self.state['players'][index] = data
    
    def handler_client(self, connection, address):
        while True:
            try:
                data  = eval(connection.recv(2028).decode('utf-8'))
                if data['collided']:
                    self.state['fruits'][0] = {'x':random.randint(0,580), 'y':random.randint(0,580)}
                self._players_management(data)
                connection.send(str(self.state).encode('utf-8')) 
            except Exception:
                self.state['players'].pop(self.clients.index(connection)) 
                self.clients.remove(connection)
                print(f'disconnected with: {address}')
                connection.close()
                break

    def receive_player(self):
        connection, address = self.server.accept()
        self.state['players'].append(eval(connection.recv(2028).decode('utf-8')))
        self.clients.append(connection)
        print(f'connected with: {address}')
        Thread(target=self.handler_client, args=(connection, address)).start()

if __name__ == '__main__':
    server = Server()
    while True:
        try:
            server.receive_player()
        except Exception: pass