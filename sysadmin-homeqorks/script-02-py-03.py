#!/usr/bin/env python3

import os
import sys

# root_path='~/netology/sysadm-homeworks'
root_path='/home/alexey/Projects/devops-netology'
current_path = sys.path[0]
if len(sys.argv) > 2:
    print('Error: Support only one path')
    exit(1)
elif len(sys.argv) == 2:
    full_path = sys.argv[1]
else: 
    full_path = current_path

if not full_path.startswith(root_path):
    print('Error: Not supported  path')
    exit(1)

bash_command = ['cd {}'.format(full_path), 'git ls-files -dmo']
result_os = os.popen(' && '.join(bash_command)).readlines()
for one_row in result_os:
    out_line = full_path + '/' + one_row
    print (out_line,end='')

