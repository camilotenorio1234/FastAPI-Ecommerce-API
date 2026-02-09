from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, timezone


# Modelo para la dirección
class DireccionModel(BaseModel):
    calle: str
    ciudad: str
    departamento: str
    codigo_postal: str
    pais: str


# Modelo para el historial de compras
class HistorialCompraModel(BaseModel):
    orden_id: str
    fecha: datetime
    total: float


# Modelo para un ítem en el carrito
class CarritoItemModel(BaseModel):
    producto_id: str
    cantidad: int
    precio: float


# Modelo principal del cliente
class ClienteModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    nombre_completo: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[DireccionModel] = None
    contraseña_hash: str
    fecha_registro: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    estado_cuenta: str = "activo"  # Estados: activo, inactivo, suspendido
    historial_compras: Optional[List[HistorialCompraModel]] = []
    carrito_actual: Optional[List[CarritoItemModel]] = []
    deseos: Optional[List[str]] = []

    class Config:
        populate_by_name = True  # Cambiado de allow_population_by_field_name
        from_attributes = True  # Cambiado de orm_mode
        json_encoders = {ObjectId: str}
