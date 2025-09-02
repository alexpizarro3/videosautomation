def mejorar_prompt_gemini(prompt, genai_model):
    """
    Envía el prompt a Gemini para que lo reescriba de forma detallada, específica y creativa, limitado a 450 caracteres.
    """
    instruction = (
        "Fusiona los conceptos principales extraídos del análisis de los videos de la cuenta de TikTok con las tendencias virales actuales. Genera un prompt para imagen que sea único, creativo y visualmente impactante, evitando repeticiones y asegurando variedad en sujetos, acciones, entornos y estilos visuales. Describe sujeto, acción, entorno, estilo visual y ambiente, e incluye detalles de sonido envolvente, adictivo y efectos ASMR en la escena. Limita el resultado a máximo 450 caracteres. Prompt base: " + prompt
    )
    response = genai_model.generate_content(instruction)
    texto = response.text.strip() if hasattr(response, 'text') else str(response)
    return texto[:450]
def mejorar_prompt(prompt):
    """
    Convierte un prompt general en uno detallado y específico, describiendo sujeto, acción, entorno, estilo y ambiente.
    """
    # Extraer palabras clave dinámicamente
    palabras = prompt.split()
    sujeto = next((w for w in palabras if w.lower() not in ['con', 'de', 'en', 'y', 'el', 'la', 'los', 'las', 'un', 'una', 'por', 'para', 'como', 'que', 'del', 'al']), None)
    accion = next((w for w in palabras if w.lower().endswith('ando') or w.lower().endswith('iendo')), None)
    entorno = next((w for w in palabras if w.lower() in ['playa','acuario','espacio','cielo','agua','plato','fuego','hielo','bosque','ciudad','montaña','mar','desierto']), None)
    estilo = next((w for w in palabras if w.lower() in ['digital','surrealista','fantasía','arte','estética','vibrante','llamativo','realista','minimalista','retro','moderno']), None)
    partes = []
    if sujeto:
        partes.append(f"Sujeto principal: {sujeto.capitalize()}.")
    if accion:
        partes.append(f"Acción: {accion}.")
    if entorno:
        partes.append(f"Entorno: {entorno}.")
    if estilo:
        partes.append(f"Estilo visual: {estilo}.")
    partes.append("Colores vivos, detalles realistas, ambiente creativo y viral.")
    prompt_detallado = ' '.join(partes)
    return prompt_detallado if len(partes) > 1 else prompt[:450]

import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
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

def get_gemini_trends_sdk(conceptos_top):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    instruction = (
        f"Analiza las tendencias virales actuales en TikTok que estén relacionadas con estos conceptos: {conceptos_top}. "
        "Devuelve una lista de 6 tendencias virales concretas y actuales, con una breve descripción de cada una. Responde solo con la lista en formato JSON."
    )
    response = model.generate_content(instruction)
    texto = response.text.strip() if hasattr(response, 'text') else str(response)
    return texto

def generate_fusion_prompts(conceptos, tendencias):
    prompts = []
    for concepto in conceptos:
        prompt = (
            f"Genera una imagen digital hiperrealista de {concepto} fusionado con tendencias virales reales como: {tendencias}. "
            "Colores vibrantes, ambiente creativo y viral. Responde solo con imagen PNG."
        )
        prompts.append(prompt)
    while len(prompts) < 6:
        prompts.append(
            f"Genera una imagen digital hiperrealista fusionando los conceptos principales de mis videos top con las tendencias virales reales de TikTok: {tendencias}. "
            "Colores vibrantes, ambiente creativo y viral. Responde solo con imagen PNG."
        )
    return prompts[:6]

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
    tendencias = get_gemini_trends_sdk(conceptos_top_str)
    fusion_prompts = generate_fusion_prompts(conceptos, tendencias)
    # Inicializar modelo Gemini
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    # Mejorar cada prompt usando Gemini
    fusion_prompts_mejorados = [mejorar_prompt_gemini(p, model) for p in fusion_prompts]
    # Limpiar y ajustar cada prompt enriquecido
    def limpiar_prompt(p):
        # Eliminar advertencias y formato innecesario
        p = p.replace('```', '').replace('Prompt:', '').replace('No puedo generar imágenes PNG directamente.', '')
        p = p.replace('No puedo generar imágenes PNG.', '').replace('Mi función es procesar texto.', '')
        p = p.replace('Te he dado un prompt que si lo introduces en un generador de imágenes de IA como Midjourney, Stable Diffusion o Dall-E 2 debería darte la imagen que ', '')
        p = p.replace('Proporciono el prompt de texto para que lo uses en un generador de imágenes de IA como Midjourney, Dall-E o Stable Diffusion.', '')
        p = p.replace('Soy un modelo de lenguaje.', '')
        p = p.replace('/imagine prompt:', '')
        p = p.replace('![Imagen generada a partir del prompt](image_from_prompt.png)', '')
        p = p.replace('El prompt para esta imagen sería (abreviado para ajustarse al límite de caracteres):', '')
        p = p.replace('**Capibara chef ASMR playa frutal:**', '')
        p = p.strip()
        # Asegurar encabezado y guía
        if not p.lower().startswith('genera una imagen digital hiperrealista'):
            p = 'Genera una imagen digital hiperrealista de ' + p
        if 'Responde solo con imagen PNG.' not in p:
            p = p + ' Responde solo con imagen PNG.'
        return p[:450]
    fusion_prompts_limpios = [limpiar_prompt(p) for p in fusion_prompts_mejorados]
    output_file = 'data/analytics/fusion_prompts_auto.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'prompts': fusion_prompts_limpios}, f, indent=2, ensure_ascii=False)
    print(f"Prompts generados y guardados en {output_file}:")
    for i, p in enumerate(fusion_prompts_limpios, 1):
        print(f"{i}. {p}\n")

if __name__ == "__main__":
    main()
