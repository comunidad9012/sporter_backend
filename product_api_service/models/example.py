from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from product_api_service.database.custom_declarative_base import CustomBase


class Ejemplo(CustomBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(40))
    cuerpo: Mapped[str] = mapped_column(String(100))
