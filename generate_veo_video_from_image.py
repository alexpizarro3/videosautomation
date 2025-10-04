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
    
    # ANÁLISIS DE METADATOS
    try:
        metadata_analyzer = ImageMetadataAnalyzer()
        print("   Analizador de metadatos inicializado")
    except Exception as e:
        print(f"   Error inicializando analizador: {e}")
        print("   Continuando con sistema legacy...")
        metadata_analyzer = None
    
    # PRIMERA OPCIÓN: Usar prompts profesionales si existen
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
            )
            
            mejores = []
            
            imagenes = [f"data/images/viral_image_{i+1}.png" for i in range(6)]
            
            # Score images based on their content
            scored_images = []
            for i, imagen in enumerate(imagenes):
                if os.path.exists(imagen):
                    image_context = metadata_analyzer.get_video_prompt_context(imagen) if metadata_analyzer else {}
                    score = image_context.get("image_analysis", {}).get("aesthetic_score", 0)
                    scored_images.append((score, imagen))
            
            # Sort images by score and take the top 3
            top_images = sorted(scored_images, reverse=True)[:3]

            for i, (score, imagen) in enumerate(top_images):
                # Mapear prompt a imagen seleccionada inteligentemente
                enhanced_prompt = sorted_prompts[i]
                
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
                    
                    # --- MODIFICACIÓN PARA INYECTAR ELEMENTOS DINÁMICOS ---
                    original_prompt = enhanced_prompt["prompt"]
                    
                    # Elementos dinámicos a inyectar
                    dynamic_elements_to_add = "Adicionalmente, la escena debe fusionar elementos de hielo, fuego y lava en un torbellino dinámico, con transparencias de colores vibrantes y cortes rítmicos estilo ASMR."

                    # Buscamos la sección CONCEPTO VISUAL para añadir los elementos
                    visual_concept_marker = "CONCEPTO VISUAL:"
                    
                    modified_prompt = original_prompt
                    if visual_concept_marker in original_prompt:
                        lines = original_prompt.split('\n')
                        for i, line in enumerate(lines):
                            if visual_concept_marker in line:
                                # Añadir los elementos después de la línea del concepto visual
                                lines.insert(i + 1, dynamic_elements_to_add)
                                modified_prompt = '\n'.join(lines)
                                break
                    else:
                        # Si no hay sección, la creamos al principio
                        modified_prompt = f"{visual_concept_marker}\n{dynamic_elements_to_add}\n\n{original_prompt}"
                    # --- FIN DE LA MODIFICACIÓN ---

                    item_data = {
                        "prompt": modified_prompt,
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
    
    # FALLBACK: Sistema legacy mejorado
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
        'cottagecore', 'aesthetic', 'liminal', 'hypnotic', 'therapeutic', 'immersive',
        'oddly satisfying', 'satisfacción', 'relajante'
    ]

trending_keywords = ['challenge', 'storytime', 'tutorial', 'unboxing', 'review']

def score_prompt(p: str) -> int:
    s = 0
    low = p.lower()
    
    # Score básico por keywords
    for kw in keywords_virales:
        if kw in low:
            s += 1

    # Score por trending keywords
    for kw in trending_keywords:
        if kw in low:
            s += 2
            
    # Bonificaciones especiales
    s += low.count('asmr') * 3  # ASMR es muy viral
    s += low.count('adictivo') * 2
    s += low.count('viral') * 2
    s += low.count('satisfying') * 3
    s += low.count('oddly satisfying') * 4
    s += low.count('hipnótico') * 2
    
    # Bonus por elementos técnicos
    technical_terms = ['hiperrealista', 'cinematográfico', 'profesional', 'ultra', '4k']
    for term in technical_terms:
        if term in low:
            s += 1
            
    return s

    scored = [(score_prompt(p), i, p) for i, p in enumerate(prompts)]
    
    print("Scores de todos los prompts:")
    for score, idx, p in scored:
        print(f"  - Prompt {idx+1}: Score {score}")

    top3_prompts = sorted(scored, reverse=True)[:3]

    # --- NEW LOGIC: Score and sort images independently ---
    print("\nScoring images based on aesthetic and viral potential...")
    scored_images = []
    if metadata_analyzer:
        for imagen_path in imagenes:
            if os.path.exists(imagen_path):
                try:
                    # Use a more comprehensive scoring from metadata
                    image_context = metadata_analyzer.get_video_prompt_context(imagen_path)
                    if image_context and not image_context.get('error'):
                        analysis = image_context.get("image_analysis", {})
                        # Combine multiple metrics for a more robust score
                        aesthetic_score = analysis.get("aesthetic_score", 0)
                        clarity_score = analysis.get("clarity_score", 0)
                        # A simple composite score
                        composite_score = (aesthetic_score * 0.7) + (clarity_score * 0.3)
                        scored_images.append((composite_score, imagen_path))
                        print(f"  - {os.path.basename(imagen_path)}: Score {composite_score:.2f}")
                    else:
                        # Fallback for images that can't be analyzed
                        scored_images.append((0, imagen_path))
                        print(f"  - {os.path.basename(imagen_path)}: Could not analyze, score 0")
                except Exception as e:
                    print(f"  - Error scoring {os.path.basename(imagen_path)}: {e}")
                    scored_images.append((0, imagen_path))
            else:
                # Handle missing images gracefully
                scored_images.append((-1, imagen_path)) # Use -1 to ensure they are at the bottom
    else:
        # If no analyzer, just use existing images in order
        print("   Metadata analyzer not available. Using images in default order.")
        scored_images = [(0, img) for img in imagenes if os.path.exists(img)]

    # Sort images by their score, highest first, and filter out non-existent ones
    top_images = [img for score, img in sorted(scored_images, reverse=True) if score >= 0]
    
    if not top_images:
        print("\n❌ No suitable images found after scoring. Aborting video generation.")
        return []
    # --- END NEW LOGIC ---

    mejores = []
    
    print("\nTop 3 prompts and images selected:")
    # Pair top prompts with top images
    for i, (prompt_data, imagen) in enumerate(zip(top3_prompts, top_images)):
        (score, idx, prompt_original) = prompt_data
        print(f"  {i+1}. Prompt {idx+1} (Score: {score}) paired with Image {os.path.basename(imagen)}")
        
        if not imagen: # Should not happen with the new logic, but as a safeguard
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
        
        # Inicializar el prompt con un concepto base
        prompt_video = "Crea un video inmersivo y ultra-viral."

        # Usar el análisis de la imagen como el núcleo del prompt si está disponible
        if image_context and "image_analysis" in image_context:
            analysis = image_context["image_analysis"]
            main_theme = analysis.get("main_theme", "una escena visualmente impactante")
            
            # Construir el concepto visual dinámicamente
            visual_concept = f"CONCEPTO VISUAL:\nCrea un video cinematográfico inmersivo de {main_theme}, fusionando elementos de hielo, fuego y lava en un torbellino dinámico. Incorpora transparencias de colores vibrantes que fluyen y se mezclan, creando un efecto visual hipnótico. El ritmo del video debe tener cortes rápidos y precisos al estilo ASMR, sincronizados con los efectos visuales para una máxima satisfacción. "
            
            if analysis.get("dominant_colors"):
                colors_str = ", ".join(analysis["dominant_colors"][:3])
                visual_concept += f"La paleta de colores debe ser similar a {colors_str}, evocando un ambiente {analysis.get('mood', 'cautivador')}. "
            
            if analysis.get("detected_objects"):
                objects_str = ", ".join(analysis["detected_objects"][:4])
                visual_concept += f"Destaca los siguientes elementos: {objects_str}. "

            prompt_video += "\n\n" + visual_concept

        else:
            # Fallback si no hay análisis de imagen
            prompt_video += "\n\nCONCEPTO VISUAL:\n" + prompt_original

        # ADICIONES PROFESIONALES ESPECÍFICAS (enriquecidas con metadatos)
        professional_additions = [
            "\n\nESPECIFICACIONES TÉCNICAS:",
            "- Cinematografía fluida con movimientos suaves e hipnóticos en slow motion para una experiencia inmersiva.",
            "- Efectos visuales sutiles que amplifican la experiencia.",
            "- Iluminación cinematográfica premium con contraste perfecto.",
            "- Composición visual estudiada optimizada para formato vertical 9:16.",
            "- Timing preciso diseñado para máximo retention rate en TikTok."
        ]

        # DISEÑO DE AUDIO
        audio_design = [
            "\n\nDISEÑO DE AUDIO (NO NEGOCIABLE):",
            "- Sonido 100% ASMR envolvente de principio a fin.",
            "- Frecuencias específicas que activan una fuerte respuesta ASMR (tingles).",
            "- Ambiente sonoro totalmente inmersivo y relajante.",
            "- Masterizado profesionalmente para auriculares y altavoces móviles."
        ]

        # ELEMENTOS VIRALES
        viral_elements = [
            "\n\nELEMENTOS VIRALES (FOCO PRINCIPAL):",
            "- Potencial viral extremo, diseñado para ser compartido masivamente.",
            "- Calibrado para rewatching infinito y loops perfectos.",
            "- Duración ideal 15-30 segundos.",
            "- Timing calculado para máximo dopamine hit y engagement."
        ]
        
        # ESTILO VISUAL
        visual_style = [
            "\n\nESTILO VISUAL:",
            "Renderizado hiperrealista cinematográfico con acabado profesional de estudio."
        ]

        # OBJETIVO
        objective = [
            "\n\nOBJETIVO PRINCIPAL:",
            "Crear el video más viral posible. El objetivo es máximo engagement, shares orgánicos y un retention rate superior al 85%. "
        ]

        # Unir todas las secciones
        prompt_video += "\n".join(professional_additions)
        prompt_video += "\n".join(audio_design)
        prompt_video += "\n".join(viral_elements)
        prompt_video += "\n".join(visual_style)
        prompt_video += "\n".join(objective)

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
        print(f"   Preview: {prompt_preview}...\n")
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
            "average_viral_score": sum(v.get('viral_score', 0) for v in video_prompt_map) / len(video_prompt_map) if video_prompt_map else 0,
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
        print(f"   -Conexion a internet")
        print(f"   - Configuracion de GEMINI_API_KEY")

if __name__ == "__main__":
    main()