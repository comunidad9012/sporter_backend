from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import INTEGER

from product_api_service.database.custom_declarative_base import CustomBase


class Producto(CustomBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(40))
    descripcion: Mapped[str] = mapped_column(String(255))
    precio: Mapped[int] = mapped_column(INTEGER(unsigned=True))
    existencias: Mapped[int] = mapped_column(INTEGER(unsigned=True))
