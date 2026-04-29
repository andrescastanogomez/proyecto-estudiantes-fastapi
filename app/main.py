import mimetypes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.controllers import estudiante_controller, usuario_controller
from app.database import engine, Base

# Fix para que Windows reconozca archivos .js correctamente
mimetypes.add_type('application/javascript', '.js')

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD Estudiantes con OTP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(usuario_controller.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(estudiante_controller.router, prefix="/api", tags=["Estudiantes"])

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="static", html=True), name="static_root")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)