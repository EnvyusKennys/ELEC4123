# python3

import socket
import select
import random
import requests


class Server():

    def __init__(self):
        self.IP = '149.171.36.192'
        self.local = '127.0.0.1'
        self.port = 4000
        self.snoop = 8189
        self.http = 8190
        self.pr = '00000100'

    def Run(self):
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.bind((self.local, self.port))
        s1.listen(5)

        while True:
            conn, addr = s1.accept()
            print(addr, "has been connected")

            try:
                s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s2.connect((self.IP, self.snoop))
                print("Socket connected.")
            except s2.error as err:
                print('Socket failed.')

            sr = '00000008'
            request = sr + self.pr

            s2.send(request.encode('utf-8'))
            while True:
                ready = select.select([s2], [], [], 10)
                if ready[0]:
                    data = s2.recv(1024)
                    data = data.hex()
                    print(str(data))

            s2.close()

        s1.close()

    # def Post(self):
    #     s = self.sock
    #     s.connect((self.IP, self.http))


s = Server()
s.Run()
