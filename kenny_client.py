'''
ELEC4123 DP - Network Task Client
>>> Yijie Shen (z5211003)
>>> Zhelin Jia (z5140809)
>>> Guxi Liu (z5210591)
>>> Jun Han (z5206270)
'''
import socket
import time
from struct import*
import select
import random
import requests

# The server's IP address and port number
HOST = '149.171.36.192'
PORT = 8189

# '!' -> Network format which is Big-Endian; 'I' -> Unsigned integer which is 4 bytes long
# Sr = 1
# Pr = 12
# snoop_request = pack('!II', Sr, Pr) 
# print(snoop_request)

print('1. Creating socket')
# AF_INET -> IPv4, SOCK_DGRAM -> UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print('2. Connecting to the server')
    try:
        s.connect((HOST,PORT))
        print('Socket connected.')
    except s.error as err:
        print('Socket failed.')

    # print('3. Sending message: ' + str(snoop_request) + ' to the server')
    # s.sendall(snoop_request)

    print('4. Receiving message from the server')
    Sr = 1
    for Pr in range(1,11):
        print('Enter While Loop!')
        snoop_request = pack('!II', Sr, Pr) 
        s.sendall(snoop_request)
        data = s.recv(1024)
        # if len(data) <= 0:
        #     break
        # if not data:
        #     break
        # Hex the data
        data_hex = data.hex()
        # Print the data
        print('Received:', data)
        print('Hex Data: ', data_hex)
        print('Pr: ', data_hex[0:8])
        print('Msg Identifier: ', data_hex[8:16])
        print('Actual Msg: ', data_hex[16:])
        time.sleep(2)

    print('5. Closing the socket')
    s.close()
