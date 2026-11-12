import sys
from pathlib import Path

# Asegurar que el directorio 'src' esté en sys.path para resolver imports modulares
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from fastapi import FastAPI
from database import Base, engine
from models.productos import Producto  # IMPORTANTE para que se cree la tabla en SQLite # noqa: F401
from routers.productos import productos_routers
from routers.saludar import saludar_routers

# Crea las tablas y la base de datos real SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Práctico FastAPI 4: SQLAlchemy",
    description="API CRUD de Productos utilizando FastAPI y SQLAlchemy con SQLite real, modularizada según la arquitectura de clases.",
    version="1.0.0"
)

# Incluimos los routers (Path Operations modularizadas)
app.include_router(productos_routers, tags=["Productos"], prefix="/productos")
app.include_router(saludar_routers, tags=["Saludos"], prefix="/saludar")


@app.get("/", tags=["General"])
def read_root():
    """Ruta inicial con información y accesos a la documentación."""
    return {
        "mensaje": "Bienvenido al Práctico 4 de FastAPI con SQLAlchemy",
        "documentacion": "/docs",
        "redoc": "/redoc"
    }
