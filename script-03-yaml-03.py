#!/usr/bin/env python3

import io
import json
import socket
import sys
import yaml

hosts = ('drive.google.com', 'mail.google.com', 'google.com')

new_format = 'yaml'

data_in = []


def data_check(sample_data):
    """Проверка  хостов входного файла."""
    try:
        for [o_host] in [x.keys() for x in sample_data]:
            if o_host not in hosts:
                print(f'Warning host {host} will be replaced')
        return True
    except Exception as exp:
        return False


if len(sys.argv) > 2:
    print('Error: Support only one file')
    exit(1)
elif len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print('Error: Need file name') 
    exit(1)

if not filename.endswith('.json') and not filename.endswith('.yaml'):
    print(f'Wrong type extension{filename}')
    exit(1)


with open(filename, 'r') as stream:
    try:
        print(f'Try {filename} as json format')
        data_in = json.load(stream)
    except json.JSONDecodeError as exc:
        print(f'File name as json have error {exc}, try as yaml format')
        with open(filename, 'r') as second_stream:
            try:
                data_in = yaml.safe_load(second_stream)
                new_format = 'json'
            except yaml.YAMLError as exc:
                print(f'File name as yaml have error {exc}')
                exit(1)

if not data_check(data_in):
    print(f'File  {filename} data format will be replaced')
    data = []
    for one_host in hosts:
        data.append ({one_host: '0.0.0.0'})
    data_in = data

data_out = []
for [[host, addr]] in [x.items() for x in data_in]:
    new_addr = socket.gethostbyname(host)
    if addr != new_addr:
        print('ERROR  {} IP mismatch: {} {}.'.format(host, addr, new_addr))
    data_out.append({host: new_addr})


file_info = filename.split('.')
if new_format == 'yaml':
    new_filename = f'{file_info[0]}.yaml'
    with io.open(new_filename, 'w', encoding='utf8') as outfile:
        yaml.dump(data_out, outfile, default_flow_style=False, allow_unicode=True)
else:
    new_filename = f'{file_info[0]}.json'
    with open(new_filename, "w") as outfile:
        json.dump(data_out, outfile)

print(f'Input file {filename} updated and stored in file {new_filename}')
