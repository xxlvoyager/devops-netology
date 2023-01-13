#!/usr/bin/env python3

import json
import socket

hosts = ('drive.google.com', 'mail.google.com', 'google.com')
filename = 'hosts_state.json'

try:
    f = open(filename)
    data = json.load(f)
    f.close()

except FileNotFoundError:
    data = {}

for one_host in hosts:
    new_addr = socket.gethostbyname(one_host)
    try:    
        old_addr = data[one_host]
        if old_addr != new_addr:
            print('ERROR  {} IP mismatch: {} {}.'.format(one_host, old_addr, new_addr))
            # [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>.
            data[one_host] = new_addr
        else:
            print(one_host,'-',data[one_host])
    except  KeyError:
        data[one_host] = new_addr


with open(filename, "w") as outfile:
    json.dump(data, outfile)

