import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

# Importar modelos para registrarlos en SQLModel.metadata (gestión con Alembic)
from models.categoria import Categoria    # noqa: F401
from models.producto import Producto      # noqa: F401
from models.usuarios import Usuario       # noqa: F401

from routers.auth import auth_routers
from routers.categorias import categorias_routers
from routers.productos import productos_routers
from routers.saludar import saludar_routers

app = FastAPI()

app.title = "Práctico FastAPI: SQLModel, Alembic, Paginación y Auth"

# Incluimos los routers (path operations)
app.include_router(categorias_routers, tags=["Categorías"], prefix="/categorias")
app.include_router(productos_routers, tags=["Productos"], prefix="/productos")
app.include_router(saludar_routers, tags=["Saludos"], prefix="/saludar")
app.include_router(auth_routers, tags=["Autenticación"], prefix="/auth")
# ^ Tags agrupa en la documentación
# ^ Prefix le pone prefijos a las urls de cada path operation definido en ese router

# Para paginar los resultados de la app:
add_pagination(app)


# Request -> Middleware -> Path Operation -> Middleware -> Response
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",  # entorno desarrollo
        "http://localhost:5500",  # entorno desarrollo
        # "*", wildcard ! Cualquier origen
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def read_root():
    return {
        "mensaje": "Bienvenido a la API de E-Commerce con SQLModel y Alembic",
        "documentacion": "/docs",
        "redoc": "/redoc"
    }
