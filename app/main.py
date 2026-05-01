import mimetypes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.controllers import usuario_controller, estudiante_controller
from app.database import Base, engine

# MIME fixes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema OTP")

# CORS
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

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")