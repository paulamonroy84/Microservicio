from fastapi import FastAPI
from app.models.request_models import Solicitud
from app.services.orchestrator import procesar_solicitud

app = FastAPI(
    title="Microservicio IA BPO",
    description="Servicio transversal IA para automatización de solicitudes",
    version="1.0"
)


@app.get("/")
def home():

    return {
        "mensaje": "Microservicio funcionando correctamente"
    }


@app.post("/procesar_solicitud")
def procesar(data: Solicitud):

    return procesar_solicitud(data.model_dump())