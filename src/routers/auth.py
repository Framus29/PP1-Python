from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from core.auth import get_password_hash, verify_password
from database import get_db
from models.usuarios import Usuario, UsuarioCreate, UsuarioLogin, UsuarioPublic

auth_routers = APIRouter()


@auth_routers.post(
    "/register",
    response_model=UsuarioPublic,
    status_code=status.HTTP_201_CREATED,
)  # REGISTER: CREACIÓN DE MODELO USUARIO
async def register(usuario_nuevo: UsuarioCreate, db: Session = Depends(get_db)):
    # El email es UNIQUE: validamos antes para devolver un 400 claro.
    existe = db.exec(
        select(Usuario).where(Usuario.email == usuario_nuevo.email)
    ).first()
    if existe is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese email",
        )

    usuario_db = Usuario.model_validate(usuario_nuevo)

    # Lógica de encriptación (hasheo) de contraseña
    usuario_db.contraseña = get_password_hash(usuario_nuevo.contraseña)

    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db


@auth_routers.post("/login")
async def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    query = select(Usuario).where(Usuario.email == usuario.email)
    usuario_db = db.exec(query).first()

    if usuario_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    resultado = verify_password(usuario.contraseña, usuario_db.contraseña)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    # Idealmente, si coincide, generar y devolver el JWT Token (contexto de login)
    return {"coincide": resultado, "usuario": usuario_db.email}
