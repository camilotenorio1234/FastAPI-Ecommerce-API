from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from enum import Enum


class EstadoProducto(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    AGOTADO = "agotado"


class EspecificacionModel(BaseModel):
    clave: str
    valor: str


class ProductoModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nombre: str
    descripcion: Optional[str] = None
    categoria: List[str]  # Lista jerárquica, ej. ["Electrónica", "Smartphones"]
    marca: Optional[str] = None
    precio: float = Field(gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(ge=0, description="El stock no puede ser negativo")
    estado: EstadoProducto = EstadoProducto.ACTIVO
    imagenes: Optional[List[str]] = []  # Convertido a lista de cadenas
    calificaciones: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)
    total_calificaciones: Optional[int] = 0  # Número de personas que calificaron
    especificaciones: Optional[List[EspecificacionModel]] = []
    deseos_count: Optional[int] = Field(default=0, ge=0)
    ventas_count: Optional[int] = Field(default=0, ge=0)
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_actualizacion: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
