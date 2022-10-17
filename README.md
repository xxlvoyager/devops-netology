# Домашнее задание к занятию "3.2. Работа в терминале, лекция 2"

1. Комманда `cd` является встроенной в shell, команды делаются встроенными либо из соображений производительности -- встроенные команды исполняются быстрее, чем внешние, которые, как правило, запускаются в дочернем процессе, либо из-за необходимости прямого доступа к внутренним структурам командного интерпретатора.
2. `grep -c <some_string> <some_file>` эквивалент `grep <some_string> <some_file> | wc -l`
3. PID 1  /sbin/init         линк  /sbin/init -> /lib/systemd/systemd
4. ls > /dev/{terminal} or  or /dev/{pseudoterminal}/num конкретно в виртуальноей машине находясь в pts/1   ls / > /dev/pts/0 
5. из pts/1     ps |tee  /dev/pts/0  
6. Возможно перенаправить из pts в tty например: ls > /dev/tty6
7. Выполнение комманды bash 5>&1 приевдет к созданию дочернего процесса с файловым дескриптором 5 и он будет перенаправлен в stdout родительский процесса, теперь если выполнить echo netology > /proc/$$/fd/5 то сообщение netology появиться в консоле.
8. После выполнения комманды bash 5>&1 можно перенаправить вывод следующим образом <some_command> 2>/dev/stdout 1> /dev/fd/5 | <another_command>.
9. Комманда cat /proc/$$/environ выведет данные окружения для текущего процесса, иначе эти данные можно получить командой env
10. Файл только для чтения `/proc/[pid]/cmdline` содержит полную коммандную стороку процесса PID.
Файл `/proc/[pid]/exe` В Linux 2.2 и более поздних версиях этот файл представляет собой символическую ссылку, содержащую фактический путь к выполняемой команде.     
11. Процессор AMD Ryzen 7 поддерживает SSE  начиная с SSE до SSE4.2
12. Что бы выполнить удаленныей запрос нужно изменить конфиг .ssh/config
    добавив в строчку `RequestTTY yes` или использовать опцию 
    `ssh  -o "requestTTY=yes" localhost tty`. 
13. Работает если добавить `echo 0 > /proc/sys/kernel/yama/ptrace_scope`
или поправить ptrace_scope в `/etc/sysctl.d/10-ptrace.conf`.<br>
В консоле 1 `desown <pid_or_name_bg_process>`<br>
В консоле 2 `repryr <pid>`
14. Команда  `sudo echo string > /root/new_file` выполняется в оболочке пользователя, которая не имеет прав на создание файла в директории root
в случае с коммандой `echo string | sudo tee /root/new_file` для tee будет создана новая оболчка с правами root.
Комманда tee пзваоляет читать стандартный ввод и направлять его в стандартный вывод и файл(ы).