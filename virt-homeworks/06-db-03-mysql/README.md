# Домашнее задание к занятию "6.3. MySQL"



## Задача 1

Сооздаем файл `compose.yml` 

```yaml
version: '3.1'

services:

  db:
    image: mysql:8
    command: --default-authentication-plugin=mysql_native_password
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    ports:
      - 3306:3306


```

устанвливаем на хосте пароль  для сервиса в переменной и запусакем сервис
```bash

export MYSQL_ROOT_PASSWORD="my precious"
docker compose up -d

```

подключаемся к удаленнной консоли по TCP  или через `docker compose exec` и создаем базу данных

```bash

mysql -h localhost -P 3306 --protocol=tcp -u root  -p${MYSQL_ROOT_PASSWORD}
# via docker
# docker-compose exec db mysql -p${MYSQL_ROOT_PASSWORD}

mysql> create database test_db;
Query OK, 1 row affected (0,01 sec)

```

восстанавливаем базу данных

```bash

mysql -h localhost -P 3306 --protocol=tcp -u root  -p${MYSQL_ROOT_PASSWORD}  test_db < test_data/test_dump.sql

```

Перейдим в управляющую консоль `mysql` внутри контейнера.


```console
mysql> \s
--------------
mysql  Ver 8.0.32-0ubuntu0.22.04.2 for Linux on x86_64 ((Ubuntu))

Connection id:		12
Current database:	test_db
Current user:		root@172.21.0.1
SSL:			Cipher in use is TLS_AES_256_GCM_SHA384
Current pager:		stdout
Using outfile:		''
Using delimiter:	;
Server version:		8.0.32 MySQL Community Server - GPL
Protocol version:	10
Connection:		localhost via TCP/IP
Server characterset:	utf8mb4
Db     characterset:	utf8mb4
Client characterset:	utf8mb4
Conn.  characterset:	utf8mb4
TCP port:		3306
Binary data as:		Hexadecimal
Uptime:			31 min 29 sec

Threads: 2  Questions: 49  Slow queries: 0  Opens: 179  Flush tables: 3  Open tables: 97  Queries per second avg: 0.025
--------------

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test_db            |
+--------------------+
5 rows in set (0,00 sec)

mysql> show tables;
+-------------------+
| Tables_in_test_db |
+-------------------+
| orders            |
+-------------------+
1 row in set (0,01 sec)

mysql> select * from orders where price > 300;
+----+----------------+-------+
| id | title          | price |
+----+----------------+-------+
|  2 | My little pony |   500 |
+----+----------------+-------+
1 row in set (0,00 sec)


```

## Задача 2

Используем следующие команды в консоли

```sql
CREATE USER  'test'@'localhost' IDENTIFIED WITH mysql_native_password BY 'test-pass'
    WITH MAX_QUERIES_PER_HOUR 100
    PASSWORD EXPIRE INTERVAL 180 DAY
    FAILED_LOGIN_ATTEMPTS 3
    ATTRIBUTE '{"fname": "James", "lname": "Pretty"}';



GRANT ALL PRIVILEGES ON test_db  TO 'test'@'localhost';
```

Выполняем и просматриваем результаты

```console
mysql> CREATE USER  'test'@'localhost' IDENTIFIED WITH mysql_native_password BY 'test-pass'
    ->     WITH MAX_QUERIES_PER_HOUR 100
    ->     PASSWORD EXPIRE INTERVAL 180 DAY
    ->     FAILED_LOGIN_ATTEMPTS 3
    ->     ATTRIBUTE '{"fname": "James", "lname": "Pretty"}';
Query OK, 0 rows affected (0,00 sec)

mysql> GRANT ALL PRIVILEGES ON test_db  TO 'test'@'localhost';
Query OK, 0 rows affected, 1 warning (0,01 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0,01 sec)

mysql> SHOW GRANTS for 'test'@'localhost';
+-------------------------------------------------------------------+
| Grants for test@localhost                                         |
+-------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `test`@`localhost`                          |
| GRANT ALL PRIVILEGES ON `test_db`.`test_db` TO `test`@`localhost` |
+-------------------------------------------------------------------+
2 rows in set (0,00 sec)

mysql> select * from information_schema.USER_ATTRIBUTES;
+------------------+-----------+---------------------------------------+
| USER             | HOST      | ATTRIBUTE                             |
+------------------+-----------+---------------------------------------+
| root             | %         | NULL                                  |
| mysql.infoschema | localhost | NULL                                  |
| mysql.session    | localhost | NULL                                  |
| mysql.sys        | localhost | NULL                                  |
| root             | localhost | NULL                                  |
| test             | localhost | {"fname": "James", "lname": "Pretty"} |
+------------------+-----------+---------------------------------------+
6 rows in set (0,00 sec)


mysql> select * from information_schema.USER_ATTRIBUTES where USER='test';
+------+-----------+---------------------------------------+
| USER | HOST      | ATTRIBUTE                             |
+------+-----------+---------------------------------------+
| test | localhost | {"fname": "James", "lname": "Pretty"} |
+------+-----------+---------------------------------------+
1 row in set (0,00 sec)

```

## Задача 3

Установите профилирование `SET profiling = 1`.
Изучите вывод профилирования команд `SHOW PROFILES;`.

```console

mysql> SELECT TABLE_NAME,        ENGINE FROM   information_schema.TABLES WHERE  TABLE_SCHEMA = 'test_db';
+------------+--------+
| TABLE_NAME | ENGINE |
+------------+--------+
| orders     | InnoDB |
+------------+--------+
1 row in set (0,00 sec)

mysql>  SET profiling = 1;
Query OK, 0 rows affected, 1 warning (0,00 sec)

mysql> select * from orders;
+----+-----------------------+-------+
| id | title                 | price |
+----+-----------------------+-------+
|  1 | War and Peace         |   100 |
|  2 | My little pony        |   500 |
|  3 | Adventure mysql times |   300 |
|  4 | Server gravity falls  |   300 |
|  5 | Log gossips           |   123 |
+----+-----------------------+-------+
5 rows in set (0,00 sec)

mysql> insert into orders(title, price) values ('Banan', 1);
Query OK, 1 row affected (0,00 sec)

mysql> delete  from  orders where title='Banan';
Query OK, 1 row affected (0,01 sec)

mysql> SHOW PROFILES;
+----------+------------+------------------------------------------------------+
| Query_ID | Duration   | Query                                                |
+----------+------------+------------------------------------------------------+
|        1 | 0.00063925 | select * from orders                                 |
|        2 | 0.00507150 | insert into orders(title, price) values ('Banan', 1) |
|        3 | 0.00471200 | delete  from  orders where title='Banan'             |
+----------+------------+------------------------------------------------------+
3 rows in set, 1 warning (0,01 sec)

mysql> SHOW PROFILE;
+--------------------------------+----------+
| Status                         | Duration |
+--------------------------------+----------+
| starting                       | 0.000103 |
| Executing hook on transaction  | 0.000013 |
| starting                       | 0.000019 |
| checking permissions           | 0.000016 |
| Opening tables                 | 0.000069 |
| init                           | 0.000017 |
| System lock                    | 0.000062 |
| updating                       | 0.000375 |
| end                            | 0.000016 |
| query end                      | 0.000012 |
| waiting for handler commit     | 0.003787 |
| closing tables                 | 0.000038 |
| freeing items                  | 0.000159 |
| cleaning up                    | 0.000028 |
+--------------------------------+----------+
14 rows in set, 1 warning (0,01 sec)

mysql> ALTER TABLE orders ENGINE = MyISAM;
Query OK, 5 rows affected (0,04 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql>  SET profiling = 1;
Query OK, 0 rows affected, 1 warning (0,01 sec)

mysql> select * from orders;
+----+-----------------------+-------+
| id | title                 | price |
+----+-----------------------+-------+
|  1 | War and Peace         |   100 |
|  2 | My little pony        |   500 |
|  3 | Adventure mysql times |   300 |
|  4 | Server gravity falls  |   300 |
|  5 | Log gossips           |   123 |
+----+-----------------------+-------+
5 rows in set (0,00 sec)

mysql> insert into orders(title, price) values ('Banan', 1);
Query OK, 1 row affected (0,00 sec)

mysql> delete  from  orders where title='Banan';
Query OK, 1 row affected (0,00 sec)

mysql> SHOW PROFILES;
+----------+------------+------------------------------------------------------+
| Query_ID | Duration   | Query                                                |
+----------+------------+------------------------------------------------------+
|        1 | 0.00070450 | select * from orders                                 |
|        2 | 0.00244225 | insert into orders(title, price) values ('Banan', 1) |
|        3 | 0.00321225 | delete  from  orders where title='Banan'             |
+----------+------------+------------------------------------------------------+
3 rows in set, 1 warning (0,00 sec)

mysql> SHOW PROFILE;
+--------------------------------+----------+
| Status                         | Duration |
+--------------------------------+----------+
| starting                       | 0.000104 |
| Executing hook on transaction  | 0.000013 |
| starting                       | 0.000019 |
| checking permissions           | 0.000015 |
| Opening tables                 | 0.000063 |
| init                           | 0.000017 |
| System lock                    | 0.000055 |
| updating                       | 0.000263 |
| end                            | 0.000015 |
| query end                      | 0.000011 |
| waiting for handler commit     | 0.002383 |
| closing tables                 | 0.000078 |
| freeing items                  | 0.000153 |
| cleaning up                    | 0.000024 |
+--------------------------------+----------+
14 rows in set, 1 warning (0,00 sec)


```

## Задача 4

Уточняем количество памяти доступной машине:

```console
cat /proc/meminfo |grep MemTotal
MemTotal:       16330272 kB
```

Установим размер буфера кэширования в 5 GB

Добавляем в секцию [mysqld] файла `my.cnf`  согласно ТЗ.

```console
[mysqld]
# движок InnoDB
default-storage-engine=InnoDB

# Скорость IO важнее сохранности данных
innodb_flush_log_at_trx_commit = 2

# Нужна компрессия таблиц для экономии места на диске
protocol_compression_algorithms=zstd

# Размер буффера с незакомиченными транзакциями 1 Мб
innodb_log_buffer_size = 1M

# Буффер кеширования 30% от ОЗУ
innodb_buffer_pool_size = 5G

# Размер файла логов операций 100 Мб
innodb_log_file_size = 100М
```
