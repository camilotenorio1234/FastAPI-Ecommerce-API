from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, timezone

from app.schemas.producto_shemas import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
)


class ProductoService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db["productos"]

    # Crear producto
    async def crear_producto(self, producto_data: ProductoCreate) -> ProductoResponse:
        producto = producto_data.model_dump()
        # Convertimos las URLs a cadenas
        if producto.get("imagenes"):
            producto["imagenes"] = [{"url": str(imagen["url"]), "es_principal": imagen["es_principal"]} for imagen in producto["imagenes"]]
        producto["fecha_creacion"] = datetime.now(timezone.utc)
        producto["fecha_actualizacion"] = datetime.now(timezone.utc)
        producto_id = await self.collection.insert_one(producto)
        producto["_id"] = str(producto_id.inserted_id)
        return ProductoResponse.model_validate(producto)

    # Obtener producto por ID
    async def obtener_producto(self, producto_id: str) -> ProductoResponse:
        producto = await self.collection.find_one({"_id": ObjectId(producto_id)})
        if producto:
            producto["_id"] = str(producto["_id"])
            return ProductoResponse.model_validate(producto)
        return None

    # Listar todos los productos
    async def obtener_todos_productos(self) -> list[ProductoResponse]:
        productos = await self.collection.find().to_list(100)
        for producto in productos:
            producto["_id"] = str(producto["_id"])
        return [ProductoResponse.model_validate(p) for p in productos]

    # Actualizar producto
    async def actualizar_producto(self, producto_id: str, producto_data: ProductoUpdate) -> ProductoResponse:
        datos_actualizados = {
            **producto_data.model_dump(exclude_unset=True),
            "fecha_actualizacion": datetime.now(timezone.utc)
        }
        result = await self.collection.update_one({"_id": ObjectId(producto_id)}, {"$set": datos_actualizados})
        if result.modified_count:
            return await self.obtener_producto(producto_id)
        return None

    # Eliminar producto
    async def eliminar_producto(self, producto_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(producto_id)})
        return result.deleted_count > 0
