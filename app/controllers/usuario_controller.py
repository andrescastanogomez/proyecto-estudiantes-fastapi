from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servicios
import threading

router = APIRouter()

@router.post("/registrar")
def registrar(correo: str, db: Session = Depends(get_db)):
    try:
        servicios.crear_usuario(db, correo)
        return {"status": "success", "mensaje": "Usuario listo"}
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return {"status": "success", "mensaje": "Ya registrado"}

@router.post("/login")
def login(correo: str, db: Session = Depends(get_db)):
    codigo = servicios.generar_otp_simulado(db, correo)

    if not codigo:
        # Si llega aquí, es porque el correo no está en el archivo .db
        raise HTTPException(status_code=404, detail="Correo no encontrado")

    # Enviar correo en segundo plano
    threading.Thread(
        target=servicios.enviar_correo_otp, 
        args=(correo.lower().strip(), codigo)
    ).start()

    return {"status": "success", "mensaje": "Código enviado"}

@router.post("/verificar")
def verificar(correo: str, otp: str, db: Session = Depends(get_db)):
    if servicios.verificar_otp_db(db, correo, otp):
        return {"status": "success", "mensaje": "Acceso concedido"}
    raise HTTPException(status_code=401, detail="Código incorrecto")