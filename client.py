# python3

import socket
import select
import random
import requests
import codecs
from struct import *
from typing import List


class Client():

    def __init__(self):
        self.IP = '149.171.36.192'
        self.local = '127.0.0.1'
        self.port = 4000
        self.snoop = 8189
        self.http = 8190
        self.pr = 100
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)

    def Run(self):

        try:
            self.sock.connect((self.IP, self.snoop))
            print("Socket connected.")

            sr = 20
            request = pack('!II', sr, self.pr)
            print('Request message:', request)

            self.sock.sendall(request)
            ready = select.select([self.sock], [], [], 10)
            if ready[0]:
                # while True:
                data = self.sock.recv(1024)
                data = data.hex()
                pr_rec = data[0:8]
                msg_id = data[8:16]
                msg = bytearray.fromhex(data[16:]).decode()
                result = [int(msg_id, 16), msg]
                print(result)
                return result
            else:
                print('Timed out.')

        except Exception as err:
            print('Socket closed')
            self.sock.close()


c = Client()
c.Run()
