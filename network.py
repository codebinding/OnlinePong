import socket
import pickle
from paddle import PygamePaddle, SimplePaddle
from ball import PygameBall, SimpleBall

class ServerNetwork:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ("192.168.3.60", 55553)
        self.sock.bind(self.address)
        self.sock.listen(2)

    def accept(self):
        return self.sock.accept()

    def send(self, conn, paddle, scores, ball):
        p = SimplePaddle(paddle)
        s = scores
        b = SimpleBall(ball)
        conn.sendall(pickle.dumps((p, s, b)))

    def recv(self, conn):
        return pickle.loads(conn.recv(4096))    # paddle

class ClientNetwork:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ("192.168.3.60", 55553)

    def connect(self):
        self.sock.connect(self.address)
        return pickle.loads(self.sock.recv(4096))   # paddle, scores, ball

    def send(self, paddle):
        self.sock.sendall(pickle.dumps(SimplePaddle(paddle)))   
        return pickle.loads(self.sock.recv(4096))   # paddle, scores, ball

    def close(self):
        self.sock.close()