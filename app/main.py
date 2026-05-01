import mimetypes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.controllers import estudiante_controller, usuario_controller
from app.database import engine, Base

# Solución para Windows: Forzar MIME types
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Proyecto Estudiantes OTP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. API Routers
app.include_router(usuario_controller.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(estudiante_controller.router, prefix="/api", tags=["Estudiantes"])

# 2. Montar archivos estáticos
# IMPORTANTE: La carpeta 'static' debe existir en la raíz del proyecto
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Servir el Index
@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)