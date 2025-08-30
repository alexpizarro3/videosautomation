"""
Genera imágenes usando Gemini 2.5 Flash Preview a partir de los prompts generados automáticamente
"""

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import json

import os

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Cargar prompts generados automáticamente
prompts_path = os.getenv('PROMPTS_JSON', 'data/analytics/fusion_prompts_auto.json')
with open(prompts_path, 'r', encoding='utf-8') as f:
    prompts = json.load(f).get('prompts', [])

for idx, prompt in enumerate(prompts):
    print(f"Prompt {idx+1}: {prompt}\n")
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )
    print("Raw Gemini API response:")
    print(response)
    if response and response.candidates:
        candidate = response.candidates[0]
        if candidate and candidate.content and hasattr(candidate.content, 'parts'):
            for part in candidate.content.parts:  # type: ignore
                if getattr(part, 'text', None) is not None:
                    print(part.text)
                elif getattr(part, 'inline_data', None) is not None and getattr(part.inline_data, 'data', None) is not None:
                    image = Image.open(BytesIO(part.inline_data.data))  # type: ignore
                    image_path = f'gemini_image_{idx+1}.png'
                    image.save(image_path)
                    print(f"Imagen guardada en {image_path}")
                    # image.show()  # Opcional: mostrar la imagen
