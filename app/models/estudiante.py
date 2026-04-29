from sqlalchemy import Column, Integer, String
from app.database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    carrera = Column(String)
    email = Column(String)