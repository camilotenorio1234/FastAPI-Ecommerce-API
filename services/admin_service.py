from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.admin import AdminModel
from app.schemas.admin_shemas import AdminCreate, AdminUpdate

class AdminService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db["admins"]

    async def crear_admin(self, admin_data: AdminCreate):
        # Usamos model_dump() en lugar de dict()
        admin = admin_data.model_dump()
        admin["contraseña_hash"] = admin["contraseña"]  # Aquí iría el hash real
        del admin["contraseña"]  # Eliminamos la contraseña original
        admin_id = await self.collection.insert_one(admin)
        admin["_id"] = str(admin_id.inserted_id)
        return admin

    async def obtener_admin(self, admin_id: str):
        admin = await self.collection.find_one({"_id": ObjectId(admin_id)})
        if admin:
            admin["_id"] = str(admin["_id"])
        return admin

    async def actualizar_admin(self, admin_id: str, admin_data: AdminUpdate):
        # Usamos model_dump() para extraer los datos del esquema
        datos_actualizados = {
            k: v for k, v in admin_data.model_dump(exclude_unset=True).items() if v is not None
        }
        result = await self.collection.update_one(
            {"_id": ObjectId(admin_id)}, {"$set": datos_actualizados}
        )
        if result.modified_count:
            return await self.obtener_admin(admin_id)
        return None

    async def eliminar_admin(self, admin_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(admin_id)})
        return result.deleted_count
