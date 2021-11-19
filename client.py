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
                print('----- Socket Connected! -----')
            except s.error as err:
                print('----- Socket Connection Failed! -----')

            # Sending snoop request & Receiving message from the server
            # Sr is a random number between 10-20
            Sr = random.randint(10, 20)
            print('Sr is:', Sr)
            msg_repeated = 0
            Pr_l = []
            id_l = []
            id_l_int = []
            msg_len_l = []
            msg_dict = {}
            # Send snoope request with differnt [Pr] to get differnt responses
            for Pr in range(1,2000):

                # '!' -> Netwrok format which is Big-Endian; 'I' Unsigned integer which is 4 bytes each
                print(f'----- Sr [{Sr}]: Receiving Message Pr No. [{Pr}] -----')
                snoop_request = pack('!II', Sr, Pr) 
                s.sendall(snoop_request)
                res = s.recv(1024)
                res_hex = res.hex()
                # Get the same message for at least 5 times
                if res_hex.endswith('04'):
                    if msg_repeated == 3:
                        print('----- At least 3 [\x04] received. Client Stop! ------\n')
                        break
                    else:
                        msg_repeated+=1

                # Get rid of duplicate response base on received Pr
                rec_pr = res_hex[0:8]
                if rec_pr in Pr_l:
                    continue
                else:
                    Pr_l.append(rec_pr)
                
                # Store received messages in a dictionary [key: msg_identifier, value: msg]
                msg = res[8:]
                msg_len = len(msg)
                msg_id = res_hex[8:16]
                if msg in msg_dict.values():
                    continue
                else:
                    id_l.append(msg_id)
                    id_l_int.append(int(msg_id,16))
                    msg_len_l.append(msg_len)
                    msg_dict[msg_id] = msg
            
            # Closing socket
            try:
                s.close()
                print('----- Socket Closed! -----')
            except:
                print('----- Socket Closing Failed! -----')

            return msg_dict

# c = Client()
# c.Run()
