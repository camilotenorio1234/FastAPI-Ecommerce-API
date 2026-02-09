from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class EstadoOrden(str, Enum):
    pendiente = "pendiente"
    en_proceso = "en proceso"
    enviado = "enviado"
    entregado = "entregado"
    cancelado = "cancelado"

class EstadoPago(str, Enum):
    pendiente = "pendiente"
    pagado = "pagado"
    reembolsado = "reembolsado"

class MetodoPago(str, Enum):
    tarjeta_credito = "tarjeta de crédito"
    transferencia = "transferencia"
    pse = "PSE"
    efectivo = "efectivo"

class ProductoOrden(BaseModel):
    producto_id: str
    nombre_producto: Optional[str] = None
    cantidad: int
    precio_unitario: float
    subtotal: float

class DireccionEnvio(BaseModel):
    calle: str
    ciudad: str
    departamento: str
    codigo_postal: str
    pais: str
    telefono: Optional[str] = None
    instrucciones_adicionales: Optional[str] = None

class OrdenCreate(BaseModel):
    cliente_id: str
    productos: List[ProductoOrden]
    total: float
    direccion_envio: DireccionEnvio
    metodo_envio: Optional[str] = None
    metodo_pago: MetodoPago
    notas: Optional[str] = None

class OrdenUpdate(BaseModel):
    estado: Optional[EstadoOrden]
    estado_pago: Optional[EstadoPago]
    tracking_number: Optional[str]
    notas: Optional[str]

class OrdenResponse(OrdenCreate):
    id: str = Field(alias="_id")
    fecha_pedido: datetime
    estado: EstadoOrden
    estado_pago: EstadoPago
    transaccion_id: Optional[str] = None

    class Config:
        from_attributes = True  # Cambiado de orm_mode
