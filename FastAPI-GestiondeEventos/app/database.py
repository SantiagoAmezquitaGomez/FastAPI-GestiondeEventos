# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
# CONEXION A LA BASE DE DATOS
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb+srv://santy:santy1@clustersa.a1wdk.mongodb.net/")

cliente = AsyncIOMotorClient(MONGO_DETAILS)
base_datos = cliente.gestion_eventos

# Definir las colecciones
coleccion_eventos = base_datos.get_collection("eventos")
coleccion_participantes = base_datos.get_collection("participantes")
