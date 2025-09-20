# -*- coding: utf-8 -*-
"""
Genera videos con Gemini/Veo 3 a partir de imágenes y guarda los MP4 localmente.
"""

import os
import re
import json
import time
import mimetypes
import random
from typing import List, Dict, Optional

from dotenv import load_dotenv
from src.utils.gemini_web_client import GeminiWebClient

# Importar nuestros módulos de prompts virales y análisis de imágenes
from viral_video_prompt_generator import ViralVideoPromptGenerator, enhance_existing_prompts
from image_metadata_analyzer import ImageMetadataAnalyzer
from viral_image_selector import ViralImageSelector

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
# Selección de prompts PROFESIONALES
# ------------------------

def seleccionar_mejores_imagenes_y_prompts() -> List[Dict[str, str]]:
    """
    Sistema PROFESIONAL: Usa selector inteligente + prompts virales optimizados con análisis de metadatos,
    caso contrario usa el sistema legacy con mejoras.
    """
    
    print("Iniciando análisis avanzado de imágenes...")
    
    # 1. SELECTOR INTELIGENTE DE IMÁGENES
    print("Seleccionando mejores imágenes con criterios virales profesionales...")
    try:
        viral_selector = ViralImageSelector()
        best_images = viral_selector.select_best_images(num_select=3)
        print(f"   {len(best_images)} imágenes seleccionadas por potencial viral")
    except Exception as e:
        print(f"   Error en selector viral: {e}")
        print("   Usando selección secuencial...")
        best_images = []
    
    # 2. ANÁLISIS DE METADATOS
    try:
        metadata_analyzer = ImageMetadataAnalyzer()
        print("   Analizador de metadatos inicializado")
    except Exception as e:
        print(f"   Error inicializando analizador: {e}")
        print("   Continuando con sistema legacy...")
        metadata_analyzer = None
    
    # 2. PRIMERA OPCIÓN: Usar prompts profesionales si existen
    enhanced_file = "data/analytics/fusion_prompts_auto_enhanced.json"
    if os.path.exists(enhanced_file):
        print("Usando prompts PROFESIONALES optimizados...")
        with open(enhanced_file, "r", encoding="utf-8") as f:
            enhanced_data = json.load(f)
        
        enhanced_prompts = enhanced_data.get("enhanced_prompts", [])
        if enhanced_prompts:
            # Ordenar por score viral y tomar top 3
            sorted_prompts = sorted(
                enhanced_prompts, 
                key=lambda x: x["metadata"]["predicted_engagement"],
                reverse=True
            )[:3]
            
            mejores = []
            
            # Usar imágenes seleccionadas inteligentemente
            if best_images:
                selected_image_paths = [img['path'] for img in best_images]
                print(f"   Usando imágenes seleccionadas por IA: {[os.path.basename(p) for p in selected_image_paths]}")
            else:
                # Fallback a orden secuencial
                imagenes = [f"data/images/viral_image_{i+1}.png" for i in range(6)]
                selected_image_paths = [img for img in imagenes if os.path.exists(img)][:3]
                print(f"   Fallback: usando orden secuencial")
            
            for i, enhanced_prompt in enumerate(sorted_prompts):
                # Mapear prompt a imagen seleccionada inteligentemente
                if i < len(selected_image_paths):
                    imagen = selected_image_paths[i]
                else:
                    # Si no hay suficientes imágenes seleccionadas, usar fallback
                    imagenes = [f"data/images/viral_image_{i+1}.png" for i in range(6)]
                    imagen = next((im for im in imagenes if os.path.exists(im)), None)
                
                if imagen:
                    # Enriquecer con análisis de metadatos si está disponible
                    image_context = None
                    if metadata_analyzer:
                        try:
                            image_context = metadata_analyzer.get_video_prompt_context(imagen)
                            if image_context.get('error'):
                                print(f"   No se pudo analizar {imagen}: {image_context['error']}")
                                image_context = None
                            else:
                                print(f"   Metadatos extraídos para {imagen}")
                        except Exception as e:
                            print(f"   Error analizando {imagen}: {e}")
                            image_context = None
                    
                    item_data = {
                        "prompt": enhanced_prompt["prompt"],
                        "imagen": imagen,
                        "metadata": enhanced_prompt["metadata"],
                        "viral_score": enhanced_prompt["metadata"]["predicted_engagement"]
                    }
                    
                    # Agregar contexto de imagen si está disponible
                    if image_context:
                        item_data["image_context"] = image_context
                        # Actualizar metadatos con información de la imagen
                        if "image_analysis" in image_context:
                            analysis = image_context["image_analysis"]
                            item_data["metadata"]["detected_theme"] = analysis.get("main_theme", "")
                            item_data["metadata"]["image_colors"] = analysis.get("dominant_colors", [])
                            item_data["metadata"]["image_mood"] = analysis.get("mood", "")
                    
                    mejores.append(item_data)
            
            print(f"{len(mejores)} prompts profesionales seleccionados")
            for i, item in enumerate(mejores, 1):
                print(f"   {i}. Score viral: {item['viral_score']}/100")
                print(f"      Categoría: {item['metadata']['viral_category']}")
                if item.get('image_context'):
                    theme = item['image_context'].get('image_analysis', {}).get('main_theme', 'N/A')
                    print(f"      Tema detectado: {theme}")
            
            return mejores
    
    # 2. FALLBACK: Sistema legacy mejorado
    print("Prompts profesionales no disponibles, usando sistema legacy mejorado...")
    
    with open("data/analytics/fusion_prompts_auto.json", "r", encoding="utf-8") as f:
        prompts_data = json.load(f)
    prompts = prompts_data["prompts"]

    imagenes = [f"data/images/viral_image_{i+1}.png" for i in range(6)]
    
    # Keywords virales actualizados 2025
    keywords_virales = [
        'asmr', 'kawaii', 'capibara', 'explosión', 'colores vibrantes', 'pastel', 'fruta',
        'atardecer', 'gaviotas', 'gelatina', 'acuario', 'pecera', 'playero', 'relajante',
        'adictivo', 'macro', 'neon', 'viral', 'miniatura', 'crujiente', 'sonido', 'burbuja',
        'crema', 'rosa', 'turquesa', 'summer', 'foodart', 'satisfying', 'tingles', 'dreamcore',
        'cottagecore', 'aesthetic', 'liminal', 'hypnotic', 'therapeutic', 'immersive'
    ]

    def score_prompt(p: str) -> int:
        s = 0
        low = p.lower()
        
        # Score básico por keywords
        for kw in keywords_virales:
            if kw in low:
                s += 1
                
        # Bonificaciones especiales
        s += low.count('asmr') * 3  # ASMR es muy viral
        s += low.count('adictivo') * 2
        s += low.count('viral') * 2
        s += low.count('satisfying') * 2
        s += low.count('hipnótico') * 2
        
        # Bonus por elementos técnicos
        technical_terms = ['hiperrealista', 'cinematográfico', 'profesional', 'ultra', '4k']
        for term in technical_terms:
            if term in low:
                s += 1
                
        return s

    scored = [(score_prompt(p), i, p) for i, p in enumerate(prompts)]
    top3 = sorted(scored, reverse=True)[:3]

    mejores = []
    
    # Usar imágenes seleccionadas inteligentemente si están disponibles
    if best_images:
        selected_image_paths = [img['path'] for img in best_images]
        print(f"   Sistema legacy usando imágenes seleccionadas por IA: {[os.path.basename(p) for p in selected_image_paths]}")
    else:
        imagenes = [f"data/images/viral_image_{i+1}.png" for i in range(6)]
        selected_image_paths = [img for img in imagenes if os.path.exists(img)]
        print(f"   Sistema legacy usando orden secuencial")
    
    for i, (score, idx, prompt_original) in enumerate(top3):
        # Mapear a imagen seleccionada inteligentemente
        if best_images and i < len(selected_image_paths):
            imagen = selected_image_paths[i]
        else:
            # Fallback al mapeo original
            imagenes = [f"data/images/viral_image_{i+1}.png" for i in range(6)]
            imagen = imagenes[idx] if idx < len(imagenes) and os.path.exists(imagenes[idx]) else None
            if not imagen:
                imagen = next((im for im in imagenes if os.path.exists(im)), None)
        
        if not imagen:
            continue
        
        # ANÁLISIS DE METADATOS PARA MEJORAR EL PROMPT
        image_context = None
        if metadata_analyzer:
            try:
                image_context = metadata_analyzer.get_video_prompt_context(imagen)
                if image_context.get('error'):
                    print(f"   No se pudo analizar {imagen}: {image_context['error']}")
                    image_context = None
                else:
                    print(f"   Metadatos extraídos para {imagen}")
            except Exception as e:
                print(f"   Error analizando {imagen}: {e}")
                image_context = None
        
        # MEJORAS PROFESIONALES al prompt legacy
        prompt_video = prompt_original
        
        # Transformaciones básicas imagen → video
        prompt_video = re.sub(r'Genera una imagen digital hiperrealista de', 'Crea un video ASMR cinematográfico ultra viral de', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'Genera una imagen digital hiperrealista', 'Crea un video ASMR cinematográfico viral', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'Genera una imagen', 'Crea un video hipnótico', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'\bimagen(es)?\b', 'video', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'\bImagen(es)?\b', 'Video', prompt_video, flags=re.IGNORECASE)
        
        # Eliminar referencias de formato
        prompt_video = re.sub(r'Formato PNG\.‏?', '', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'Responde solo con imagen PNG\.‏?', '', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'\bPNG\b', '', prompt_video, flags=re.IGNORECASE)
        
        # Mejoras de estilo
        prompt_video = re.sub(r'estilo hiperrealista', 'estilo cinematográfico profesional viral', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'estilo visual hiperrealista', 'estilo visual cinematográfico viral', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'estilo diorama hiperrealista', 'estilo diorama cinematográfico immersivo', prompt_video, flags=re.IGNORECASE)
        
        # ADICIONES PROFESIONALES ESPECÍFICAS (enriquecidas con metadatos)
        professional_additions = [
            "\n\nESPECIFICACIONES TÉCNICAS PROFESIONALES:",
            "- Cinematografía fluida con movimientos hipnóticos en slow motion",
            "- Audio ASMR binaural 3D perfectamente calibrado para auriculares", 
            "- Iluminación cinematográfica premium con contraste perfecto",
            "- Composición visual estudiada optimizada para formato vertical 9:16",
            "- Timing preciso diseñado para máximo retention rate en TikTok"
        ]
        
        # Enriquecer con información de metadatos si está disponible
        if image_context and "image_analysis" in image_context:
            analysis = image_context["image_analysis"]
            
            # Agregar información específica basada en el análisis
            if analysis.get("dominant_colors"):
                colors_str = ", ".join(analysis["dominant_colors"][:3])
                professional_additions.append(f"- Paleta de colores optimizada: {colors_str} para máximo impacto visual")
            
            if analysis.get("mood"):
                professional_additions.append(f"- Ambiente emocional: {analysis['mood']} diseñado para engagement")
            
            if analysis.get("movement_potential"):
                movements = ", ".join(analysis["movement_potential"][:2])
                professional_additions.append(f"- Elementos de movimiento viral: {movements}")
            
            if analysis.get("viral_hooks"):
                hooks = ", ".join(analysis["viral_hooks"][:2])
                professional_additions.append(f"- Hooks virales detectados: {hooks}")
        
        professional_additions.extend([
            "\nOBJETIVO VIRAL:",
            "Video ultra adictivo diseñado para generar rewatching compulsivo,",
            "shares orgánicos y engagement masivo. Optimizado para algoritmo",
            "TikTok con elementos que activan dopamine hits instantáneos."
        ])
        
        prompt_video += "\n".join(professional_additions)

        item_data = {
            "prompt": prompt_video.strip(), 
            "imagen": imagen,
            "viral_score": score,
            "legacy_enhanced": True
        }
        
        # Agregar contexto de imagen si está disponible
        if image_context:
            item_data["image_context"] = image_context
            item_data["detected_theme"] = image_context.get("image_analysis", {}).get("main_theme", "")
            
        mejores.append(item_data)

    print(f"{len(mejores)} prompts legacy mejorados seleccionados")
    for i, item in enumerate(mejores, 1):
        print(f"   {i}. Score viral: {item['viral_score']}")
        if item.get('detected_theme'):
            print(f"      Tema detectado: {item['detected_theme']}")
    
    return mejores

def main():
    print("GENERADOR DE VIDEOS VIRALES PROFESIONALES")
    print("=" * 60)
    
    # 1) Seleccionar mejores prompts (profesionales o legacy mejorados)
    mejores = seleccionar_mejores_imagenes_y_prompts()
    if not mejores:
        print("No hay imágenes disponibles (data/images/viral_image_*.png).")
        return

    print(f"{len(mejores)} prompts optimizados seleccionados:")
    for i, item in enumerate(mejores, 1):
        print(f"OPCION {i}:")
        print(f"   Imagen: {item['imagen']}")
        print(f"   Score viral: {item.get('viral_score', 'N/A')}")
        if 'metadata' in item and item['metadata']:
            try:
                metadata = item['metadata']
                if isinstance(metadata, dict):
                    print(f"   Categoria: {metadata.get('viral_category', 'N/A')}")
                    print(f"   Estilo: {metadata.get('style_preference', 'N/A')}")
                    target_demo = metadata.get('target_demographics', [])
                    if isinstance(target_demo, list) and target_demo:
                        print(f"   Target: {', '.join(target_demo)}")
                else:
                    print(f"    Metadata: {metadata}")
            except Exception:
                print(f"   Prompt profesional detectado")
        elif item.get('legacy_enhanced'):
            print(f"   Tipo: Legacy mejorado profesionalmente")
        # Mostrar preview del prompt
        prompt_preview = item['prompt'][:200].replace('\n', ' ')
        print(f"   Preview: {prompt_preview}...")
        print(f"   Longitud total: {len(item['prompt'])} caracteres")

    # Generación automática sin confirmación
    print(f"Iniciando generación automática de {len(mejores)} videos profesionales")
    print("   Esto puede tomar varios minutos por video...")
    print("   MODO AUTOMATICO - Sin intervención humana")

    # Inicializar cliente Veo
    print("Inicializando cliente Veo...")
    veo_client = GeminiWebClient()
    video_prompt_map = []

    # 2) Generar videos
    for i, item in enumerate(mejores[:3], 1):
        print(f"{'='*60}")
        print(f"GENERANDO VIDEO {i}/{len(mejores[:3])}")
        print(f"Imagen: {item['imagen']}")
        print(f"Score viral: {item.get('viral_score', 'N/A')}")
        print(f"{'='*60}")
        # Mostrar prompt completo para este video
        print(f"PROMPT PROFESIONAL:")
        print("-" * 40)
        print(item['prompt'])
        print("-" * 40)
        print(f"Enviando a Veo 3... (esto puede tomar 5-10 minutos)")

        # La lógica de cierre de explorador, scroll y mouse ya está en GeminiWebClient
        out = veo_client.generate_video_from_image_and_prompt(item["imagen"], item["prompt"])
        if out:
            video_data = {
                "video": out,
                "prompt": item["prompt"],
                "imagen": item["imagen"],
                "viral_score": item.get('viral_score'),
                "generation_timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            if item.get('metadata'):
                video_data["metadata"] = item["metadata"]
            video_prompt_map.append(video_data)
            print(f"Video {i} generado exitosamente: {out}")
            print(f"Score viral: {item.get('viral_score', 'N/A')}")
        else:
            print(f"Video {i} falló con Veo3 - intentando fallback Pollinations IA...")
            try:
                from pollinations_fallback import pollinations_generate_video
                poll_out = pollinations_generate_video(item["imagen"], item["prompt"])
                if poll_out:
                    video_data = {
                        "video": poll_out,
                        "prompt": item["prompt"],
                        "imagen": item["imagen"],
                        "viral_score": item.get('viral_score'),
                        "generation_timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "fallback": "pollinations"
                    }
                    if item.get('metadata'):
                        video_data["metadata"] = item["metadata"]
                    video_prompt_map.append(video_data)
                    print(f"Video {i} generado con Pollinations: {poll_out}")
                else:
                    print(f"Pollinations IA también falló para el video {i}")
            except Exception as e:
                print(f"Error en fallback Pollinations IA: {e}")

    # 3) Guardar mapeo con información profesional
    ensure_dir("data")
    timestamp = int(time.time())
    mapeo_file = f"video_prompt_map_professional_{timestamp}.json"
    
    final_data = {
        "videos": video_prompt_map,
        "generation_info": {
            "total_videos": len(video_prompt_map),
            "successful_generations": len([v for v in video_prompt_map if v.get("video")]),
            "average_viral_score": sum(v.get("viral_score", 0) for v in video_prompt_map) / len(video_prompt_map) if video_prompt_map else 0,
            "generation_date": time.strftime('%Y-%m-%d %H:%M:%S'),
            "system_version": "Professional Viral Prompts v2.0"
        }
    }
    
    with open(mapeo_file, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    # 4) Resumen final
    print(f"{'='*60}")
    print(f"GENERACION COMPLETADA")
    print(f"{'='*60}")
    print(f"Videos generados: {len(video_prompt_map)}")
    print(f"Score viral promedio: {final_data['generation_info']['average_viral_score']:.1f}")
    print(f"Mapeo guardado: {mapeo_file}")
    
    if video_prompt_map:
        print(f"VIDEOS GENERADOS:")
        for i, video in enumerate(video_prompt_map, 1):
            print(f"   {i}. {video['video']}")
            print(f"      Score: {video.get('viral_score', 'N/A')}")
            if video.get('metadata'):
                print(f"      Categoria: {video['metadata']['viral_category']}")
        print(f"PROXIMOS PASOS:")
        print(f"   1. Revisar videos en data/videos/")
        print(f"   2. Procesar para TikTok con crop_con_zoom.py")
        print(f"   3. Subir con el uploader automatizado")
        print(f"   4. Monitorear metricas de engagement")
    else:
        print(f"No se generaron videos. Revisar:")
        print(f"   - Limites de API Veo 3")
        print(f"   - Conexion a internet")
        print(f"   - Configuracion de GEMINI_API_KEY")

if __name__ == "__main__":
    main()