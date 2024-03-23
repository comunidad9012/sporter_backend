from pydantic import BaseModel, Field, PositiveInt


class Ejemplo(BaseModel):
    nombre: str = Field(min_length=2, max_length=40)
    titulo: str = Field(min_length=2, max_length=100)
