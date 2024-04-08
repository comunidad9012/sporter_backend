from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import INTEGER

from product_api_service.database.custom_declarative_base import CustomBase


class Producto(CustomBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(40))
    descripcion: Mapped[str] = mapped_column(String(255))
    precio: Mapped[int] = mapped_column(INTEGER(unsigned=True))
    existencias: Mapped[int] = mapped_column(INTEGER(unsigned=True))
    img_orig_name: Mapped[str] = mapped_column(String(100))
    img_rand_name: Mapped[str] = mapped_column(String(36))
    id_etiqueta: Mapped[int] = mapped_column(ForeignKey("etiqueta.id"))
    etiqueta: Mapped["Etiqueta"] = relationship(back_populates="producto")


    def serialize(self):

        as_dictionary = {}

        for column in self.__class__.__table__.columns:
            as_dictionary.setdefault(column.name, getattr(self, column.name))

        return as_dictionary
