import mimetypes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.controllers import estudiante_controller, usuario_controller
from app.database import engine, Base

# Forzar tipos MIME para evitar errores de carga en Windows/Navegadores
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

# Crear las tablas en la base de datos de Render al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Gestión Estudiantes OTP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RUTAS DE LA API ---
# El prefijo /usuarios se suma a las rutas del controlador (ej: /usuarios/login)
app.include_router(usuario_controller.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(estudiante_controller.router, prefix="/api", tags=["Estudiantes"])

# --- ARCHIVOS ESTÁTICOS ---
# Monta la carpeta static para que Render encuentre el CSS y JS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)