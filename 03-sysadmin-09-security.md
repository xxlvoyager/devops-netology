1. 

Демонстрация работы Bitwarden плагина

<img src=Screenshot_09_2.png alt="Screenshot">

---

2. Демонстрация подключения двухфакторной аутенификации к Bitwarden

<img src=Screenshot_09_1.png alt="Screenshot">

---

3. 

Установку сервера apache2 проводим в лабораторой работе из предидущего ДЗ. Устанавливаем на сервере с адресом `10.150.0.2`

`sudo apt install apache2`
`sudo a2enmod ssl`
`systemctl restart apache`

После установки создаем запись в
`/etc/hosts`

       10.150.0.2 www.test.com

Генерируем ключи ssl

```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout /etc/ssl/private/apache-selfsigned.key \
-out /etc/ssl/certs/apache-selfsigned.crt \
-subj "/C=RU/ST=Moscow/L=Moscow/O=Company Name/OU=Org/CN=www.test.com"
```

создаем файл кофигурации 

`/etc/apache2/sites-available/www_test_com.conf`

``` 
<VirtualHost *:443>
ServerName your_domain_or_ip
DocumentRoot /var/www/www_test_com
SSLEngine on
SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt
SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
</VirtualHost>
```

файл начальной страницы

`/var/www/www_test_com/index.html`

       <h1>Welcome Linux-3 as www.test.com</h1>

Делаем сайт доступным, тестируем конфиг, перезапускаем сервер

```
a2ensite www_test_com.conf
apache2ctl configtest
systemctl reload apache2
```

обновляем сертификы в ситеме

       update-ca-certificates --fresh

Проверяем

`curl https:/www.test.com`

       <h1>Welcome Linux-3 as www.test.com</h1>

Копируем сертификат`/etc/ssl/certs/apache-selfsigned.crt` на соседние машины в папку `/usr/local/share/ca-certificates`.

Обновляем сертификаты на соседних машинах
`update-ca-certificates --fresh`

добавлем везде в `/etc/hosts`

       10.150.0.2 www.test.com

Проверям `curl https:/www.test.com`

---

4.

Проверяем на уязвимости наш сайт

`eve@linuxserver:~/testssl.sh$ ./testssl.sh -U --sneaky https://www.test.com`

```
###########################################################
    testssl.sh       3.2rc2 from https://testssl.sh/dev/
    (9304bb8 2022-11-25 18:23:58)

      This program is free software. Distribution and
             modification under GPLv2 permitted.
      USAGE w/o ANY WARRANTY. USE IT AT YOUR OWN RISK!

       Please file bugs @ https://testssl.sh/bugs/

###########################################################

 Using "OpenSSL 1.0.2-bad (1.0.2k-dev)" [~183 ciphers]
 on linuxserver:./bin/openssl.Linux.x86_64
 (built: "Sep  1 14:03:44 2022", platform: "linux-x86_64")


 Start 2022-11-28 10:39:29        -->> 10.150.0.2:443 (www.test.com) <<--

 A record via:           /etc/hosts 
 rDNS (10.150.0.2):      www.test.com.
 Service detected:       HTTP


 Testing vulnerabilities 

-------------- часть вывода пропущена---------------------
 
 
 LUCKY13 (CVE-2013-0169), experimental     potentially VULNERABLE, uses cipher block chaining (CBC) ciphers with TLS. Check patches
 Winshock (CVE-2014-6321), experimental    not vulnerable (OK)
 RC4 (CVE-2013-2566, CVE-2015-2808)        no RC4 ciphers detected (OK)


 Done 2022-11-28 10:40:04 [  37s] -->> 10.150.0.2:443 (www.test.com) <<--
```

Сркипт нашел одну потенциальную уязвимость.

---

5.

Генерируем ключ `ssh-keygen`

``` 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/eve/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/eve/.ssh/id_rsa
Your public key has been saved in /home/eve/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:XVYNUKF/o3M49cU+95hwlDOx5R9HBRSAb2GJbR+Gpn0 eve@linux-3
The key's randomart image is:
+---[RSA 3072]----+
|           +oBO*.|
|          o Ooo o|
|           B++..o|
|         ..o+.EO |
|        S .. .B+*|
|             .+=B|
|            .=.o=|
|             o+o+|
|              o .|
+----[SHA256]-----+
```

Копируем ключ на соседнюю машину 

`eve@linux-3:~$ ssh-copy-id eve@10.150.0.1`

```
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/eve/.ssh/id_rsa.pub"
The authenticity of host '10.150.0.1 (10.150.0.1)' can't be established.
ECDSA key fingerprint is SHA256:2Ppq3TVtielJ/jOO3avUwQr5g1T9J9+er0OIN4a3geQ.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
eve@10.150.0.1's password: 

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'eve@10.150.0.1'"
and check to make sure that only the key(s) you wanted were added
```

проверяем достуность машины

`ssh eve@10.150.0.1`

---

6.

Генерируем ключ  `ssh-keygen` с названием `id_rsa_two`

Копируем ключ на соседнюю машину 

`ssh-copy-id -i id_rsa_two.pub  eve@10.150.0.1`

Проверяем работу ключа 

`ssh  -i ~/.ssh/id_rsa_two  eve@10.150.0.1`

Создаем файл кофигурации `.ssh/config`

'''
Host linux-2
    HostName 10.150.0.1
    User eve
    IdentityFile ~/.ssh/id_rsa_two

'''

проверяем достуность машины

`ssh 10.150.0.1`

---

7. 

Собираем дамп
`tcpdump -w 0001.pcap -i eno1 -c 100`

```
tcpdump: listening on eno1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
100 packets captured
171 packets received by filter
0 packets dropped by kernel
```

открываем файл в Wireshark

<img src=Screenshot_Wireshark.png alt="Wireshark">

На скриншоте выделен фрагмент обмена по протоколу ARP

---

8.

Сканируем хост scanme.nmap.org

`nmap -p0- -v -A -T4 scanme.nmap.org`


```
------------- Часть вывода пропущена ---------------
Scanning scanme.nmap.org (45.33.32.156) [65536 ports]
Discovered open port 22/tcp on 45.33.32.156
Discovered open port 80/tcp on 45.33.32.156
Discovered open port 9929/tcp on 45.33.32.156
Discovered open port 31337/tcp on 45.33.32.156

------------- Часть вывода пропущена ---------------

PORT      STATE    SERVICE    VERSION
0/tcp     filtered unknown
22/tcp    open     ssh        OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 ac:00:a0:1a:82:ff:cc:55:99:dc:67:2b:34:97:6b:75 (DSA)
|   2048 20:3d:2d:44:62:2a:b0:5a:9d:b5:b3:05:14:c2:a6:b2 (RSA)
|   256 96:02:bb:5e:57:54:1c:4e:45:2f:56:4c:4a:24:b2:57 (ECDSA)
|_  256 33:fa:91:0f:e0:e1:7b:1f:6d:05:a2:b0:f1:54:41:56 (ED25519)
80/tcp    open     http       Apache httpd 2.4.7 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: 156515DA3C0F7DC6B2493BD5CE43F795
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Go ahead and ScanMe!
9929/tcp  open     nping-echo Nping echo
31337/tcp open     tcpwrapped


------------- Часть вывода пропущена ---------------
```

9.

Устанавливаем фаервол

`sudo apt install ufw`

создаем кофигурационные файлы для разрешенных на портах 22,80,443 приложений  в директории `/etc/ufw/applications.d`
root@linuxserver:/etc/ufw/applications.d# ls
`apache2-ufw.profile`  

```
[Apache]
title=Web Server
description=Apache v2 web server.
ports=80/tcp

[Apache Secure]
title=Web Server (HTTPS)
description=Apache v2 web server.
ports=443/tcp
```

`openssh-server-ufw.profile`

```
[OpenSSH]
title=Secure shell server
description=OpenSSH protocol.
ports=22/tcp
```

Запускаем фаервол

`sudo ufw enable`

       Firewall is active and enabled on system start


Смотрим состяное 

`sudo ufw status verbose`

```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip
```

Смотрим разрешенные приложения

`sudo ufw app list`

```
Available applications:
  Apache
  Apache Secure
  OpenSSH
```

Смотрим детали о приложения

`sudo ufw app info all`

```
Profile: Apache
Title: Web Server
Description: Apache v2 web server.
server.

Port:
  80/tcp

--

Profile: Apache Secure
Title: Web Server (HTTPS)
Description: Apache v2 web server.

Port:
  443/tcp

--

Profile: OpenSSH
Title: Secure shell server
Description: OpenSSH protocol.

Port:
  22/tcp
```
