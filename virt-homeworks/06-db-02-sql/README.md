# Домашнее задание к занятию "6.2. SQL"

## Задача 1

Создем файл `compose.yml`

```yaml
services:
  db:
    image: 'postgres:12'
    environment:
      - POSTGRES_HOST_AUTH_METHOD=trust
      - POSTGRES_USER=test-admin-user
      - POSTGRES_DB=test_db
      - TZ=Europe/Moscow
      - PGTZ=Europe/Moscow
    ports:
      - '5432:5432'
    volumes:
      - 'postgres_backup:/var/lib/postgresql/backup'
      - 'postgres_data:/var/lib/postgresql/data/'

volumes:
  postgres_data: null
  postgres_backup: null

```

Поднимаем `docker`

```bash
docker-compose up

```
## Задача 2

Создаем файл `task2.ddl`

```sql

CREATE TABLE IF NOT EXISTS orders(
    id serial PRIMARY KEY,
    name TEXT NOT NULL,
    price INT NOT NULL);

CREATE TABLE IF NOT EXISTS clients(
    id serial PRIMARY KEY,
    full_name TEXT NOT NULL,
    country TEXT NOT NULL,
    orders INT,
    CONSTRAINT fk_orders  FOREIGN KEY (id)
    REFERENCES orders(id) ON DELETE SET NULL);

CREATE INDEX country_idx ON clients(country);

CREATE ROLE  "test-simple-user" LOGIN;
GRANT SELECT,INSERT,UPDATE,DELETE ON clients, orders   TO "test-simple-user";

```

Запускаем на исполнение

```console
$psql -h localhost --username test-admin-user --dbname test_db -f task2.ddl 
CREATE SCHEMA
CREATE TABLE
CREATE TABLE
CREATE ROLE
GRANT
```

Получаем информацию для отчета в консоли

```console
$ psql -h localhost --username test-admin-user --dbname test_db
psql (14.6 (Ubuntu 14.6-0ubuntu0.22.04.1), server 12.14 (Debian 12.14-1.pgdg110+1))
Type "help" for help.

test_db=# \l
                                             List of databases
   Name    |      Owner      | Encoding |  Collate   |   Ctype    |            Access privileges            
-----------+-----------------+----------+------------+------------+-----------------------------------------
 postgres  | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =c/"test-admin-user"                   +
           |                 |          |            |            | "test-admin-user"=CTc/"test-admin-user"
 template1 | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =c/"test-admin-user"                   +
           |                 |          |            |            | "test-admin-user"=CTc/"test-admin-user"
 test_db   | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)

test_db=# \d clients
                              Table "public.clients"
  Column   |  Type   | Collation | Nullable |               Default               
-----------+---------+-----------+----------+-------------------------------------
 id        | integer |           | not null | nextval('clients_id_seq'::regclass)
 full_name | text    |           | not null | 
 country   | text    |           | not null | 
 orders    | integer |           |          | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
    "country_idx" btree (country)
Foreign-key constraints:
    "fk_orders" FOREIGN KEY (id) REFERENCES orders(id) ON DELETE SET NULL

test_db=# \d orders
                            Table "public.orders"
 Column |  Type   | Collation | Nullable |              Default               
--------+---------+-----------+----------+------------------------------------
 id     | integer |           | not null | nextval('orders_id_seq'::regclass)
 name   | text    |           | not null | 
 price  | integer |           | not null | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "fk_orders" FOREIGN KEY (id) REFERENCES orders(id) ON DELETE SET NULL

test_db=# SELECT * FROM information_schema.role_table_grants WHERE grantee='test-simple-user';
     grantor     |     grantee      | table_catalog | table_schema | table_name | privilege_type | is_grantable | with_hierarchy 
-----------------+------------------+---------------+--------------+------------+----------------+--------------+----------------
 test-admin-user | test-simple-user | test_db       | public       | clients    | INSERT         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | clients    | SELECT         | NO           | YES
 test-admin-user | test-simple-user | test_db       | public       | clients    | UPDATE         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | clients    | DELETE         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | orders     | INSERT         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | orders     | SELECT         | NO           | YES
 test-admin-user | test-simple-user | test_db       | public       | orders     | UPDATE         | NO           | NO
 test-admin-user | test-simple-user | test_db       | public       | orders     | DELETE         | NO           | NO
(8 rows)

test_db=# \dp orders
                                          Access privileges
 Schema |  Name  | Type  |              Access privileges              | Column privileges | Policies 
--------+--------+-------+---------------------------------------------+-------------------+----------
 public | orders | table | "test-admin-user"=arwdDxt/"test-admin-user"+|                   | 
        |        |       | "test-simple-user"=arwd/"test-admin-user"   |                   | 
(1 row)

test_db=# \dp clients
                                           Access privileges
 Schema |  Name   | Type  |              Access privileges              | Column privileges | Policies 
--------+---------+-------+---------------------------------------------+-------------------+----------
 public | clients | table | "test-admin-user"=arwdDxt/"test-admin-user"+|                   | 
        |         |       | "test-simple-user"=arwd/"test-admin-user"   |                   | 
(1 row)


```

## Задача 3 и 4

Создаем файл `task3.ddl`

```sql

INSERT INTO orders(name, price) VALUES
    ('Шоколад', 10),
    ('Принтер', 3000),
    ('Книга', 500),
    ('Монитор', 7000),
    ('Гитара', 4000);

INSERT INTO clients(full_name, country) VALUES
    ('Иванов Иван Иванович', 'USA'),
    ('Петров Петр Петрович', 'Canada'),
    ('Иоганн Себастьян Бах', 'Japan'),
    ('Ронни Джеймс Дио', 'Russia'),
    ('Ritchie Blackmore', 'Russia');

update clients  set orders = orders.id  
    from orders  where orders.name='Книга' and 
    clients.full_name ='Иванов Иван Иванович';

update clients  set orders = orders.id  
    from orders  where orders.name='Гитара' and 
    clients.full_name ='Иоганн Себастьян Бах';

update clients  set orders = orders.id  from orders  
    where orders.name='Монитор' and 
    clients.full_name ='Петров Петр Петрович';

select count(*) from orders;

select count(*) from clients;

select full_name, orders.name  from clients INNER JOIN  orders  ON  clients.orders = orders.id;

```

Запускаем на исполнение

```
$ psql -h localhost --username test-admin-user --dbname test_db -f task3.ddl 
INSERT 0 5
INSERT 0 5
UPDATE 1
UPDATE 1
UPDATE 1
 count 
-------
     5
(1 row)

 count 
-------
     5
(1 row)

      full_name       |  name   
----------------------+---------
 Иванов Иван Иванович | Книга
 Иоганн Себастьян Бах | Гитара
 Петров Петр Петрович | Монитор
(3 rows)

```

## Задача 5

Запускае  EXPLAIN параметром ANALYZE оператор будет выполнен на самом деле, а не только запланирован в консоли psql

```console

test_db=# EXPLAIN (ANALYZE true)  select full_name, orders.name  from clients INNER JOIN  orders  ON  clients.orders = orders.id;
                                                   QUERY PLAN                                                    
-----------------------------------------------------------------------------------------------------------------
 Hash Join  (cost=37.00..57.24 rows=810 width=64) (actual time=0.176..0.183 rows=3 loops=1)
   Hash Cond: (clients.orders = orders.id)
   ->  Seq Scan on clients  (cost=0.00..18.10 rows=810 width=36) (actual time=0.016..0.018 rows=5 loops=1)
   ->  Hash  (cost=22.00..22.00 rows=1200 width=36) (actual time=0.071..0.072 rows=5 loops=1)
         Buckets: 2048  Batches: 1  Memory Usage: 17kB
         ->  Seq Scan on orders  (cost=0.00..22.00 rows=1200 width=36) (actual time=0.046..0.050 rows=5 loops=1)
 Planning Time: 0.219 ms
 Execution Time: 0.224 ms
(8 rows) 


```

Результат  выполнения показывает, что как будут  сканироваться таблицы - "Seq Scan" затрагиваемые оператором, и затраты реусурсов.

## Задача 6

Выполняем команду для создания архива глобальных настроек (пользователь test-simple-user ) БД test_db

```bash

docker-compose exec db bash -c 'pg_dump --username test-admin-user  test_db -F c  > /var/lib/postgresql/backup/test_db.dump'
docker-compose exec db bash -c 'pg_dumpall --username test-admin-user  --globals-only   > /var/lib/postgresql/backup/useraccts.sql'

```

Останавливаем контейнер

`docker-compose down`

Удаляем  `volume postgres_data`

`docker volume rm 06-db-02-sql_postgres_data`

Запускае docker

`docker-compose up -d`

Подключаемчя к консоли и проверяем отсутствие созданных ранее таблиц

```console
$ psql -h localhost --username test-admin-user --dbname test_db
psql (14.6 (Ubuntu 14.6-0ubuntu0.22.04.1), server 12.14 (Debian 12.14-1.pgdg110+1))
Type "help" for help.

test_db=#  \d orders
Did not find any relation named "orders".
test_db=# \d clients
Did not find any relation named "clients".
test_db=# 

```

Восстанавливаем  пользователей, базу и проверяем восстановление

```console

$ docker-compose exec db bash -c 'psql --username test-admin-user  --dbname test_db -f  /var/lib/postgresql/backup/useraccts.sql'
SET
SET
SET
ALTER ROLE
CREATE ROLE
ALTER ROLE

$ docker-compose exec db bash -c 'pg_restore --username test-admin-user  -d test_db /var/lib/postgresql/backup/test_db.dump'

$ psql -h localhost --username test-admin-user --dbname test_db -c 'select full_name, orders.name  from clients INNER JOIN  orders  ON  clients.orders = orders.id;'
      full_name       |  name   
----------------------+---------
 Иванов Иван Иванович | Книга
 Иоганн Себастьян Бах | Гитара
 Петров Петр Петрович | Монитор
(3 rows)

```

---
