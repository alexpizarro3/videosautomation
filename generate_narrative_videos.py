import json
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import requests
import time
from src.utils.gemini_web_client import GeminiWebClient

# Cargar variables de entorno
load_dotenv()

def load_winning_story_data():
    """
    Carga los datos de la historia ganadora y evaluación
    """
    evaluation_file = 'data/analytics/story_evaluation.json'
    stories_file = 'data/analytics/story_prompts_narrative.json'
    
    if not os.path.exists(evaluation_file):
        print(f"❌ Error: No se encontró {evaluation_file}")
        print("📋 Ejecuta primero: python select_best_story.py")
        return None, None
    
    # Cargar evaluación
    with open(evaluation_file, 'r', encoding='utf-8') as f:
        evaluation = json.load(f)
    
    # Cargar historias originales
    with open(stories_file, 'r', encoding='utf-8') as f:
        stories_data = json.load(f)
    
    winning_story_key = evaluation['seleccion']['historia_seleccionada']
    winning_story = stories_data['stories_generated'][winning_story_key]
    
    print(f"🏆 Historia seleccionada: {winning_story['titulo']}")
    return winning_story, evaluation

def verify_images():
    """
    Verifica que las imágenes necesarias estén disponibles
    """
    required_images = [
        'data/images/gemini_image_1.png',
        'data/images/gemini_image_2.png', 
        'data/images/gemini_image_3.png'
    ]
    
    available_images = []
    for img_path in required_images:
        if os.path.exists(img_path):
            available_images.append(img_path)
        else:
            print(f"❌ Imagen faltante: {img_path}")
    
    print(f"🖼️  Imágenes disponibles: {len(available_images)}/3")
    return available_images

def create_narrative_video_prompts(winning_story):
    """
    Crea prompts específicos para cada video que mantenga la narrativa ASMR
    """
    narrative_prompts = []
    
    # Información base de la historia
    story_title = winning_story.get('titulo', '')
    story_concept = winning_story.get('concepto_general', '')
    asmr_audio = winning_story.get('sonido_envolvente', '')
    
    # Crear prompts para cada secuencia
    for seq_num in range(1, 4):
        seq_key = f'secuencia_{seq_num}'
        
        if seq_key in winning_story:
            sequence = winning_story[seq_key]
            
            # Prompt específico para video narrativo con ASMR
            video_prompt = f"""
            HISTORIA: {story_title}
            SECUENCIA {seq_num}: {sequence['titulo']}
            
            DESCRIPCIÓN VISUAL: {sequence['descripcion_visual']}
            ELEMENTOS ASMR: {sequence['elementos_asmr']}
            
            INSTRUCCIONES PARA VIDEO:
            - Crear video de 4-6 segundos basado en la imagen proporcionada
            - Mantener continuidad narrativa con las secuencias anteriores
            - Incluir movimientos sutiles que realcen los elementos ASMR
            - Sonido envolvente: {asmr_audio}
            - Audio específico: {sequence['elementos_asmr']}
            - Sin efectos visuales de ecualizador o elementos de audio visibles
            - Movimientos fluidos y hipnóticos
            - Transiciones suaves para conexión narrativa
            - Enfoque en texturas, sonidos y experiencias sensoriales
            - Mantener estética viral de TikTok
            
            CONTINUIDAD NARRATIVA:
            - Este es el capítulo {seq_num} de 3 de la historia "{story_title}"
            - Debe conectar visualmente con las secuencias previas
            - Crear expectativa para la siguiente secuencia (si no es la última)
            - Mantener coherencia de iluminación, estilo y ambiente
            
            AUDIO ENVOLVENTE ESPECÍFICO:
            - Sonidos principales: {sequence['elementos_asmr']}
            - Ambiente sonoro: Continuo y envolvente
            - Sin música de fondo, solo sonidos ASMR puros
            - Audio binaural para máxima inmersión
            - Sonidos adictivos que mantengan la atención
            """
            
            narrative_prompts.append({
                'secuencia': seq_num,
                'titulo': sequence['titulo'],
                'imagen_source': f'data/images/gemini_image_{seq_num}.png',
                'video_output': f'data/videos/narrative_video_{seq_num}.mp4',
                'prompt_completo': video_prompt.strip(),
                'elementos_asmr': sequence['elementos_asmr'],
                'duracion_estimada': '4-6 segundos'
            })
    
    return narrative_prompts

def enhance_video_prompt(client, prompt_data):
    """
    Mejora el prompt usando la app web de Gemini para optimización de Veo3.
    """
    enhancement_prompt = f"""
    Optimiza este prompt para la generación de video con Veo3 manteniendo la narrativa ASMR:
    
    PROMPT ORIGINAL:
    {prompt_data['prompt_completo']}
    
    MEJORAS NECESARIAS:
    - Hacer más específico para generación de video
    - Optimizar para Veo3 y contenido viral
    - Mantener el enfoque ASMR envolvente
    - Especificar movimientos y transiciones
    - Detallar los elementos sonoros sin efectos visuales
    - Asegurar que sea adictivo y viral
    
    RESPONDE SOLO CON EL PROMPT OPTIMIZADO PARA VEO3:
    """
    
    try:
        optimized_prompt = client.generate_text(enhancement_prompt)
        print(f"✨ Prompt optimizado para secuencia {prompt_data['secuencia']}")
        return optimized_prompt.strip()
        
    except Exception as e:
        print(f"⚠️ Error optimizando prompt: {e}")
        return prompt_data['prompt_completo']

# This function is now replaced by the Veo3 generation method in GeminiWebClient.

def create_video_generation_batch(narrative_prompts):
    """
    Crea un lote de generación para todos los videos narrativos
    """
    generation_batch = {
        "timestamp": datetime.now().isoformat(),
        "story_type": "narrative_asmr",
        "total_videos": len(narrative_prompts),
        "generation_method": "veo3_sequential",
        "asmr_settings": {
            "sound_type": "envolvente",
            "audio_mode": "binaural",
            "no_visual_equalizers": True,
            "continuous_narrative": True
        },
        "videos_to_generate": []
    }
    
    for prompt_data in narrative_prompts:
        video_info = {
            "sequence": prompt_data['secuencia'],
            "title": prompt_data['titulo'],
            "source_image": prompt_data['imagen_source'],
            "output_video": prompt_data['video_output'],
            "asmr_elements": prompt_data['elementos_asmr'],
            "duration": prompt_data['duracion_estimada'],
            "prompt": prompt_data['prompt_completo'],
            "narrative_position": f"{prompt_data['secuencia']}/3"
        }
        generation_batch["videos_to_generate"].append(video_info)
    
    return generation_batch

def generate_narrative_videos(narrative_prompts):
    """
    Genera los 3 videos narrativos secuenciales
    """
    generated_videos = []
    generation_log = {
        "timestamp": datetime.now().isoformat(),
        "narrative_generation": True,
        "videos_generated": [],
        "asmr_continuous": True
    }
    
    print("🎬 Iniciando generación de videos narrativos...")
    
    for i, prompt_data in enumerate(narrative_prompts, 1):
        print(f"\n📹 Generando video {i}/3: {prompt_data['titulo']}")
        
        # Verificar que la imagen existe
        if not os.path.exists(prompt_data['imagen_source']):
            print(f"❌ Imagen no encontrada: {prompt_data['imagen_source']}")
            continue
        
        # Optimizar prompt para Veo3
        print("✨ Optimizando prompt para Veo3...")
        optimized_prompt = enhance_video_prompt(prompt_data)
        
        # Generar video
        success = generate_video_with_fallback(
            optimized_prompt,
            prompt_data['imagen_source'],
            prompt_data['video_output']
        )
        
        # Registrar resultado
        video_result = {
            "sequence": prompt_data['secuencia'],
            "title": prompt_data['titulo'],
            "output_file": prompt_data['video_output'],
            "source_image": prompt_data['imagen_source'],
            "asmr_elements": prompt_data['elementos_asmr'],
            "status": "generated" if success else "failed",
            "prompt_used": optimized_prompt
        }
        
        generation_log["videos_generated"].append(video_result)
        
        if success:
            generated_videos.append(prompt_data['video_output'])
            print(f"✅ Video {i} generado exitosamente")
        else:
            print(f"❌ Error generando video {i}")
    
    return generated_videos, generation_log

def save_generation_results(narrative_prompts, generation_log, batch_info):
    """
    Guarda los resultados de la generación narrativa
    """
    os.makedirs('data/analytics', exist_ok=True)
    
    complete_results = {
        "timestamp": datetime.now().isoformat(),
        "generation_type": "narrative_asmr_videos",
        "story_completed": True,
        "videos_in_sequence": len(narrative_prompts),
        "asmr_continuous": True,
        "narrative_prompts": narrative_prompts,
        "generation_log": generation_log,
        "batch_info": batch_info,
        "next_step": "procesar_final_tiktok.py",
        "pipeline_status": "ready_for_processing"
    }
    
    # Guardar resultados completos
    results_file = 'data/analytics/narrative_video_generation.json'
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(complete_results, f, indent=2, ensure_ascii=False)
    
    # Guardar batch de generación para referencia
    batch_file = 'data/analytics/veo3_generation_batch.json'
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(batch_info, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados guardados en: {results_file}")
    print(f"📋 Batch info en: {batch_file}")
    
    return results_file

def main():
    """
    Función principal que ejecuta la generación de videos narrativos
    """
    print("🎭 Iniciando generación de videos narrativos ASMR...")
    
    # 1. Cargar historia ganadora
    print("🏆 Cargando historia ganadora...")
    winning_story, evaluation = load_winning_story_data()
    
    if not winning_story:
        return False
    
    # 2. Verificar imágenes
    print("🖼️  Verificando imágenes...")
    available_images = verify_images()
    
    if len(available_images) < 3:
        print("❌ Faltan imágenes necesarias")
        return False
    
    # 3. Crear prompts narrativos
    print("📝 Creando prompts narrativos secuenciales...")
    narrative_prompts = create_narrative_video_prompts(winning_story)
    
    # 4. Crear batch de generación
    print("📋 Preparando batch de generación...")
    batch_info = create_video_generation_batch(narrative_prompts)
    
    # 5. Generar videos narrativos
    print("🎬 Generando videos con narrativa ASMR envolvente...")
    generated_videos, generation_log = generate_narrative_videos(narrative_prompts)
    
    # 6. Guardar resultados
    print("💾 Guardando resultados de generación...")
    results_file = save_generation_results(narrative_prompts, generation_log, batch_info)
    
    # 7. Reporte final
    print(f"\n📊 REPORTE DE GENERACIÓN:")
    print(f"🎬 Videos programados: {len(narrative_prompts)}")
    print(f"✅ Videos procesados: {len(generated_videos)}")
    print(f"🎵 ASMR envolvente: Activado")
    print(f"📚 Narrativa secuencial: Completa")
    
    if len(generated_videos) == 3:
        print(f"\n🎉 ¡Generación narrativa completada!")
        print(f"📂 Videos listos en: data/videos/")
        print(f"📋 Siguiente paso: python procesar_final_tiktok.py")
        return True
    else:
        print(f"\n⚠️  Generación completada con advertencias")
        print(f"📝 Revisa los archivos _info.json para detalles")
        return False

if __name__ == "__main__":
    main()
