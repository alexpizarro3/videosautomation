import json
import os
from dotenv import load_dotenv
from src.utils.gemini_web_client import GeminiWebClient

load_dotenv()

def load_scrap_results(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_main_concepts(videos_metrics):
    conceptos = []
    for video in videos_metrics:
        ai = video['metrics'].get('ai_analysis', {})
        concept = ai.get('concept', '').replace('\n', ' ').replace('*', '').strip()
        if concept and not concept.startswith('No analizado') and 'Error Gemini Vision' not in concept:
            conceptos.append(concept)
    return conceptos

def generate_viral_prompts_with_selenium(conceptos):
    """
    Genera 6 prompts virales usando Gemini Web UI con Selenium.
    """
    base_prompt = f"""Eres un experto en contenido viral de TikTok y en la creación de prompts para IA generativa de imágenes.
Tu objetivo es crear 6 prompts de imagen que sean visualmente espectaculares, ultra coloridos y adictivos, basados en los siguientes conceptos extraídos de videos virales.

CONCEPTOS VIRALES DETECTADOS:
{conceptos}

REQUISITOS PARA CADA PROMPT:
1.  **Concepto Visualmente Adictivo:** La idea central debe ser hipnótica y memorable.
2.  **Ultra Colorido:** Describe paletas de colores vibrantes, saturadas y con contrastes fuertes.
3.  **Estilo Cinematográfico y Realista:** El prompt debe incluir términos como "hyperrealistic", "cinematic lighting", "4K", "8K", "professional photography", "octane render".
4.  **Estética ASMR:** Añade elementos visuales que evoquen sensaciones ASMR como "satisfying textures", "glossy surfaces", "soft focus", "intricate details".
5.  **En Inglés:** Todos los prompts deben estar en inglés para maximizar la compatibilidad.

FORMATO DE RESPUESTA:
Responde únicamente con un objeto JSON que contenga una sola clave, "prompts", que sea una lista de 6 strings.

Ejemplo de respuesta:
{{
    "prompts": [
        "A hyperrealistic 4K image of a glossy, vibrant blue crystal being cut with a glowing laser, casting cinematic lighting and intricate details on a dark, satisfyingly textured surface, professional photography, octane render.",
        "Another prompt...",
        "..."
    ]
}}
"""
    try:
        client = GeminiWebClient()
        response_text = client.generate_text(base_prompt)
        client.close()

        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1]

        prompts_data = json.loads(response_text.strip())
        return prompts_data.get("prompts", [])
    except Exception as e:
        print(f"Error generando prompts con Gemini: {e}")
        return create_fallback_prompts()

def create_fallback_prompts():
    """
    Crea una lista de prompts de respaldo en caso de error.
    """
    return [
        "A hyperrealistic 4K image of a capybara chef slicing glowing crystal vegetables in a cyberpunk kitchen, cinematic lighting, ASMR satisfying textures.",
        "Professional photography of a miniature volcano erupting with glossy chocolate lava over a landscape of vibrant, detailed strawberries, 8K, octane render.",
        "An oddly satisfying video of a hydraulic press crushing a variety of colorful, glassy objects, soft focus, intricate details, hyperrealistic.",
        "Cinematic shot of a giant, fluffy cat walking through a miniature city like Godzilla, vibrant color palette, strong contrast, professional photography.",
        "A hyperrealistic 4K image of a person walking on a beach made of sparkling, colorful crystals, with waves of liquid gold, cinematic lighting.",
        "Close-up of a bee collecting pollen from a flower made of intricate, glowing glass, satisfying textures, soft focus, 8K, octane render."
    ]

def main():
    # Buscar el archivo tiktok_metrics_xxxxxxxxxx.json más reciente
    analytics_dir = 'data/analytics'
    metric_files = [f for f in os.listdir(analytics_dir) if f.startswith('tiktok_metrics_') and f.endswith('.json')]
    if not metric_files:
        raise FileNotFoundError('No se encontró ningún archivo tiktok_metrics_xxxxxxxxxx.json en data/analytics')
    
    latest_file = max(metric_files, key=lambda x: os.path.getctime(os.path.join(analytics_dir, x)))
    scrap_json = os.path.join(analytics_dir, latest_file)
    
    data = load_scrap_results(scrap_json)
    conceptos = extract_main_concepts(data.get('videos_metrics', []))
    conceptos_top_str = ', '.join(conceptos)

    print(">> Generando prompts virales con Selenium...")
    fusion_prompts = generate_viral_prompts_with_selenium(conceptos_top_str)

    if not fusion_prompts:
        print("[!] No se pudieron generar prompts. Usando fallbacks.")
        fusion_prompts = create_fallback_prompts()

    output_file = 'data/analytics/fusion_prompts_auto.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'prompts': fusion_prompts}, f, indent=2, ensure_ascii=False)
    
    print(f"Prompts generados y guardados en {output_file}:")
    for i, p in enumerate(fusion_prompts, 1):
        print(f"{i}. {p}\n")

if __name__ == "__main__":
    main()