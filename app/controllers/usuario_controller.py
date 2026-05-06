from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servicios
import threading

router = APIRouter()

@router.post("/registrar")
def registrar(correo: str, db: Session = Depends(get_db)):
    # 1. Crear el objeto
    nuevo_usuario = models.Usuario(correo=correo)
    db.add(nuevo_usuario)
    
    # 2. ¡CRÍTICO! Sin esto, el registro es "exitoso" en memoria pero no se guarda
    db.commit() 
    
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario registrado"}

@router.post("/login")
def login(correo: str, db: Session = Depends(get_db)):
    # 1. Busca al usuario en la base de datos
    # Se asegura de limpiar el correo (espacios y minúsculas) para evitar errores
    correo_limpio = correo.lower().strip()
    user = db.query(models.Usuario).filter(models.Usuario.correo == correo_limpio).first()
    
    # 2. Si no existe, lanza el 404 que estás viendo en Render
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # 3. Si existe, aquí es donde llamarías a la función de generar y enviar el OTP
    # Por ahora, devolvemos el mensaje de éxito
    return {"status": "success", "mensaje": "OTP enviado a su correo"}


@router.post("/verificar")
def verificar(correo: str, otp: str, db: Session = Depends(get_db)):
    if servicios.verificar_otp_db(db, correo, otp):
        return {"status": "success", "mensaje": "Acceso concedido"}
    raise HTTPException(status_code=401, detail="Código incorrecto")