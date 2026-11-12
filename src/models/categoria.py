from sqlmodel import Field, Relationship, SQLModel


# Consultar producto.py para explicación más detallada

class CategoriaBase(SQLModel):
    nombre: str = Field(max_length=100)
    descripcion: str | None = None
    activo: bool = True


class Categoria(CategoriaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Para evitar import circular, Producto va en str
    productos: list["Producto"] | None = Relationship(back_populates="categoria")


class CategoriaPublic(CategoriaBase):
    id: int
