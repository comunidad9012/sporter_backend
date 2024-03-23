from pydantic import BaseModel, Field, PositiveInt


class Producto(BaseModel):
    nombre: str = Field(min_length=2, max_length=40)
    descripcion: str = Field(min_length=2, max_length=255)
    precio: PositiveInt
    existencias: PositiveInt
