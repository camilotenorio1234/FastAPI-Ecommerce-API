from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class Direccion(BaseModel):
    calle: str
    ciudad: str
    departamento: str
    codigo_postal: str
    pais: str

class HistorialCompra(BaseModel):
    orden_id: str
    fecha: datetime
    total: float

class CarritoItem(BaseModel):
    producto_id: str
    cantidad: int
    precio: float

# Esquema base compartido por otros esquemas
class ClienteBase(BaseModel):
    nombre_completo: str
    email: EmailStr
    telefono: Optional[str]
    direccion: Optional[Direccion]

# Esquema para crear un cliente
class ClienteCreate(ClienteBase):
    contraseña: str  # Campo adicional requerido para la creación

# Esquema para actualizar un cliente
class ClienteUpdate(ClienteBase):
    nombre_completo: Optional[str]  # Los campos son opcionales al actualizar
    telefono: Optional[str]
    direccion: Optional[Direccion]

# Esquema para la respuesta de un cliente
class ClienteResponse(ClienteBase):
    id: str
    fecha_registro: datetime
    estado_cuenta: str
    historial_compras: List[HistorialCompra] = []
    carrito_actual: List[CarritoItem] = []
    deseos: List[str] = []

    class Config:
        from_attributes = True
