import sys
import uuid
from pathlib import Path

# Evita errores de encoding en consolas Windows (cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_api_completa():
    print("Iniciando pruebas de FastAPI con SQLModel, Alembic, paginación y auth...\n")

    # 1. Root
    res = client.get("/")
    assert res.status_code == 200
    print("✓ GET / OK")

    # 2. Saludo
    res = client.get("/saludar/")
    assert res.status_code == 200
    print("✓ GET /saludar/ OK")

    # 3. Registro de usuario (contraseña hasheada con bcrypt)
    email = f"tester_{uuid.uuid4().hex[:8]}@mail.com"
    res = client.post(
        "/auth/register",
        json={"nombre": "Tester", "email": email, "contraseña": "secreto123"},
    )
    assert res.status_code == 200, res.text
    assert res.json()["email"] == email
    assert "contraseña" not in res.json()
    print(f"✓ POST /auth/register OK (usuario: {email})")

    # 4. Email duplicado -> 400
    res = client.post(
        "/auth/register",
        json={"nombre": "Tester", "email": email, "contraseña": "secreto123"},
    )
    assert res.status_code == 400
    print("✓ POST /auth/register email duplicado -> 400 OK")

    # 5. Login correcto e incorrecto
    res = client.post(
        "/auth/login", json={"email": email, "contraseña": "secreto123"}
    )
    assert res.status_code == 200
    assert res.json()["coincide"] is True
    print("✓ POST /auth/login OK")

    res = client.post(
        "/auth/login", json={"email": email, "contraseña": "incorrecta"}
    )
    assert res.status_code == 401
    print("✓ POST /auth/login credenciales inválidas -> 401 OK")

    # 6. Crear Categoría
    res = client.post(
        "/categorias/",
        json={
            "nombre": "Consolas",
            "descripcion": "Consolas de nueva generación",
            "activo": True,
        },
    )
    assert res.status_code == 200, res.text
    cat = res.json()
    cat_id = cat["id"]
    assert cat["nombre"] == "Consolas"
    print(f"✓ POST /categorias/ OK (ID: {cat_id})")

    # 7. Listar Categorías (paginado)
    res = client.get("/categorias/")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data and "total" in data
    assert data["total"] >= 1
    print(f"✓ GET /categorias/ paginado OK (Total: {data['total']})")

    # 8. Crear Producto con FK a Categoría
    res = client.post(
        "/productos/",
        json={
            "nombre": "PlayStation 5 Slim",
            "descripcion": "Consola Sony con DualSense",
            "precio": 549.99,
            "stock": 10,
            "categoria_id": cat_id,
            "activo": True,
        },
    )
    assert res.status_code == 200, res.text
    prod = res.json()
    prod_id = prod["id"]
    assert prod["categoria"]["id"] == cat_id
    print(f"✓ POST /productos/ OK (ID: {prod_id}, FK categoria_id: {cat_id})")

    # 9. Listar Productos (paginado, con categoría anidada)
    res = client.get("/productos/")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data and "total" in data
    print(f"✓ GET /productos/ paginado OK (Total: {data['total']})")

    # 10. GET Producto con ProductoNested
    res = client.get(f"/productos/{prod_id}")
    assert res.status_code == 200
    assert res.json()["categoria"]["nombre"] == "Consolas"
    print(f"✓ GET /productos/{prod_id} con ProductoNested OK")

    # 11. GET Categoría con CategoriaNested (lista de productos)
    res = client.get(f"/categorias/{cat_id}")
    assert res.status_code == 200
    assert len(res.json()["productos"]) >= 1
    print(f"✓ GET /categorias/{cat_id} con CategoriaNested OK")

    # 12. PUT Producto
    res = client.put(
        f"/productos/{prod_id}",
        json={
            "nombre": "PlayStation 5 Slim",
            "precio": 499.99,
            "stock": 14,
            "activo": True,
        },
    )
    assert res.status_code == 200
    assert res.json()["precio"] == 499.99
    print(f"✓ PUT /productos/{prod_id} OK")

    # 13. Borrado lógico Producto
    res = client.delete(f"/productos/{prod_id}?logico=true")
    assert res.status_code == 200
    assert client.get(f"/productos/{prod_id}").json()["activo"] is False
    print(f"✓ DELETE /productos/{prod_id}?logico=true OK")

    # 14. Borrado físico Producto
    res = client.delete(f"/productos/{prod_id}")
    assert res.status_code == 200
    assert client.get(f"/productos/{prod_id}").status_code == 404
    print(f"✓ DELETE /productos/{prod_id} OK (verificado 404)")

    # 15. PUT y DELETE Categoría
    res = client.put(
        f"/categorias/{cat_id}",
        json={"nombre": "Consolas", "descripcion": "Actualizado", "activo": True},
    )
    assert res.status_code == 200
    print(f"✓ PUT /categorias/{cat_id} OK")

    res = client.delete(f"/categorias/{cat_id}")
    assert res.status_code == 200
    assert client.get(f"/categorias/{cat_id}").status_code == 404
    print(f"✓ DELETE /categorias/{cat_id} OK (verificado 404)")

    print("\n¡Todas las pruebas pasaron satisfactoriamente! (100% OK)")


if __name__ == "__main__":
    test_api_completa()
