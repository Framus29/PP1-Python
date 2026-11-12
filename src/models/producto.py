# MODELO:
# Clases que representan TABLAS reales en la DB

# Ahora usamos SQLModel, que por detrás funciona con sqlalchemy.
from sqlmodel import Field, SQLModel, Relationship
from .categoria import Categoria

# VIEJO, CON SQLALCHEMY:
# class Producto(Base):
#     __tablename__ = "producto"
#     id = Column(Integer, primary_key=True)
#     nombre = Column(String)
#     ...

# AHORA, con SQLModel:
class ProductoBase(SQLModel):  # parecido a ProductoCreateUpdate
    nombre: str = Field(max_length=100)
    descripcion: str | None = None
    precio: float
    stock: int | None = None
    activo: bool = True
    #Establecemos la Clave Foránea
    categoria_id: int | None = Field(default=None, foreign_key="categoria.id")


class Producto(ProductoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Campo anidado
    categoria: Categoria | None = Relationship(back_populates="productos")


class ProductoPublic(ProductoBase):
    id: int
