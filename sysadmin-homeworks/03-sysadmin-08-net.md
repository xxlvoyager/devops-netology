## Подготовка оборудования

Собираем лабораторную работу
<img src=Screenshot_EVE-NG_2.png alt="Screenshot EVE-NG">

В качестве коммутатора L3 используем эмулятор `Cisco IOS Software`  в качестве машин образы `ubuntu-20` собранные по рекомендации  https://github.com/svmyasnikov/eve-ng.

---

## Ответы на воросы домашнего задания

1. Поиск маршрута к публичному IP адресу

Уточняем IP адрес выданный провайдером:
`curl ifconfig.me`

    92.42.9.16

`show ip route 92.42.9.16`

```
Routing entry for 92.42.8.0/23
  Known via "bgp 6447", distance 20, metric 0
  Tag 3303, type external
  Last update from 217.192.89.50 2w3d ago
  Routing Descriptor Blocks:
  * 217.192.89.50, from 217.192.89.50, 2w3d ago
      Route metric is 0, traffic share count is 1
      AS Hops 3
      Route tag 3303
      MPLS label: none
```

`show  ip bgp 92.42.9.16`
```
route-views>show  ip bgp 92.42.9.16                     
BGP routing table entry for 92.42.8.0/23, version 2533275792
Paths: (22 available, best #18, table default)
----------- часть вывода пропущена -------------------------
  Refresh Epoch 1
  3303 12389 44963
    217.192.89.50 from 217.192.89.50 (138.187.128.158)
      Origin IGP, localpref 100, valid, external, best
      Community: 3303:1004 3303:1006 3303:1030 3303:3056
      path 7FE1718A2488 RPKI State not found
      rx pathid: 0, tx pathid: 0x0
----------- конец вывода пропущен  -------------------------
 ```

Лучший маршрут через bgp 3303, черз 3 AS


Далее удалось подключиться к серверу `Swisscom IP+ route server (AS3303)`

`telnet route-server.ip-plus.net`
 ```
 RS_AS3303>show  ip route 92.42.9.16
Routing entry for 92.42.8.0/23
  Known via "bgp 65097", distance 200, metric 550000
  Tag 65000, type internal
  Last update from 193.247.173.45 4w4d ago
  Routing Descriptor Blocks:
  * 193.247.173.45, from 193.247.173.45, 4w4d ago
      Route metric is 550000, traffic share count is 1
      AS Hops 2
      Route tag 65000
      MPLS label: none
RS_AS3303>show  ip bgp 92.42.9.16  
BGP routing table entry for 92.42.8.0/23, version 222772991
BGP Bestpath: deterministic-med
Paths: (1 available, best #1, table default)
  Not advertised to any peer
  Refresh Epoch 1
  (65000) 12389 44963
    193.247.173.45 from 193.247.173.45 (138.187.128.161)
      Origin IGP, metric 550000, localpref 300, valid, confed-external, best
      Community: 3303:1004 3303:1006 3303:1030 3303:3056
      Extended Community: 0x4300:0:1
      rx pathid: 0, tx pathid: 0x0
 ```

 Здесь видим осталось 2 AS, через внутреннй BGP 65097.

 2. Работа с dummy интерфейсами
 Для работы с интерфесом необходимо загрузить модуля ядра
 `sudo modprobe dummy`

 Для автоматической загрузки
 добавляем  файл
`/etc/modprobe.d/dummy.conf`

    options dummy numdummies=2

и строку в `/etc/modules`

    dummy

Далее создаем интерфейсы

`ip link add type dummy dummy0`
`ip link add type dummy dummy1`
Создаем маршруты
`ip addr add 10.80.0.1/24 dev dummy0`
`ip addr add 10.90.0.1/24 dev dummy1`

Поднимаем интерфейсы

`ip link set dummy0 up`
`ip link set dummy1 up`

Проверяем таблицу маршрутизации, появились строки

    10.80.0.0/24 dev dummy0 proto kernel scope link src 10.100.0.1
    10.90.0.0/24 dev dummy1 proto kernel scope link src 10.100.0.1


3. Открытые порты TCP

Существцет несколько способов посмотреть открутые порты TCP на Ubuntu

`sudo ss -lpnt`
```
State     Recv-Q    Send-Q       Local Address:Port        Peer Address:Port    Process                                                                         
LISTEN    0         511                0.0.0.0:80               0.0.0.0:*        users:(("nginx",pid=660,fd=5),("nginx",pid=654,fd=5))                          
LISTEN    0         4096         127.0.0.53%lo:53               0.0.0.0:*        users:(("systemd-resolve",pid=590,fd=13))                                      
LISTEN    0         128                0.0.0.0:22               0.0.0.0:*        users:(("sshd",pid=662,fd=3))                                                  
LISTEN    0         128                0.0.0.0:23               0.0.0.0:*        users:(("inetd",pid=611,fd=7))                                                 
LISTEN    0         128                   [::]:22                  [::]:*        users:(("sshd",pid=662,fd=4))
```

`sudo netstat -plnt`

```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      654/nginx: master p 
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      590/systemd-resolve 
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      662/sshd: /usr/sbin 
tcp        0      0 0.0.0.0:23              0.0.0.0:*               LISTEN      611/inetd           
tcp6       0      0 :::22                   :::*                    LISTEN      662/sshd: /usr/sbin
```

или через сканер портов 

`sudo nmap localhost`

```
Starting Nmap 7.80 ( https://nmap.org ) at 2022-11-23 06:50 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000040s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
23/tcp open  telnet
80/tcp open  http
```

или через открытые файлы

`sudo lsof -nP -iTCP -sTCP:LISTEN`
```
COMMAND   PID            USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
systemd-r 590 systemd-resolve   13u  IPv4  20213      0t0  TCP 127.0.0.53:53 (LISTEN)
inetd     611            root    7u  IPv4  22328      0t0  TCP *:23 (LISTEN)
nginx     654            root    5u  IPv4  22635      0t0  TCP *:80 (LISTEN)
nginx     660          nobody    5u  IPv4  22635      0t0  TCP *:80 (LISTEN)
sshd      662            root    3u  IPv4  23073      0t0  TCP *:22 (LISTEN)
sshd      662            root    4u  IPv6  23084      0t0  TCP *:22 (LISTEN)
```

4. Просмотр UDP аналогичен TCP, в коммандах меняет тип протокола

`sudo ss -plnu`
```
State     Recv-Q    Send-Q       Local Address:Port        Peer Address:Port    Process                                                                         
UNCONN    0         0             0.0.0.0%ens4:520              0.0.0.0:*        users:(("bird",pid=671,fd=8))                                                  
UNCONN    0         0            127.0.0.53%lo:53               0.0.0.0:*        users:(("systemd-resolve",pid=590,fd=12))
```

`sudo lsof -nP -iUDP`
```
COMMAND   PID            USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
systemd-r 590 systemd-resolve   12u  IPv4  20212      0t0  UDP 127.0.0.53:53 
bird      671            bird    8u  IPv4  23105      0t0  UDP *:520 
```



5. Диаграмма L3 сети собранной в лабораторной работе
<img src=lab-2.drawio.png alt="Схема сети L3">

6.Конфигурация nginx в режиме балансировки трафика

`/etc/nginx/nginx.conf` 
```
load_module /usr/lib/nginx/modules/ngx_stream_module.so; 

events {
    worker_connections 1024;
}
stream {

  upstream backends {
    server 10.150.0.2:80;
    server 10.200.0.2:80;
  }

  server {
    listen 80;
    proxy_pass backends;
    proxy_responses 1;
  }
}
```

Демонстрация работы

```
eve@Linux-2:~$ curl 10.150.0.2
Linux-3

eve@Linux-2:~$ curl 10.200.0.2
Linux-1

eve@Linux-2:~$ curl localhost
Linux-3

eve@Linux-2:~$ curl localhost
Linux-1

```
6. Кофигурация bird2


`/etc/bird/bird.conf`
``` 
log syslog all;
protocol kernel {
	ipv4 {
		export all;
	};
	persist; }
# Default is export none
# Don't remove routes on BIRD shutdown
protocol device {
}

protocol rip {
ipv4 {
import all;
export all;
};
interface "ens4";
}
protocol direct {
ipv4;
interface "ens*";
interface "dummy*";
}
```
Демонстрация работы 

`birdc`
```
bird>show rip neighbors 
bird>       rip1:
IP address                Interface  Metric Routes    Seen
10.100.0.1                ens4            1      3  18.620
bird> show route
bird>       Table master4:
0.0.0.0/0            unicast [rip1 19:44:58.288] (120/2)
	via 10.100.0.1 on ens4
10.100.0.0/24        unicast [direct1 19:44:58.282] * (240)
	dev ens4
192.168.255.0/24     unicast [rip1 19:44:58.288] (120/2)
	via 10.100.0.1 on ens4
192.168.250.0/24     unicast [rip1 19:44:58.288] (120/2)
	via 10.100.0.1 on ens4
10.200.0.0/24        unicast [direct1 19:44:58.282] * (240)
	dev ens5
10.150.0.0/24        unicast [direct1 19:44:58.282] * (240)
	dev ens3
```

В консоли роутера vIOS

`show ip rip database`

``` 
0.0.0.0/0    auto-summary
0.0.0.0/0    redistributed
    [1] via 0.0.0.0, 
10.0.0.0/8    auto-summary
10.100.0.0/24    directly connected, GigabitEthernet0/2
10.150.0.0/24
    [1] via 10.100.0.2, 00:00:22, GigabitEthernet0/2
10.200.0.0/24
    [1] via 10.100.0.2, 00:00:22, GigabitEthernet0/2
192.168.250.0/24    auto-summary
192.168.250.0/24    directly connected, GigabitEthernet0/1
192.168.255.0/24    auto-summary
192.168.255.0/24    directly connected, GigabitEthernet0/0
```

После создания интерфейсов dimmy в пункте 2
```
bird> show route 
bird>       Table master4:
0.0.0.0/0            unicast [rip1 19:44:58.288] (120/2)
	via 10.100.0.1 on ens4
10.100.0.0/24        unicast [direct1 19:44:58.282] * (240)
	dev ens4
192.168.255.0/24     unicast [rip1 19:44:58.288] (120/2)
	via 10.100.0.1 on ens4
10.90.0.0/24         unicast [direct1 07:20:25.151] * (240)
	dev dummy1
192.168.250.0/24     unicast [rip1 19:44:58.288] (120/2)
	via 10.100.0.1 on ens4
10.200.0.0/24        unicast [direct1 19:44:58.282] * (240)
	dev ens5
10.80.0.0/24         unicast [direct1 07:20:16.251] * (240)
	dev dummy0
10.150.0.0/24        unicast [direct1 19:44:58.282] * (240)
	dev ens3
bird> 
```

на роутере

```
Router#show ip rip database 
0.0.0.0/0    auto-summary
0.0.0.0/0    redistributed
    [1] via 0.0.0.0, 
10.0.0.0/8    auto-summary
10.80.0.0/24
    [1] via 10.100.0.2, 00:00:17, GigabitEthernet0/2
10.90.0.0/24
    [1] via 10.100.0.2, 00:00:17, GigabitEthernet0/2
10.100.0.0/24    directly connected, GigabitEthernet0/2
10.150.0.0/24
    [1] via 10.100.0.2, 00:00:17, GigabitEthernet0/2
10.200.0.0/24
    [1] via 10.100.0.2, 00:00:17, GigabitEthernet0/2
192.168.250.0/24    auto-summary
192.168.250.0/24    directly connected, GigabitEthernet0/1
192.168.255.0/24    auto-summary
192.168.255.0/24    directly connected, GigabitEthernet0/
```


7.

Запускаем  в докере netbox https://github.com/netbox-community/netbox-docker.git


заполняем информацию о роутере из лабораторной работы

создаем скрипт для получения информации

```
TOKEN="587033751ea954a4ab31740f26d6e801220882f6"
respond=`curl -X GET \
-H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
-H "Accept: application/json; indent=4" \
http://localhost:8000/api/ipam/ip-addresses/ 2>/dev/null`
echo $respond | jq .
```

фрагмет ответа на запрос скрипта

```
{
  "count": 4,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "url": "http://localhost:8000/api/ipam/ip-addresses/3/",
      "display": "10.100.0.0/24",
      "family": {
        "value": 4,
        "label": "IPv4"
      },
      "address": "10.100.0.0/24",
      "vrf": null,
      "tenant": null,
      "status": {
        "value": "active",
        "label": "Active"
      },
      "role": null,
      "assigned_object_type": null,
      "assigned_object_id": null,
      "assigned_object": null,
      "nat_inside": null,
      "nat_outside": [],
      "dns_name": "",
      "description": "Lan-2",
      "tags": [],
      "custom_fields": {},
      "created": "2022-11-23T10:02:00.415983Z",
      "last_updated": "2022-11-23T10:02:00.416017Z"
    },
    {
      "id": 4,
      "url": "http://localhost:8000/api/ipam/ip-addresses/4/",
      "display": "10.100.0.1/32",
      "family": {
        "value": 4,
        "label": "IPv4"
      },
      "address": "10.100.0.1/32",
      "vrf": null,
      "tenant": null,
      "status": {
        "value": "active",
        "label": "Active"
      },
      "role": null,
      "assigned_object_type": "dcim.interface",
      "assigned_object_id": 1,
      "assigned_object": {
        "id": 1,
        "url": "http://localhost:8000/api/dcim/interfaces/1/",
        "display": "Gi0/2",
        "device": {
          "id": 2,
          "url": "http://localhost:8000/api/dcim/devices/2/",
          "display": "Cisco vIOS (2)",
          "name": null
        },
        "name": "Gi0/2",
        "cable": null,
        "_occupied": false
      },
      "nat_inside": null,
      "nat_outside": [],
      "dns_name": "",
      "description": "Gi0/2",
      "tags": [],
      "custom_fields": {},
      "created": "2022-11-23T10:08:37.325708Z",
      "last_updated": "2022-11-23T10:20:28.889306Z"
    },
--------------------- оставшаяся часть опущена------------------------------
```



Приложения.

конфигурация интерфейсов и RIP роутера 
```
nterface GigabitEthernet0/0
 ip address 192.168.255.2 255.255.255.0
 ip virtual-reassembly in
 duplex auto
 speed auto
 media-type rj45
!
interface GigabitEthernet0/1
 ip address 192.168.250.2 255.255.255.0
 duplex auto
 speed auto
 media-type rj45
!
interface GigabitEthernet0/2
 ip address 10.100.0.1 255.255.255.0
 ip virtual-reassembly in
 duplex auto
 speed auto
 media-type rj45
 no mop enabled

!
router rip
 version 2
 passive-interface GigabitEthernet0/0
 network 192.168.250.0
 network 192.168.255.0
 default-information originate
 no auto-summary
!

```
Конфигурации netplan на ubunu машинах
`Linux-1`
```
network:
  ethernets:
    ens3:
      dhcp4: false      
      link-local: [ ]
      addresses: [10.200.0.2/24]
      gateway4: 10.200.0.1
      nameservers: 
        addresses: [8.8.8.8]
      link-local: [ ]
  version: 2
```

`Linux-2`
```
network:
  ethernets:
    ens3:
      dhcp4: false
      addresses:
        - 10.150.0.1/24    
    ens4:
      dhcp4: false
      addresses:
        - 10.100.0.2/24 
      nameservers:
        addresses: 
          - 8.8.8.8      
    ens5:
      dhcp4: false
      addresses:
        - 10.200.0.1/24    
  version: 2


```

`Linux-3`
```
network:
  ethernets:
    ens3:
      dhcp4: false      
      link-local: [ ]
      addresses: [10.150.0.2/24]
      gateway4: 10.150.0.1
      nameservers: 
        addresses: [8.8.8.8]
  version: 2

```