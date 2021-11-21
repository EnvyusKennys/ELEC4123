'''
ELEC4123 DP - Network Task Client
>>> Yijie Shen (z5211003)
>>> Zhelin Jia (z5140809)
>>> Guxi Liu (z5210591)
>>> Jun Han (z5206270)
'''
from struct import *

class Client():

    def __init__(self, client_socket, Sr, Pr, host, port):
        self.Sr = Sr
        self.Pr = Pr
        self.client_socket = client_socket
        self.snoop_host = host
        self.snoop_port = port

    def Run(self):
        # Connecting to the server
        try:
            self.client_socket.connect((self.snoop_host,self.snoop_port))
            print('---------- Socket Connected! ----------\n')
        except self.client_socket.error as err:
            print('---------- Socket Connection Failed! ----------\n')

        # '!' -> Netwrok format which is Big-Endian; 'I' Unsigned integer which is 4 bytes each
        print(f'--- Sr [{self.Sr}]: Receiving Message Pr No. [{self.Pr}] ---')
        snoop_request = pack('!II', self.Sr, self.Pr) 
        self.client_socket.sendall(snoop_request)
        res = self.client_socket.recv(1024)
        
        return res
        
