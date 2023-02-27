# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1


Создаем Dockerfile

```docker
FROM centos:7.9.2009

EXPOSE 9200

USER 0

ENV ES_HOME=/usr/share/elasticsearch 

RUN yum -y install vim java-11-openjdk java-11-openjdk-devel

COPY elasticsearch.repo /etc/yum.repos.d/elasticsearch.repo

RUN rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch

RUN yum -y install --enablerepo=elasticsearch elasticsearch

COPY elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

WORKDIR ${HOME}

USER 999

CMD ["sh", "-c", "${ES_HOME}/bin/elasticsearch"]

```

Кофиуграционный файл `elasticsearch.yml`

```yaml
node.name: netology_test
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
transport.host: 127.0.0.1
http.host: 0.0.0.0

```
Файл репозитория для `elasticsearch.repo `

```
[elasticsearch]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=0
autorefresh=1
type=rpm-md

```

compose.yml

```yaml
services:
  es:
    build:
      context: ./
      dockerfile: ./Dockerfile
    ports:
      - '9200:9200'

```

Собираем и запускаем образ
```bash
docker compose build
docker compose up
```

После старта запрашиваем главную страницу `curl localhost:9200`
```json
{
  "name" : "netology_test",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "xcgRdKipSaSOfxUodEAKrQ",
  "version" : {
    "number" : "7.17.9",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "ef48222227ee6b9e70e502f0f0daa52435ee634d",
    "build_date" : "2023-01-31T05:34:43.305517834Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

```


Отправляем образ в репозиторий

```bash
docker build -t xxlvoyager/elasticsearch:7.17.9  .
docker push xxlvoyager/elasticsearch:7.17.9 
```

Ссылка на репозиторий

https://hub.docker.com/r/xxlvoyager/elasticsearch/tags


## Задача 2

Создаем индексы




```console
PUT /ind-1
{
  "settings": {
    "index": {
      "number_of_shards": 1,  
      "number_of_replicas": 0 
    }
  }
}
PUT /ind-2
{
  "settings": {
    "index": {
      "number_of_shards": 2,  
      "number_of_replicas": 1 
    }
  }
}
PUT /ind-3
{
  "settings": {
    "index": {
      "number_of_shards": 4,  
      "number_of_replicas": 2 
    }
  }
}
```

```console

GET _cat/indices

green  open .geoip_databases                SG_ZIRpnQha3eQ2ewmCa_A 1 0 41   0  39.6mb  39.6mb
green  open .apm-custom-link                FiVZpk4VRraYavvXbLZLTg 1 0  0   0    226b    226b
green  open .kibana_task_manager_1          e7nWZw7FS6ym3PuLUH1-UA 1 0  5 930 178.5kb 178.5kb
green  open .apm-agent-configuration        LQ4I8ZLSQnK_urqI18UGgw 1 0  0   0    226b    226b
green  open ind-1                           QR_aqNpMRq6TChjlPyJR0g 1 0  0   0    226b    226b
green  open .kibana-event-log-7.10.2-000001 G_8wFnPDRwa9HJd2Gt1BZg 1 0  1   0   5.6kb   5.6kb
green  open .kibana_1                       VrgU1UmTQQyVgpatnR-IRg 1 0 19   4   4.2mb   4.2mb
yellow open ind-3                           tSTA1XxgQJOZ1eNr7C6YSA 4 2  0   0    904b    904b
yellow open ind-2                           K6dGwSZDQsi9b7OG-Z2z5w 2 1  0   0    452b    452b

```

Часть индексов с состоянии `yellow` поскольку  кластер состоит из одной ноды и  нет реплик.

## Задача 3

Дорабатываем файлы `compose.yml` 

```yaml
services:
  elasticsearch:
    image: xxlvoyager/elasticsearch:7.17.9
    volumes:
      - ./elasticsearch.yml:/etc/elasticsearch/elasticsearch.yml:ro
      - ./snapshots:/usr/share/elasticsearch/snapshots
    ports:
      - '9200:9200'
  kibana:
    image: docker.elastic.co/kibana/kibana:7.10.2
    ports:
      - '5601:5601'
    depends_on:
      - elasticsearch


```

и `elasticsearch.yaml`

```yaml
node.name: netology_test
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
path.repo: ["/usr/share/elasticsearch/snapshots"]
transport.host: 127.0.0.1
http.host: 0.0.0.0

```

Поднимаем контейнер и подключаемся к Dev Tool Kibana

создаем репозиторий

``` console
PUT _snapshot/netology_backup
{
  "type": "fs",
  "settings": {
    "location": "/usr/share/elasticsearch/snapshots"
  }
}

{
  "acknowledged" : true
}

```

Создаем индекс и бекап

```console
PUT /test
{
  "settings": {
    "index": {
      "number_of_shards": 1,  
      "number_of_replicas": 0 
    }
  }
}

{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test"
}

GET _cat/indices

green open .geoip_databases                T7l0a0dhQAGaYWOoOAcbwg 1 0 41  0 39.6mb 39.6mb
green open .apm-custom-link                elVuO-1bS2WKALuVlA8clA 1 0  0  0   226b   226b
green open test                            DKQD6OGNScCq4nvbFFjYSA 1 0  0  0   226b   226b
green open .kibana_task_manager_1          7M1CfQeeTayMgiL6Ocadyg 1 0  5 27 65.1kb 65.1kb
green open .apm-agent-configuration        ndeT8vnWQQKdQZR7GIxvVg 1 0  0  0   226b   226b
green open .kibana_1                       O4RHLKS8TnKcHNwP1PY26w 1 0 12  0  2.1mb  2.1mb
green open .kibana-event-log-7.10.2-000001 OjPnty7ERoShCWgAIlN_oA 1 0  1  0  5.5kb  5.5kb


PUT /_snapshot/netology_backup/backup_2702?wait_for_completion=true
{
  "indices": "test",
  "ignore_unavailable": "true",
  "include_global_state": false
}

{
  "snapshot" : {
    "snapshot" : "backup_2702",
    "uuid" : "oOQoIbwQSeKgSilcQ-tk8A",
    "repository" : "netology_backup",
    "version_id" : 7170999,
    "version" : "7.17.9",
    "indices" : [
      "test"
    ],
    "data_streams" : [ ],
    "include_global_state" : false,
    "state" : "SUCCESS",
    "start_time" : "2023-02-27T17:00:15.458Z",
    "start_time_in_millis" : 1677517215458,
    "end_time" : "2023-02-27T17:00:15.458Z",
    "end_time_in_millis" : 1677517215458,
    "duration_in_millis" : 0,
    "failures" : [ ],
    "shards" : {
      "total" : 1,
      "failed" : 0,
      "successful" : 1
    },
    "feature_states" : [ ]
  }
}


```

Удаляем индекс, создаем новый индекс, восстанавливаем базу

```console

DELETE test

{
  "acknowledged" : true
}

PUT /test-2
{
  "settings": {
    "index": {
      "number_of_shards": 1,  
      "number_of_replicas": 0 
    }
  }
}

{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test-2"
}

GET _cat/indices

green open test-2                          K6NPZ3KFTBuzMkSNds7lxA 1 0  0  0   226b   226b
green open .geoip_databases                T7l0a0dhQAGaYWOoOAcbwg 1 0 41  0 39.6mb 39.6mb
green open .apm-custom-link                elVuO-1bS2WKALuVlA8clA 1 0  0  0   226b   226b
green open .kibana_task_manager_1          7M1CfQeeTayMgiL6Ocadyg 1 0  5 36 30.2kb 30.2kb
green open .apm-agent-configuration        ndeT8vnWQQKdQZR7GIxvVg 1 0  0  0   226b   226b
green open .kibana_1                       O4RHLKS8TnKcHNwP1PY26w 1 0 13  2  2.1mb  2.1mb
green open .kibana-event-log-7.10.2-000001 OjPnty7ERoShCWgAIlN_oA 1 0  1  0  5.6kb  5.6kb



POST /_snapshot/netology_backup/backup_2702/_restore?wait_for_completion=true

{
  "snapshot" : {
    "snapshot" : "backup_2702",
    "indices" : [
      "test"
    ],
    "shards" : {
      "total" : 1,
      "failed" : 0,
      "successful" : 1
    }
  }
}

GET _cat/indices

green open test-2                          K6NPZ3KFTBuzMkSNds7lxA 1 0  0  0   226b   226b
green open .geoip_databases                T7l0a0dhQAGaYWOoOAcbwg 1 0 41  0 39.6mb 39.6mb
green open test                            cy2CGsPvR7uIWreeIScPeg 1 0  0  0   226b   226b
green open .apm-custom-link                elVuO-1bS2WKALuVlA8clA 1 0  0  0   226b   226b
green open .kibana_task_manager_1          7M1CfQeeTayMgiL6Ocadyg 1 0  5 42 78.8kb 78.8kb
green open .apm-agent-configuration        ndeT8vnWQQKdQZR7GIxvVg 1 0  0  0   226b   226b
green open .kibana-event-log-7.10.2-000001 OjPnty7ERoShCWgAIlN_oA 1 0  1  0  5.6kb  5.6kb
green open .kibana_1                       O4RHLKS8TnKcHNwP1PY26w 1 0 14  4  2.1mb  2.1mb
```

---
