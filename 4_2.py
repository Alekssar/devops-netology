#!/usr/bin/env python3

import socket
import time

server_ip = {'drive.google.com':'', 'mail.google.com':'', 'google.com':''}
print("Start cheking IP.")
while(1==1):
    for srv in server_ip.keys():
        ip = socket.gethostbyname(srv)
        if(ip == server_ip[srv]):
            print(f'{srv} - {ip}')
        elif(server_ip[srv]==''):
            server_ip[srv] = ip
        else:
            print(f'[ERROR] {srv} IP mismatch: {server_ip[srv]} {ip}')
            server_ip[srv] = ip
    time.sleep(10)