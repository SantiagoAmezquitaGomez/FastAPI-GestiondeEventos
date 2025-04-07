# app/modelos/participante.py
from pydantic import BaseModel, EmailStr
from typing import Optional
#se crean los partiicipantes 
class ParticipanteBase(BaseModel):
    nombre: str
    email: EmailStr
    evento_id: Optional[str] = None  # id del evento al que está registrado

class ParticipanteCrear(ParticipanteBase):
    pass
#se asigna un id al participante y se crea un estado de confirmacion
class Participante(ParticipanteBase):
    id: str
    confirmado: bool = False  # Estado de confirmación

    class Config:
        orm_mode = True
