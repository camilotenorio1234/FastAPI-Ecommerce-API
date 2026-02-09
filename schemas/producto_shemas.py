from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Especificacion(BaseModel):
    clave: str
    valor: str


class Imagen(BaseModel):
    url: str  # Convertido a cadena
    es_principal: Optional[bool] = False


# Para solicitudes de creación de producto
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: List[str]
    marca: Optional[str] = None
    precio: float = Field(gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(ge=0, description="El stock no puede ser negativo")
    estado: Optional[str] = "activo"
    imagenes: Optional[List[Imagen]] = []
    especificaciones: Optional[List[Especificacion]] = []


# Para solicitudes de actualización de producto
class ProductoUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    categoria: Optional[List[str]]
    marca: Optional[str]
    precio: Optional[float]
    stock: Optional[int]
    estado: Optional[str]
    imagenes: Optional[List[Imagen]]
    especificaciones: Optional[List[Especificacion]]


# Para respuestas con todos los datos
class ProductoResponse(BaseModel):
    id: str = Field(alias="_id")
    nombre: str
    descripcion: Optional[str]
    categoria: List[str]
    marca: Optional[str]
    precio: float
    stock: int
    estado: str
    imagenes: Optional[List[Imagen]]
    especificaciones: Optional[List[Especificacion]]
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
