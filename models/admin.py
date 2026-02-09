from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

class RegistroActividadModel(BaseModel):
    accion: str
    fecha: datetime = Field(default_factory=datetime.now)
    detalle: Optional[str] = None

class AdminModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nombre_completo: str
    email: EmailStr
    contraseña_hash: str
    rol: str = "administrador"  # administrador, editor, supervisor
    permisos: Optional[List[str]] = []  # Ejemplo: ["gestión_productos", "gestión_usuarios", "reportes"]
    registro_actividades: Optional[List[RegistroActividadModel]] = []
    alertas: Optional[List[str]] = []

    class Config:
        populate_by_name = True  # Cambiado de allow_population_by_field_name
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
