'''
ELEC4123 DP - Network Task Client
>>> Yijie Shen (z5211003)
>>> Zhelin Jia (z5140809)
>>> Guxi Liu (z5210591)
>>> Jun Han (z5206270)
'''
import socket
from struct import*

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
    Sr = 19
    msg_repeated = 0
    Pr_l = []
    id_l = []
    id_l_int = []
    msg_len_l = []
    msg_dict = {}
    # Send snoope request with differnt [Pr] to get differnt responses
    for Pr in range(1,1000):
        # '!' -> Netwrok format which is Big-Endian; 'I' Unsigned integer which is 4 bytes each
        print(f'----- Receiving Message Pr No. [{Pr}] -----')
        snoop_request = pack('!II', Sr, Pr) 
        s.sendall(snoop_request)
        res = s.recv(1024)
        res_hex = res.hex()
        # Get the same message for at least 5 times
        if res_hex.endswith('04'):
            if msg_repeated == 5:
                print('----- Five [\x04] received, Break For-loop! ------\n')
                break
            else:
                msg_repeated+=1

        # Get rid of duplicate response base on received Pr
        rec_pr = res_hex[0:8]
        if rec_pr in Pr_l:
            print('----- Duplicate Pr Received! -----')
            print('Duplicate Meassge Received:', res)
            print('Hex res:', res_hex)
            print('Pr:', res_hex[0:8])
            print('Msg Identifier:', res_hex[8:16])
            print('Actual Msg:', res_hex[16:], '\n')
            continue
        else:
            Pr_l.append(rec_pr)
        
        # Store received messages in a dictionary [key: msg_identifier, value: msg]
        msg = res[8:]
        msg_len = len(msg)
        msg_id = res_hex[8:16]
        if msg in msg_dict.values():
            print('----- Duplicate Message! -----')
            print('Last Meassge Received:', res)
            print('Hex res:', res_hex)
            print('Pr:', res_hex[0:8])
            print('Msg Identifier:', res_hex[8:16])
            print('Actual Msg:', res_hex[16:], '\n')
            continue
        else:
            id_l.append(msg_id)
            id_l_int.append(int(msg_id,16))
            msg_len_l.append(msg_len)
            msg_dict[msg_id] = msg
        
        # Print responses
        print('Received:', res)
        print('Hex res:', res_hex)
        print('Pr:', res_hex[0:8])
        print('Msg Identifier:', res_hex[8:16])
        print('Actual Msg:', res_hex[16:], '\n')

    print('5. Closing the socket.')
    try:
        s.close()
        print('----- Socket Closed! -----')
    except:
        print('----- Socket Closing Failed! -----')

    # Mod [msg_id] with [whole_message_length] to get the position of the this msg
    # Msg_position is a dictionary with [key: msg_position, value: msg_id]
    msg_position = {}
    whole_msg_len = len(msg_dict)
    for id in msg_dict.keys():
        msg_id_int = int(id,16)
        mod_id = msg_id_int%whole_msg_len
        if mod_id == 0:
            mod_id = whole_msg_len
        msg_position[mod_id] = id

    final_msg = ''
    for position in sorted(msg_position):
        original_id = msg_position[position]
        final_msg = final_msg + msg_dict[original_id].decode('utf-8')

    print('Pr list:', Pr_l)
    print('Lengh of messages:', msg_len_l)
    print('Message ID list:', id_l)
    print('Message ID list int format:', id_l_int)
    print('Message dictionary:', msg_dict)
    print('Final message:', final_msg)
