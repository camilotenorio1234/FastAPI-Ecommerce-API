from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class RegistroActividad(BaseModel):
    accion: str
    fecha: datetime = Field(default_factory=datetime.now)
    detalle: Optional[str] = None

class AdminBase(BaseModel):
    nombre_completo: str
    email: EmailStr
    rol: Optional[str] = "administrador"  # administrador, editor, supervisor
    permisos: Optional[List[str]] = []

class AdminCreate(AdminBase):
    contraseña: str

class AdminUpdate(AdminBase):
    nombre_completo: Optional[str]
    email: Optional[EmailStr]
    permisos: Optional[List[str]]

class AdminResponse(AdminBase):
    id: str
    registro_actividades: Optional[List[RegistroActividad]] = []
    alertas: Optional[List[str]] = []

    class Config:
        from_attributes = True  # Cambiado de orm_mode
