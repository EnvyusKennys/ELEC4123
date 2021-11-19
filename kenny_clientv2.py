'''
ELEC4123 DP - Network Task Client
>>> Yijie Shen (z5211003)
>>> Zhelin Jia (z5140809)
>>> Guxi Liu (z5210591)
>>> Jun Han (z5206270)
'''
import socket
import random
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
    for Pr in range(1,1000):
        # '!' -> Netwrok format which is Big-Endian; 'I' Unsigned integer which is 4 bytes each
        print(f'----- Receiving Message Pr No. [{Pr}] -----')
        snoop_request = pack('!II', Sr, Pr) 
        s.sendall(snoop_request)
        res = s.recv(1024)
        res_hex = res.hex()
        # Get the same message for at least 5 times
        if res_hex.endswith('04'):
            if msg_repeated == 3:
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
    pkt_per_msg = len(msg_dict)
    for id in msg_dict.keys():
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

    final_msg = ''
    for position in sorted(msg_position):
        original_id = msg_position[position]
        final_msg = final_msg + msg_dict[original_id].decode('utf-8')

    final_msg = final_msg[final_msg.find('\x04')+1:] + final_msg[:final_msg.find('\x04')+1]

    print('Sr is:', Sr)
    print('Pr list:', Pr_l)
    print('Lengh of messages:', msg_len_l)
    print('Message ID list:', id_l)
    print('Message ID list int format:', id_l_int)
    print('Message dictionary:', msg_dict)
    print('Final message:', final_msg)
    msg_1000 = 'Mdtufx2UMHDk1BddiTT3SS0T8sEbLUReC6kwg2cgiETUgj7Ia1xjKgfUVs3RipVOgrUKvg0mgOZRuVuLZlLHtCmpa0XjhRfsj6n49UxlYUA0XCbrLAdCQV7e7yO0SwTIFwlrbcvQCeAecJeT3W1ZiLafgFEmztYLLNoSWs03tfSLxIKeTqrklgYWPlCwcspBbQjaD00ROD194olhJFt3gXX6nwOCVoPwjzJ28Fcd3pCeNAgrEHcMG975BaOFRtUCaqGjBzgCw7OrLES1G5f8gE8mCvdxspe72lzbQ1d6qO2owNW8iBLFxFbKUqwVmkGbO4oGUkEjhGOY1GmDcg1VASfCdc4ERSgJYFalUInwKIkFCMyqc6OJzvaENPYkPPeB4tn5ia6Z1yNZUYogALI7qWKOTfVY9iPYagLZmhMWsftpbe50DfEk5ih25FYgUyS0P5LoVl5MN5YkVf5CsSsGPvLiz8UtVR7J0dB4jc6DWwJcR4EUXbiOns75oe4qVKlrr2AFvd0FGbh0OoKMdxRQ3AZhreLQUVUuFJQlSpdNMufC3ApKVwQNE4VTUMnULXrnuutjb4hNhdG2Z8gl3WBOZrAuAabpsREEgYVqsXtWzsd7SGeYSJrTM03hJEnSzSBeOj0tZBQMlMyxqiWlCzTN83qNRu4elspuH77i74EQ0s4m1J6l50F9uDm179vQKIULhXKbNzf5oJXTQDCm48sGqIWjuXCmzDsEAfd5FlEgTCCURguGnXzGWuefkFGDeCOh2mr8HlnAIRoBVaCHO9HPsT9QEqUHR6GAjPSjO0W9H4oKTOFMaPrD10qS3wia5pTbxSVCr4ABauhrYd8A0jLmurvdSBsdPcSsbZH2nW2DF6M3IHiAMVEDfxvZZSx7rTVcsLZTH466V0JUI61xHqDCcgpweEvYcnjKXDyg1YlofpIg5JhhpCXXHrsihGBeDMOXVXxXZWdQbSghML3zuaZKPTw7w8wbN6nWs37HUD0q\x04'
    msg_2000 = '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\x04'
    if final_msg == msg_2000:
        print('FUCK YEEEE!')
    else: 
        print('AH SHIT!')
