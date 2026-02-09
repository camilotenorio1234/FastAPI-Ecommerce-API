from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.cliente_shemas import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
)
from app.services.cliente_service import ClienteService
from app.config import get_database



router = APIRouter()

# Dependencia para obtener la base de datos
def get_db() -> AsyncIOMotorDatabase:
    db = get_database()
    if db is None:
        raise RuntimeError("Database not initialized")
    return db


# Crear cliente
@router.post("/", response_model=ClienteResponse)
async def create_cliente(cliente: ClienteCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ClienteService(db)
    return await service.crear_cliente(cliente)

# Obtener cliente por ID
@router.get("/{cliente_id}", response_model=ClienteResponse)
async def get_cliente(cliente_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ClienteService(db)
    cliente = await service.obtener_cliente(cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# Listar todos los clientes
@router.get("/", response_model=list[ClienteResponse])
async def get_all_clientes(db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ClienteService(db)
    return await service.listar_clientes()

# Actualizar cliente
@router.put("/{cliente_id}", response_model=ClienteResponse)
async def update_cliente(cliente_id: str, cliente_data: ClienteUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ClienteService(db)
    cliente_actualizado = await service.actualizar_cliente(cliente_id, cliente_data)
    if cliente_actualizado is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente_actualizado

# Eliminar cliente
@router.delete("/{cliente_id}", response_model=dict)
async def delete_cliente(cliente_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = ClienteService(db)
    eliminado = await service.eliminar_cliente(cliente_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado correctamente"}
