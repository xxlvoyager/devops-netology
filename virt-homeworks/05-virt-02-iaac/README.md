
# Домашнее задание к занятию "2. Применение принципов IaaC в работе с виртуальными машинами"

---

## Задача 1

Основополагающим принципом IaaC является Идемпотентность объектов разработки.

За счет обеспечения стабильности среды разработки возможно:

- Получить ускорение и повысить эффективность разработки

- Ускорить производство и вывод на рынок новых продуктов


## Задача 2


- Чем Ansible выгодно отличается от других систем управление конфигурациями?

Основное преимущество Ansible низкий порог входа : SSH + Python


- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

Более надежным является метод PUSH поскольку запускается на управляющем хосте и последовательно выполняет команды, 
но возникает проблема со скоростью работы и зависимость от стабильности сети.
При использовании метода PULL сценарий исполняется на конечных хостах 
и за счет параллельного исполнения достигается более высока скорость работы. 
Необходима дополнительная установка на удаленные машины рабочей копии Ansible.


## Задача 3

Установить на личный компьютер:

- VirtualBox
- Vagrant
- Ansible

```
$ ansible --version
ansible [core 2.14.1]
  config file = None
  configured module search path = ['/home/alexey/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/alexey/.local/lib/python3.10/site-packages/ansible
  ansible collection location = /home/alexey/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/alexey/.local/bin/ansible
  python version = 3.10.6 (main, Nov 14 2022, 16:10:14) [GCC 11.3.0] (/usr/bin/python3)
  jinja version = 3.0.3
  libyaml = True

$ VirtualBox --help
Oracle VM VirtualBox VM Selector v6.1.40
(C) 2005-2022 Oracle Corporation
All rights reserved.

No special options.

If you are looking for --startvm and related options, you need to use VirtualBoxVM.

$ vagrant -v
Vagrant 2.3.4

```

*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*

## Задача 4 (*)

Клонируем репозиторий https://github.com/netology-code/virt-homeworks.git

Заходим в папку `virt-homeworks/05-virt-02-iaac/src/vagrant`

Поднимаем vagrant

```

vagrant up

```

После установки подключаемся к консоли

```
$vagrant ssh
Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.4.0-135-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri 13 Jan 2023 07:20:24 AM UTC

  System load:  0.04               Users logged in:          0
  Usage of /:   13.2% of 30.34GB   IPv4 address for docker0: 172.17.0.1
  Memory usage: 28%                IPv4 address for eth0:    10.0.2.15
  Swap usage:   0%                 IPv4 address for eth1:    192.168.56.11
  Processes:    112


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Fri Jan 13 07:18:06 2023 from 10.0.2.2
vagrant@server1:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
vagrant@server1:~$ docker -v
Docker version 20.10.22, build 3a2c30b
```
