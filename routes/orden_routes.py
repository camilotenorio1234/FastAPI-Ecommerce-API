from fastapi import APIRouter, HTTPException, Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.orden_shemas import (
    OrdenCreate,
    OrdenUpdate,
    OrdenResponse,
)
from app.services.orden_service import OrdenService
from app.config import get_database



router = APIRouter()

# Dependencia para obtener la base de datos
def get_db() -> AsyncIOMotorDatabase:
    db = get_database()
    if db is None:
        raise RuntimeError("Database not initialized")
    return db


@router.post("/", response_model=OrdenResponse)
async def create_order(order: OrdenCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = OrdenService(db)
    return await service.crear_orden(order)


@router.get("/", response_model=List[OrdenResponse])
async def get_all_orders(db: AsyncIOMotorDatabase = Depends(get_db)):
    service = OrdenService(db)
    return await service.obtener_todas_ordenes()


@router.get("/{order_id}", response_model=OrdenResponse)
async def get_order(order_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = OrdenService(db)
    order = await service.obtener_orden(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order


@router.put("/{order_id}", response_model=OrdenResponse)
async def update_order(order_id: str, order_data: OrdenUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = OrdenService(db)
    updated_order = await service.actualizar_orden(order_id, order_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return updated_order


@router.delete("/{order_id}")
async def delete_order(order_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = OrdenService(db)
    result = await service.eliminar_orden(order_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return {"message": "Orden eliminada correctamente"}


@router.post("/{order_id}/procesar_pago")
async def process_payment(order_id: str, transaccion_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Ruta para procesar el pago de una orden.
    """
    service = OrdenService(db)
    updated_order = await service.procesar_pago(order_id, transaccion_id)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada o el procesamiento falló")
    return updated_order
