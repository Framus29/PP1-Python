from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from database import get_db
from models.productos import Producto
from schemas.productos import (
    ProductoSchema,
    ProductoCreateSchema,
    ProductoUpdateSchema,
)

productos_routers = APIRouter()

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {"detail": "Producto no encontrado"}
            }
        },
    },
}


# =======================================================
# PATH OPERATIONS (CRUD CON BASE DE DATOS REAL SQLITE)
# =======================================================

# 1. READ ALL - Obtener todos los productos
@productos_routers.get(
    "/",
    response_model=List[ProductoSchema],
    summary="Listar todos los productos"
)
async def get_productos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retorna la lista de productos almacenados en la base de datos real SQLite.
    Equivale a: SELECT * FROM productos LIMIT limit OFFSET skip
    """
    productos = db.query(Producto).offset(skip).limit(limit).all()
    return productos


# 2. READ BY ID - Obtener un producto por su clave primaria
@productos_routers.get(
    "/{id}",
    response_model=ProductoSchema,
    responses=NOT_FOUND_RESPONSE,
    summary="Obtener un producto por su ID"
)
async def get_producto_by_id(
    id: Annotated[int, Path(gt=0, description="ID del producto")],
    db: Session = Depends(get_db)
):
    """
    Busca un producto por su ID usando db.get().
    """
    producto = db.get(Producto, id)
    if producto is not None:
        return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


# 3. CREATE - Crear un nuevo producto en la base de datos
@productos_routers.post(
    "/",
    response_model=ProductoSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto"
)
async def crear_producto(
    producto_nuevo: ProductoCreateSchema,
    db: Session = Depends(get_db)
):
    """
    Crea e inserta un nuevo registro en la tabla 'productos'.
    """
    # Instanciamos el modelo SQLAlchemy con los datos validados de Pydantic
    db_producto = Producto(**producto_nuevo.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


# 4. UPDATE - Actualizar un producto existente
@productos_routers.put(
    "/{id}",
    response_model=ProductoSchema,
    responses=NOT_FOUND_RESPONSE,
    summary="Actualizar un producto existente"
)
async def editar_producto(
    id: Annotated[int, Path(gt=0, description="ID del producto")],
    producto_editar: ProductoUpdateSchema,
    db: Session = Depends(get_db)
):
    """
    Actualiza los campos de un producto existente en la base de datos.
    """
    db_producto = db.get(Producto, id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Modificar solo los campos provistos
    datos_actualizar = producto_editar.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(db_producto, clave, valor)

    db.commit()
    db.refresh(db_producto)
    return db_producto


# 5. DELETE - Eliminar un producto (soporta borrado físico y borrado lógico)
@productos_routers.delete(
    "/{id}",
    responses=NOT_FOUND_RESPONSE,
    summary="Eliminar un producto por ID"
)
async def borrar_producto(
    id: Annotated[int, Path(gt=0, description="ID del producto")],
    db: Session = Depends(get_db),
    logico: Annotated[bool, Query(description="True para borrado lógico (activo=False)")] = False
):
    """
    Elimina un producto de la base de datos SQLite.
    Si logico=True, desactiva el producto sin borrar el registro.
    """
    db_producto = db.get(Producto, id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if logico:
        db_producto.activo = False
        db.commit()
        return {"mensaje": f"Producto con ID {id} desactivado (borrado lógico)"}
    else:
        db.delete(db_producto)
        db.commit()
        return {"mensaje": f"Producto con ID {id} eliminado exitosamente de la base de datos"}
