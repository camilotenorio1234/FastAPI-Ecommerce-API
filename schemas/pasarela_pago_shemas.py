from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransaccionCreate(BaseModel):
    orden_id: str
    cliente_id: str
    metodo_pago: str
    monto: float
    moneda: str = "COP"

class TransaccionUpdate(BaseModel):
    estado: Optional[str]
    referencia_pago: Optional[str]
    transaccion_id: Optional[str]
    fecha_actualizacion: Optional[datetime]

class TransaccionResponse(BaseModel):
    id: str
    orden_id: str
    cliente_id: str
    estado: str
    metodo_pago: str
    referencia_pago: Optional[str]
    transaccion_id: Optional[str]
    monto: float
    moneda: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True  # Cambiado de orm_mode
