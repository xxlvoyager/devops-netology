#!/usr/bin/env python3

import os
import sys

current_path = sys.path[0]

bash_command = ['cd {}'.format(current_path), 'git ls-files -dmo']
result_os = os.popen(' && '.join(bash_command)).readlines()
for one_row in result_os:
    out_line = current_path + '/' + one_row
    print (out_line,end='')

