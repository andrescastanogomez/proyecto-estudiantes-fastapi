from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.estudiante import Estudiante
from app.models.usuario import Usuario

router = APIRouter(tags=["Estudiantes"])

@router.get("/estudiantes")
def obtener_mis_estudiantes(correo: str, db: Session = Depends(get_db)):
    admin = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not admin:
        return []
    return db.query(Estudiante).filter(Estudiante.owner_id == admin.id).all()

@router.post("/estudiantes")
def crear_estudiante(nombre: str, apellido: str, carrera: str, email: str, admin_correo: str, db: Session = Depends(get_db)):
    admin = db.query(Usuario).filter(Usuario.correo == admin_correo).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")
    
    nuevo = Estudiante(nombre=nombre, apellido=apellido, carrera=carrera, email=email, owner_id=admin.id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/estudiantes/{id}")
def actualizar_estudiante(id: int, nombre: str, apellido: str, carrera: str, email: str, admin_correo: str, db: Session = Depends(get_db)):
    admin = db.query(Usuario).filter(Usuario.correo == admin_correo).first()
    est = db.query(Estudiante).filter(Estudiante.id == id, Estudiante.owner_id == admin.id).first()
    
    if not est:
        raise HTTPException(status_code=404, detail="No encontrado")
    
    est.nombre, est.apellido, est.carrera, est.email = nombre, apellido, carrera, email
    db.commit()
    return {"status": "actualizado"}

@router.delete("/estudiantes/{id}")
def eliminar_estudiante(id: int, admin_correo: str, db: Session = Depends(get_db)):
    admin = db.query(Usuario).filter(Usuario.correo == admin_correo).first()
    est = db.query(Estudiante).filter(Estudiante.id == id, Estudiante.owner_id == admin.id).first()
    
    if not est:
        raise HTTPException(status_code=404, detail="No encontrado")
    
    db.delete(est)
    db.commit()
    return {"status": "eliminado"}
@router.get("/estudiantes/conteo")
def obtener_conteo(admin_correo: str, db: Session = Depends(get_db)):
    # Contamos cuántos estudiantes pertenecen a este admin
    admin = db.query(Usuario).filter(Usuario.correo == admin_correo.lower().strip()).first()
    if not admin:
        return {"total": 0}
    
    total = db.query(Estudiante).filter(Estudiante.owner_id == admin.id).count()
    return {"total": total}