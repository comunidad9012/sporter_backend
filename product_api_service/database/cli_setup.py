import bcrypt
from flask.cli import AppGroup
from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from product_api_service import models
from product_api_service.database.custom_declarative_base import CustomBase
from product_api_service.database.engine import (
    DB_CREDENTIALS,
    ENGINE,
    URL,
    create_engine,
)

db_setup: AppGroup = AppGroup("db-cli")


@db_setup.command("crear-tablas")
def create_schemas(test_db: bool = False):
    """Crear las tablas de la DB"""
    _orm_create_models()
    _orm_creat_admin()


@db_setup.command("crear-db")
def create_db(test_db: bool = False):
    """Crea la DB sin las tablas"""
    _orm_create_db()


@db_setup.command("crear-todo")
def create_everything(test_db: bool = False):
    """Crea la DB y las TABLAS"""
    _orm_create_db()
    _orm_create_models()


def _orm_creat_admin():
    session_local = sessionmaker(autoflush=False, autocommit=False, bind=ENGINE)

    with session_local() as sesion:
        passwd = bcrypt.hashpw("1234567890".encode("UTF-8"), bcrypt.gensalt())

        usuario_admin = models.User(
            nombre="admin",
            usuario="admin",
            correo="admin@example.com",
            is_admin=1,
            contraseña=passwd,
        )

        sesion.add(usuario_admin)

        sesion.commit()


def _orm_create_models():
    CustomBase.metadata.create_all(ENGINE)


def _orm_create_db():
    DB_NAME = DB_CREDENTIALS.pop("database")
    SETUP_ENGINE = create_engine(URL.create(**DB_CREDENTIALS))

    with Session(bind=SETUP_ENGINE) as SETUP_SESSION:
        SETUP_SESSION.execute(text(f"CREATE DATABASE {DB_NAME}"))
