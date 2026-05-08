import json


with open("app/config/delegations.json", "r", encoding="utf-8") as f:
    delegaciones_config = json.load(f)



def definir_siguiente_paso(compania: str,
                            categoria: str,
                            solicitud_valida: bool):

    if not solicitud_valida:

        return "CIERRE_POR_INFORMACION_INSUFICIENTE"

    delegaciones = delegaciones_config.get(compania, [])

    if categoria in delegaciones:

        return "GESTION_EXTERNA"

    return "RESPUESTA_DIRECTA"