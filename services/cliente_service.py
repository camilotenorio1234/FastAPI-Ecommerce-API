from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, timezone

from app.schemas.cliente_shemas import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
)


class ClienteService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db["clientes"]

    # Crear cliente
    async def crear_cliente(self, cliente_data: ClienteCreate) -> ClienteResponse:
        cliente = cliente_data.model_dump()
        cliente["fecha_registro"] = datetime.now(timezone.utc)
        cliente_id = await self.collection.insert_one(cliente)
        cliente["_id"] = str(cliente_id.inserted_id)
        return ClienteResponse(
            id=cliente["_id"],
            nombre_completo=cliente["nombre_completo"],
            email=cliente["email"],
            telefono=cliente.get("telefono"),
            direccion=cliente.get("direccion"),
            fecha_registro=cliente["fecha_registro"],
            estado_cuenta="activo",
            historial_compras=[],
            carrito_actual=[],
            deseos=[]
        )

    # Obtener cliente por ID
    async def obtener_cliente(self, cliente_id: str) -> ClienteResponse:
        cliente = await self.collection.find_one({"_id": ObjectId(cliente_id)})
        if cliente:
            # Transformar `_id` y asegurar que todos los campos requeridos estén presentes
            cliente["id"] = str(cliente.pop("_id"))
            cliente["estado_cuenta"] = cliente.get("estado_cuenta", "activo")
            cliente["historial_compras"] = cliente.get("historial_compras", [])
            cliente["carrito_actual"] = cliente.get("carrito_actual", [])
            cliente["deseos"] = cliente.get("deseos", [])
            return ClienteResponse.model_validate(cliente)
        return None

    # Listar todos los clientes
    async def listar_clientes(self) -> list[ClienteResponse]:
        clientes = await self.collection.find().to_list(100)
        for cliente in clientes:
            cliente["id"] = str(cliente.pop("_id"))
            cliente["estado_cuenta"] = cliente.get("estado_cuenta", "activo")
            cliente["historial_compras"] = cliente.get("historial_compras", [])
            cliente["carrito_actual"] = cliente.get("carrito_actual", [])
            cliente["deseos"] = cliente.get("deseos", [])
        return [ClienteResponse.model_validate(c) for c in clientes]

    # Actualizar cliente
    async def actualizar_cliente(self, cliente_id: str, cliente_data: ClienteUpdate) -> ClienteResponse:
        datos_actualizados = {
            **cliente_data.model_dump(exclude_unset=True),
            "ultima_actualizacion": datetime.now(timezone.utc)
        }
        result = await self.collection.update_one({"_id": ObjectId(cliente_id)}, {"$set": datos_actualizados})
        if result.modified_count:
            return await self.obtener_cliente(cliente_id)
        return None

    # Eliminar cliente
    async def eliminar_cliente(self, cliente_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(cliente_id)})
        return result.deleted_count > 0
