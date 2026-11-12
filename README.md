# Práctico FastAPI 4: SQLAlchemy

Proyecto modularizado de **FastAPI** con **SQLAlchemy** y base de datos local **SQLite**, siguiendo la arquitectura de clases del repositorio de referencia ([FacuLemo/fastapi-2026](https://github.com/FacuLemo/fastapi-2026)).

---

## 📋 Requisitos de la consigna cumplidos

- **SQLAlchemy en requirements:** Especificado en `requirements.txt` junto con FastAPI y Uvicorn.
- **`database.py`:** Configura el `engine`, sesión (`SessionLocal`), `Base = declarative_base()` y el generador de dependencia `get_db()`.
- **Modelo de base de datos (temática libre):** Modelo `Producto` en `src/models/productos.py` que representa la tabla `productos`.
- **Path Operations de CRUD con SQLite real:** Modularizadas en `src/routers/productos.py` con operaciones `GET`, `POST`, `PUT` y `DELETE` (soporta borrado físico y lógico).

---

## 📁 Arquitectura Modularizada (`src/`)

```text
Practico 4/
│
├── requirements.txt         # Dependencias del proyecto (FastAPI, SQLAlchemy, etc.)
├── base_de_datos.db         # Base de datos SQLite real generada automáticamente
├── seed.py                  # Script para poblar la DB con datos iniciales de prueba
├── test_api.py              # Pruebas automáticas completas del CRUD
├── main.py                  # Punto de entrada raíz
└── src/
    ├── database.py          # Conexión, Engine, SessionLocal, Base y get_db()
    ├── main.py              # Aplicación FastAPI e inclusión de routers
    │
    ├── models/              # Modelos ORM (tablas de SQLAlchemy)
    │   ├── __init__.py
    │   └── productos.py     # Clase Producto (Base)
    │
    ├── schemas/             # Esquemas de validación Pydantic
    │   ├── __init__.py
    │   ├── tipos.py         # Type Aliases reutilizables con Annotated y Field
    │   └── productos.py     # ProductoSchema, ProductoCreateSchema, ProductoUpdateSchema
    │
    └── routers/             # Routers con las Path Operations (CRUD)
        ├── __init__.py
        ├── productos.py     # Endpoints CRUD de productos con Depends(get_db)
        └── saludar.py       # Endpoint de saludo
```

---

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Poblar la base de datos (opcional)
Para insertar productos de ejemplo:
```bash
python seed.py
```

### 3. Iniciar el servidor
Puedes levantarlo con cualquiera de las siguientes opciones:

- Con FastAPI CLI:
  ```bash
  fastapi dev src/main.py
  ```
- O con Uvicorn:
  ```bash
  uvicorn src.main:app --reload
  ```
  *(o directamente `uvicorn main:app --reload`)*

Servidor disponible en: `http://127.0.0.1:8000`

---

## 📖 Documentación Interactiva (Swagger / ReDoc)

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🛠️ Endpoints del CRUD (`/productos`)

| Método | Endpoint | Descripción | Código de respuesta |
| :--- | :--- | :--- | :--- |
| `POST` | `/productos/` | Crea un nuevo producto en SQLite | `201 Created` |
| `GET` | `/productos/` | Lista todos los productos (`skip` y `limit`) | `200 OK` |
| `GET` | `/productos/{id}` | Obtiene un producto por su clave primaria | `200 OK` / `404 Not Found` |
| `PUT` | `/productos/{id}` | Modifica los datos de un producto | `200 OK` / `404 Not Found` |
| `DELETE` | `/productos/{id}` | Elimina físicamente el producto | `200 OK` / `404 Not Found` |
| `DELETE` | `/productos/{id}?logico=true` | Borrado lógico (marca `activo = False`) | `200 OK` / `404 Not Found` |

---

## 🧪 Ejecutar pruebas automáticas

Para verificar que todos los endpoints y la persistencia en SQLite funcionan correctamente:
```bash
python test_api.py
```
