import smtplib
import random
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from app.models.usuario import Usuario

GMAIL_USER = "nacionalspod@gmail.com"
GMAIL_PASSWORD = "jiobcdliuhblpljn"

def enviar_correo_otp(destinatario, otp):
    cuerpo = f"Tu código de acceso es: {otp}"

    mensaje = MIMEText(cuerpo)
    mensaje["Subject"] = "Código de Seguridad"
    mensaje["From"] = GMAIL_USER
    mensaje["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(GMAIL_USER, GMAIL_PASSWORD.replace(" ", ""))
        servidor.send_message(mensaje)


def generar_otp_simulado(db: Session, correo: str):
    correo_limpio = correo.lower().strip()

    usuario = db.query(Usuario).filter(
        Usuario.correo == correo_limpio
    ).first()

    if not usuario:
        return None

    otp = str(random.randint(100000, 999999))
    usuario.otp = otp
    db.commit()

    return otp


def verificar_otp_db(db: Session, correo: str, otp: str):
    correo_limpio = correo.lower().strip()

    usuario = db.query(Usuario).filter(
        Usuario.correo == correo_limpio,
        Usuario.otp == otp
    ).first()

    if usuario:
        usuario.otp = None
        db.commit()
        return True

    return False