from fastapi import APIRouter, HTTPException, Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.producto_shemas import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
)
from app.services.producto_service import ProductoService
from app.config import get_database



router = APIRouter()

# Dependencia para obtener la base de datos
def get_db() -> AsyncIOMotorDatabase:
    db = get_database()
    if db is None:
        raise RuntimeError("Database not initialized")
    return db

@router.post("/", response_model=ProductoResponse)
async def create_producto(producto: ProductoCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ProductoService(db)
    return await service.crear_producto(producto)

@router.get("/", response_model=List[ProductoResponse])
async def get_all_productos(db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ProductoService(db)
    return await service.obtener_todos_productos()

@router.get("/{producto_id}", response_model=ProductoResponse)
async def get_producto(producto_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ProductoService(db)
    producto = await service.obtener_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoResponse)
async def update_producto(producto_id: str, producto_data: ProductoUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ProductoService(db)
    producto_actualizado = await service.actualizar_producto(producto_id, producto_data)
    if producto_actualizado is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto_actualizado

@router.delete("/{producto_id}")
async def delete_producto(producto_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ProductoService(db)
    result = await service.eliminar_producto(producto_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}
