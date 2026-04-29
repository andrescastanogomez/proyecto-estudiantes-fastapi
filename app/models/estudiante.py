from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    carrera = Column(String)
    email = Column(String)
    # Relación con el usuario:
    owner_id = Column(Integer, ForeignKey("usuarios.id"))