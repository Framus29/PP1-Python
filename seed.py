import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from sqlmodel import Session, select
from database import engine
from models.categoria import Categoria
from models.producto import Producto

CATEGORIAS_INICIALES = [
    {"nombre": "Computación",   "descripcion": "Laptops, componentes y equipos de alto rendimiento", "activo": True},
    {"nombre": "Monitores",     "descripcion": "Monitores gamer y de productividad",                 "activo": True},
    {"nombre": "Periféricos",   "descripcion": "Teclados mecánicos, ratones y accesorios para PC",   "activo": True},
    {"nombre": "Audio",         "descripcion": "Auriculares y periféricos de sonido envolvente",     "activo": True},
    {"nombre": "Mobiliario",    "descripcion": "Sillas ergonómicas y escritorios gamer",             "activo": True},
    {"nombre": "Almacenamiento","descripcion": "SSDs y memorias de alta velocidad",                  "activo": True},
]

PRODUCTOS_INICIALES = [
    {"nombre": "Laptop Gamer Lenovo Legion",       "descripcion": "Intel Core i7, 16GB RAM, 512GB SSD, RTX 4060", "precio": 1399.99, "stock": 8,  "categoria_nombre": "Computación",    "activo": True},
    {"nombre": "Monitor Curvo Samsung 27\"",        "descripcion": "FHD 144Hz 1ms FreeSync",                       "precio": 249.50,  "stock": 15, "categoria_nombre": "Monitores",       "activo": True},
    {"nombre": "Teclado Mecánico Redragon Kumara", "descripcion": "Switches Outemu Blue, retroiluminación RGB",    "precio": 45.00,   "stock": 25, "categoria_nombre": "Periféricos",     "activo": True},
    {"nombre": "Mouse Logitech G502 HERO",         "descripcion": "Sensor HERO 25K, 11 botones programables",     "precio": 49.99,   "stock": 30, "categoria_nombre": "Periféricos",     "activo": True},
    {"nombre": "Auriculares HyperX Cloud II",      "descripcion": "Sonido envolvente 7.1 con micrófono desmontable","precio": 89.90, "stock": 12, "categoria_nombre": "Audio",           "activo": True},
    {"nombre": "Silla Gamer Ergonómica",           "descripcion": "Reclinable 180° con almohadillas lumbar",      "precio": 180.00,  "stock": 5,  "categoria_nombre": "Mobiliario",      "activo": True},
    {"nombre": "SSD NVMe 1TB Kingston",            "descripcion": "PCIe 4.0 hasta 3500MB/s de lectura",           "precio": 75.25,   "stock": 40, "categoria_nombre": "Almacenamiento",  "activo": True},
    {"nombre": "Webcam Logitech C920 Pro HD",      "descripcion": "Full HD 1080p con micrófono estéreo integrado","precio": 69.99,   "stock": 18, "categoria_nombre": "Periféricos",     "activo": True},
]


def seed_data():
    with Session(engine) as session:
        try:
            print("--- Poblando Categorías ---")
            cat_map = {}
            cat_insertadas = 0

            for cat_data in CATEGORIAS_INICIALES:
                existe = session.exec(
                    select(Categoria).where(Categoria.nombre == cat_data["nombre"])
                ).first()
                if not existe:
                    nueva_cat = Categoria(**cat_data)
                    session.add(nueva_cat)
                    session.commit()
                    session.refresh(nueva_cat)
                    cat_map[nueva_cat.nombre] = nueva_cat.id
                    cat_insertadas += 1
                else:
                    cat_map[existe.nombre] = existe.id

            print(f"Categorías insertadas: {cat_insertadas} (Total: {len(cat_map)})")

            print("\n--- Poblando Productos con Foreign Key ---")
            prod_insertados = 0
            for prod_data in PRODUCTOS_INICIALES:
                existe = session.exec(
                    select(Producto).where(Producto.nombre == prod_data["nombre"])
                ).first()
                if not existe:
                    nuevo_prod = Producto(
                        nombre=prod_data["nombre"],
                        descripcion=prod_data["descripcion"],
                        precio=prod_data["precio"],
                        stock=prod_data["stock"],
                        categoria_id=cat_map.get(prod_data["categoria_nombre"]),
                        activo=prod_data["activo"],
                    )
                    session.add(nuevo_prod)
                    prod_insertados += 1

            session.commit()
            print(f"Productos insertados: {prod_insertados}")

            print("\n--- Verificación de relaciones anidadas ---")
            categorias = session.exec(select(Categoria)).all()
            for cat in categorias:
                print(f"\n[Categoría ID {cat.id}] {cat.nombre}")
                for p in (cat.productos or []):
                    print(f"  └─ [Producto ID {p.id}] {p.nombre} | ${p.precio} | Stock: {p.stock}")

            print("\nBase de datos poblada exitosamente.")

        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            raise


if __name__ == "__main__":
    seed_data()
