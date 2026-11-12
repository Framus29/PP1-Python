from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

# Ahora que usamos SQLModel no traemos nada de sqlalchemy.
from sqlmodel import Session, select

from database import get_db
from models.anidados import ProductoNested

# Y también nuestros schemas son los models. (fíjense los response_model)
from models.categoria import Categoria
from models.producto import Producto, ProductoBase, ProductoPublic

productos_routers = APIRouter()


# Constante, mayúsculas con snake_case
NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Producto no encontrado",
                }
            }
        },
    },
}


def _validar_categoria(db: Session, categoria_id: int | None) -> None:
    """Valida que la FK recibida apunte a una categoría existente."""
    if categoria_id is not None and db.get(Categoria, categoria_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La categoría con id {categoria_id} no existe",
        )


# get all productos (paginado, con categoría anidada)
@productos_routers.get("/", response_model=Page[ProductoNested])
async def get_productos(db: Session = Depends(get_db)):
    # EN SQL SERÍA: SELECT * FROM producto
    # CON SQLALCHEMY: db.query(Producto).all()
    return paginate(db, select(Producto))  # paginado directo en la DB


# get by id
@productos_routers.get(
    "/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=ProductoNested,
)
async def get_producto_by_id(
    id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)
):
    prod_obtenido = db.get(Producto, id)
    if prod_obtenido is not None:
        return prod_obtenido
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@productos_routers.post(
    "/",
    response_model=ProductoNested,
    status_code=status.HTTP_201_CREATED,
)  # VALIDO EL DATO DE SALIDA
async def crear_producto(
    producto_nuevo: ProductoBase, db: Session = Depends(get_db)
):  # VALIDO EL DATO DE ENTRADA
    _validar_categoria(db, producto_nuevo.categoria_id)

    # Ya no instancio ningún Objeto, sino que hago model_validate
    producto_db = Producto.model_validate(producto_nuevo)
    db.add(producto_db)
    # persistimos en la db con commit
    db.commit()
    # refrescamos UNA INSTANCIA (objeto)
    db.refresh(producto_db)
    return producto_db


@productos_routers.put(
    "/{id}", responses=NOT_FOUND_RESPONSE, response_model=ProductoPublic
)
async def editar_producto(
    id: Annotated[int, Path(gt=0, description="Id del producto. >0")],
    producto_editar: ProductoBase,
    db: Session = Depends(get_db),
):
    _validar_categoria(db, producto_editar.categoria_id)

    prod_obtenido = db.get(Producto, id)

    if prod_obtenido is not None:
        prod_obtenido.nombre = producto_editar.nombre
        prod_obtenido.descripcion = producto_editar.descripcion
        prod_obtenido.precio = producto_editar.precio
        prod_obtenido.stock = producto_editar.stock
        prod_obtenido.activo = producto_editar.activo
        prod_obtenido.categoria_id = producto_editar.categoria_id
        db.commit()
        db.refresh(prod_obtenido)
        return prod_obtenido

    raise HTTPException(status_code=404, detail="Producto no encontrado")


@productos_routers.delete(
    "/{id}",  # ?logico=false
    responses=NOT_FOUND_RESPONSE,  # DOCUMENTACION
    response_model=list[ProductoPublic],  # VALIDACION DATOS DE SALIDA
)
async def borrar_producto(
    id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
):
    prod_obtenido = db.get(Producto, id)
    if prod_obtenido is not None:
        if logico:
            prod_obtenido.activo = False
        else:
            db.delete(prod_obtenido)
        db.commit()
        return db.exec(select(Producto)).all()
    raise HTTPException(status_code=404, detail="Producto no encontrado")
