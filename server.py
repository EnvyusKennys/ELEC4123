'''
ELEC4123 DP - Network Task Control Server
>>> Yijie Shen (z5211003)
>>> Zhelin Jia (z5140809)
>>> Guxi Liu (z5210591)
>>> Jun Han (z5206270)
'''
import socket
import random
from client import Client

class Server():
    def __init__(self):
        self.IP = '149.171.36.192'
        self.http = 8190
        self.snoop = 8189
        self.httpStatus = 200
        self.Sr = 0
        self.Pr = 0
        self.msg_no = 1
        self.msg_repeated = 0
        self.multi_dup_check = 0
        self.Pr_l = []
        self.msg_dict = {}
        self.res_msg = ''

    def GetMessage(self, client_socket, Sr, Pr):
        # Send snoope request with differnt [Pr] to get differnt responses
        for Pr in range(1,2000):
            # One client connet and get one response
            client1 = Client(client_socket, Sr, Pr, self.IP, self.snoop)
            res = client1.Run()
            res_hex = res.hex()
            # Get the same message for at least 3 times to make sure all msg received
            if res_hex.endswith('04'):
                if self.msg_repeated == 3:
                    print('<<< SUCCESS: All Message Packets Received. Client Stop! >>>')
                    break
                else:
                    self.msg_repeated+=1
            # Get rid of duplicate response base on received Pr
            rec_pr = res_hex[0:8]
            if rec_pr in self.Pr_l:
                continue
            else:
                self.Pr_l.append(rec_pr) 
            # Store received msg in a dictionary [key: msg_identifier, value: msg]
            msg = res[8:]
            msg_id = res_hex[8:16]
            # Get rid of duplicate msg
            if msg in self.msg_dict.values():
                # If 10 consecutive dup msgs received -> Sr is a mutiple of pkt/msg -> change Sr
                multi_dup_check+=1
                if multi_dup_check == 10:
                    print(f'<<< WARNING: Bad Sr [{Sr}] Detected. Sr Changed to [{Sr+1}] >>>\n')
                    Sr+=1
                continue
            else:
                # No consecutive dup msgs found, store msg
                multi_dup_check = 0
                self.msg_dict[msg_id] = msg
        
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

    def Run(self):
        # Creating socket for clients [AF_INET: IPv4, SOCK_DGRAM: UDP]
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            while self.httpStatus == 200 or self.httpStatus == 406:
                print(f'---------- Recovering Message No. [{self.msg_no}] ----------\n')
                # Get new message and reconstruct the message
                self.Sr = random.randint(10, 20)
                self.Pr = 0
                self.msg_repeated = 0
                self.multi_dup_check = 0
                self.Pr_l = []
                self.msg_dict = {}
                self.res_msg = ''
                self.GetMessage(client_socket, self.Sr, self.Pr)
                self.Reconstruct()

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
                    self.httpStatus = 200
                    print('<<< Post Success! >>>\n')
                elif "406" in status.decode():
                    self.httpStatus = 406
                    print('<<< Post Failed! >>>\n')
                elif "205" in status.decode():
                    self.httpStatus = 205
                    print('<<< All Messages Recovered! >>>\n')
                else:
                    print('<<< Unexpected Status! >>>\n')
                self.msg_no+=1
            
            # Closing client socket
            try:
                client_socket.close()
                print('---------- Client Socket Closed! ----------\n')
            except:
                print('---------- Client Socket Closing Failed! ----------\n')
            # Clsoing http server socket
            try:
                s.close()
                print('---------- HTTP Server Socket Closed! ----------\n')
            except:
                print('---------- HTTP Server Socket Closing Failed! ----------\n')

control_server = Server()
control_server.Run()
