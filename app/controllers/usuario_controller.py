from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servicios

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/registrar")
def registrar(correo: str, db: Session = Depends(get_db)):
    return servicios.crear_usuario(db, correo)

@router.post("/login")
def login(correo: str, db: Session = Depends(get_db)):
    codigo = servicios.generar_otp_simulado(db, correo)
    if not codigo:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "OTP generado, revisa la consola"}

@router.post("/verificar")
def verificar(correo: str, otp: str, db: Session = Depends(get_db)):
    es_valido = servicios.verificar_otp_db(db, correo, otp)
    if not es_valido:
        raise HTTPException(status_code=400, detail="OTP incorrecto o expirado")
    return {"mensaje": "Login exitoso"}