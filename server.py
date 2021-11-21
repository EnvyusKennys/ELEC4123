# draft for control server

import socket
import requests
from client import Client

class Server():
    def __init__(self):
        self.msg_dict = {}
        self.httpStatus = 200
        self.IP = '149.171.36.192'
        self.http = 8190
        self.res_msg = ''

    def GetMessage(self):
        c = Client()
        self.msg_dict = c.Run()
        
    def Reconstruct(self):
        # Mod [msg_id] with [whole_message_length] to get the position of the this msg
        pkt_per_msg = len(self.msg_dict)
        # Msg_position is a dictionary with [key: msg_position, value: msg_id]
        msg_position = {}
        for id in self.msg_dict.keys():
            msg_id_int = int(id,16)
            # When pkt/msg is longer than msg_id, mod operation will not work
            if pkt_per_msg > msg_id_int:
                mod_id = msg_id_int - pkt_per_msg
                msg_position[mod_id] = id
            # When pkt/msg is shorter than msg_id, use mod operation
            else:
                mod_id = (msg_id_int)%(pkt_per_msg)
                if mod_id == 0:
                    mod_id = pkt_per_msg
                msg_position[mod_id] = id
        # Decode the message with 'utf-8'
        for position in sorted(msg_position):
            original_id = msg_position[position]
            self.res_msg = self.res_msg + self.msg_dict[original_id].decode('utf-8')
        self.res_msg = self.res_msg[self.res_msg.find('\x04')+1:] + self.res_msg[:self.res_msg.find('\x04')+1]
        
        return self.res_msg

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
                print('Message recovered.')
            else:
                print('Unexpected status.')

control_server = Server()
control_server.GetMessage()
control_server.Reconstruct()
control_server.Post()
