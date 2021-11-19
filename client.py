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
Pkts = []
EOF_Pkts = []
Uni_Pkts = set()
Dist = []
res_msg = ''
httpStatus = 200
end_msg = ''

while httpStatus == 200 or httpStatus == 406:
    while len(EOF_Pkts) < 5:
        msg = c.Run()

        if msg is None:
            print('Snoop failed.')
            c.Close()
            quit()
        if "\x04" in msg[1]:
            print('EOF found')
            EOF_Pkts.append(msg[0])
            end_msg = msg[1]

            Pkts.append([msg[0], msg[1]])
            Uni_Pkts.add(msg[1])

    print('Totally 5 EOF has detected.')
    i = 1

    while i < len(EOF_Pkts):
        Dist.append(EOF_Pkts[i] - EOF_Pkts[i-1])
        i = i + 1

    print('Dist length:', str(len(Dist)))
    j = 1

    while j < len(Dist):
        flag = 1
        length = Dist[j]
        messages: List[str] = [''] * length
        for pkt in Pkts:
            index = (int(pkt[0]) - int(EOF_Pkts[0] - 1)) % length
            print(str(index))
            if messages[index] == '':
                messages[index] = pkt[1]
            else:
                if messages[index] != pkt[1]:
                    print(f'Combine error with corresponding length {length}')
                    flag = 0

        if flag == 1:
            res_msg == ''.join(messages)
            print('message: ', res_msg)
            break
        j = j + 1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((c.IP, c.http))
    header = 'POST /session HTTP/1.1\r\n'
    host = 'HOST: ' + c.IP + ":8190\r\n"
    contentlength = 'Content-Length: ' + str(len(res_msg)) + '\r\n\r\n'
    data = header + host + contentlength + res_msg

    s.sendall(str.encode(data))
    status = s.recv(4096)

    if "200" in status.decode():
        httpStatus = 200
        print('Post success.')
    elif "406" in status.decode():
        httpStatus = 406
        print('Post failed.')
    else:
        httpStatus = 205
