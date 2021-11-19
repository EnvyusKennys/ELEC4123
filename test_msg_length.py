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
                print('----- Five [\x04] received, Break For-loop! ------\n')
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

    # Testing:
    print('Sr is:', Sr)
    print('Pr list:', Pr_l)
    print('Lengh of messages:', msg_len_l)
    print('Message ID list:', id_l)
    print('Message ID list int format:', id_l_int)
    print('Message dictionary:', msg_dict)
    print('Final message:', final_msg)
    msg_1000 = 'Mdtufx2UMHDk1BddiTT3SS0T8sEbLUReC6kwg2cgiETUgj7Ia1xjKgfUVs3RipVOgrUKvg0mgOZRuVuLZlLHtCmpa0XjhRfsj6n49UxlYUA0XCbrLAdCQV7e7yO0SwTIFwlrbcvQCeAecJeT3W1ZiLafgFEmztYLLNoSWs03tfSLxIKeTqrklgYWPlCwcspBbQjaD00ROD194olhJFt3gXX6nwOCVoPwjzJ28Fcd3pCeNAgrEHcMG975BaOFRtUCaqGjBzgCw7OrLES1G5f8gE8mCvdxspe72lzbQ1d6qO2owNW8iBLFxFbKUqwVmkGbO4oGUkEjhGOY1GmDcg1VASfCdc4ERSgJYFalUInwKIkFCMyqc6OJzvaENPYkPPeB4tn5ia6Z1yNZUYogALI7qWKOTfVY9iPYagLZmhMWsftpbe50DfEk5ih25FYgUyS0P5LoVl5MN5YkVf5CsSsGPvLiz8UtVR7J0dB4jc6DWwJcR4EUXbiOns75oe4qVKlrr2AFvd0FGbh0OoKMdxRQ3AZhreLQUVUuFJQlSpdNMufC3ApKVwQNE4VTUMnULXrnuutjb4hNhdG2Z8gl3WBOZrAuAabpsREEgYVqsXtWzsd7SGeYSJrTM03hJEnSzSBeOj0tZBQMlMyxqiWlCzTN83qNRu4elspuH77i74EQ0s4m1J6l50F9uDm179vQKIULhXKbNzf5oJXTQDCm48sGqIWjuXCmzDsEAfd5FlEgTCCURguGnXzGWuefkFGDeCOh2mr8HlnAIRoBVaCHO9HPsT9QEqUHR6GAjPSjO0W9H4oKTOFMaPrD10qS3wia5pTbxSVCr4ABauhrYd8A0jLmurvdSBsdPcSsbZH2nW2DF6M3IHiAMVEDfxvZZSx7rTVcsLZTH466V0JUI61xHqDCcgpweEvYcnjKXDyg1YlofpIg5JhhpCXXHrsihGBeDMOXVXxXZWdQbSghML3zuaZKPTw7w8wbN6nWs37HUD0q\x04'
    msg_2000 = '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\x04'
    msg_2500 = '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\x04'
    msg_5000 = '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\x04'
    if final_msg == msg_1000:
        print('FUCK YEEEE!')
    else: 
        print('AH SHIT!')
