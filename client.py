# python3

import socket
import select
import random
import requests


class Client():

    def __init__(self):
        self.IP = '127.0.0.1'
        self.port = 4000

    def Run(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket connected.")
        except socket.error as err:
            print("Socket failed.")

        s.connect((self.IP, self.port))
        s.send(bytes('', 'utf-8'))

        res = s.recv(1024)
        print(res)
        s.close()


c = Client()
c.Run()
