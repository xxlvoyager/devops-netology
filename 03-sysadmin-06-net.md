1.
---

Создаем запрос к сайту указанному в задании и получаем ответ:

```
Trying 151.101.129.69...
Connected to stackoverflow.com.
Escape character is '^]'.
GET /questions HTTP/1.0
HOST: stackoverflow.com

HTTP/1.1 403 Forbidden
```

Пролученный код из секции Client Error 4xx
ошибки пользователя,  ответ  403 означает, что сервер понял запрос, но отказывается его выполнять, без указания причины.
Если модернизировать наш запрос, с указанием User-Agent, например кодовое слово  Mozilla (наследие от  компании Netscape), получаем другой ответ:

```
GET /questions HTTP/1.0
HOST: stackoverflow.com
User-Agent: Mozilla

HTTP/1.1 301 Moved Permanently
Connection: close
cache-control: no-cache, no-store, must-revalidate
location: https://stackoverflow.com/questions
x-request-guid: 99b7e7cd-d7e2-4c12-b7d4-6e3f1483044c
feature-policy: microphone 'none'; speaker 'none'
content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com
Accept-Ranges: bytes
Date: Sat, 12 Nov 2022 09:42:33 GMT
Via: 1.1 varnish
X-Served-By: cache-fra-eddf8230081-FRA
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1668246153.127578,VS0,VE92
Vary: Fastly-SSL
X-DNS-Prefetch-Control: off
Set-Cookie: prov=52934283-2e63-7806-8a76-84b687bc56dc; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly
```

Код ответна сервера изменился на секцию  Redirection 3xx,
полученнный код 301 перенаправляет нас на ссылку по защищенному протоколу https.

---

2.

Обращаемя к сайту из браузера в режиме разработчика
получаем ответ сайта в консоли разработчика 

<img src=https://raw.githubusercontent.com/xxlvoyager/devops-netology/main/Screenshot_F12.png alt="Screenshot Console">

Код полученный браузером изменился на 307, который указывает, что запрошенный ресурс был временно перемещен на URL-адрес, указанный в заголовках Location.
Единственная разница между 307 и 302 заключается в том, что 307 гарантирует, что метод и тело не будут изменены при выполнении перенаправленного запроса. Для запросов GET их поведение идентично.

Самым длительным был ответ на зпрос самого документа 538 ms.


---

3.

Для выяснения адреса выдаваемого оператором восрользуемя утилитой curl

```

curl ifconfig.net
92.42.9.20

```

*Поскольку адрес динамический, нет остнований для беспокойства при его публикации.*

---

4.

Выясняем принадлежность адреса к автономной системе

```
whois -h whois.radb.net 92.42.9.20
route:          92.42.8.0/23
descr:          KMVtelecom users
origin:         AS44963
mnt-by:         DAVV-MNT
created:        2014-01-02T19:00:34Z
last-modified:  2014-01-02T19:00:34Z
source:         RIPE
```

----

5. 
Для просмотра всех автономных сетей воспользуемся утилитой treaceroute

`traceroute -An 8.8.8.8`

обработаем зпрос при помощи пайплайна

```

for AS in `traceroute -An 8.8.8.8 |grep -v '8.8.8.8'| awk '{print $3}' |grep -v '*' | tr -d '['| tr -d ']'|uniq`;  
> do  whois -h whois.radb.net $AS; done|egrep 'aut-num|as-name'
aut-num:        AS44963
as-name:        POTOK-AS
aut-num:        AS12389
as-name:        ROSTELECOM-AS
aut-num:    AS15169
as-name:    Google

```

---

6.

Делаем трассировку при помощи MTR

<img src=https://raw.githubusercontent.com/xxlvoyager/devops-netology/main/Screenshot-MTR.png alt="MTR Console">

Pings – подразделяется на Last, Avg, Best, Wrst и StDev.
            — Last – время задержки последнего пакета;
            — Avg – среднее время задержки;
            — Best – наименьшее время задержки;
            — Wrst – наибольшее время задержки;
            — StDev – стандартное отклонение времени задержки. 

Самое высокое среднее время задержки на сети AS15169 Google

---

7.

Смотрим  записи типа NS и типа A  на одном из корневых серверов Интернета `a.root-servers.net`

```
dig @198.41.0.4   -t A -t NS  dns.google

;; AUTHORITY SECTION:
google.			172800	IN	NS	ns-tld4.charlestonroadregistry.com.
google.			172800	IN	NS	ns-tld3.charlestonroadregistry.com.
google.			172800	IN	NS	ns-tld1.charlestonroadregistry.com.
google.			172800	IN	NS	ns-tld2.charlestonroadregistry.com.
google.			172800	IN	NS	ns-tld5.charlestonroadregistry.com.

;; ADDITIONAL SECTION:
ns-tld4.charlestonroadregistry.com. 172800 IN A	216.239.38.105
ns-tld4.charlestonroadregistry.com. 172800 IN AAAA 2001:4860:4802:38::69
ns-tld3.charlestonroadregistry.com. 172800 IN A	216.239.36.105
ns-tld3.charlestonroadregistry.com. 172800 IN AAAA 2001:4860:4802:36::69
ns-tld1.charlestonroadregistry.com. 172800 IN A	216.239.32.105
ns-tld1.charlestonroadregistry.com. 172800 IN AAAA 2001:4860:4802:32::69
ns-tld2.charlestonroadregistry.com. 172800 IN A	216.239.34.105
ns-tld2.charlestonroadregistry.com. 172800 IN AAAA 2001:4860:4802:34::69
ns-tld5.charlestonroadregistry.com. 172800 IN A	216.239.60.105
ns-tld5.charlestonroadregistry.com. 172800 IN AAAA 2001:4860:4805::69

```


Таким образом у dns.google по 5 адресов серверов ipv4 и ipv6

---

8.

Автоматизируем запрос для получения Reverse DNS: 

```

for AAA in `dig -4 @198.41.0.4   -t A   dns.google | grep   -A 10 'ADDITIONAL SECTION'| awk '{print $5}'`; do dig -x $AAA; done | grep -A1 'ANSWER SECTION'|egrep -v ';' |awk '{print $5, $1}'


ns-tld4.charlestonroadregistry.com. 105.38.239.216.in-addr.arpa.
 --
ns-tld4.charlestonroadregistry.com. 9.6.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.3.0.0.2.0.8.4.0.6.8.4.1.0.0.2.ip6.arpa.
 --
ns-tld3.charlestonroadregistry.com. 105.36.239.216.in-addr.arpa.
 --
ns-tld3.charlestonroadregistry.com. 9.6.0.0.0.0.0.0.0.0.0.0.0.0.0.0.6.3.0.0.2.0.8.4.0.6.8.4.1.0.0.2.ip6.arpa.
 --
ns-tld1.charlestonroadregistry.com. 105.32.239.216.in-addr.arpa.
 --
ns-tld1.charlestonroadregistry.com. 9.6.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.3.0.0.2.0.8.4.0.6.8.4.1.0.0.2.ip6.arpa.
 --
ns-tld2.charlestonroadregistry.com. 105.34.239.216.in-addr.arpa.
 --
ns-tld2.charlestonroadregistry.com. 9.6.0.0.0.0.0.0.0.0.0.0.0.0.0.0.4.3.0.0.2.0.8.4.0.6.8.4.1.0.0.2.ip6.arpa.
 --
ns-tld5.charlestonroadregistry.com. 105.60.239.216.in-addr.arpa.
 --
ns-tld5.charlestonroadregistry.com. 9.6.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.5.0.8.4.0.6.8.4.1.0.0.2.ip6.arpa.

```
