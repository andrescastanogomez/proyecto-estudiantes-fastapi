from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.controllers import usuario_controller, estudiante_controller # 1. Importamos el nuevo controlador

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI OTP Service")

# 1. CONFIGURACIÓN DE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. INCLUSIÓN DE RUTAS
app.include_router(usuario_controller.router)
app.include_router(estudiante_controller.router, prefix="/api") # 2. Registramos las rutas del CRUD

# 3. ARCHIVOS ESTÁTICOS
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. RUTA PRINCIPAL
@app.get("/")
async def leer_index():
    return FileResponse("static/index.html")