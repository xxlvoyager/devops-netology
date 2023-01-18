
# Домашнее задание к занятию "3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера"

---

## Задача 1

Создаем `Dockerfile`

```
FROM nginx:1.23.3
COPY index.html  /usr/share/nginx/html/
```

создаем файл `index.html`

```

<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>

```

собираем образ `docker build -t xxlvoyager/devops:0.0.1  .`

зпускае образ `docker run -d -p 80:80 xxlvoyager/devops:0.0.1`

проверяем работу сервиса

```
$ curl localhost
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```

Загружаем образ в репозиторий

```
docker login
docker push  xxlvoyager/devops:0.0.1
```

Страница образа доступна по адресу

https://hub.docker.com/r/xxlvoyager/devops/tags

Tag 0.0.1

## Задача 2

Посмотрите на сценарий ниже и ответьте на вопрос:
"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высоконагруженное монолитное java веб-приложение; физическая машина и виртуальная машина
- Nodejs веб-приложение; docker
- Мобильное приложение c версиями для Android и iOS; docker
- Шина данных на базе Apache Kafka; для тестирования с низкой нагрузкой можно использовать docker иначе кластер физических или  виртуальных машин
- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana; для тестирования с низкой нагрузкой можно использовать docker иначе кластер физических или  виртуальных машин
- Мониторинг-стек на базе Prometheus и Grafana; docker
- MongoDB, как основное хранилище данных для java-приложения; кластер физических или  виртуальных машин
- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry. При небольшой нагрузке можно использовать docker


## Задача 3
```
docker run  -d -t -v `pwd`:/data centos
docker run  -d -t -v `pwd`:/data debian

docker ps
CONTAINER ID   IMAGE                          COMMAND       CREATED              STATUS              PORTS     NAMES
b60c3abe9793   debian                         "bash"        24 seconds ago       Up 24 seconds                 wonderful_golick
d37971d02caa   centos                         "/bin/bash"   About a minute ago   Up About a minute             trusting_gates


$ docker exec -it trusting_gates bash
[root@d37971d02caa /]# echo netology devops > /data/filename.txt
[root@d37971d02caa /]# exit
exit

$ echo Test host > secondfile.txt

$ docker exec -it wonderful_golick bash
root@b60c3abe9793:/# cat /data/filename.txt 
netology devops
root@b60c3abe9793:/# cat /data/secondfile.txt 
Test host
root@b60c3abe9793:/# exit
exit

```


## Задача 4 (*)

```
$curl https://raw.githubusercontent.com/netology-code/virt-video-code/main/docker/Dockerfile > Dockerfile

$touch ansible.cfg

$docker build -t xxlvoyager/devops:0.0.2 .

$ docker run xxlvoyager/devops:0.0.2
ansible-playbook [core 2.14.1]
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.9/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible-playbook
  python version = 3.9.16 (main, Dec 10 2022, 13:47:19) [GCC 10.3.1 20210424] (/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = False

$docker login

$docker push  xxlvoyager/devops:0.0.2

```
Ссылка на репозиторий

https://hub.docker.com/r/xxlvoyager/devops/tags

Tag 0.0.2

---

