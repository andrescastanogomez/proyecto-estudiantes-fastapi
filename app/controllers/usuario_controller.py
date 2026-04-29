from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servicios

# Sin prefijo aquí para evitar el error de ruta duplicada
router = APIRouter(tags=["Usuarios"])

@router.post("/login")  # Debe ser POST
def login(correo: str, db: Session = Depends(get_db)):
    codigo = servicios.generar_otp_simulado(db, correo)
    if not codigo:
        # Si devuelve 404, el JS registrará al usuario automáticamente
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "OTP generado"}

@router.post("/registrar")
def registrar(correo: str, db: Session = Depends(get_db)):
    return servicios.crear_usuario(db, correo)

@router.post("/verificar")
def verificar(correo: str, otp: str, db: Session = Depends(get_db)):
    es_valido = servicios.verificar_otp_db(db, correo, otp)
    if not es_valido:
        raise HTTPException(status_code=400, detail="Código incorrecto")
    return {"mensaje": "Login exitoso"}