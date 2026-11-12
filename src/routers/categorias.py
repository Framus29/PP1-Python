from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

# Ahora que usamos SQLModel no traemos nada de sqlalchemy.
from sqlmodel import Session, select

from database import get_db
from models.anidados import CategoriaNested

# Y también nuestros schemas son los models. (fíjense los response_model)
from models.categoria import Categoria, CategoriaBase, CategoriaPublic

categorias_routers = APIRouter()


# Constante, mayúsculas con snake_case
NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Categoría no encontrada",
                }
            }
        },
    },
}


# get all categorias (paginado)
@categorias_routers.get("/", response_model=Page[CategoriaPublic])
async def get_categorias(db: Session = Depends(get_db)):
    return paginate(db, select(Categoria))


# get by id (con datos anidados de productos)
@categorias_routers.get(
    "/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=CategoriaNested,
)
async def get_categoria_by_id(
    id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)
):
    cat_obtenida = db.get(Categoria, id)
    if cat_obtenida is not None:
        return cat_obtenida
    raise HTTPException(status_code=404, detail="Categoría no encontrada")


@categorias_routers.post(
    "/",
    response_model=CategoriaPublic,
    status_code=status.HTTP_201_CREATED,
)
async def crear_categoria(
    categoria_nueva: CategoriaBase, db: Session = Depends(get_db)
):
    categoria_db = Categoria.model_validate(categoria_nueva)
    db.add(categoria_db)
    db.commit()
    db.refresh(categoria_db)
    return categoria_db


@categorias_routers.put(
    "/{id}", responses=NOT_FOUND_RESPONSE, response_model=CategoriaPublic
)
async def editar_categoria(
    id: Annotated[int, Path(gt=0, description="Id de la categoría. >0")],
    categoria_editar: CategoriaBase,
    db: Session = Depends(get_db),
):
    cat_obtenida = db.get(Categoria, id)

    if cat_obtenida is not None:
        cat_obtenida.nombre = categoria_editar.nombre
        cat_obtenida.descripcion = categoria_editar.descripcion
        cat_obtenida.activo = categoria_editar.activo
        db.commit()
        db.refresh(cat_obtenida)
        return cat_obtenida

    raise HTTPException(status_code=404, detail="Categoría no encontrada")


@categorias_routers.delete(
    "/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=list[CategoriaPublic],
)
async def borrar_categoria(
    id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
):
    cat_obtenida = db.get(Categoria, id)
    if cat_obtenida is not None:
        if logico:
            cat_obtenida.activo = False
        else:
            db.delete(cat_obtenida)
        db.commit()
        return db.exec(select(Categoria)).all()
    raise HTTPException(status_code=404, detail="Categoría no encontrada")
