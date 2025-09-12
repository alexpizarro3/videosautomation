# -*- coding: utf-8 -*-
"""
Genera videos narrativos ASMR con Veo3 basado en generate_veo_video_from_image.py
Características:
- Sonido ASMR adictivo de principio a fin
- Narrativa secuencial coherente 
- Integración completa con Veo3
- Sistema de fallback automático
"""

import os
import re
import json
import time
import mimetypes
import random
from typing import List, Dict, Optional
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar variables de entorno
load_dotenv()

# ------------------------
# Utilidades (copiadas del original)
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

# ------------------------
# Generación con Veo3 (basado en el original)
# ------------------------

# ------------------------
# Cliente Veo para Narrativas (basado en el original)
# ------------------------

class NarrativeVeoClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("VEO3_API_KEY")
        assert api_key, "Falta GEMINI_API_KEY (o VEO3_API_KEY) en el entorno"
        self.model_name = os.getenv("VEO3_MODEL", "models/veo-3.0-generate-preview")
        self.client = genai.Client(api_key=api_key)

    def _open_image(self, image_path: str) -> types.Image:
        mime, _ = mimetypes.guess_type(image_path)
        if not mime:
            mime = "image/png"
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        return types.Image(image_bytes=img_bytes, mime_type=mime)

    def generate_narrative_video(
        self,
        image_path: str,
        prompt: str,
        output_name: str,
        max_attempts_poll: int = 60,
        retry_on_429: int = 3
    ) -> Optional[str]:
        """Genera un video narrativo ASMR y lo guarda como mp4"""
        out_dir = "data/videos/original"  # Videos narrativos van a original
        ensure_dir(out_dir)

        # Envío con reintentos por 429/quotas
        send_attempt = 0
        operation = None
        while send_attempt <= retry_on_429:
            try:
                image_obj = self._open_image(image_path)
                print(f"   -> Modelo Veo3: {self.model_name}")
                print("   -> Enviando solicitud narrativa ASMR...")
                operation = self.client.models.generate_videos(
                    model=self.model_name,
                    prompt=prompt,
                    image=image_obj,
                    config=types.GenerateVideosConfig()
                )
                break
            except Exception as e:
                msg = str(e).lower()                
                if "429" in msg or "resource_exhausted" in msg or "quota" in msg or "rate" in msg:                    
                    print(f"[!] Limite alcanzado (intento {send_attempt+1}/{retry_on_429+1}). Backoff...")
                    backoff_sleep(send_attempt)
                    send_attempt += 1
                    continue
                print(f"[!] Error al iniciar generacion: {e}")
                return None

        if operation is None:
            print("[ERROR] No se pudo iniciar la operación (posible límite de API).")
            return None

        # Poll hasta done
        print(">> Esperando generacion...")
        attempt = 0
        while attempt < max_attempts_poll:
            if getattr(operation, "done", False):
                break
            print(f"   -> Procesando... ({attempt+1}/{max_attempts_poll})")
            time.sleep(10)
            try:
                operation = self.client.operations.get(operation)
            except Exception as e:
                print(f"[!] Error al consultar estado: {e}")
                backoff_sleep(min(attempt, 5))
            attempt += 1

        if not getattr(operation, "done", False):
            print("[!] Timeout esperando la generacion.")
            return None

        # Descargar video
        try:
            videos = getattr(getattr(operation, "response", None), "generated_videos", None)
            if not videos:
                err = getattr(operation, "error", None)                
                print(f"[!] Respuesta sin videos. Error: {err}")
                return None

            gv = videos[0]  # primer resultado
            
            # 1) descargar al file store del SDK
            self.client.files.download(file=gv.video)

            # 2) guardar en disco
            output_path = f"{out_dir}/{output_name}.mp4"
            gv.video.save(output_path)

            if os.path.exists(output_path) and os.path.getsize(output_path) > 1024:
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"[+] Video narrativo generado: {output_path} ({file_size:.1f} MB)")
                return output_path
            else:
                print(f"[!] Error: archivo no valido o muy pequeno")
                return None

        except Exception as e:
            print(f"[!] Error descargando video: {e}")
            return None

def enhance_narrative_prompt_with_ai(base_prompt: str, sequence_info: Dict) -> str:
    """
    Mejora el prompt narrativo para videos ultra coloridos y adictivos
    """
    sequence_num = sequence_info['sequence_num']
    
    # Mejoras específicas por secuencia para máxima viralidad
    if sequence_num == 1:
        # Biblioteca - Colores dorados y mágicos
        color_enhancement = """
        MEJORAS SECUENCIA 1 - BIBLIOTECA MÁGICA:
        - Rayos de sol dorados atravesando polvo brillante
        - Páginas que brillan con texto dorado al abrirse
        - Partículas mágicas flotando como luciérnagas
        - Colores: Dorado intenso, ambar cálido, marrones ricos
        - Sonidos: Susurros hipnóticos, crujidos satisfactorios de pergamino
        """
    elif sequence_num == 2:
        # Pasaje - Colores fríos y misteriosos
        color_enhancement = """
        MEJORAS SECUENCIA 2 - PASAJE MISTERIOSO:
        - Agua cristalina que refleja luz azul mágica
        - Piedras húmedas con reflejos plateados
        - Gotas de agua que brillan como diamantes
        - Colores: Azul profundo, plateado brillante, verdes esmeralda
        - Sonidos: Goteo rítmico hipnótico, ecos resonantes
        """
    else:
        # Reloj - Colores prisma y cristalinos
        color_enhancement = """
        MEJORAS SECUENCIA 3 - RELOJ MÁGICO:
        - Arena cristalina que cambia de color al fluir
        - Destellos prisma que crean arcoíris
        - Cristal que pulsa con luz interior
        - Colores: Prisma completo, cristalino, destellos iridiscentes
        - Sonidos: Flujo de arena hipnótico, resonancia cristalina
        """
    
    enhanced_prompt = base_prompt + "\n\n" + color_enhancement
    
    print(f"   -> Prompt ULTRA COLORIDO optimizado para secuencia {sequence_num}")
    return enhanced_prompt

def generate_narrative_videos_with_veo3(narrative_data: List[Dict]) -> List[str]:
    """
    Genera videos narrativos usando Veo3 (versión simplificada)
    """
    veo_client = NarrativeVeoClient()
    generated_videos = []
    
    for i, sequence_data in enumerate(narrative_data, 1):
        print(f"\n>> Generando video {i}/{len(narrative_data)}: {sequence_data['sequence_title']}")
        
        # Optimizar prompt (por ahora sin IA externa)
        optimized_prompt = enhance_narrative_prompt_with_ai(
            sequence_data['prompt'], 
            sequence_data
        )
        
        # Generar con Veo3
        video_path = veo_client.generate_narrative_video(
            sequence_data['image_path'],
            optimized_prompt,
            sequence_data['output_name']
        )
        
        if video_path:
            generated_videos.append(video_path)
            print(f"[+] Video {i} generado exitosamente")
        else:
            print(f"[!] Error generando video {i}")
        
        # Pausa entre generaciones
        if i < len(narrative_data):
            print("   -> Pausa entre generaciones...")
            time.sleep(5)
    
    return generated_videos

# ------------------------
# Función principal
# ------------------------

def main():
    """
    Función principal para generar videos narrativos con Veo3
    """
    print(">> Iniciando generación de videos narrativos ASMR con Veo3...")
    
    # Verificar API key
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('VEO3_API_KEY')
    if not api_key:
        print("[!] Error: No se encontro GEMINI_API_KEY o VEO3_API_KEY")
        return False
    
    # Cargar datos narrativos
    print(">> Cargando historia ganadora y secuencias...")
    narrative_data = prepare_narrative_images_and_prompts()
    
    if not narrative_data:
        print("[!] No se pudieron cargar datos narrativos")
        print(">> Asegurate de haber ejecutado: python select_best_story.py")
        return False
    
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
    
    # Crear log de generación
    generation_log = {
        "timestamp": datetime.now().isoformat(),
        "generation_method": "veo3_narrative",
        "asmr_enabled": True,
        "narrative_sequence": True,
        "videos_generated": []
    }
    
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
