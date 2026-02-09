from bson import ObjectId
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.orden_shemas import OrdenCreate, OrdenUpdate



class OrdenService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db["ordenes"]
        self.productos_collection = self.db["productos"]  # Referencia a la colección de productos

    async def crear_orden(self, orden_data: OrdenCreate):
        orden = orden_data.model_dump()
        orden["fecha_pedido"] = datetime.now(timezone.utc)
        orden["estado"] = "pendiente"
        orden["estado_pago"] = "pendiente"
        orden_id = await self.collection.insert_one(orden)
        orden["_id"] = str(orden_id.inserted_id)
        return orden

    async def obtener_todas_ordenes(self):
        ordenes = await self.collection.find().to_list(100)
        for orden in ordenes:
            orden["_id"] = str(orden["_id"])
        return ordenes

    async def obtener_orden(self, orden_id: str):
        orden = await self.collection.find_one({"_id": ObjectId(orden_id)})
        if orden:
            orden["_id"] = str(orden["_id"])
        return orden

    async def actualizar_orden(self, orden_id: str, orden_data: OrdenUpdate):
        datos_actualizados = {
            **orden_data.model_dump(exclude_unset=True),
            "ultima_actualizacion": datetime.now(timezone.utc)
        }
        result = await self.collection.update_one(
            {"_id": ObjectId(orden_id)}, {"$set": datos_actualizados}
        )
        if result.modified_count > 0:
            return await self.obtener_orden(orden_id)
        return None

    async def procesar_pago(self, orden_id: str, transaccion_id: str):
        # Obtener la orden
        orden = await self.obtener_orden(orden_id)
        if not orden:
            return None
        
        # Actualizar estado de pago y orden
        orden["estado_pago"] = "pagado"
        orden["estado"] = "en proceso"
        orden["transaccion_id"] = transaccion_id

        # Actualizar stock de los productos
        for producto in orden["productos"]:
            producto_id = producto["producto_id"]
            cantidad = producto["cantidad"]
            await self.productos_collection.update_one(
                {"_id": ObjectId(producto_id)},
                {"$inc": {"stock": -cantidad}}
            )

        # Guardar cambios en la orden
        await self.collection.update_one(
            {"_id": ObjectId(orden_id)},
            {"$set": {
                "estado_pago": orden["estado_pago"],
                "estado": orden["estado"],
                "transaccion_id": transaccion_id,
                "ultima_actualizacion": datetime.now(timezone.utc)
            }}
        )
        return await self.obtener_orden(orden_id)

    async def eliminar_orden(self, orden_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(orden_id)})
        return result.deleted_count
