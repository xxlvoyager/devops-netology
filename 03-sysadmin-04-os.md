## 1.
Скачиваем программу

`wget https://github.com/prometheus/node_exporter/releases/download/v1.4.0/node_exporter-1.4.0.linux-amd64.tar.gz`

Распаковываем

`tar zxvf node_exporter-1.4.0.linux-amd64.tar.gz`

Копируем исполняемый файл в общедоступную папку

`sudo cp node_exporter-1.4.0.linux-amd64/node_exporter /usr/local/bin/`

Создаем файл для unit

`sudo systemctl edit --force --full node_exporter.service`

с содержимым

```
[Unit]

Description=Node_exporter daemon
After=syslog.target network.target

[Service]

ExecStart=/usr/local/bin/node_exporter
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Перечитываем конфигурационные файлы systemd

`sudo systemctl daemon-reload `

Создаем линк

`sudo systemctl enable node_exporter.service`

Стартуем сервис 

`sudo systemctl start node_exporter.service`

Смотрим стататус


`sudo systemctl status node_exporter.service`
```
● node_exporter.service - Node_exporter daemon
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-10-25 11:56:14 MSK; 39s ago
   Main PID: 1673 (node_exporter)
      Tasks: 4 (limit: 9484)
     Memory: 2.3M
     CGroup: /system.slice/node_exporter.service
             └─1673 /usr/local/bin/node_exporter
```

Если все ок, перегружаем VM поверям еще раз.
```
● node_exporter.service - Node_exporter daemon
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-10-25 11:58:35 MSK; 1min 37s ago
   Main PID: 707 (node_exporter)
      Tasks: 5 (limit: 9484)
     Memory: 14.1M
     CGroup: /system.slice/node_exporter.service
             └─707 /usr/local/bin/node_exporter
```

---
## 2.

Получаем от node_exporter информацию от свободном дисковом пространстве 

`curl localhost:9100/metrics 2>/dev/null |grep node_filesystem_free_bytes`

Получаем информацию об ошибках netstat

`curl localhost:9100/metrics 2>/dev/null |grep netstat |grep Errors`

Нагрузка на память

`curl localhost:9100/metrics 2>/dev/null |grep pressure_memory`

Нагрузку на процессор в разрезе ядер

`curl localhost:9100/metrics 2>/dev/null |grep node_cpu_seconds_total`

---
## 3.

### Скрин полученный при доступе по сети  VM Vagrant

<img src=https://raw.githubusercontent.com/xxlvoyager/devops-netology/main/Screenshot.png alt="Screenshot Netdata">

---

## 4.

Информация в dmesg при запуске на виртуальной машине:

Прерывания система получает ом VBOX

`DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006`

Так же виртульная машина видит гипервизор обеспечивающей виртуализацию

`Hypervisor detected: KVM`

---

## 5.
nr_open - максимальное количество файлов, которое может быть выделено одним процессом
в `man proc` описано значение по умолчанию 1048576

`sudo sysctl -a |grep fs.nr_open`

`fs.nr_open = 1048576`

иначе можно посмотреть
`cat /proc/sys/fs/nr_open`

Посмотреть все ограничения ulimit
`ulimit -a`

Максимальное количество файловых дескрипторов, которые могут быть открыты

`open files                      (-n) 1024`

Установить 

```
      -S	use the `soft' resource limit
      -H	use the `hard' resource limit
```

Мягкое и жесткое ограничение не может превышать nr_open

Таким образом для достижения пользователем максимального занчения nr_open

Необходимо выполнить
`ulimit -Hn 1048576`

`ulimit -Sn 1048576`

---

## 6.
Входим под суперпользователем

`sudo su`

Запускаем процесс в новом пространстве имен

`unshare -f --pid --mount-proc sleep 1h &`

ищем наш процесс

`ps aux |grep sleep`

    root        2907  0.0  0.0   8140   516 pts/0    S    14:24   0:00 sleep 1h

подключаемся к нему

`nsenter --target 2907 --pid --mount`

смотрим список процессов

`ps aux`

    USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND

    root           1  0.0  0.0   8140   516 pts/0    S    14:24   0:00 sleep 1h

    root          12  0.1  0.0  10904  5248 pts/0    S    14:30   0:00 -bash    
    
    root          21  0.0  0.0  11524  3344 pts/0    R+   14:30   0:00 ps aux

---
## 7.
Выражение `:(){ :|:& };:` называется   fork bomb, котое начинат полследоватьельно создавать копии функции `:()`
После стабилизации системы `dmesg` дает ответ
[Tue Oct 25 14:47:12 2022] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-1.scope

По умолчанию max user processes установленно `ulimit -u`  31614

Изменить их количество можно коммандой `ulimit -S -u 5000` или настроить постояннно в файле `/etc/security/limits.conf` строками:
```
#Для группы
@group_name     hard    nproc           5000
#Для пользователя
vagrant           hard    nproc           5000
```

---

Дорабатываем /etc/systemd/system/node_exporter.service
```
[Unit]

Description=Node_exporter daemon
After=syslog.target network.target

[Service]
EnvironmentFile=/etc/systemd/node_exporter.conf
ExecStart=/usr/local/bin/node_exporter $NODE_EXPORTER
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

создаем файл /etc/systemd/node_exporter.conf

```
NODE_EXPORTER="
--collector.disable-defaults
--collector.filesystem
--collector.netstat
--collector.meminfo
--collector.cpu
"
```

далее

`sudo systemctl daemon-reload`

`sudo systemctl restart node_exporter.service`
