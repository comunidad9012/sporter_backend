from pydantic import BaseModel, Field

class User(BaseModel):
    nombre: str = Field(min_length=5, max_length=40)
    usuario: str = Field(min_length=5, max_length=40)
    correo: str = Field(min_length=5, max_length=40)
    contraseña: str = Field(min_length=5, max_length=40)
    is_admin: bool = Field(default=0)