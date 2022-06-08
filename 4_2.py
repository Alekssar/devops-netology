#!/usr/bin/env python3

import socket
import time
import json
import yaml

srv_ip = {'drive.google.com':'', 'mail.google.com':'', 'google.com':''}
print("Start cheking IP.")
while(1==1):
    for srv in srv_ip.keys():
        ip = socket.gethostbyname(srv)
        if(ip == srv_ip[srv]):
            print(f'{srv} - {ip}')
        elif(srv_ip[srv]==''):
            srv_ip[srv] = ip
        else:
            print(f'[ERROR] {srv} IP mismatch: {srv_ip[srv]} {ip}')
            srv_ip[srv] = ip
    with open ("dz43.json", 'w') as js_file:
        js_file.write(json.dumps(srv_ip))
    with open ("dz43.yml", 'w') as yaml_file:
        yaml_file.write(yaml.dump(srv_ip))
    time.sleep(10)