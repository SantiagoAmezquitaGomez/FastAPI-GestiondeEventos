# app/modelos/evento.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
#se crean los eventos 
class EventoBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    ubicacion: str
    fecha: date
    capacidad: int

class EventoCrear(EventoBase):
    pass
#se asigna un id al evento y se crea una lista de participantes
class Evento(EventoBase):
    id: str
    participantes: List[str] = []  # Lista de IDs de participantes

    class Config:
        orm_mode = True

