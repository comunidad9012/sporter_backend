from sqlalchemy import String
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import INTEGER

from product_api_service.database.custom_declarative_base import CustomBase


class Etiqueta(CustomBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(40))
    producto: Mapped[List["Producto"]] = relationship(back_populates="etiqueta")

    def serialize(self):

        as_dictionary = {}

        for column in self.__class__.__table__.columns:
            as_dictionary.setdefault(column.name, getattr(self, column.name))

        return as_dictionary