# draft for control server

import socket
import requests
from client import Client


class Server():
    def __init__(self):
        self.Pkt = []
        self.httpStatus = 200
        self.IP = '149.171.36.192'
        self.http = 8190
        self.res_msg = ''

    def GetMessage(self):
        c = Client()
        msg = c.Run()
        self.Pkt.append(msg)

    def Reconstruct(self):
        return

    def Post(self):

        while self.httpStatus == 200 or self.httpStatus == 406:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.IP, self.http))
            header = 'POST /session HTTP/1.1\r\n'
            host = 'HOST: ' + self.IP + ":8190\r\n"
            contentlength = 'Content-Length: ' + \
                str(len(self.res_msg)) + '\r\n\r\n'
            data = header + host + contentlength + self.res_msg

            s.sendall(str.encode(data))
            status = s.recv(4096)

            if "200" in status.decode():
                httpStatus = 200
                print('Post success.')
            elif "406" in status.decode():
                httpStatus = 406
                print('Post failed.')
            elif "205" in status.decode():
                httpStatus = 205
                print('Message revocered.')
            else:
                print('Unexpected status.')
