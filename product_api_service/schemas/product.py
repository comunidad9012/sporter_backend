from pydantic import BaseModel, Field, PositiveInt
class Producto(BaseModel):
    nombre: str = Field(min_length=2, max_length=40)
    descripcion: str = Field(min_length=2, max_length=255)
    img_rand_name: str | None = Field(min_length=1, max_length=36, default=None)
    precio: PositiveInt
    existencias: PositiveInt
    img_orig_name: str | None  = Field(min_length=1, max_length=100, default=None)
    id_etiqueta: PositiveInt
