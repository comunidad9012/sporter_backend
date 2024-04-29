from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import INTEGER

from product_api_service.database.custom_declarative_base import CustomBase

class Sesion(CustomBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login_time_unix : Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("user.id"))
    usuario: Mapped["User"] = relationship(back_populates="sesiones")
    
    def serialize(self):

        as_dictionary = {}

        for column in self.__class__.__table__.columns:
            as_dictionary.setdefault(column.name, getattr(self, column.name))

        return as_dictionary