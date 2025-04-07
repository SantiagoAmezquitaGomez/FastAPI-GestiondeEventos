# app/routes/participante_routes.py
from fastapi import APIRouter, HTTPException
from app.modelos.participante import ParticipanteCrear, Participante
from app.database import coleccion_participantes, coleccion_eventos
from bson import ObjectId
#endointS para los participantes
router = APIRouter()

def formatear_participante(participante) -> dict:
    return {
        "id": str(participante["_id"]),
        "nombre": participante["nombre"],
        "email": participante["email"],
        "confirmado": participante.get("confirmado", False),
        "evento_id": participante.get("evento_id")
    }

# Registrar un participante en un evento
@router.post("/registrar/{evento_id}", response_model=Participante)
async def registrar_participante(evento_id: str, participante: ParticipanteCrear):
    evento = await coleccion_eventos.find_one({"_id": ObjectId(evento_id)})
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    if len(evento.get("participantes", [])) >= evento["capacidad"]:
        raise HTTPException(status_code=400, detail="Capacidad del evento alcanzada")

    # Asignar el evento_id al participante
    datos_participante = participante.dict()
    datos_participante["evento_id"] = evento_id  # Se asigna la referencia del evento
    
    nuevo_participante = await coleccion_participantes.insert_one(participante.dict())
    datos_participante = await coleccion_participantes.find_one({"_id": nuevo_participante.inserted_id})
    
    await coleccion_eventos.update_one(
        {"_id": ObjectId(evento_id)},
        {"$push": {"participantes": str(datos_participante["_id"])}}
    )
    
    return formatear_participante(datos_participante)

# Obtener la lista de participantes
@router.get("/", response_model=list[Participante])
async def obtener_participantes():
    participantes = []
    async for participante in coleccion_participantes.find():
        participantes.append(formatear_participante(participante))
    return participantes

# Obtener un participante por ID
@router.get("/{id}", response_model=Participante)
async def obtener_participante(id: str):
    participante = await coleccion_participantes.find_one({"_id": ObjectId(id)})
    if participante:
        return formatear_participante(participante)
    raise HTTPException(status_code=404, detail="Participante no encontrado")

# Actualizar un participante por ID
@router.put("/{id}", response_model=Participante)
async def actualizar_participante(id: str, participante_actualizado: ParticipanteCrear):
    participante = await coleccion_participantes.find_one({"_id": ObjectId(id)})
    if not participante:
        raise HTTPException(status_code=404, detail="Participante no encontrado")
    
    datos_actualizados = participante_actualizado.dict()
    await coleccion_participantes.update_one({"_id": ObjectId(id)}, {"$set": datos_actualizados})
    participante_modificado = await coleccion_participantes.find_one({"_id": ObjectId(id)})
    return formatear_participante(participante_modificado)

# Confirmar la asistencia de un participante
@router.put("/confirmar/{id}", response_model=Participante)
async def confirmar_participante(id: str):
    participante = await coleccion_participantes.find_one({"_id": ObjectId(id)})
    if not participante:
        raise HTTPException(status_code=404, detail="Participante no encontrado")
    
    await coleccion_participantes.update_one({"_id": ObjectId(id)}, {"$set": {"confirmado": True}})
    participante_confirmado = await coleccion_participantes.find_one({"_id": ObjectId(id)})
    return formatear_participante(participante_confirmado)

# Eliminar un participante por ID
@router.delete("/{id}")
async def eliminar_participante(id: str):
    participante = await coleccion_participantes.find_one({"_id": ObjectId(id)})
    if not participante:
        raise HTTPException(status_code=404, detail="Participante no encontrado")
    
    await coleccion_participantes.delete_one({"_id": ObjectId(id)})
    
    # Remover el participante de la lista de participantes en todos los eventos donde esté registrado
    await coleccion_eventos.update_many(
        {"participantes": str(id)},
        {"$pull": {"participantes": str(id)}}
    )
    
    return {"mensaje": "Participante eliminado correctamente"}
