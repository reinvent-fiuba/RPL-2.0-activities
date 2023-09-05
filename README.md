# RPL-2.0-activities

## Setup

- Install [poetry](https://python-poetry.org/) dependency manager
```
curl -sSL https://install.python-poetry.org | python3 -
```
- Install project dependencies
```
poetry install
```

- Install pre commit hooks locally (more [info](https://pre-commit.com/))
```
poetry run pre-commit install
```

## Running the project

```
poetry run start
```

By default this command will use the following DB variables:

```
DB_USER='root'
DB_PASSWORD=null
DB_HOST='127.0.0.1'
DB_PORT=3306
DB_NAME='rpl'
```

All these values can be overrided using environment variables.

```
DB_USER=rpl_activities DB_PASSWORD=rpl_activities poetry run start
```

## Hitting the service locally

```
curl http://127.0.0.1:8000/api/v2/courses/1/activities \
--header 'Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxIiwiaWF0IjoxNjMxMDA4ODAzLCJleHAiOjE2MzEwNTIwMDN9.1a20On7RXgswBvQCEDlMk2LYQ_dLr3tLIdA-OnzmrcC7vOhko98z5iywy8K13-3gYCxSg9p0RioRaiSRtxLhtA'
```

## Running tests

```
poetry run pytest
```

For running only unit tests:

```
poetry run pytest tests/unit
```

For running only http tests:

```
poetry run pytest tests/http
```

Note: By default logs aren't visible while running tests, for showing logs you will need to add the `-s` flag.




## Creating a DEV mysql instance

***ONLY THE FIRST TIME***

Span up a mysql 5.7 server in a docker container exposing the connection port 3306.
- Container name: `rpl-mysql`
- root user and passoword: `root`
- Other users: `rpl_activities` with password `rpl_activities`
- DB created with server named `rpl`

```
docker run -p 3306:3306 --name rpl-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=rpl -e MYSQL_USER=rpl_activities -e MYSQL_PASSWORD=rpl_activities -d mysql:5.7
```

Then upload the dump so you have the DB populated with real data (ping me for the dump file)

```
docker exec -i rpl-mysql sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < /path/to/all-databases.sql
```

You can validate the population connecting to the DB with our server user

```
docker exec -it rpl-mysql mysql -urpl_activities -p 
```

And then with standard SQL commands

```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.42 MySQL Community Server (GPL)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> USE rpl;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SELECT * from activities LIMIT 10;
(...)

mysql> select count(*) from activities;
+----------+
| count(*) |
+----------+
|      433 |
+----------+
1 row in set (0.00 sec)
```
