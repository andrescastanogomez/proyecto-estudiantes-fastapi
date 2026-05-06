from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servicios
from app import models
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioVerificar
import threading

router = APIRouter()

@router.post("/registrar")
def registrar(data: UsuarioCreate, db: Session = Depends(get_db)):

    correo_limpio = data.correo.lower().strip()

    existente = db.query(models.Usuario).filter(
        models.Usuario.correo == correo_limpio
    ).first()

    if existente:
        return {"status": "success", "mensaje": "Usuario ya registrado"}

    nuevo_usuario = models.Usuario(correo=correo_limpio)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"status": "success", "mensaje": "Usuario creado exitosamente"}


@router.post("/login")
def login(data: UsuarioLogin, db: Session = Depends(get_db)):

    correo_limpio = data.correo.lower().strip()

    user = db.query(models.Usuario).filter(
        models.Usuario.correo == correo_limpio
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # ✅ GENERAR OTP
    otp = servicios.generar_otp_simulado(db, correo_limpio)

    # ✅ ENVIAR CORREO EN SEGUNDO PLANO
    threading.Thread(
        target=servicios.enviar_correo_otp,
        args=(correo_limpio, otp)
    ).start()

    return {"status": "success", "mensaje": "OTP enviado al correo"}


@router.post("/verificar")
def verificar(data: UsuarioVerificar, db: Session = Depends(get_db)):

    if servicios.verificar_otp_db(db, data.correo, data.otp):
        return {"status": "success", "mensaje": "Acceso concedido"}

    raise HTTPException(status_code=401, detail="Código incorrecto")