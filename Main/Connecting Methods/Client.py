import socket
import sys
from threading import Thread


class Client:
    def __init__(self):
        self.DispName = input("What should your Display Name be? ")
        self.address = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = input("What is the IP address of your Host? ")
        self.s.connect((host_ip, 7735))
        print(f"Connected to {host_ip}, happy chatting!")
        self.Init_Msg = "Connection Successful"

    def SendData(self):
        self.s.send(bytes(f"{self.DispName}> {self.Init_Msg}", "utf-8"))
        while True:
            message = input(f"{self.DispName}> ")
            self.s.send(bytes(f"{self.DispName}> {message}", "utf-8"))

    def RecvData(self):
        while True:
            msg = self.s.recv(1024)
            print("\n" + msg.decode("utf-8"))
            sys.stdout.write(f"{self.DispName}> ")
            sys.stdout.flush()


if __name__ == "__main__":
    C = Client()
    SendThread = Thread(target=C.SendData)
    RecvThread = Thread(target=C.RecvData)

    SendThread.start()
    RecvThread.start()
