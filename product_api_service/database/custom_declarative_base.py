from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class CustomBase(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):

        class_name = cls.__name__
        tablename_char_list = []

        for index, char in enumerate(class_name):
            if char.isupper() and index != 0:
                tablename_char_list.append("_")

            tablename_char_list.append(char)

        return class_name.lower()
