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
