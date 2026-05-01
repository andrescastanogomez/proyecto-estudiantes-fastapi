from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.estudiante import Estudiante
from pydantic import BaseModel

router = APIRouter()

# Esquema para validar los datos que vienen del Frontend
class EstudianteSchema(BaseModel):
    nombre: str
    apellido: str
    carrera: str
    email: str

    class Config:
        from_attributes = True

@router.get("/estudiantes")
def listar_estudiantes(db: Session = Depends(get_db)):
    # Importante: No debe pedir parámetros obligatorios aquí para evitar el 422
    return db.query(Estudiante).all()

@router.post("/estudiantes")
def crear_estudiante(estudiante_data: EstudianteSchema, db: Session = Depends(get_db)):
    nuevo_estudiante = Estudiante(
        nombre=estudiante_data.nombre,
        apellido=estudiante_data.apellido,
        carrera=estudiante_data.carrera,
        email=estudiante_data.email
    )
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

@router.put("/estudiantes/{estudiante_id}")
def actualizar_estudiante(estudiante_id: int, estudiante_data: EstudianteSchema, db: Session = Depends(get_db)):
    db_est = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not db_est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    for key, value in estudiante_data.dict().items():
        setattr(db_est, key, value)
    
    db.commit()
    db.refresh(db_est)
    return db_est

@router.delete("/estudiantes/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    db_est = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not db_est:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(db_est)
    db.commit()
    return {"message": "Eliminado"}