from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario

from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
import os

router = APIRouter()

# 🔥 OTP en memoria
OTP_TEMP = {}

# =========================
# CONFIG CORREO (USA VARIABLES DE ENTORNO EN RENDER)
# =========================
EMAIL_USER = "nacionalspod@gmail.com"
EMAIL_PASS = "bjjsjxavestjlqfc"

def enviar_otp_email(destino, codigo):
    if not EMAIL_USER or not EMAIL_PASS:
        print("⚠️ EMAIL_USER o EMAIL_PASS no configurados")
        print(f"OTP (fallback consola): {codigo}")
        return

    mensaje = MIMEText(f"Tu código OTP es: {codigo}")
    mensaje["Subject"] = "Código OTP"
    mensaje["From"] = EMAIL_USER
    mensaje["To"] = destino

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_USER, EMAIL_PASS)
        servidor.send_message(mensaje)
        servidor.quit()

        print("📩 Correo enviado correctamente")

    except Exception as e:
        print("❌ Error enviando correo:", e)
        print(f"OTP (fallback consola): {codigo}")


# =========================
# REGISTRO
# =========================
@router.post("/registrar")
def registrar(correo: str, db: Session = Depends(get_db)):
    correo = correo.lower().strip()

    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario:
        return {"status": "success", "mensaje": "Usuario ya existe"}

    nuevo = Usuario(correo=correo)
    db.add(nuevo)
    db.commit()

    return {"status": "success", "mensaje": "Usuario registrado"}


# =========================
# LOGIN (OTP)
# =========================
@router.post("/login")
def login(correo: str, db: Session = Depends(get_db)):
    correo = correo.lower().strip()

    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Correo no registrado")

    # Evitar múltiples OTP
    if correo in OTP_TEMP:
        otp_data = OTP_TEMP[correo]
        if datetime.now() < otp_data["expira"]:
            print(f"OTP existente: {otp_data['codigo']}")
            return {"status": "success", "mensaje": "Ya tienes un OTP activo"}

    # Generar OTP
    codigo = str(random.randint(100000, 999999))

    OTP_TEMP[correo] = {
        "codigo": codigo,
        "expira": datetime.now() + timedelta(minutes=5)
    }

    print(f"--- OTP GENERADO: {codigo} ---")

    enviar_otp_email(correo, codigo)

    return {"status": "success", "mensaje": "Código enviado"}


# =========================
# VERIFICAR
# =========================
@router.post("/verificar")
def verificar(correo: str, otp: str):
    correo = correo.lower().strip()

    otp_data = OTP_TEMP.get(correo)

    if not otp_data:
        raise HTTPException(status_code=401, detail="No hay OTP activo")

    if datetime.now() > otp_data["expira"]:
        del OTP_TEMP[correo]
        raise HTTPException(status_code=401, detail="OTP expirado")

    if otp_data["codigo"] == otp:
        del OTP_TEMP[correo]
        return {"status": "success", "mensaje": "Acceso concedido"}

    raise HTTPException(status_code=401, detail="Código incorrecto")