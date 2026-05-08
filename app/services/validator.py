def validar_solicitud(texto: str):

    if not texto:
        return False

    palabras_minimas = 10

    if len(texto.split()) < palabras_minimas:
        return False

    return True