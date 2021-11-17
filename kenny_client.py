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

# AF_INET -> IPv4, SOCK_DGRAM -> UDP
print('1. Creating socket.')
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print('2. Connecting to the server.')
    try:
        s.connect((HOST,PORT))
        print('----- Socket Connected! -----')
    except s.error as err:
        print('----- Socket Connection Failed! -----')

    print('3. Sending snoop request & Receiving message from the server.')
    Sr = 1
    Pr = 1
    Pr_l = []
    msg_dict = {}
    while True:
        # Send snoope request then get the hex of the response
        print(f'----- Receiving Message No. [{Pr}] -----')
        snoop_request = pack('!II', Sr, Pr) 
        s.sendall(snoop_request)
        res = s.recv(1024)
        res_hex = res.hex()
        # Get rid of duplicate response base on received Pr
        rec_pr = res_hex[0:8]
        if rec_pr in Pr_l:
            Pr+=1
            print('----- Duplicate Pr Received! -----')
            print('Duplicate Meassge Received:', res)
            print('Hex res:', res_hex)
            print('Pr:', res_hex[0:8])
            print('Msg Identifier:', res_hex[8:16])
            print('Actual Msg:', res_hex[16:], '\n')
            time.sleep(1)
            continue
        else:
            Pr_l.append(rec_pr)
        # Store received messages in a dictionary [key: msg_identifier, value: msg]
        msg_iden = res_hex[8:16]
        msg = res_hex[16:]
        if msg in msg_dict.values():
            print('----- All Message Received! -----')
            # Print responses
            print('Last Meassge Received:', res)
            print('Hex res:', res_hex)
            print('Pr:', res_hex[0:8])
            print('Msg Identifier:', res_hex[8:16])
            print('Actual Msg:', res_hex[16:], '\n')
            break
        else:
            msg_dict[msg_iden] = msg
        # Print responses
        print('Received:', res)
        print('Hex res:', res_hex)
        print('Pr:', res_hex[0:8])
        print('Msg Identifier:', res_hex[8:16])
        print('Actual Msg:', res_hex[16:], '\n')
        # Incrementing Pr to get differnt responses
        Pr+=1
        time.sleep(1)

    print('5. Closing the socket.')
    try:
        s.close()
        print('----- Socket Closed! -----')
    except:
        print('----- Socket Closing Failed! -----')

    print(Pr_l)
    print(msg_dict)
