from pydantic import BaseModel, Field


class Etiqueta(BaseModel):
    nombre: str = Field(min_length=2, max_length=40)