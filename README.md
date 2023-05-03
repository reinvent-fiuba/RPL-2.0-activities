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

## Hitting the service locally

```
curl http://127.0.0.1:8000/api/v2/courses/1/activities
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
 