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

# message_byte = bytes('Sr', 'utf-8')

# Sr = '0000000000110010'
# Pr = '0000000000110010'
# Sr = '1100100000000000'
# Pr = '1100100000000000'
# message_byte = (Sr + Pr).encode()

# message_byte = bytes('0010' + '0010', 'utf-8')
# message_byte = b'\x35\x35\x35\x35\x35\x35\x35\x35'

# '!' -> Network format which is Big-Endian; 'I' -> Unsigned integer which is 4 bytes long
message_byte = pack('!II', 1, 100) 

# Sr = 1
# Pr = 50
# message_byte = Sr.to_bytes(4, 'big') + Pr.to_bytes(4, 'big')

snoop_request = message_byte
print(snoop_request)

print('1. Creating socket')
# AF_INET -> IPv4, SOCK_DGRAM -> UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print('2. Connecting to the server')
    #s.connect((HOST, PORT))
    try:
        s.connect((HOST,PORT))
        print('Socket connected.')
    except s.error as err:
        print('Socket failed.')

    print('3. Sending message: ' + str(snoop_request) + ' to the server')
    #s.send(snoop_request.encode('utf-8'))
    #for i in range(1,100):
    s.sendall(snoop_request)
    #s.sendto(snoop_request, (HOST, PORT))

    print('4. Receiving message from the server')
    while True: 
        #s.sendall(snoop_request)
        print('Enter While Loop!')
        data = s.recv(1024)
        print('Data Received!')
        print('Received:', data)
        if len(data) <= 0:
            break
        if not data:
            break
        # decode the data with utf-8
        data_decoded = data.decode('utf-8')
        data_hex = data.hex()
        # print the data
        print('Received:', data)
        print('Decoded: ', data_decoded)
        print('Hex Data: ', data_hex)
        #time.sleep(1)

    print('5. Closing the socket')
    s.close()
