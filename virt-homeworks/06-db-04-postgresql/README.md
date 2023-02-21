# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Поднимаем контейнер 

```yaml
services:
  db:
    image: 'postgres:13'
    environment:
      - POSTGRES_HOST_AUTH_METHOD=trust
      - POSTGRES_USER=postgres
      - POSTGRES_DB=test_database
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

Подключаемся  к БД PostgreSQL используя `psql`.

```console
psql -h localhost -U postgres 
psql (14.6 (Ubuntu 14.6-0ubuntu0.22.04.1), server 13.10 (Debian 13.10-1.pgdg110+1))
Type "help" for help.

postgres=# \l
                                   List of databases
     Name      |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
---------------+----------+----------+------------+------------+-----------------------
 postgres      | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 template1     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 test_database | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)

postgres=# \c test_database
psql (14.6 (Ubuntu 14.6-0ubuntu0.22.04.1), server 13.10 (Debian 13.10-1.pgdg110+1))
You are now connected to database "test_database" as user "postgres".
test_database=# \d
              List of relations
 Schema |     Name      |   Type   |  Owner   
--------+---------------+----------+----------
 public | orders        | table    | postgres
 public | orders_id_seq | sequence | postgres
(2 rows)

test_database=# \d orders
                                   Table "public.orders"
 Column |         Type          | Collation | Nullable |              Default               
--------+-----------------------+-----------+----------+------------------------------------
 id     | integer               |           | not null | nextval('orders_id_seq'::regclass)
 title  | character varying(80) |           | not null | 
 price  | integer               |           |          | 0
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)

test_database=# \q

```


## Задача 2


Восстанавливаем бэкап БД в `test_database`.

```console
$ psql -h localhost -U postgres -d test_database -f test_data/test_dump.sql 
SET
SET
SET
SET
SET
 set_config 
------------
 
(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
COPY 8
 setval 
--------
      8
(1 row)

ALTER TABLE
```

Перейдим в управляющую консоль `psql`

```console
psql -h localhost -U postgres -d test_database 
psql (14.6 (Ubuntu 14.6-0ubuntu0.22.04.1), server 13.10 (Debian 13.10-1.pgdg110+1))
Type "help" for help.

test_database=# ANALYZE orders;
ANALYZE
test_database=# EXPLAIN  select * from orders;
                      QUERY PLAN                       
-------------------------------------------------------
 Seq Scan on orders  (cost=0.00..1.08 rows=8 width=24)
(1 row)

test_database=# select attname, avg_width  from pg_stats where tablename = 'orders';
 attname | avg_width 
---------+-----------
 id      |         4
 title   |        16
 price   |         4
(3 rows)
```

## Задача 3

Транзакция по разбиению таблицы

```sql
BEGIN;
CREATE TABLE orders_big(id SERIAL, title VARCHAR(80) NOT NULL, price integer DEFAULT 0) PARTITION BY RANGE (price);
CREATE TABLE orders_price_gt_499 PARTITION OF orders_big FOR VALUES FROM (500) TO (2147483647);
CREATE TABLE orders_price_lte_499 PARTITION OF orders_big FOR VALUES FROM (0) TO (500);
INSERT INTO orders_big SELECT * FROM orders;
DROP TABLE orders;
ALTER TABLE orders_big RENAME TO orders;
COMMIT;
```

Если изначально известно распределение данных по полям,то разбиение можно было сделать при проектировании таблицы.

## Задача 4

Создаем бэкап

`docker-compose exec db \bash -c 'pg_dump -U postgres test_database > /var/lib/postgresql/backup/test_database.sql'`

Чтобы добавть уникальность столбца `title` для таблиц `test_database` надо в блоках  создания таблиц

`CREATE TABLE orders_price_lte_499`
`CREATE TABLE orders_price_gt_499`

изменить  строку `title character varying(80) NOT NULL`

на `title character varying(80) NOT NULL UNIQUE`

---
