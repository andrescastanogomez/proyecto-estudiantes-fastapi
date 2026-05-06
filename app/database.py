import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 📍 Lógica de persistencia para Render
if os.path.exists("/data"):
    # Si la carpeta /data existe (estamos en Render), guardamos ahí
    DB_PATH = "/data/students.db"
    print("📡 Conectado al disco persistente de Render")
else:
    # Si no existe (estamos en tu PC), guardamos en la carpeta del proyecto
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "students.db")
    print("💻 Conectado a la base de datos local")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()