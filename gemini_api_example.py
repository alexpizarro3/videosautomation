# Ejemplo actualizado para Gemini API v2.5 usando el SDK oficial
# Requiere: pip install google-genai

import os
from google import genai

def get_gemini_trends_sdk(conceptos_top):
    client = genai.Client()
    prompt = (
        f"Analiza las tendencias virales actuales en TikTok que estén relacionadas con estos conceptos: {conceptos_top}. "
        "Devuelve una lista de 6 tendencias virales concretas y actuales, con una breve descripción de cada una. Responde solo con la lista en formato JSON."
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
    conceptos_top = "capybaras, ASMR, food art, animales lindos, edición creativa, surrealismo"
    print(get_gemini_trends_sdk(conceptos_top))
