from pydantic import BaseModel

class Solicitud(BaseModel):

    compania: str
    solicitud_id: str
    solicitud_descripcion: str