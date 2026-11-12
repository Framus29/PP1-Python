# Práctico FastAPI: SQLModel, Alembic, Paginación y Autenticación

Proyecto modularizado de **FastAPI** implementando **SQLModel**, **Alembic**, **paginación** y **autenticación con bcrypt**, siguiendo la arquitectura del repositorio de referencia ([FacuLemo/fastapi-2026](https://github.com/FacuLemo/fastapi-2026)) con temática propia de **E-Commerce (Categorías y Productos)**.

---

## 📋 Requisitos de la consigna cumplidos

- **SQLModel en lugar de SQLAlchemy:** Se reemplaza `declarative_base`, `Column`, `sessionmaker` por SQLModel puro. Los modelos actúan también como schemas (igual que en el repo de referencia).
- **Alembic para migraciones:** `alembic.ini` + `env.py` conectado a `SQLModel.metadata`. Migraciones generadas con `--autogenerate`.
- **Al menos 2 modelos con relación tipo Foreign Key:** `Categoria` y `Producto` relacionados con `foreign_key="categoria.id"` y `Relationship(back_populates=...)`.
- **Clases de SQLModel (schemas) para datos anidados:** `ProductoNested` y `CategoriaNested` en `src/models/anidados.py`.
- **Paginación:** `GET /categorias/` y `GET /productos/` devuelven un `Page[...]` usando `fastapi-pagination` (parámetros `page` y `size`).
- **CORS:** Middleware configurado en `src/main.py` para permitir el consumo desde un frontend.
- **Autenticación:** registro y login de usuarios con contraseña hasheada mediante **bcrypt** (`src/core/auth.py`).

---

## 📁 Arquitectura Modularizada

```text
PP1-Python/
│
├── alembic.ini                  # Configuración principal de Alembic
├── alembic/
│   ├── env.py                   # Conectado a SQLModel.metadata
│   ├── script.py.mako           # Plantilla de migraciones
│   └── versions/
│       ├── aca9e1c40668_migracion_inicial.py
│       └── dd6de306dc9f_crear_tabla_usuarios.py
│
├── requirements.txt             # FastAPI, SQLModel, Alembic, Paginación, bcrypt
├── base_de_datos.db             # SQLite gestionada por Alembic
├── seed.py                      # Poblar la DB con datos relacionales
├── test_api.py                  # Suite de pruebas automatizadas
├── main.py                      # Punto de entrada raíz
└── src/
    ├── database.py              # engine, get_db() con SQLModel
    ├── main.py                  # FastAPI app + routers + CORS + paginación
    │
    ├── core/
    │   ├── __init__.py
    │   └── auth.py              # get_password_hash(), verify_password()
    │
    ├── models/                  # Modelos SQLModel (tabla + schema en uno)
    │   ├── __init__.py
    │   ├── categoria.py         # CategoriaBase, Categoria (table=True), CategoriaPublic
    │   ├── producto.py          # ProductoBase, Producto (table=True, FK), ProductoPublic
    │   ├── usuarios.py          # Usuario, UsuarioCreate, UsuarioPublic, UsuarioLogin
    │   └── anidados.py          # ProductoNested, CategoriaNested
    │
    └── routers/                 # Path Operations CRUD
        ├── __init__.py
        ├── categorias.py        # categorias_routers → /categorias/
        ├── productos.py         # productos_routers  → /productos/
        ├── auth.py              # auth_routers       → /auth/
        └── saludar.py           # saludar_routers    → /saludar/
```

---

## 🚀 Instalación y Uso

```bash
# 1. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones con Alembic
alembic upgrade head

# 4. Poblar la DB (opcional)
python seed.py

# 5. Iniciar el servidor
fastapi dev src/main.py
# o: uvicorn src.main:app --reload
```

Docs interactiva: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

> **Nota:** las tablas (`categoria`, `producto`, `usuario`) las gestiona Alembic. No se usa `create_all()` en la app.

---

## 🛠️ Endpoints

### Categorías (`/categorias`)
| Método | Endpoint | Descripción | Respuesta |
|:---|:---|:---|:---|
| `GET` | `/categorias/?page=1&size=50` | Lista paginada (`Page[CategoriaPublic]`) | `200 OK` |
| `GET` | `/categorias/{id}` | Por ID con productos anidados (`CategoriaNested`) | `200` / `404` |
| `POST` | `/categorias/` | Crear nueva categoría | `201 Created` |
| `PUT` | `/categorias/{id}` | Editar categoría | `200` / `404` |
| `DELETE` | `/categorias/{id}` | Borrado físico | `200` / `404` |
| `DELETE` | `/categorias/{id}?logico=true` | Borrado lógico (`activo=False`) | `200` / `404` |

### Productos (`/productos`)
| Método | Endpoint | Descripción | Respuesta |
|:---|:---|:---|:---|
| `GET` | `/productos/?page=1&size=50` | Lista paginada con categoría anidada (`Page[ProductoNested]`) | `200 OK` |
| `GET` | `/productos/{id}` | Por ID con categoría anidada (`ProductoNested`) | `200` / `404` |
| `POST` | `/productos/` | Crear (valida que `categoria_id` exista) | `201` / `400` |
| `PUT` | `/productos/{id}` | Editar producto | `200` / `400` / `404` |
| `DELETE` | `/productos/{id}` | Borrado físico | `200` / `404` |
| `DELETE` | `/productos/{id}?logico=true` | Borrado lógico (`activo=False`) | `200` / `404` |

### Autenticación (`/auth`)
| Método | Endpoint | Descripción | Respuesta |
|:---|:---|:---|:---|
| `POST` | `/auth/register` | Registrar usuario (contraseña hasheada con bcrypt) | `201` / `400` |
| `POST` | `/auth/login` | Verificar credenciales | `200` / `401` |

Ejemplo de registro:

```json
{
  "nombre": "Francisco",
  "email": "francisco@mail.com",
  "contraseña": "secreto123"
}
```

### Generales
| Método | Endpoint | Descripción |
|:---|:---|:---|
| `GET` | `/` | Mensaje de bienvenida |
| `GET` | `/saludar/` | Endpoint de prueba |

---

## 🔐 CORS

En `src/main.py` el middleware permite peticiones desde:

- `http://127.0.0.1:5500`
- `http://localhost:5500`

Podés agregar el origen de tu frontend en `allow_origins`.

---

## 🧪 Pruebas

```bash
python test_api.py
```

La suite prueba CRUD de categorías y productos, paginación, validación de FK, borrado lógico/físico y registro/login de usuarios.
