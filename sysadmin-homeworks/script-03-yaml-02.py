#!/usr/bin/env python3

import io
import json
import socket
import yaml

hosts = ('drive.google.com', 'mail.google.com', 'google.com')
filename = 'hosts_state.json'

try:
    f = open(filename)
    data = json.load(f)
    f.close()

except FileNotFoundError:
    data = []
    for one_host in hosts:
        data.append ({one_host: '0.0.0.0'})

data_out = []
for [[host, addr]] in [ x.items() for x in data]:
    new_addr = socket.gethostbyname(host)
    if addr != new_addr:
        print('ERROR  {} IP mismatch: {} {}.'.format(host, addr, new_addr))
        # [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>.
    data_out.append({host: new_addr})


with open(filename, "w") as outfile:
    json.dump(data_out, outfile)
    print ('Store json')

with io.open('hosts_state.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data_out, outfile,default_flow_style=False, allow_unicode=True)
    print ('Store yaml')

