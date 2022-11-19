## Подготовка оборудования

Собираем лабораторную работу
<img src=https://raw.githubusercontent.com/xxlvoyager/devops-netology/main/Screenshot_EVE-NG.png alt="Screenshot EVE-NG">

В качестве коммутатора L2 используем эмулятор `Cisco IOS Software, vios_l2 Software`  в качестве машин образы `ubuntu-20` собранные по рекомендации в приложении к домашнему заданию.

Используемые сети
```
Vlan 1 10.0.0.0/24
Vlan 2 192.168.250/24
Vlan 3 192.168.255.0/24
```

Добавляем в default config cisco l2 следующие значения

```
!
interface GigabitEthernet1/1
 switchport trunk encapsulation dot1q
 switchport mode trunk

!
interface GigabitEthernet0/0
 switchport access vlan 3
 switchport mode access
!
interface GigabitEthernet0/1
 switchport access vlan 3
 switchport mode access
!
interface GigabitEthernet0/2
 switchport access vlan 3
 switchport mode access
!
interface GigabitEthernet0/3
 switchport access vlan 2
 switchport mode access

interface Vlan1
 ip address 10.0.0.3 255.255.255.0

cdp run
 ```

В  Vlan 1 создаем IP адрес для управления коммутатором и отставляем  нетегированным на  интерфесе GigabitEthernet1/1.

создаем кофигурационный netplan  для Linux-1
```
network:
  ethernets:
    ens3:
      dhcp4: false      
      link-local: [ ]
      addresses: [10.0.0.2/24]
      link-local: [ ]
  vlans:
    vlan.2:
      id: 2
      link: ens3
      dhcp4: no
      addresses: [192.168.250.2/24]
      link-local: [ ]
    vlan.3:
      id: 3
      link: ens3
      dhcp4: false
      addresses: [192.168.255.10/24]
      gateway4: 192.168.255.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]     
      link-local: [ ]
```

и для Linux-2

```
network:
  ethernets:
    ens3:
      dhcp4: false
      optional: true

    ens4:
      dhcp4: false
      optional: true
  version: 2

 bonds:
  bond0:
   parameters:
     mode: balance-xor
   addresses: [192.168.255.40/24]
   gateway4: 192.168.255.1
   nameservers:
     addresses: [8.8.8.8,8.8.4.4]
   interfaces: [ens3, ens4]

```
---------

##  Ответы на поставленные вопросы

1. Смотрим интерфейсы на Linux-1 и Linux-2 командой `ip link show`

Linux-1
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 00:50:00:00:01:02 brd ff:ff:ff:ff:ff:ff
3: vlan.2@ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 00:50:00:00:01:02 brd ff:ff:ff:ff:ff:ff
4: vlan.3@ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 00:50:00:00:01:02 brd ff:ff:ff:ff:ff:ff
```

Linux-2

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens3: <BROADCAST,MULTICAST,SLAVE,UP,LOWER_UP> mtu 1500 qdisc fq_codel master bond0 state UP mode DEFAULT group default qlen 1000
    link/ether 9a:38:d9:0a:9f:08 brd ff:ff:ff:ff:ff:ff
3: ens4: <BROADCAST,MULTICAST,SLAVE,UP,LOWER_UP> mtu 1500 qdisc fq_codel master bond0 state UP mode DEFAULT group default qlen 1000
    link/ether 9a:38:d9:0a:9f:08 brd ff:ff:ff:ff:ff:ff
4: bond0: <BROADCAST,MULTICAST,MASTER,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 9a:38:d9:0a:9f:08 brd ff:ff:ff:ff:ff:ff
```


В Windows для просмотра информации об интерфейсах можно воспользоваться командой `ipconfig /all`

```

Windows IP Configuration

   Host Name . . . . . . . . . . . . : DESKTOP-E60HJ1N
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No

Ethernet adapter Ethernet:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Intel(R) PRO/1000 MT Desktop Adapter
   Physical Address. . . . . . . . . : 08-00-27-7C-F3-AE
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::d9c0:ddfb:b5b2:5a85%9(Preferred)
   IPv4 Address. . . . . . . . . . . : 192.168.0.101(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.254.0
   Lease Obtained. . . . . . . . . . : 19 ноября 2022 г. 12:05:51
   Lease Expires . . . . . . . . . . : 19 ноября 2022 г. 14:05:54
   Default Gateway . . . . . . . . . : 192.168.0.1
   DHCP Server . . . . . . . . . . . : 192.168.0.1
   DHCPv6 IAID . . . . . . . . . . . : 101187623
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-2A-D9-DD-8D-08-00-27-7C-F3-AE
   DNS Servers . . . . . . . . . . . : 192.168.0.1
   NetBIOS over Tcpip. . . . . . . . : Enabled
```

---

2. Для просмотра "соседей" используется протокол lldp, поскольку в нашей сети есть коммутатор cisco, на нем использутся протокол cdp, для поддержки этого протокола в daemon lldpd добавляем опцию -c.

Cisco L2  `show cdp neighbors` 
```
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone, 
                  D - Remote, C - CVTA, M - Two-port Mac Relay 

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
linuxserver      Gig 0/2           115               H    Linux     ens4
linuxserver      Gig 0/1           115               H    Linux     ens3
linuxserver      Gig 1/1           112               H    Linux     ens3

Total cdp entries displayed : 3
```

Linux-1 `lldpctl`

```
-------------------------------------------------------------------------------
LLDP neighbors:
-------------------------------------------------------------------------------
Interface:    ens3, via: CDPv2, RID: 1, Time: 0 day, 01:09:31
  Chassis:     
    ChassisID:    local Switch
    SysName:      Switch
    SysDescr:     Cisco  running on
                  Cisco IOS Software, vios_l2 Software (vios_l2-ADVENTERPRISEK9-M), Version 15.2(CML_NIGHTLY_20190423)FLO_DSGS7, EARLY DEPLOYMENT DEVELOPMENT BUILD, synced to  V152_6_0_81_E
                  Technical Support: http://www.cisco.com/techsupport
                  Copyright (c) 1986-2019 by Cisco Systems, Inc.
                  Compiled Tue 23-Apr-19 04:48 by mmen
    MgmtIP:       10.0.0.3
    Capability:   Bridge, on
    Capability:   Router, on
  Port:        
    PortID:       ifname GigabitEthernet1/1
    PortDescr:    GigabitEthernet1/1
    TTL:          180
  VLAN:         1, pvid: yes VLAN #1
-------------------------------------------------------------------------------

```
Linux-2 `lldpctl`
```
-------------------------------------------------------------------------------
LLDP neighbors:
-------------------------------------------------------------------------------
Interface:    ens3, via: CDPv2, RID: 1, Time: 0 day, 00:17:38
  Chassis:     
    ChassisID:    local Switch
    SysName:      Switch
    SysDescr:     Cisco  running on
                  Cisco IOS Software, vios_l2 Software (vios_l2-ADVENTERPRISEK9-M), Version 15.2(CML_NIGHTLY_20190423)FLO_DSGS7, EARLY DEPLOYMENT DEVELOPMENT BUILD, synced to  V152_6_0_81_E
                  Technical Support: http://www.cisco.com/techsupport
                  Copyright (c) 1986-2019 by Cisco Systems, Inc.
                  Compiled Tue 23-Apr-19 04:48 by mmen
    MgmtIP:       10.0.0.3
    Capability:   Bridge, on
    Capability:   Router, on
  Port:        
    PortID:       ifname GigabitEthernet0/1
    PortDescr:    GigabitEthernet0/1
    TTL:          180
  VLAN:         3, pvid: yes VLAN #3
-------------------------------------------------------------------------------
Interface:    ens4, via: CDPv2, RID: 1, Time: 0 day, 00:17:18
  Chassis:     
    ChassisID:    local Switch
    SysName:      Switch
    SysDescr:     Cisco  running on
                  Cisco IOS Software, vios_l2 Software (vios_l2-ADVENTERPRISEK9-M), Version 15.2(CML_NIGHTLY_20190423)FLO_DSGS7, EARLY DEPLOYMENT DEVELOPMENT BUILD, synced to  V152_6_0_81_E
                  Technical Support: http://www.cisco.com/techsupport
                  Copyright (c) 1986-2019 by Cisco Systems, Inc.
                  Compiled Tue 23-Apr-19 04:48 by mmen
    MgmtIP:       10.0.0.3
    Capability:   Bridge, on
    Capability:   Router, on
  Port:        
    PortID:       ifname GigabitEthernet0/2
    PortDescr:    GigabitEthernet0/2
    TTL:          180
  VLAN:         3, pvid: yes VLAN #3
-------------------------------------------------------------------------------

```

3. 
Для разделения сетей коммутатора д2 используется  технология VLAN.
Если используется Ubuntu версии 17.10 и выше, то для поддержки vlan необходимо установить пакет ifupdown или настраивать VLAN интерфейсы через netplan. Конфигурация Linux-1 сделана с применением VLAN.
Нетегированный VLAN1 используется для управления коммутатором, VLAN2 и VLAN3 используются для соединия с сответствующими сетями.


--- 

4. 

В Linux есть следующие типы агрегации интерфейсов

mode=0 (balance-rr)
Последовательно кидает пакеты, с первого по последний интерфейс.
mode=1 (active-backup)
Один из интерфейсов активен. Если активный интерфейс выходит из строя (link down и т.д.), другой интерфейс заменяет активный. Не требует дополнительной настройки коммутатора
mode=2 (balance-xor)
Передачи распределяются между интерфейсами на основе формулы ((MAC-адрес источника) XOR (MAC-адрес получателя)) % число интерфейсов. Один и тот же интерфейс работает с определённым получателем. Режим даёт балансировку нагрузки и отказоустойчивость.
mode=3 (broadcast)
Все пакеты на все интерфейсы
mode=4 (802.3ad)
Link Agregation — IEEE 802.3ad, требует от коммутатора настройки.
mode=5 (balance-tlb)
Входящие пакеты принимаются только активным сетевым интерфейсом, исходящий распределяется в зависимости от текущей загрузки каждого интерфейса. Не требует настройки коммутатора.
mode=6 (balance-alb)
Тоже самое что 5, только входящий трафик тоже распределяется между интерфейсами. Не требует настройки коммутатора, но интерфейсы должны уметь изменять MAC.

В конфигурации Linux-2 использована агрегация интерфейсов mode=2

---

5. 
В сети с маской /29 маскимальное количество хостов 6, из сети класса C /24 можно получить 32 сети с маской /29 (255.255.255.248).

Напрмер из сети 10.0.0.0/24 можно получить сети:
10.0.0.96/29  и 10.0.0.248/29.
---

6. 
Для объединения сетей можно использовать сеть из диапазона 100.64.0.0 — 100.127.255.255. С учетом потребности объединения достаточтно будет сети с маской 255.255.255.192 (/26) которая включает в себя максимально 62 хоста.

--- 


7. 

Таблицу ARP можно посмотреть командой `ip neighbour` или `arp` из пакета `net-tools`. В windows так же используется `arp`.

Для удаления записи можно воспользоваться коммандой 
`sudo ip neighbour del $IP dev $IF`
где например `IP=10.0.0.2  IF=ens4` или `sudo arp -d $IP`.

Удаление всей таблицы `sudo ip neigh flush all`.