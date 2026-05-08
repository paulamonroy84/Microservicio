import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Cargar categorías
with open("config/categories.json", "r") as file:
    categories_config = json.load(file)


def clasificar_con_ia(descripcion, compania):

    categorias_empresa = categories_config.get(
        compania,
        ["General"]
    )

    prompt = f"""
    Eres un clasificador de solicitudes.

    Clasifica la siguiente solicitud en UNA SOLA categoría.

    Categorías permitidas:
    {categorias_empresa}

    Solicitud:
    {descripcion}

    Responde únicamente con el nombre de la categoría.
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    categoria = response.choices[0].message.content.strip()

    return categoria