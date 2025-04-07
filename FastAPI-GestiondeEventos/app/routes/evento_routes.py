# app/routes/evento_routes.py
from fastapi import APIRouter, HTTPException
from app.modelos.evento import EventoCrear, Evento
from app.database import coleccion_eventos
from bson import ObjectId
from datetime import datetime, date

#Endpoint para los eventos 
router = APIRouter()

def formatear_evento(evento) -> dict:
    # definir la fecha como un formato que solo tiene dia mes y año 
    fecha = evento["fecha"]
    if isinstance(fecha, datetime):
        fecha_formateada = fecha.strftime("%Y-%m-%d")
    else:
        fecha_formateada = fecha
# se crea un evento con los datos que se le asignan
def formatear_evento(evento) -> dict:
    return {
        "id": str(evento["_id"]),
        "titulo": evento["titulo"],
        "descripcion": evento.get("descripcion"),
        "ubicacion": evento["ubicacion"],
        "fecha": evento["fecha"],
        "capacidad": evento["capacidad"],
        "participantes": evento.get("participantes", [])
    }

# Crear un nuevo evento
@router.post("/", response_model=Evento)
async def crear_evento(evento: EventoCrear):
    datos_evento = evento.dict()
    # Si la fecha es de tipo date, convertirla a datetime (hora 00:00:00)
    if isinstance(datos_evento.get("fecha"), date) and not isinstance(datos_evento.get("fecha"), datetime):
        datos_evento["fecha"] = datetime.combine(datos_evento["fecha"], datetime.min.time())
    datos_evento["participantes"] = []
    nuevo_evento = await coleccion_eventos.insert_one(datos_evento)
    evento_creado = await coleccion_eventos.find_one({"_id": nuevo_evento.inserted_id})
    return formatear_evento(evento_creado)

# Obtener la lista de eventos
@router.get("/", response_model=list[Evento])
async def obtener_eventos():
    eventos = []
    async for evento in coleccion_eventos.find():
        eventos.append(formatear_evento(evento))
    return eventos

# Obtener un evento por ID
@router.get("/{id}", response_model=Evento)
async def obtener_evento(id: str):
    evento = await coleccion_eventos.find_one({"_id": ObjectId(id)})
    if evento:
        return formatear_evento(evento)
    raise HTTPException(status_code=404, detail="Evento no encontrado")

# Actualizar un evento por ID
@router.put("/{id}", response_model=Evento)
async def actualizar_evento(id: str, evento_actualizado: EventoCrear):
    evento = await coleccion_eventos.find_one({"_id": ObjectId(id)})
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    datos_actualizados = evento_actualizado.dict()
    # Mantenemos la lista de participantes sin modificar
    datos_actualizados["participantes"] = evento.get("participantes", [])
    
    await coleccion_eventos.update_one({"_id": ObjectId(id)}, {"$set": datos_actualizados})
    evento_modificado = await coleccion_eventos.find_one({"_id": ObjectId(id)})
    return formatear_evento(evento_modificado)

# Eliminar un evento por ID
@router.delete("/{id}")
async def eliminar_evento(id: str):
    evento = await coleccion_eventos.find_one({"_id": ObjectId(id)})
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    await coleccion_eventos.delete_one({"_id": ObjectId(id)})
    
    # Nota: Aquí se podría limpiar la relación en la colección de participantes si es necesario.
    return {"mensaje": "Evento eliminado correctamente"}
