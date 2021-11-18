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
from typing import final
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
    #Sr = 13
    Sr = 1
    Pr = 1
    Pr_l = []
    iden_l = []
    msg_dict = {}
    # Send snoope request then get the hex of the response
    while True:
        # '!' -> Netwrok format which is Big-Endian; 'I' Unsigned integer which is 4 bytes each
        print(f'----- Receiving Message Pr No. [{Pr}] -----')
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
            time.sleep(0.1)
            continue
        else:
            Pr_l.append(rec_pr)
        
        # Store received messages in a dictionary [key: msg_identifier, value: msg]
        msg_iden = res_hex[8:16]
        #msg = res_hex[16:]
        msg = res[8:]
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
            iden_l.append(msg_iden)
            msg_dict[msg_iden] = msg
        
        # Print responses
        print('Received:', res)
        print('Hex res:', res_hex)
        print('Pr:', res_hex[0:8])
        print('Msg Identifier:', res_hex[8:16])
        print('Actual Msg:', res_hex[16:], '\n')
        # Incrementing Pr to get differnt responses
        Pr+=1
        time.sleep(0.1)

    print('5. Closing the socket.')
    try:
        s.close()
        print('----- Socket Closed! -----')
    except:
        print('----- Socket Closing Failed! -----')

    final_msg = ''
    for key in sorted(msg_dict):
        final_msg = final_msg + msg_dict[key].decode('utf-8')

    print('Pr list:', Pr_l)
    print('Message ID list:',iden_l)
    print('Message dictionary:',msg_dict)
    print('Final message:',final_msg)
