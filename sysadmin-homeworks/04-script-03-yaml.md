# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

### Цель задания

В результате выполнения этого задания вы:

1. Познакомитесь с синтаксисами JSON и YAML.
2. Узнаете как преобразовать один формат в другой при помощи пары строк.

### Чеклист готовности к домашнему заданию

Установлена библиотека pyyaml для Python 3.

### Инструкция к заданию 

1. Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys-24/04-script-03-yaml/README.md).
2. Заполните недостающие части документа решением задач (заменяйте `???`, остальное в шаблоне не меняйте, чтобы не сломать форматирование текста, подсветку синтаксиса и прочее) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желанию.
3. Любые вопросы по выполнению заданий спрашивайте в чате учебной группы и/или в разделе “Вопросы по заданию” в личном кабинете.


------

## Задание 1

## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:

```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

### Ваш скрипт:
```
   { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : "7.1.7.5" 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
```

---

## Задание 2

В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
#!/usr/bin/env python3

import io
import json
import socket
import yaml

hosts = ('drive.google.com', 'mail.google.com', 'google.com')
filename = 'hosts_state.json'

try:
    f = open(filename)
    data = json.load(f)
    f.close()

except FileNotFoundError:
    data = []
    for one_host in hosts:
        data.append ({one_host: '0.0.0.0'})

data_out = []
for [[host, addr]] in [ x.items() for x in data]:
    new_addr = socket.gethostbyname(host)
    if addr != new_addr:
        print('ERROR  {} IP mismatch: {} {}.'.format(host, addr, new_addr))
        # [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>.
    data_out.append({host: new_addr})


with open(filename, "w") as outfile:
    json.dump(data_out, outfile)
    print ('Store json')

with io.open('hosts_state.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data_out, outfile,default_flow_style=False, allow_unicode=True)
    print ('Store yaml')

```

### Вывод скрипта при запуске при тестировании:
```
ERROR  drive.google.com IP mismatch: 172.217.168.238 173.194.222.194.
ERROR  mail.google.com IP mismatch: 142.251.36.5 108.177.14.18.
ERROR  google.com IP mismatch: 142.251.36.46 64.233.165.102.
Store json
Store yaml

```

### json-файл(ы), который(е) записал ваш скрипт:
```json
[{"drive.google.com": "173.194.222.194"}, {"mail.google.com": "108.177.14.18"}, {"google.com": "64.233.165.102"}]
```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
- drive.google.com: 173.194.222.194
- mail.google.com: 108.177.14.18
- google.com: 64.233.165.102

```

---

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

### Ваш скрипт:
```python
#!/usr/bin/env python3

import io
import json
import socket
import sys
import yaml

hosts = ('drive.google.com', 'mail.google.com', 'google.com')

new_format = 'yaml'

data_in = []


def data_check(sample_data):
    """Проверка  хостов входного файла."""
    try:
        for [o_host] in [x.keys() for x in sample_data]:
            if o_host not in hosts:
                print(f'Warning host {host} will be replaced')
        return True
    except Exception as exp:
        return False


if len(sys.argv) > 2:
    print('Error: Support only one file')
    exit(1)
elif len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print('Error: Need file name') 
    exit(1)

if not filename.endswith('.json') and not filename.endswith('.yaml'):
    print(f'Wrong type extension{filename}')
    exit(1)


with open(filename, 'r') as stream:
    try:
        print(f'Try {filename} as json format')
        data_in = json.load(stream)
    except json.JSONDecodeError as exc:
        print(f'File name as json have error {exc}, try as yaml format')
        with open(filename, 'r') as second_stream:
            try:
                data_in = yaml.safe_load(second_stream)
                new_format = 'json'
            except yaml.YAMLError as exc:
                print(f'File name as yaml have error {exc}')
                exit(1)

if not data_check(data_in):
    print(f'File  {filename} data format will be replaced')
    data = []
    for one_host in hosts:
        data.append ({one_host: '0.0.0.0'})
    data_in = data

data_out = []
for [[host, addr]] in [x.items() for x in data_in]:
    new_addr = socket.gethostbyname(host)
    if addr != new_addr:
        print('ERROR  {} IP mismatch: {} {}.'.format(host, addr, new_addr))
    data_out.append({host: new_addr})


file_info = filename.split('.')
if new_format == 'yaml':
    new_filename = f'{file_info[0]}.yaml'
    with io.open(new_filename, 'w', encoding='utf8') as outfile:
        yaml.dump(data_out, outfile, default_flow_style=False, allow_unicode=True)
else:
    new_filename = f'{file_info[0]}.json'
    with open(new_filename, "w") as outfile:
        json.dump(data_out, outfile)

print(f'Input file {filename} updated and stored in file {new_filename}')

```

### Пример работы скрипта:
```
./script-03-yaml-03.py  hosts_state.json
Try hosts_state.json as json format
ERROR  google.com IP mismatch: 64.233.165.102 64.233.165.100.
Input file hosts_state.json updated and stored in file hosts_state.yaml

./script-03-yaml-03.py  hosts_state.yaml
Try hosts_state.yaml as json format
File name as json have error Expecting value: line 1 column 1 (char 0), try as yaml format
ERROR  mail.google.com IP mismatch: 108.177.14.18 108.177.14.83.
Input file hosts_state.yaml updated and stored in file hosts_state.json

mv hosts_state.json hosts_state.yaml 

./script-03-yaml-03.py  hosts_state.yaml
Try hosts_state.yaml as json format
ERROR  mail.google.com IP mismatch: 108.177.14.18 108.177.14.17.
Input file hosts_state.yaml updated and stored in file hosts_state.yaml

```
----

### Правила приема домашнего задания

В личном кабинете отправлена ссылка на .md файл в вашем репозитории.

-----

### Критерии оценки

Зачет - выполнены все задания, ответы даны в развернутой форме, приложены соответствующие скриншоты и файлы проекта, в выполненных заданиях нет противоречий и нарушения логики.

На доработку - задание выполнено частично или не выполнено, в логике выполнения заданий есть противоречия, существенные недостатки. 
 
Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.
Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

