# MODELO:
# Clases que representan TABLAS reales en la DB
# controladas por SQLAlchemy (Base o Declarative Base)
from database import Base
from sqlalchemy import Boolean, Column, Float, Integer, String


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    descripcion = Column(String(255), nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    categoria = Column(String(50), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
