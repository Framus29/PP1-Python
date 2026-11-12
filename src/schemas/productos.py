from typing import Optional
from pydantic import BaseModel, ConfigDict
from .tipos import StrCortito, PrecioFloat


class ProductoBaseSchema(BaseModel):
    nombre: StrCortito
    descripcion: Optional[str] = None
    precio: PrecioFloat
    stock: int = 0
    categoria: Optional[str] = None
    activo: bool = True


class ProductoCreateSchema(ProductoBaseSchema):
    pass


class ProductoUpdateSchema(BaseModel):
    nombre: Optional[StrCortito] = None
    descripcion: Optional[str] = None
    precio: Optional[PrecioFloat] = None
    stock: Optional[int] = None
    categoria: Optional[str] = None
    activo: Optional[bool] = None


class ProductoSchema(ProductoBaseSchema):
    id: int

    # Configuración para permitir la conversión de objetos ORM a Pydantic
    model_config = ConfigDict(from_attributes=True)
