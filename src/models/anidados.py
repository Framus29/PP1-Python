from .producto import ProductoPublic, Producto
from .categoria import CategoriaPublic, Categoria


#Producto Anidado
class ProductoNested(ProductoPublic):
    categoria: Categoria | None = None


class CategoriaNested(CategoriaPublic):
    productos: list[Producto] = []
