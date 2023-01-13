#!/usr/bin/expect -f

set timeout -1
spawn /usr/bin/telnet 10.0.10.17

#expect "Username(1-32 chars):"
expect "Username"
send -- "admin\n"

expect "Password"
send -- "88776655\n"

expect "QTECH"
send -- "show ip\n"

expect "QTECH"
send -- "exit\n"

expect eof
