from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.admin_shemas import AdminCreate, AdminUpdate
from app.services.admin_service import AdminService
from app.config import get_database



router = APIRouter()

# Dependencia para obtener la base de datos
def get_db() -> AsyncIOMotorDatabase:
    db = get_database()
    if db is None:
        raise RuntimeError("Database not initialized")
    return db


@router.post("/", response_model=dict)
async def create_admin(admin: AdminCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = AdminService(db)
    return await service.crear_admin(admin)

@router.get("/{admin_id}", response_model=dict)
async def get_admin(admin_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = AdminService(db)
    admin = await service.obtener_admin(admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin no encontrado")
    return admin

@router.put("/{admin_id}", response_model=dict)
async def update_admin(admin_id: str, admin_data: AdminUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = AdminService(db)
    admin_actualizado = await service.actualizar_admin(admin_id, admin_data)
    if admin_actualizado is None:
        raise HTTPException(status_code=404, detail="Admin no encontrado")
    return admin_actualizado

@router.delete("/{admin_id}")
async def delete_admin(admin_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = AdminService(db)
    result = await service.eliminar_admin(admin_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Admin no encontrado")
    return {"message": "Admin eliminado correctamente"}
