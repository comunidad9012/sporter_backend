from os import getenv

from sqlalchemy.engine import URL, create_engine

DB_CREDENTIALS = {
    "drivername": getenv("MYSQL_DRIVERNAME"),
    "username": getenv("MYSQL_USERNAME"),
    "password": getenv("MYSQL_PASSWORD"),
    "host": getenv("MYSQL_HOST"),
    "port": getenv("MYSQL_PORT"),
    "database": getenv("MYSQL_DATABASE"),
}

DB_URL = URL.create(**DB_CREDENTIALS)

ENGINE = create_engine(DB_URL)
