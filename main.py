from typing import Annotated

from fastapi import FastAPI, Body, Path, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()


app.title = "Mi primera API"


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",  # entorno desarrollo
        "https://Framus29.github.io/front",  # entorno producción
        # "*", wildcard ! Cualquier origen
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


NOT_FOUND_RESPONSE = {
    404: {"description": "Response not found si no se encuentra el id",
          "content": {
              "aplication/json": {
                  "example": {
                      "detail": "Articulo no encontrado"
                }
            }
        },
    },
}


IntPositivo = Annotated[int, Field(gt=0)]
StrCortito = Annotated[str, Field(max_length=30)]
IntPrecioVenta = Annotated[int, Field(gt=5000, lt=9999999)]
boolActivo = Annotated[bool, Field(description="Sigue disponible?")]


class ComponenteSchema(BaseModel):
    id: Annotated[int, Field(gt=0, description="ID del articulo", deprecated=True)]
    nombre: StrCortito
    precio: IntPrecioVenta = 15000
    activo: boolActivo = True


class ComponenteUpdateSchema(BaseModel):
    nombre: StrCortito
    precio: IntPrecioVenta = 20000
    activo: boolActivo = True

componentes_Pc = [
    {"id":1, "nombre":"Procesador Amd ryzen 5 9600x", "precio":400000, "activo":True},
    {"id":2, "nombre":"Mother Asus b840m Wifi Pro", "precio": 230000, "activo":True},
    {"id":3, "nombre":"NVIDIA GeForce RTX 5060Ti 16gb", "precio":995000, "activo":True},
    {"id":4, "nombre":"TEAMGROUP MP44Q M.2 SSD 2tb", "precio":193000, "activo":True},
    {"id":5, "nombre":"Memoria Ram kingstom 16gb 6000mhz", "precio":280000, "activo":True}
]


@app.get("/componentes_Pc", response_model=list[ComponenteSchema])
async def buscar_por_Nombre(
    nombre: StrCortito
):
    for componente in componentes_Pc:
        if componente["nombre"] == nombre:
            return componente
        return {"Detalle": "no se encontro"}
    return componentes_Pc


@app.get("/componentes_Pc/{id}",
         responses=NOT_FOUND_RESPONSE,
         response_model=ComponenteSchema,
)
async def Buscar_por_ID(
    id: Annotated[int, Path(gt=0)]
):
    for componente in componentes_Pc:
        if componente["id"] == id:
            return componente
        raise HTTPException(status_code=404, detail="Artiiculo no encontrado")


@app.post("/componentes_Pc",response_model=[ComponenteSchema])
async def Crear_Componente(componente_nuevo: ComponenteSchema):
    componentes_Pc.append(componente_nuevo.model_dump())
    return componentes_Pc


@app.delete("/componentes_Pc/{id}", responses=NOT_FOUND_RESPONSE, response_model=[ComponenteSchema])
async def Borrar_Componente(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[bool, Query(description="Mantener registro?")] = False
) -> ComponenteSchema:
    for componente in componentes_Pc:
        if componente["id"] == id:
            if logico:
                componente["activo"]=False
            else:
                componentes_Pc.remove(componente)
            return {"detalle":"Borrado Completamente"}
        raise HTTPException(status_code=404, detail="Articulo no encontrado")


@app.put("/componentes_Pc/{id}", responses=NOT_FOUND_RESPONSE, response_model=ComponenteSchema)
async def Editar_Componente(
    id: Annotated[int, Path(gt=0, description="ID del producto. >0")],
    nombre: Annotated[str, Body(max_length=50)],
    precio: Annotated[float, Body(ge=50000)]
):

    for componente in componentes_Pc:
        if componente["id"] == id:
            componente["nombre"] = nombre
            componente["precio"] = precio
            return componente
    raise HTTPException(status_code=404, detail="Articulo no encontrado")