from sqlalchemy import Column, Integer, String
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    # Es vital que el correo sea único para que el registro no duplique usuarios
    correo = Column(String, unique=True, index=True, nullable=False)
    # El campo OTP debe permitir nulos (nullable=True) porque al inicio está vacío
    otp = Column(String, nullable=True)