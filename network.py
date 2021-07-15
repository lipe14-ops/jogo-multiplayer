import socket

class Network:
    def __init__(self, addr):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr

    def connect(self, data):
        try:
            self.client.connect(self.addr)
            self.client.send(str(data).encode('utf-8'))
        except:
            pass
    
    def send_reply(self, reply):
        try:
            self.client.send(str(reply).encode('utf-8'))
            return eval(self.client.recv(2028).decode('utf-8'))
        except Exception as e:
            print(e)