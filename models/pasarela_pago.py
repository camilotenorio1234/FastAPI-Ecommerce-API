from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone


class TransaccionModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    orden_id: str  # Relación con la orden
    cliente_id: str
    estado: str = "pendiente"  # pendiente, aprobado, rechazado
    metodo_pago: str  # tarjeta de crédito, PSE, etc.
    referencia_pago: Optional[str] = "SIN_REFERENCIA"  # Referencia generada por PayU
    transaccion_id: Optional[str] = "SIN_TRANSACCION"  # ID único generado por PayU
    monto: float
    moneda: str = "COP"  # Por defecto, pesos colombianos
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_actualizacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True  # Cambiado de allow_population_by_field_name
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
