from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definimos la ruta de la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"

# 2. Creamos el motor de conexión
# check_same_thread=False es exclusivo de SQLite para permitir múltiples hilos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creamos la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Creamos la clase Base para los modelos
Base = declarative_base()

# 5. Dependencia para obtener la DB en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()