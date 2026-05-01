from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servicios
import threading

router = APIRouter()

# =========================
# REGISTRAR USUARIO
# =========================
@router.post("/registrar")
def registrar(correo: str, db: Session = Depends(get_db)):
    correo_limpio = correo.lower().strip()

    try:
        servicios.crear_usuario(db, correo_limpio)

        # Intento enviar correo de bienvenida (no bloquea)
        try:
            servicios.enviar_correo_bienvenida(correo_limpio)
        except Exception as e:
            print("Error correo bienvenida:", e)

        return {"status": "success", "mensaje": "Usuario listo para ingresar"}

    except Exception:
        return {"status": "success", "mensaje": "El usuario ya estaba registrado"}


# =========================
# LOGIN - GENERAR OTP
# =========================
@router.post("/login")
def login(correo: str, db: Session = Depends(get_db)):
    correo_limpio = correo.lower().strip()

    codigo = servicios.generar_otp_simulado(db, correo_limpio)

    if not codigo:
        raise HTTPException(status_code=404, detail="Correo no encontrado")

    print(f"--- OTP GENERADO: {codigo} ---")

    # 🔥 ENVÍO ASYNC (NO BLOQUEA)
    def enviar_async():
        try:
            servicios.enviar_correo_otp(correo_limpio, codigo)
            print("📩 Correo enviado correctamente")
        except Exception as e:
            print("❌ Error enviando correo:", e)

    threading.Thread(target=enviar_async).start()

    return {"status": "success", "mensaje": "Código enviado correctamente"}


# =========================
# VERIFICAR OTP
# =========================
@router.post("/verificar")
def verificar(correo: str, otp: str, db: Session = Depends(get_db)):
    correo_limpio = correo.lower().strip()

    if servicios.verificar_otp_db(db, correo_limpio, otp):
        return {"status": "success", "mensaje": "Acceso concedido"}

    raise HTTPException(status_code=401, detail="Código incorrecto")