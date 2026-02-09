from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.pasarela_pago_shemas import (
    TransaccionCreate,
    TransaccionUpdate,
    TransaccionResponse,
)
from app.services.pasarela_pago_service import TransaccionService
from app.config import get_database



router = APIRouter()

# Dependencia para obtener la base de datos
def get_db() -> AsyncIOMotorDatabase:
    db = get_database()
    if db is None:
        raise RuntimeError("Database not initialized")
    return db



@router.post("/", response_model=TransaccionResponse)
async def create_transaction(transaccion: TransaccionCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Crear una nueva transacción.
    """
    service = TransaccionService(db)
    return await service.crear_transaccion(transaccion)


@router.post("/notificacion")
async def notificacion_pagos(notificacion: dict, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Ruta para recibir notificaciones (webhooks) de la pasarela de pagos.
    """
    service = TransaccionService(db)

    referencia_pago = notificacion.get("reference_sale")
    estado = notificacion.get("state_pol")
    transaccion_id = notificacion.get("transaction_id")

    # Mapear el estado recibido al interno
    estado_mapeado = "aprobado" if estado == "APPROVED" else "rechazado"
    transaccion = await service.actualizar_transaccion(
        transaccion_id=referencia_pago,
        transaccion_data=TransaccionUpdate(
            estado=estado_mapeado,
            transaccion_id=transaccion_id,
        ),
    )

    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    # Aquí podrías también procesar la orden correspondiente.
    return {"message": "Notificación procesada correctamente"}


@router.get("/{transaccion_id}", response_model=TransaccionResponse)
async def get_transaction(transaccion_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Obtener una transacción por su ID.
    """
    service = TransaccionService(db)
    transaccion = await service.obtener_transaccion(transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


@router.put("/{transaccion_id}", response_model=TransaccionResponse)
async def update_transaction(transaccion_id: str, transaccion_data: TransaccionUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Actualizar una transacción existente.
    """
    service = TransaccionService(db)
    transaccion_actualizada = await service.actualizar_transaccion(transaccion_id, transaccion_data)
    if not transaccion_actualizada:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion_actualizada
