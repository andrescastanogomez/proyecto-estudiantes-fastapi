import smtplib
import random
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from app.models.usuario import Usuario

# --- CONFIGURACIÓN MAESTRA ---
GMAIL_USER = "nacionalspod@gmail.com"
GMAIL_PASSWORD = "bjjsjxavestjlqfc" 

def enviar_correo_otp(destinatario, otp):
    # Nombre que el usuario verá en su bandeja de entrada
    NOMBRE_REMITENTE = "Soporte OTP" 
    
    # Diseño del mensaje
    cuerpo_mensaje = f"""
    Hola,
    
    Has solicitado un código de verificación para acceder a nuestro sistema.
    
    Tu código de seguridad es: {otp}
    
    Este código es personal y no debes compartirlo con nadie. Si no has solicitado este acceso, puedes ignorar este mensaje.
    
    Atentamente,
    El equipo de Soporte
    """
    
    mensaje = MIMEText(cuerpo_mensaje)
    mensaje["Subject"] = f"🔑 Código de verificación: {otp}"
    mensaje["From"] = f"{NOMBRE_REMITENTE} <{GMAIL_USER}>"
    mensaje["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            # .replace(" ", "") asegura que no haya espacios en la contraseña
            servidor.login(GMAIL_USER, GMAIL_PASSWORD.replace(" ", ""))
            servidor.send_message(mensaje)
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False

# 1. REGISTRAR: Crea usuario y manda el primer OTP
def crear_usuario(db: Session, correo: str):
    otp = str(random.randint(100000, 999999))
    nuevo_usuario = Usuario(correo=correo, otp=otp)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    enviar_correo_otp(correo, otp)
    print(f"--- OTP DE REGISTRO ENVIADO A {correo}: {otp} ---")
    return nuevo_usuario

# 2. LOGIN: Genera nuevo OTP para usuarios que ya existen
def generar_otp_simulado(db: Session, correo: str):
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario:
        return None
    
    otp = str(random.randint(100000, 999999))
    usuario.otp = otp
    db.commit()
    
    enviar_correo_otp(correo, otp)
    print(f"--- OTP DE LOGIN ENVIADO A {correo}: {otp} ---")
    return otp

# 3. VERIFICAR: Comprueba el código y lo limpia de la DB
def verificar_otp_db(db: Session, correo: str, otp: str):
    usuario = db.query(Usuario).filter(Usuario.correo == correo, Usuario.otp == otp).first()
    if usuario:
        # Borramos el OTP después de usarlo por seguridad
        usuario.otp = None 
        db.commit()
        return True
    return False