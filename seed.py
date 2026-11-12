import sys
from pathlib import Path

# Agregar src a sys.path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from database import engine, SessionLocal, Base
from models.productos import Producto

# Asegurar que las tablas existan
Base.metadata.create_all(bind=engine)

PRODUCTOS_INICIALES = [
    {
        "nombre": "Laptop Gamer Lenovo Legion",
        "descripcion": "Intel Core i7, 16GB RAM, 512GB SSD, RTX 4060",
        "precio": 1399.99,
        "stock": 8,
        "categoria": "Computación",
        "activo": True
    },
    {
        "nombre": "Monitor Curvo Samsung 27\"",
        "descripcion": "FHD 144Hz 1ms FreeSync",
        "precio": 249.50,
        "stock": 15,
        "categoria": "Monitores",
        "activo": True
    },
    {
        "nombre": "Teclado Mecánico Redragon Kumara",
        "descripcion": "Switches Outemu Blue, retroiluminación RGB",
        "precio": 45.00,
        "stock": 25,
        "categoria": "Periféricos",
        "activo": True
    },
    {
        "nombre": "Mouse Logitech G502 HERO",
        "descripcion": "Sensor HERO 25K, 11 botones programables",
        "precio": 49.99,
        "stock": 30,
        "categoria": "Periféricos",
        "activo": True
    },
    {
        "nombre": "Auriculares HyperX Cloud II",
        "descripcion": "Sonido envolvente 7.1 con micrófono desmontable",
        "precio": 89.90,
        "stock": 12,
        "categoria": "Audio",
        "activo": True
    },
    {
        "nombre": "Silla Gamer Ergonómica",
        "descripcion": "Reclinable 180° con almohadillas lumbar y cervical",
        "precio": 180.00,
        "stock": 5,
        "categoria": "Mobiliario",
        "activo": True
    },
    {
        "nombre": "Disco Solido SSD NVMe 1TB Kingston",
        "descripcion": "PCIe 4.0 velocidades de lectura hasta 3500MB/s",
        "precio": 75.25,
        "stock": 40,
        "categoria": "Almacenamiento",
        "activo": True
    },
    {
        "nombre": "Webcam Logitech C920 Pro HD",
        "descripcion": "Resolución Full HD 1080p con micrófono estéreo integrado",
        "precio": 69.99,
        "stock": 18,
        "categoria": "Video",
        "activo": True
    }
]


def seed_data():
    db = SessionLocal()
    try:
        count_existentes = db.query(Producto).count()
        print(f"Productos existentes en base_de_datos.db: {count_existentes}")

        insertados = 0
        for item in PRODUCTOS_INICIALES:
            existe = db.query(Producto).filter(Producto.nombre == item["nombre"]).first()
            if not existe:
                nuevo_prod = Producto(**item)
                db.add(nuevo_prod)
                insertados += 1

        db.commit()
        print(f"Se insertaron con éxito {insertados} nuevos productos en la base de datos.")

        print("\n--- Listado actual de base_de_datos.db ---")
        productos = db.query(Producto).all()
        for p in productos:
            print(f"ID {p.id}: {p.nombre} | ${p.precio} | Stock: {p.stock} | Cat: {p.categoria} | Activo: {p.activo}")

    except Exception as e:
        db.rollback()
        print(f"Error al poblar la base de datos: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
