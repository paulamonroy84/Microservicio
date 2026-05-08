from datetime import datetime

from app.services.validator import validar_solicitud
from app.services.classifier_ai import clasificar_con_ia
from app.services.priority_ai import prioridad_con_ia
from app.services.justification_ai import justificar_con_ia
from app.services.decision_engine import definir_siguiente_paso
from app.services.external_platform import crear_caso_externo
from app.utils.logger import logger


def procesar_solicitud(data: dict):

    try:

        descripcion = data["solicitud_descripcion"]
        compania = data["compania"]

        logger.info(f"Procesando solicitud {data['solicitud_id']}")

        # VALIDACIÓN
        es_valida = validar_solicitud(descripcion)

        if not es_valida:

            logger.warning("Solicitud con información insuficiente")

            return {
                "compania": compania,
                "solicitud_id": data["solicitud_id"],
                "solicitud_fecha": str(datetime.now()),
                "proximo_paso": "CIERRE_POR_INFORMACION_INSUFICIENTE",
                "justificacion": "La solicitud no contiene información suficiente.",
                "estado": "cerrado"
            }

        # CLASIFICACIÓN IA
        categoria = clasificar_con_ia(
            descripcion,
            compania
        )   

        # PRIORIDAD IA
        prioridad = prioridad_con_ia(
            descripcion,
            categoria
        )

        # DECISIÓN
        siguiente_paso = definir_siguiente_paso(
            compania,
            categoria,
            es_valida
        )

        # JUSTIFICACIÓN IA
        justificacion = justificar_con_ia(
            descripcion,
            categoria,
            prioridad
        )

        # INTEGRACIÓN EXTERNA
        id_externo = None
        estado = "cerrado"

        if siguiente_paso == "GESTION_EXTERNA":

            id_externo = crear_caso_externo()
            estado = "pendiente"

        resultado = {

            "compania": compania,

            "solicitud_id": data["solicitud_id"],

            "solicitud_fecha": str(datetime.now()),

            "solicitud_tipo": categoria,

            "solicitud_prioridad": prioridad,

            "solicitud_id_plataforma_externa": id_externo,

            "proximo_paso": siguiente_paso,

            "justificacion": justificacion,

            "estado": estado
        }

        logger.info(f"Solicitud procesada correctamente")

        return resultado

    except Exception as e:

        logger.error(f"Error procesando solicitud: {str(e)}")

        return {
            "error": str(e),
            "mensaje": "Error interno del microservicio"
        }