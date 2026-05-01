from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import servicios

# Mantenemos sin prefijo para que coincida con tus llamadas actuales /usuarios/login
router = APIRouter(tags=["Usuarios"])

@router.post("/login")
def login(correo: str, db: Session = Depends(get_db)):
    # Normalización para evitar errores por mayúsculas o espacios accidentales
    correo_limpio = correo.lower().strip() 
    
    try:
        # Generamos el OTP usando el servicio
        codigo = servicios.generar_otp_simulado(db, correo_limpio)
        if not codigo:
            # Si el servicio devuelve None, es porque el correo no existe en la BD
            raise HTTPException(status_code=404, detail="El correo no está registrado")
        
        # Imprimimos en consola para que puedas verlo durante la sustentación
        print(f"--- OTP GENERADO PARA {correo_limpio}: {codigo} ---")
        return {"mensaje": "OTP generado", "status": "success"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/registrar")
def registrar(correo: str, db: Session = Depends(get_db)):
    # Normalizamos antes de guardar en la base de datos
    correo_limpio = correo.lower().strip()
    try:
        # Intentamos crear el usuario
        nuevo_usuario = servicios.crear_usuario(db, correo_limpio)
        return {"mensaje": "Usuario creado exitosamente", "usuario": nuevo_usuario}
    except Exception as e:
        # Si el correo ya existe, el servicio o la BD lanzarán un error
        raise HTTPException(status_code=400, detail="Error al registrar: el correo ya existe")

@router.post("/verificar")
def verificar(correo: str, otp: str, db: Session = Depends(get_db)):
    # Normalización vital para que coincida con lo guardado en el login
    correo_normalizado = correo.lower().strip() 
    
    try:
        es_valido = servicios.verificar_otp_db(db, correo_normalizado, otp)
        
        if not es_valido:
            raise HTTPException(status_code=400, detail="Código OTP incorrecto o expirado")
        
        return {
            "mensaje": "Login exitoso", 
            "status": "success",
            "correo": correo_normalizado
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error durante la verificación")