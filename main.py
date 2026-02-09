from fastapi import FastAPI
from app.routes import (
    cliente_routes,
    admin_routes,
    producto_routes,
    orden_routes,
    pasarela_pago_routes,
)
from app.config import connect_to_mongo, close_mongo_connection
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Rutas
app.include_router(cliente_routes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(admin_routes.router, prefix="/admins", tags=["Admins"])
app.include_router(producto_routes.router, prefix="/productos", tags=["Productos"])
app.include_router(orden_routes.router, prefix="/ordenes", tags=["Órdenes"])
app.include_router(pasarela_pago_routes.router, prefix="/pagos", tags=["Pasarela de Pagos"])

@app.on_event("startup")
async def startup():
    connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    close_mongo_connection()
