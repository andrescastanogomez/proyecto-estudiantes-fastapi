
from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    correo: EmailStr

class UsuarioLogin(BaseModel):
    correo: EmailStr

class UsuarioVerificar(BaseModel):
    correo: EmailStr
    otp: str