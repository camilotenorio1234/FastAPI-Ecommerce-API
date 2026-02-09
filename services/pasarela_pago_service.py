from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException
from datetime import datetime, timezone

from app.schemas.pasarela_pago_shemas import (
    TransaccionCreate,
    TransaccionUpdate,
    TransaccionResponse,
)



class TransaccionService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db["transacciones"]

    async def crear_transaccion(self, transaccion_data: TransaccionCreate) -> TransaccionResponse:
        """
        Crear una nueva transacción.
        """
        transaccion = transaccion_data.model_dump()
        transaccion["estado"] = "pendiente"
        transaccion["fecha_creacion"] = datetime.now(timezone.utc)
        transaccion["fecha_actualizacion"] = datetime.now(timezone.utc)
        # Si no se pasan valores, asignar valores por defecto
        transaccion["referencia_pago"] = transaccion.get("referencia_pago", "SIN_REFERENCIA")
        transaccion["transaccion_id"] = transaccion.get("transaccion_id", "SIN_TRANSACCION")

        try:
            # Insertar la transacción en la base de datos
            result = await self.collection.insert_one(transaccion)
            # Asignar el ID generado por MongoDB
            transaccion["_id"] = str(result.inserted_id)
            transaccion["id"] = transaccion["_id"]  # Mapear _id a id
            return TransaccionResponse.model_validate(transaccion)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear la transacción: {e}")

    async def obtener_transaccion(self, transaccion_id: str) -> TransaccionResponse:
        """
        Obtener una transacción por su ID.
        """
        try:
            transaccion = await self.collection.find_one({"_id": ObjectId(transaccion_id)})
            if transaccion:
                transaccion["_id"] = str(transaccion["_id"])
                transaccion["id"] = transaccion["_id"]  # Mapear _id a id
                return TransaccionResponse.model_validate(transaccion)
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener la transacción: {e}")

    async def actualizar_transaccion(self, transaccion_id: str, transaccion_data: TransaccionUpdate) -> TransaccionResponse:
        """
        Actualizar una transacción existente.
        """
        datos_actualizados = {
            **transaccion_data.model_dump(exclude_unset=True),
            "fecha_actualizacion": datetime.now(timezone.utc),
        }

        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(transaccion_id)}, {"$set": datos_actualizados}
            )
            if result.modified_count > 0:
                return await self.obtener_transaccion(transaccion_id)
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar la transacción: {e}")
