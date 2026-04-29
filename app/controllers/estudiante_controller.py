from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.estudiante import Estudiante 

router = APIRouter()

# 1. OBTENER TODOS LOS ESTUDIANTES (READ)
@router.get("/estudiantes")
def obtener_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()

# 2. CREAR UN ESTUDIANTE (CREATE)
@router.post("/estudiantes")
def crear_estudiante(nombre: str, apellido: str, carrera: str, email: str, db: Session = Depends(get_db)):
    nuevo = Estudiante(nombre=nombre, apellido=apellido, carrera=carrera, email=email)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# 3. ACTUALIZAR ESTUDIANTE (UPDATE) - ¡ESTO ERA LO QUE FALTABA!
@router.put("/estudiantes/{id}")
def actualizar_estudiante(id: int, nombre: str, apellido: str, carrera: str, email: str, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    estudiante.nombre = nombre
    estudiante.apellido = apellido
    estudiante.carrera = carrera
    estudiante.email = email
    
    db.commit()
    return {"message": "Actualizado con éxito"}

# 4. ELIMINAR ESTUDIANTE (DELETE)
@router.delete("/estudiantes/{id}")
def eliminar_estudiante(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db.delete(estudiante)
    db.commit()
    return {"message": "Eliminado con éxito"}