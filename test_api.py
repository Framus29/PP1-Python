import sys
from pathlib import Path

# Agregar src a sys.path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_modular_crud():
    print("Iniciando pruebas del CRUD modularizado...")

    # 1. Test Root
    res = client.get("/")
    assert res.status_code == 200, f"Error en GET /: {res.text}"
    print("✓ GET / OK")

    # 2. Test Saludo router
    res = client.get("/saludar/")
    assert res.status_code == 200, f"Error en GET /saludar/: {res.text}"
    print("✓ GET /saludar/ OK")

    # 3. Test Create Producto (POST /productos/)
    payload = {
        "nombre": "Gamepad Inalámbrico Bluetooth",
        "descripcion": "Compatible con PC y Consolas, batería recargable",
        "precio": 39.99,
        "stock": 20,
        "categoria": "Accesorios",
        "activo": True
    }
    res = client.post("/productos/", json=payload)
    assert res.status_code == 201, f"Error en POST /productos/: {res.text}"
    data = res.json()
    producto_id = data["id"]
    assert data["nombre"] == payload["nombre"]
    assert data["precio"] == payload["precio"]
    print(f"✓ POST /productos/ OK (Creado producto ID: {producto_id})")

    # 4. Test List Productos (GET /productos/)
    res = client.get("/productos/")
    assert res.status_code == 200, f"Error en GET /productos/: {res.text}"
    productos = res.json()
    assert len(productos) >= 1
    print(f"✓ GET /productos/ OK (Total: {len(productos)} productos)")

    # 5. Test Get By ID (GET /productos/{id})
    res = client.get(f"/productos/{producto_id}")
    assert res.status_code == 200, f"Error en GET /productos/{producto_id}: {res.text}"
    assert res.json()["id"] == producto_id
    print(f"✓ GET /productos/{producto_id} OK")

    # 6. Test Update (PUT /productos/{id})
    update_data = {
        "precio": 34.99,
        "stock": 25
    }
    res = client.put(f"/productos/{producto_id}", json=update_data)
    assert res.status_code == 200, f"Error en PUT /productos/{producto_id}: {res.text}"
    updated = res.json()
    assert updated["precio"] == 34.99
    assert updated["stock"] == 25
    assert updated["nombre"] == payload["nombre"]
    print(f"✓ PUT /productos/{producto_id} OK")

    # 7. Test Borrado Lógico (DELETE /productos/{id}?logico=true)
    res = client.delete(f"/productos/{producto_id}?logico=true")
    assert res.status_code == 200, f"Error en DELETE lógico: {res.text}"
    res_check = client.get(f"/productos/{producto_id}")
    assert res_check.json()["activo"] is False
    print(f"✓ DELETE /productos/{producto_id}?logico=true OK (Borrado lógico)")

    # 8. Test Borrado Físico (DELETE /productos/{id})
    res = client.delete(f"/productos/{producto_id}")
    assert res.status_code == 200, f"Error en DELETE físico: {res.text}"
    print(f"✓ DELETE /productos/{producto_id} OK (Borrado físico)")

    # 9. Verify 404
    res = client.get(f"/productos/{producto_id}")
    assert res.status_code == 404, f"Se esperaba 404 pero se obtuvo {res.status_code}"
    print(f"✓ GET /productos/{producto_id} devuelve 404 (eliminado)")

    print("\n¡Todas las pruebas del CRUD modularizado pasaron satisfactoriamente!")


if __name__ == "__main__":
    test_modular_crud()
