# app/main.py
from fastapi import FastAPI
from app.routes import evento_routes, participante_routes

# Importar los routers de eventos y participantes
#FastAPI interfaz tiitulo y descripcion 
app = FastAPI(
    title="API de Gestión de Eventos y Participantes",
    description="API para crear, leer, actualizar y eliminar eventos y gestionar participantes.",
    version="1.0.0"
)

# Incluir routers de eventos y participantes
app.include_router(evento_routes.router, prefix="/eventos", tags=["Eventos"])
app.include_router(participante_routes.router, prefix="/participantes", tags=["Participantes"])
