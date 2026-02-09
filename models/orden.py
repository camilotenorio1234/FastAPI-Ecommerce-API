from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, timezone
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


class ProductoOrdenModel(BaseModel):
    producto_id: str
    nombre_producto: Optional[str] = None  # Opcional para evitar búsquedas adicionales
    cantidad: int
    precio_unitario: float
    subtotal: float


class DireccionEnvioModel(BaseModel):
    calle: str
    ciudad: str
    departamento: str
    codigo_postal: str
    pais: str
    telefono: Optional[str] = None  # Agregado para logística
    instrucciones_adicionales: Optional[str] = None  # Instrucciones opcionales


class OrdenModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    cliente_id: str
    fecha_pedido: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    estado: EstadoOrden = EstadoOrden.pendiente  # Enum para estados de la orden
    productos: List[ProductoOrdenModel]
    total: float
    direccion_envio: DireccionEnvioModel
    metodo_envio: Optional[str] = None
    tracking_number: Optional[str] = None  # Puede tener validaciones de formato
    metodo_pago: MetodoPago  # Enum para métodos de pago
    estado_pago: EstadoPago = EstadoPago.pendiente  # Enum para estados de pago
    transaccion_id: Optional[str] = None
    notas: Optional[str] = None  # Notas adicionales para la orden

    class Config:
        populate_by_name = True  # Cambiado de allow_population_by_field_name
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
