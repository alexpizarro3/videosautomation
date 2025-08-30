def mejorar_prompt_gemini(prompt, genai_model):
    """
    Envía el prompt a Gemini para que lo reescriba de forma detallada, específica y creativa, limitado a 450 caracteres.
    """
    instruction = (
        "Fusiona los conceptos principales extraídos del análisis de los videos de la cuenta de TikTok con las tendencias virales actuales. Genera un prompt para imagen que sea muy detallado, específico y creativo, describiendo sujeto, acción, entorno, estilo visual y ambiente, y que resulte visualmente impactante y viral. Limítalo a máximo 450 caracteres. Prompt base: " + prompt
    )
    response = genai_model.generate_content(instruction)
    texto = response.text.strip() if hasattr(response, 'text') else str(response)
    return texto[:450]
def mejorar_prompt(prompt):
    """
    Convierte un prompt general en uno detallado y específico, describiendo sujeto, acción, entorno, estilo y ambiente.
    """
    import re
    # Extraer sujeto, acción, entorno y estilo si existen
    sujeto = re.search(r'(roedor|capibara|hámster|fruta|sandía|naranja|grapes|animal)', prompt, re.IGNORECASE)
    entorno = re.search(r'(playa|acuario|fondo borroso|superficie rocosa|espacio|cielo|agua|plato|fuego|hielo|colores vibrantes)', prompt, re.IGNORECASE)
    accion = re.search(r'(sosteniendo|interactuando|cortando|emite luz|flames|burbujas|resplandor|surfeando)', prompt, re.IGNORECASE)
    estilo = re.search(r'(digital|surrealista|fantasía|arte|estética|vibrante|llamativo)', prompt, re.IGNORECASE)
    # Construir prompt detallado
    partes = []
    if sujeto:
        partes.append(f"Sujeto principal: {sujeto.group(0).capitalize()}.")
    if accion:
        partes.append(f"Acción: {accion.group(0)}.")
    if entorno:
        partes.append(f"Entorno: {entorno.group(0)}.")
    if estilo:
        partes.append(f"Estilo visual: {estilo.group(0)}.")
    partes.append("Colores vivos, detalles realistas, ambiente creativo y viral.")
    prompt_detallado = ' '.join(partes)
    # Si no se pudo extraer nada, devolver el original limitado
    return prompt_detallado if len(partes) > 1 else prompt[:450]

import json
import os
from google import genai

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

def generate_fusion_prompts(conceptos, tendencias):
    prompts = []
    for concepto in conceptos:
        prompt = f"{concepto} fusionado con tendencias virales reales como: {tendencias}. Imagen llamativa, creativa y viral."
        prompts.append(prompt)
    while len(prompts) < 6:
        prompts.append(f"Fusiona los conceptos principales de mis videos top con las tendencias virales reales de TikTok: {tendencias}. Imagen llamativa, creativa y viral.")
    return prompts[:6]

def main():
    scrap_json = os.getenv('SCRAP_JSON', 'data/analytics/tiktok_metrics_1756530212.json')
    data = load_scrap_results(scrap_json)
    conceptos = extract_main_concepts(data.get('videos_metrics', []))
    conceptos_top_str = ', '.join(conceptos)
    tendencias = get_gemini_trends_sdk(conceptos_top_str)
    fusion_prompts = generate_fusion_prompts(conceptos, tendencias)
    # Inicializar modelo Gemini
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Mejorar cada prompt usando Gemini
    fusion_prompts_mejorados = [mejorar_prompt_gemini(p, model) for p in fusion_prompts]
    # Limitar cada prompt a 450 caracteres máximo (por seguridad)
    fusion_prompts_limited = [p[:450] for p in fusion_prompts_mejorados]
    output_file = 'data/analytics/fusion_prompts_auto.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'prompts': fusion_prompts_limited}, f, indent=2, ensure_ascii=False)
    print(f"Prompts generados y guardados en {output_file}:")
    for i, p in enumerate(fusion_prompts, 1):
        print(f"{i}. {p}\n")

if __name__ == "__main__":
    main()
