import socket
import sys
from threading import Thread


class Host:
    def __init__(self):
        self.DispName = input("What should your Display Name be? ")
        self.address = None

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((socket.gethostbyname(socket.gethostname()), 7735))
        self.s.listen(5)
        print(f"Your IP address is {socket.gethostbyname(socket.gethostname())}")
        self.initial_message = "Connection Success"

    def SendData(self, Conn, name):
        while True:
            message = input(f"{name}> ")
            Conn.send(bytes(f"{name}> {message}", "utf-8"))

    def RecvData(self, Conn):
        while True:
            msg = Conn.recv(1024)
            print("\n" + msg.decode("utf-8"))
            sys.stdout.write(f"{self.DispName}> ")
            sys.stdout.flush()
    def ConnectionHandler(self):
        while True:
            conn, addr = self.s.accept()
            print(f"Connected to {addr}")
            SendThread = Thread(target=self.SendData, args=(conn, self.DispName))
            RecvThread = Thread(target=self.RecvData, args=(conn,))
            SendThread.start()
            RecvThread.start()


if __name__ == "__main__":
    H = Host()
    H.ConnectionHandler()

