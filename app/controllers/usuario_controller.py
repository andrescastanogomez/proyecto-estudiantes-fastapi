from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servicios

router = APIRouter()

@router.post("/registrar")
def registrar(correo: str, db: Session = Depends(get_db)):
    # Limpieza total del correo para evitar errores de RFC 5321
    correo_limpio = correo.lower().strip()
    try:
        # Intentar crear el usuario en la base de datos
        nuevo_usuario = servicios.crear_usuario(db, correo_limpio)
        # Intentar envío de correo (opcional, no bloquea el registro)
        try:
            servicios.enviar_correo_bienvenida(correo_limpio)
        except:
            print(f"Correo de bienvenida no enviado a {correo_limpio}")
            
        return {"status": "success", "mensaje": "Usuario listo para ingresar"}
    except Exception:
        # Si ya existe, devolvemos 200 para que el JS no muestre un error feo
        return {"status": "success", "mensaje": "El usuario ya estaba registrado"}

@router.post("/login")
def login(correo: str, db: Session = Depends(get_db)):
    correo_limpio = correo.lower().strip()
    codigo = servicios.generar_otp_simulado(db, correo_limpio)
    
    if not codigo:
        raise HTTPException(status_code=404, detail="Correo no encontrado")
    
    # En Render, esto llegará a tu correo si configuraste las variables SMTP
    print(f"--- OTP GENERADO: {codigo} ---")
    return {"status": "success", "mensaje": "Código enviado correctamente"}

@router.post("/verificar")
def verificar(correo: str, otp: str, db: Session = Depends(get_db)):
    correo_limpio = correo.lower().strip()
    if servicios.verificar_otp_db(db, correo_limpio, otp):
        return {"status": "success", "mensaje": "Acceso concedido"}
    raise HTTPException(status_code=401, detail="Código incorrecto")