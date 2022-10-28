1. 

Sparse file позволяет экономить место на диске
за счет записи информации о нулевых последовательностях, вместо самих последовательностей. VirtualBox поддерживает работу с разреженными файлами.

Следующий примем это  демонстрирует:

Смотрим свободное место к корневом разделе

`df -h /`
```
Filesystem                  Size  Used Avail Use% Mounted on
/dev/mapper/vgvagrant-root   62G  1.4G   57G   3% /
```

Создаем "пустой" разреженный файл размером 500G

`truncate -s500G /sparse-file`

`ls -la /sparse-file` 

```
-rw-r--r-- 1 root root 536870912000 Oct 28 12:02 /sparse-file
```

Проверяем свободное место на диске 

`df -h /`

```
Filesystem                  Size  Used Avail Use% Mounted on
/dev/mapper/vgvagrant-root   62G  1.4G   57G   3% /
```


---

2.

Файлы, являющиеся жесткой ссылкой на один объект не могут иметь разных прав
поскольку они ссылаются на одинаковый Device_id Inode_id.

---

3.
Создаем виртуальную машину и 
подключаемся к ней.  Проверяем `lsbkl` имеющиеся диски
```
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                    8:0    0   64G  0 disk 
├─sda1                 8:1    0  512M  0 part /boot/efi
├─sda2                 8:2    0    1K  0 part 
└─sda5                 8:5    0 63.5G  0 part 
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
sdb                    8:16   0  2.5G  0 disk 
sdc                    8:32   0  2.5G  0 disk
```

---

4.


Заходим под супрпользователем
`sudo su`

Создаем первый диск при помощи команды 

`fdisk /dev/sdb` 

проверяем результат 

`fdisk -l /dev/sdb`

```
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xac03e819

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 4196351 4194304    2G 83 Linux
/dev/sdb2       4196352 5242879 1046528  511M 83 Linux
```

---

5.
копируем таблицу разделов на второй диск

`sfdisk -d /dev/sdb | sfdisk /dev/sdc`

проверяем,  что получилоськомандой `lsblk`
```
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                    8:0    0   64G  0 disk 
├─sda1                 8:1    0  512M  0 part /boot/efi
├─sda2                 8:2    0    1K  0 part 
└─sda5                 8:5    0 63.5G  0 part 
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
sdb                    8:16   0  2.5G  0 disk 
├─sdb1                 8:17   0    2G  0 part 
└─sdb2                 8:18   0  511M  0 part 
sdc                    8:32   0  2.5G  0 disk 
├─sdc1                 8:33   0    2G  0 part 
└─sdc2                 8:34   0  511M  0 part 

```

---

6.

Собераем  RAID1 на паре разделов по 2 Гб

`mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1`

---

7.

Собераем  RAID0 на второй паре  разделов

`mdadm --create --verbose /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2`

---

8.

Создаем PV на полученных массивах

`pvcreate /dev/md0`

`pvcreate /dev/md0`

---

9.

Создаем грппу физических томов из RAID массивов   

`vgcreate netology  /dev/md0 /dev/md1`

---

10.

Создаем логический диск с размещением на RAID0 (md1)

`lvcreate   -L 100 -n lvl_test netology /dev/md1`

---

11.

Создаем файловую систему на логическом диске

`mkfs.ext4 /dev/netology/lvl_test`

---

12.
Создаем директорию и монтируем логический диск

`mkdir /home/vagrant/test/`

`mount /dev/netology/lvl_test /home/vagrant/test/`

---

13. 

Скачиваем файл и проверяем его наличие

`ls -la /home/vagrant/test/test.gz `

    -rw-r--r-- 1 root root 22424257 Oct 28 11:29 /home/vagrant/test/test.gz

14.

Просматриваем устройства
`lsblk`

```
NAME                    MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                       8:0    0   64G  0 disk  
├─sda1                    8:1    0  512M  0 part  /boot/efi
├─sda2                    8:2    0    1K  0 part  
└─sda5                    8:5    0 63.5G  0 part  
  ├─vgvagrant-root      253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1    253:1    0  980M  0 lvm   [SWAP]
sdb                       8:16   0  2.5G  0 disk  
├─sdb1                    8:17   0    2G  0 part  
│ └─md0                   9:0    0    2G  0 raid1 
└─sdb2                    8:18   0  511M  0 part  
  └─md1                   9:1    0 1018M  0 raid0 
    └─netology-lvl_test 253:2    0  100M  0 lvm   /home/vagrant/test
sdc                       8:32   0  2.5G  0 disk  
├─sdc1                    8:33   0    2G  0 part  
│ └─md0                   9:0    0    2G  0 raid1 
└─sdc2                    8:34   0  511M  0 part  
  └─md1                   9:1    0 1018M  0 raid0 
    └─netology-lvl_test 253:2    0  100M  0 lvm   /home/vagrant/test
```

---

15.

Тестируем файл

`gzip -t /home/vagrant/test/test.gz |echo $?`

    0


---

16.

Перемещаем содержимое логического диска с RAID0 на RAID1

`pvmove -n lvl_test /dev/md1`
```
  /dev/md1: Moved: 16.00%
  /dev/md1: Moved: 100.00%
```

Проверяем

`lsblk`
``` 
NAME                    MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                       8:0    0   64G  0 disk  
├─sda1                    8:1    0  512M  0 part  /boot/efi
├─sda2                    8:2    0    1K  0 part  
└─sda5                    8:5    0 63.5G  0 part  
  ├─vgvagrant-root      253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1    253:1    0  980M  0 lvm   [SWAP]
sdb                       8:16   0  2.5G  0 disk  
├─sdb1                    8:17   0    2G  0 part  
│ └─md0                   9:0    0    2G  0 raid1 
│   └─netology-lvl_test 253:2    0  100M  0 lvm   /home/vagrant/test
└─sdb2                    8:18   0  511M  0 part  
  └─md1                   9:1    0 1018M  0 raid0 
sdc                       8:32   0  2.5G  0 disk  
├─sdc1                    8:33   0    2G  0 part  
│ └─md0                   9:0    0    2G  0 raid1 
│   └─netology-lvl_test 253:2    0  100M  0 lvm   /home/vagrant/test
└─sdc2                    8:34   0  511M  0 part  
  └─md1                   9:1    0 1018M  0 raid0
```

---

17.

Делаем  --fail на устройство на RAID1 

`mdadm   /dev/md0 --fail    /dev/sdb1`

    mdadm: set /dev/sdb1 faulty in /dev/md0

---

18. 

Проверяем dmesg

`dmesg -T |tail -2`

```
[Fri Oct 28 13:05:11 2022] md/raid1:md0: Disk failure on sdb1, disabling device.
                           md/raid1:md0: Operation continuing on 1 devices.

```

---

19.

Тестируем файл

`gzip -t /home/vagrant/test/test.gz |echo $?`

    0

---

20.

Разбираем виртуальную машину

`vagrant destroy`

```
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
```