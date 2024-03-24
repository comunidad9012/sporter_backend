from pydantic import BaseModel, Field, PositiveInt


class Ejemplo(BaseModel):
    titulo: str = Field(min_length=2, max_length=40)
    cuerpo: str = Field(min_length=2, max_length=100)
