from sqlalchemy import String, Boolean
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import INTEGER

from product_api_service.database.custom_declarative_base import CustomBase

#alta y baja de usuario con login, separando admin de cliente (admin puede hacer ABM de productos)


class User(CustomBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(40))
    usuario: Mapped[str] = mapped_column(String(40))
    correo:Mapped[str] = mapped_column(String(80))
    contraseña: Mapped[str] = mapped_column(String(60))
    is_admin: Mapped[bool] = mapped_column(Boolean)
    sesiones: Mapped[List["Sesion"]] = relationship(back_populates="usuario")

    def serialize(self):

        as_dictionary = {}

        for column in self.__class__.__table__.columns:
            as_dictionary.setdefault(column.name, getattr(self, column.name))

        return as_dictionary