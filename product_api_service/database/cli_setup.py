from sqlalchemy import text
from sqlalchemy.orm import Session
from flask.cli import AppGroup
from product_api_service import models
from product_api_service.database.custom_declarative_base import CustomBase
from product_api_service.database.engine import (
    ENGINE,
    DB_CREDENTIALS,
    URL,
    create_engine,
)

db_setup: AppGroup = AppGroup("db-cli")


@db_setup.command("crear-tablas")
def create_schemas(test_db: bool = False):
    """Crear las tablas de la DB"""
    _orm_create_models()


@db_setup.command("crear-db")
def create_db(test_db: bool = False):
    """Crea la DB sin las tablas"""
    _orm_create_db()


@db_setup.command("crear-todo")
def create_everything(test_db: bool = False):
    """Crea la DB y las TABLAS"""
    _orm_create_db()
    _orm_create_models()


def _orm_create_models():
    CustomBase.metadata.create_all(ENGINE)


def _orm_create_db():
    DB_NAME = DB_CREDENTIALS.pop("database")
    SETUP_ENGINE = create_engine(URL.create(**DB_CREDENTIALS))

    with Session(bind=SETUP_ENGINE) as SETUP_SESSION:
        SETUP_SESSION.execute(text(f"CREATE DATABASE {DB_NAME}"))
