# -*- coding: utf-8 -*-
"""
Genera videos narrativos ASMR con Veo3 usando Selenium para interacción web.
Características:
- Sonido ASMR adictivo de principio a fin
- Narrativa secuencial coherente 
- Integración completa con Veo3 a través de su interfaz web
- Mejora de prompts con Gemini (Selenium)
"""

import os
import json
import time
import random
from typing import List, Dict, Optional
from datetime import datetime

from dotenv import load_dotenv
from src.utils.gemini_web_client import GeminiWebClient

# Cargar variables de entorno
load_dotenv()

# ------------------------
# Utilidades
# ------------------------

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def backoff_sleep(attempt: int):
    """Exponential backoff con jitter, máx 60s."""
    delay = min(60, (2 ** attempt) + random.uniform(0, 1))
    time.sleep(delay)

# ------------------------
# Funciones de carga de datos narrativos
# ------------------------

def load_narrative_story_data():
    """
    Carga los datos de la historia ganadora para narrativa ASMR
    """
    evaluation_file = 'data/analytics/story_evaluation.json'
    stories_file = 'data/analytics/story_prompts_narrative.json'
    
    if not os.path.exists(evaluation_file):
        print(f"[!] Error: No se encontro {evaluation_file}")
        print(">> Ejecuta primero: python select_best_story.py")
        return None, None
    
    # Cargar evaluación
    with open(evaluation_file, 'r', encoding='utf-8') as f:
        evaluation = json.load(f)
    
    # Cargar historias originales
    with open(stories_file, 'r', encoding='utf-8') as f:
        stories_data = json.load(f)
    
    winning_story_key = evaluation['seleccion']['historia_seleccionada']
    winning_story = stories_data['stories_generated'][winning_story_key]
    
    print(f"[+] Historia seleccionada: {winning_story['titulo']}")
    return winning_story, evaluation

def prepare_narrative_images_and_prompts():
    """
    Prepara las imágenes narrativas y sus prompts optimizados para Veo3
    """
    # Cargar historia ganadora
    winning_story, evaluation = load_narrative_story_data()
    if not winning_story:
        return []
    
    # Verificar imágenes narrativas
    narrative_images = [
        'data/images/gemini_image_1.png',
        'data/images/gemini_image_2.png', 
        'data/images/gemini_image_3.png'
    ]
    
    available_images = []
    for img_path in narrative_images:
        if os.path.exists(img_path):
            available_images.append(img_path)
        else:
            print(f"[!] Imagen narrativa faltante: {img_path}")
    
    if len(available_images) < 3:
        print(f"\n[!] Error crítico: Solo se encontraron {len(available_images)}/3 imágenes narrativas necesarias.")
        print("[!] El pipeline no puede continuar sin las 3 imágenes de la historia.")
        return []
    
    # Crear datos para cada secuencia narrativa
    narrative_data = []
    for i in range(1, 4):
        seq_key = f'secuencia_{i}'
        if seq_key in winning_story:
            sequence = winning_story[seq_key]
            
            # Prompt ASMR optimizado para videos VIVOS y COLORIDOS
            veo3_prompt = f"""
            NARRATIVA ASMR VIRAL - CAPÍTULO {i}/3 - ULTRA COLORIDO Y ADICTIVO
            
            HISTORIA: {winning_story.get('titulo', '')}
            SECUENCIA: {sequence['titulo']}
            
            DESCRIPCIÓN VISUAL VIBRANTE:
            {sequence['descripcion_visual']}
            
            MEJORAS VISUALES OBLIGATORIAS:
            - Colores vibrantes y saturados que hipnoticen
            - Iluminación dramática con contrastes intensos
            - Partículas brillantes flotando en el aire
            - Texturas ultra detalladas y táctiles
            - Reflejos dorados y plateados que capten la luz
            - Movimientos fluidos y orgánicos constantes
            - Efectos de profundidad y dimensión
            - Colores que cambien sutilmente para mantener atención
            
            SONIDOS ASMR ULTRA ADICTIVOS:
            - Audio principal: {sequence['elementos_asmr']}
            - Ambiente base: {winning_story.get('sonido_envolvente', 'Sonido envolvente continuo')}
            - Capas adicionales: Susurros hipnóticos, crujidos satisfactorios
            - Frecuencias: Audio binaural 3D que envuelve completamente
            - Intensidad: Sonidos que generen escalofríos y satisfacción
            - Ritmo: Patrones rítmicos que mantengan enganchado al espectador
            - Variación: Texturas sonoras que cambien cada 2-3 segundos
            
            INSTRUCCIONES TÉCNICAS PARA VEO3:
            - Duración: 6-8 segundos para máxima inmersión
            - Movimientos: Constantes, hipnóticos, nunca estáticos
            - Zoom: Acercamientos progresivos a texturas detalladas
            - Iluminación: Dinámica, con cambios sutiles de intensidad
            - Efectos: Partículas, destellos, reflejos constantes
            - Colores: Paleta vibrante que evolucione durante el video
            - Audio: Envolvente 360°, sin música de fondo, solo ASMR puro
            - Adicción: Cada segundo debe generar satisfacción sensorial
            
            ELEMENTOS DE VIRALIDAD OBLIGATORIOS:
            - Factor WOW desde el primer segundo
            - Texturas tan reales que den ganas de tocar
            - Sonidos que generen respuesta física inmediata
            - Colores que no se puedan ignorar en el feed
            - Movimientos que obliguen a ver el video completo
            - Transiciones que conecten perfectamente con el siguiente
            
            CONTEXTO NARRATIVO EN ESPAÑOL:
            Capítulo {i} de 3 - {sequence['titulo']}
            Historia: {winning_story.get('concepto_general', '')}
            
            RESULTADO ESPERADO: Video ASMR ultra viral, colorido, adictivo que sea imposible de parar de ver
            """.strip()
            
            narrative_data.append({
                'image_path': available_images[i-1],
                'prompt': veo3_prompt,
                'sequence_num': i,
                'sequence_title': sequence['titulo'],
                'asmr_elements': sequence['elementos_asmr'],
                'output_name': f'narrative_video_{i}'
            })
    
    print(f"[i] Preparadas {len(narrative_data)} secuencias narrativas para Veo3")
    return narrative_data

def enhance_narrative_prompt_with_ai(client: GeminiWebClient, base_prompt: str, sequence_info: Dict) -> str:
    """
    Mejora el prompt narrativo para videos ultra coloridos y adictivos usando Gemini (Selenium).
    """
    sequence_num = sequence_info['sequence_num']
    sequence_title = sequence_info['sequence_title']
    asmr_elements = sequence_info['asmr_elements']

    enhancement_prompt_template = f"""
    Eres un experto en la creación de prompts para IA generativa de videos (como Veo3).
    Tu tarea es mejorar un prompt básico para que produzca videos de alta calidad, ultra coloridos, adictivos y con una estética ASMR específica, optimizados para viralidad en plataformas como TikTok.

    PROMPT ORIGINAL PARA VIDEO (Capítulo {sequence_num}/3 - {sequence_title}):
    "{base_prompt}"

    ELEMENTOS ASMR CLAVE: {asmr_elements}

    MEJORAS REQUERIDAS:
    1.  **Detalles Técnicos para Video:** Incorpora términos como "cinematic 4K", "8K", "ultra-realistic", "hyper-detailed", "smooth camera movements", "dynamic lighting", "volumetric fog", "depth of field", "slow motion".
    2.  **Estética ASMR Visual:** Añade elementos visuales que evoquen sensaciones ASMR, como "satisfying textures", "glossy surfaces", "soft focus", "intricate details", "mesmerizing patterns", "fluid motion", "sparkling particles".
    3.  **Estética ASMR Auditiva (implícita en el video):** Aunque el video es visual, el prompt debe sugerir la calidad del sonido ASMR. Usa frases como "visual representation of crisp ASMR sounds", "visuals that evoke tingling sensations", "hypnotic audio-visual experience".
    4.  **Composición y Color:** Especifica una paleta de colores vibrante y saturada, composición dinámica y atractiva (ej. "vibrant color palette", "saturated hues", "strong contrast", "golden hour lighting", "neon accents").
    5.  **Viralidad:** Incluye elementos que hagan el video irresistible y compartible, como "captivating", "mesmerizing", "addictive loop", "satisfying loop", "viral potential".
    6.  **Claridad y Concisión:** El prompt final debe ser claro, directo y estar en inglés para maximizar la compatibilidad con los modelos de IA.

    RESPONDE ÚNICAMENTE CON EL PROMPT MEJORADO EN INGLÉS. No incluyas explicaciones, texto introductorio ni marcadores de código como ```json o ```.
    """

    print(f"   -> Solicitando mejora de prompt a Gemini para secuencia {sequence_num}...")
    enhanced_prompt = client.generate_text(enhancement_prompt_template)

    if enhanced_prompt:
        print(f"   -> [+] Prompt mejorado por Gemini para secuencia {sequence_num}: {enhanced_prompt[:100]}...")
        return enhanced_prompt
    else:
        print(f"   -> [!] Gemini no devolvió un prompt mejorado. Usando prompt original para secuencia {sequence_num}.")
        return base_prompt

def generate_narrative_videos_with_veo3(narrative_data: List[Dict]) -> List[str]:
    """
    Genera videos narrativos usando Veo3 a través de Selenium.
    """
    veo_client = GeminiWebClient()
    generated_videos = []
    
    try:
        for i, sequence_data in enumerate(narrative_data, 1):
            print(f"\n>> Generando video {i}/{len(narrative_data)}: {sequence_data['sequence_title']}")
            
            # Optimizar prompt usando Gemini (Selenium)
            optimized_prompt = enhance_narrative_prompt_with_ai(
                veo_client, # Pasar la instancia del cliente Selenium
                sequence_data['prompt'], 
                sequence_data
            )
            
            # Generar con Veo3 usando Selenium
            video_path = None
            try:
                video_path = veo_client.generate_video_from_image_and_prompt(
                    sequence_data['image_path'],
                    optimized_prompt
                )
                
                if video_path:
                    # Renombrar el archivo descargado al nombre deseado
                    output_dir = "data/videos/original"
                    ensure_dir(output_dir)
                    final_video_name = f"{sequence_data['output_name']}.mp4"
                    final_video_path = os.path.join(output_dir, final_video_name)
                    
                    # Asegurarse de que el archivo descargado existe antes de intentar moverlo
                    if os.path.exists(video_path):
                        if os.path.exists(final_video_path):
                            os.remove(final_video_path) # Eliminar si ya existe para evitar errores
                        os.rename(video_path, final_video_path)
                        
                        generated_videos.append(final_video_path)
                        print(f"[+] Video {i} generado exitosamente: {final_video_path}")
                    else:
                        print(f"[!] Error: El archivo descargado no se encontró en {video_path}")
                else:
                    print(f"[!] Error: generate_video_from_image_and_prompt no devolvió una ruta válida para video {i}")
            except Exception as e:
                print(f"[!] Error generando video {i} con Selenium: {e}")
            
            # Pausa entre generaciones
            if i < len(narrative_data):
                print("   -> Pausa entre generaciones...")
                time.sleep(5)
    finally:
        veo_client.close()
    
    return generated_videos

# ------------------------
# Bloque principal para ejecución directa
# ------------------------

def main():
    print("\n=== GENERACIÓN DE VIDEOS NARRATIVOS ASMR CON VEO3 ===")
    narrative_data = prepare_narrative_images_and_prompts()
    if not narrative_data:
        print("[!] No se pudo preparar la narrativa. Verifica los archivos e imágenes requeridas.")
        return

    # Generar videos secuenciales
    generated_videos = []
    generation_log = {
        "timestamp": datetime.now().isoformat(),
        "generation_method": "veo3_narrative",
        "asmr_enabled": True,
        "narrative_sequence": True,
        "videos_generated": []
    }
    
    print(f">> Generando {len(narrative_data)} videos narrativos con Veo3...")
    
    # Generar videos usando Veo3
    generated_videos = generate_narrative_videos_with_veo3(narrative_data)
    
    # Completar log con resultados
    for i, sequence_data in enumerate(narrative_data):
        result = {
            "sequence": i + 1,
            "title": sequence_data['sequence_title'],
            "asmr_elements": sequence_data['asmr_elements'],
            "image_source": sequence_data['image_path'],
            "status": "success" if i < len(generated_videos) else "failed"
        }
        
        if i < len(generated_videos):
            result["video_path"] = generated_videos[i]
        
        generation_log["videos_generated"].append(result)
    
    # Guardar log de generación
    ensure_dir('data/analytics')
    log_file = 'data/analytics/narrative_veo3_generation.json'
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(generation_log, f, indent=2, ensure_ascii=False)
    
    # Reporte final
    print(f"\n[+] REPORTE NARRATIVO VEO3:")
    print(f"   -> Videos programados: {len(narrative_data)}")    
    print(f"[+] Videos generados: {len(generated_videos)}")
    print(f"   -> ASMR envolvente: Activado")
    print(f"   -> Narrativa secuencial: Completa")
    print(f"   -> Log guardado: {log_file}")
    
    if len(generated_videos) == len(narrative_data):
        print(f"\n>> ¡Generacion narrativa Veo3 completada!")
        print(f"[i] Videos en: data/videos/")
        print(f">> Siguiente paso: python procesar_final_tiktok.py")
        return True
    else:
        print(f"\n[!] Generacion completada con {len(narrative_data) - len(generated_videos)} errores")
        return False

if __name__ == "__main__":
    main()