# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

### Цель задания

В результате выполнения этого задания вы:

1. Познакомитесь с синтаксисом Python.
2. Узнаете, для каких типов задач его можно использовать.
3. Воспользуетесь несколькими модулями для работы с ОС.


### Инструкция к заданию

1. Установите Python 3 любой версии.
2. Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-01-bash/README.md).
3. Заполните недостающие части документа решением задач (заменяйте `???`, остальное в шаблоне не меняйте, чтобы не сломать форматирование текста, подсветку синтаксиса). Вместо логов можно вставить скриншоты по желанию.
4. Для проверки домашнего задания преподавателем в личном кабинете прикрепите и отправьте ссылку на решение в виде md-файла в вашем Github.
5. Любые вопросы по выполнению заданий спрашивайте в чате учебной группы и/или в разделе “Вопросы по заданию” в личном кабинете.

------

## Задание 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:

| Вопрос  | Ответ |
| ------------- | ------------- |
| Какое значение будет присвоено переменной `c`?  | ???  |
| Как получить для переменной `c` значение 12?  | ???  |
| Как получить для переменной `c` значение 3?  | ???  |

------

## Задание 2

Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. 

Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
import sys

current_path = sys.path[0]

bash_command = ['cd {}'.format(current_path), 'git ls-files -dmo']
result_os = os.popen(' && '.join(bash_command)).readlines()
for one_row in result_os:
    out_line = current_path + '/' + one_row
    print (out_line,end='')

```

### Вывод скрипта при запуске при тестировании:
```
$ ./test.py 
/home/alexey/Projects/devops-netology/04-script-02-py.md
/home/alexey/Projects/devops-netology/test.py
/home/alexey/Projects/devops-netology/test2.py
/home/alexey/Projects/devops-netology/test3.p
```

------

## Задание 3

Доработать скрипт выше так, чтобы он не только мог проверять локальный репозиторий в текущей директории, но и умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
import sys

# root_path='~/netology/sysadm-homeworks'

# используется для демонстрации
root_path='/home/alexey/Projects/devops-netology' 

current_path = sys.path[0]
if len(sys.argv) > 2:
    print('Error: Support only one path')
    exit(1)
elif len(sys.argv) == 2:
    full_path = sys.argv[1]
else: 
    full_path = current_path

if not full_path.startswith(root_path):
    print('Error: Not supported  path')
    exit(1)

bash_command = ['cd {}'.format(full_path), 'git ls-files -dmo']
result_os = os.popen(' && '.join(bash_command)).readlines()
for one_row in result_os:
    out_line = full_path + '/' + one_row
    print (out_line,end='')
```

### Вывод скрипта при запуске при тестировании:
```
./test2.py 
/home/alexey/Projects/devops-netology/04-script-02-py.md
/home/alexey/Projects/devops-netology/test.py
/home/alexey/Projects/devops-netology/test2.py
/home/alexey/Projects/devops-netology/test3.py
(devops-netology) alexey@dexp:~/Projects/devops-netology$ ./test2.py /some/path
Error: Not supported  path
(devops-netology) alexey@dexp:~/Projects/devops-netology$ ./test2.py /some/path /more/path
Error: Support only one path

```

------

## Задание 4

Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. 

Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. 

Мы хотим написать скрипт, который: 
- опрашивает веб-сервисы, 
- получает их IP, 
- выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. 

Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
#!/usr/bin/env python3
import json
import socket

hosts = ('drive.google.com', 'mail.google.com', 'google.com')
filename = 'hosts_state.json'

try:
    f = open(filename)
    data = json.load(f)
    f.close()

except FileNotFoundError:
    data = {}

for one_host in hosts:
    new_addr = socket.gethostbyname(one_host)
    try:    
        old_addr = data[one_host]
        if old_addr != new_addr:
            print('ERROR  {} IP mismatch: {} {}.'.format(one_host, old_addr, new_addr))
            # [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>.
            data[one_host] = new_addr
        else:
            print(one_host,'-',data[one_host])
    except  KeyError:
        data[one_host] = new_addr


with open(filename, "w") as outfile:
    json.dump(data, outfile)
```

### Вывод скрипта при запуске при тестировании:
```
$python3 test3.py 

drive.google.com - 173.194.73.194
mail.google.com - 74.125.131.19
ERROR  google.com IP mismatch: 64.233.162.113 64.233.162.100.
```

------

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз: 
* переносить архив с нашими изменениями с сервера на наш локальный компьютер, 
* формировать новую ветку, 
* коммитить в неё изменения, 
* создавать pull request (PR) 
* и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. 

Мы хотим максимально автоматизировать всю цепочку действий. 
* Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым).
* При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. 
* С директорией локального репозитория можно делать всё, что угодно. 
* Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. 

Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 

### Ваш скрипт:
```python
#!/usr/bin/env python3
"""
this script use GitHub CLI 
to get help goto https://docs.github.com/en/rest
"""
import json
import os
import re
import sys
from  datetime import datetime

from git import Repo

if len(sys.argv) != 2:
    print('Error: Wrong argumets')
    exit(1)

git_path = '{}/.git'.format(sys.path[0])

commit_message = sys.argv[1]

# pull_request the same neame of commit

pull_request = commit_message

repo = Repo(git_path)
origin = repo.remote(name='origin')
origin.pull()
original_branch = repo.active_branch
branch_name = 'feature/{}'.format(hash(datetime.now()))
branch = repo.create_head(branch_name)
branch.checkout()
repo.git.add('.')
repo.index.commit(commit_message)
repo.git.push('--set-upstream', 'origin', branch)
original_branch.checkout()


remote_url = repo.remote().url
remote_repo = re.sub('.git','', re.sub('..*/', '', remote_url))
remote_user = re.sub('..*:','', re.sub('/..*', '', remote_url))


command_chunk = ('/usr/bin/gh  api --method POST', 
                 '-H "Accept: application/vnd.github+json"',
                 '/repos/{}/{}/pulls'.format(remote_user, remote_repo),
                 '-f title="{}"'.format(pull_request),
                 '-f body="Please pull these awesome changes in!"',
                 '-f head="{}"'.format(branch_name),
                 '-f base="main"'
                 )


bash_command = ' '.join(command_chunk)

result_os = os.popen(bash_command).readlines()

result = json.loads(result_os[0])

print('Created pull request', result['uri'] )

```

### Вывод скрипта при запуске при тестировании:
```

$ ./git_repo.py 'Update git_repo.py'
Created pull request https://api.github.com/repos/xxlvoyager/devops-netology/pulls/17

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

