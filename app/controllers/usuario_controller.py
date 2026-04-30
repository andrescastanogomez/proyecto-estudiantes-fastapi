from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servicios

# Sin prefijo aquí para evitar el error de ruta duplicada
router = APIRouter(tags=["Usuarios"])

@router.post("/login")
def login(correo: str, db: Session = Depends(get_db)):
    correo_limpio = correo.lower().strip() # <-- La mejora técnica
    codigo = servicios.generar_otp_simulado(db, correo_limpio)
    if not codigo:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "OTP generado"}

@router.post("/registrar")
def registrar(correo: str, db: Session = Depends(get_db)):
    return servicios.crear_usuario(db, correo)

@router.post("/verificar")
def verificar(correo: str, otp: str, db: Session = Depends(get_db)):
    # Normalizamos el correo igual que en el login para que coincida con la BD
    correo_normalizado = correo.lower().strip() 
    es_valido = servicios.verificar_otp_db(db, correo_normalizado, otp)
    
    if not es_valido:
        raise HTTPException(status_code=400, detail="Código incorrecto")
    return {"mensaje": "Login exitoso"}