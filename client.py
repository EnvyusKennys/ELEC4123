# python3

import socket
import random
from struct import *

class Client():

    def __init__(self):
        self.host = '149.171.36.192'
        self.snoop_port = 8189

    def Run(self):
        # Creating socket [AF_INET: IPv4, SOCK_DGRAM: UDP]
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connecting to the server
            try:
                s.connect((self.host,self.snoop_port))
                print('---------- Socket Connected! ----------\n')
            except s.error as err:
                print('---------- Socket Connection Failed! ----------\n')

            # Sending snoop request & Receiving msg from server with Sr = random number between 10-20
            Sr = random.randint(10, 20)
            multi_dup_check = 0
            msg_repeated = 0
            Pr_l = []
            id_l = []
            id_l_int = []
            msg_len_l = []
            msg_dict = {}
            # Send snoope request with differnt [Pr] to get differnt responses
            for Pr in range(1,2000):

                # '!' -> Netwrok format which is Big-Endian; 'I' Unsigned integer which is 4 bytes each
                print(f'--- Sr [{Sr}]: Receiving Message Pr No. [{Pr}] ---')
                snoop_request = pack('!II', Sr, Pr) 
                s.sendall(snoop_request)
                res = s.recv(1024)
                res_hex = res.hex()
                # Get the same message for at least 3 times to make sure all msg received
                if res_hex.endswith('04'):
                    if msg_repeated == 3:
                        print('<<< SUCCESS: All Message Packets Received. Client Stop! >>>\n')
                        break
                    else:
                        msg_repeated+=1

                # Get rid of duplicate response base on received Pr
                rec_pr = res_hex[0:8]
                if rec_pr in Pr_l:
                    continue
                else:
                    Pr_l.append(rec_pr)
                
                # Store received msg in a dictionary [key: msg_identifier, value: msg]
                msg = res[8:]
                msg_len = len(msg)
                msg_id = res_hex[8:16]
                # Get rid of duplicate msg
                if msg in msg_dict.values():
                    # If 10 consecutive dup msgs received -> Sr is a mutiple of pkt/msg -> change Sr
                    multi_dup_check+=1
                    if multi_dup_check == 10:
                        print(f'<<< WARNING: Bad Sr [{Sr}] Detected. Sr Changed to [{Sr+1}] >>>\n')
                        Sr+=1
                    continue
                else:
                    # No consecutive dup msgs found, store msg
                    multi_dup_check = 0
                    id_l.append(msg_id)
                    id_l_int.append(int(msg_id,16))
                    msg_len_l.append(msg_len)
                    msg_dict[msg_id] = msg
            
            # Closing socket
            try:
                s.close()
                print('---------- Socket Closed! ----------\n')
            except:
                print('---------- Socket Closing Failed! ----------\n')

            return msg_dict
