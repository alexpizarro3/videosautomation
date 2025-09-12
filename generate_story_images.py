import json
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
import urllib.parse
import time
from google import genai
from google.genai import types

from PIL import Image
from io import BytesIO
from google.generativeai import types

# Cargar variables de entorno
load_dotenv()

# Configurar APIs
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No se encontró GEMINI_API_KEY en las variables de entorno. Verifica tu archivo .env.")

def load_story_prompts():
    """
    Carga las historias narrativas generadas previamente
    """
    story_file = 'data/analytics/story_prompts_narrative.json'
    
    if not os.path.exists(story_file):
        print(f"[!] Error: No se encontró {story_file}")
        print(">> Ejecuta primero: python generate_story_prompts_from_scrap.py")
        return None
    
    try:
        with open(story_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        stories = data.get('stories_generated', {})
        print(f"[+] Historias cargadas: {len(stories)} historias encontradas")
        return stories
    
    except Exception as e:
        print(f"[!] Error cargando historias: {e}")
        return None

def enhance_image_prompts(stories):
    """
    Mejora los prompts de imagen usando IA para mayor calidad
    """
    enhanced_stories = {}
    
    enhancement_prompt = """
    Mejora este prompt para generación de imágenes, hazlo más específico y visual para ASMR:
    
    PROMPT ORIGINAL: {original_prompt}
    
    MEJORAS NECESARIAS:
    - Añadir detalles técnicos de fotografía (4K, hyperrealistic, professional lighting)
    - Incluir elementos ASMR específicos (texturas, materiales, superficies)
    - Especificar colores, iluminación y composición
    - Añadir términos que mejoren la calidad visual
    - Mantener el concepto ASMR narrativo original
    
    RESPONDE SOLO CON EL PROMPT MEJORADO, SIN EXPLICACIONES:
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        for story_key, story in stories.items():
            enhanced_stories[story_key] = story.copy()
            
            print(f">> Mejorando prompts para {story['titulo']}...")
            
            # Mejorar prompts de cada secuencia
            for seq_num in range(1, 4):
                seq_key = f'secuencia_{seq_num}'
                if seq_key in story:
                    original_prompt = story[seq_key]['prompt_imagen']
                    
                    # Generar prompt mejorado
                    current_prompt = enhancement_prompt.format(original_prompt=original_prompt)
                    response = model.generate_content(current_prompt)
                    enhanced_prompt = response.text.strip()
                    
                    # Actualizar con prompt mejorado
                    enhanced_stories[story_key][seq_key]['prompt_imagen_mejorado'] = enhanced_prompt
                    
                    # Pequeña pausa para evitar rate limits
                    time.sleep(1)
        
        return enhanced_stories
        
    except Exception as e:
        print(f"[!] Error mejorando prompts: {e}")
        print("[i] Usando prompts originales...")
        return stories

def generate_image_with_gemini(prompt: str, image_path: str, model_name: str, previous_sequence_title: str | None = None) -> bool:
    """
    Genera una imagen usando un modelo específico de la API de Gemini.
    Si se proporciona 'previous_sequence_title', lo usa como contexto para la secuencia.
    """
    try:
        print(f"   -> [G] Intentando con Gemini ({model_name}): {prompt[:60]}...")
        from google import genai
        from PIL import Image
        from io import BytesIO
        client = genai.Client(api_key=api_key)
        final_prompt = prompt
        if previous_sequence_title:
            print(f"   -> Usando contexto de secuencia anterior: '{previous_sequence_title}'")
            final_prompt = f"Crea la siguiente imagen en la secuencia, continuando la narrativa visual de la imagen anterior que mostraba '{previous_sequence_title}'. Ahora, genera esta nueva escena: {prompt}"
        # Ajuste para el modelo 2.0: requiere modalidad ['TEXT', 'IMAGE']
        if model_name == "gemini-2.0-flash-preview-image-generation":
            response = client.models.generate_content(
                model=model_name,
                contents=final_prompt,
                response_modalities=['TEXT', 'IMAGE']
            )
        else:
            response = client.models.generate_content(
                model=model_name,
                contents=final_prompt
            )
        if response and response.candidates:
            candidate = response.candidates[0]
            parts = getattr(candidate.content, 'parts', None)
            if parts:
                for part in parts:
                    inline_data = getattr(part, 'inline_data', None)
                    data = getattr(inline_data, 'data', None) if inline_data else None
                    if data:
                        try:
                            image = Image.open(BytesIO(data))
                            os.makedirs(os.path.dirname(image_path), exist_ok=True)
                            image.save(image_path)
                            print(f"   -> [+] Imagen Gemini guardada: {os.path.basename(image_path)}")
                            return True
                        except Exception as img_e:
                            print(f"   -> [!] Error procesando imagen Gemini: {img_e}")
        print(f"   -> [!] El modelo '{model_name}' no devolvió una imagen válida.")
        return False
    except Exception as e:
        error_message = str(e).lower()
        print(f"   -> [!] Error con modelo {model_name}.")
        if "api_key" in error_message:
            print("       Causa probable: La API Key de Gemini es inválida o no está configurada.")
            print("       Solución: Verifica el archivo .env y la variable GEMINI_API_KEY.")
        elif "not found" in error_message or "404" in error_message:
            print(f"       Causa probable: El modelo '{model_name}' no está disponible para tu cuenta o no existe.")
            print("       Solución: Verifica los modelos disponibles en tu consola de Google AI.")
        elif "quota" in error_message or "resource_exhausted" in error_message:
            print("       Causa probable: Has excedido la cuota de uso de la API (rate limit).")
            print("       Solución: Espera unos minutos antes de volver a intentarlo.")
        else:
            print(f"       Detalle del error: {e}")
        return False

def generate_images_pollinations(prompt, image_path):
    """
    Genera imágenes usando Pollinations.ai como alternativa
    """
    try:
        print("   -> [P] Usando fallback: Pollinations.ai...")
        # Mejorar prompt para Pollinations
        enhanced_prompt = f"{prompt}, 4K, hyperrealistic, professional photography, ASMR aesthetic, viral content"
        
        # URL de Pollinations.ai
        url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(enhanced_prompt, safe='')
        
        # Realizar petición
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            # Guardar imagen
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            
            print(f"[+] Imagen generada: {os.path.basename(image_path)}")
            return True
        else:
            print(f"[!] Error en API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[!] Error generando imagen con Pollinations: {e}")
        return False

def create_fallback_images():
    """
    Crea archivos placeholder si no se pueden generar imágenes
    """
    image_info = [
        ("story1_image_1.png", "Chef de Cristal - Secuencia 1"),
        ("story1_image_2.png", "Chef de Cristal - Secuencia 2"), 
        ("story1_image_3.png", "Chef de Cristal - Secuencia 3"),
        ("story2_image_1.png", "Texturas Mágicas - Secuencia 1"),
        ("story2_image_2.png", "Texturas Mágicas - Secuencia 2"),
        ("story2_image_3.png", "Texturas Mágicas - Secuencia 3")
    ]
    
    # Crear directorio
    os.makedirs('data/images', exist_ok=True)
    
    for filename, description in image_info:
        filepath = f"data/images/{filename}"
        
        # Crear archivo de texto como placeholder
        with open(filepath.replace('.png', '_prompt.txt'), 'w', encoding='utf-8') as f:
            f.write(f"Placeholder para: {description}\n")
            f.write(f"Archivo: {filename}\n")
            f.write("Generar imagen con herramienta externa usando este prompt.\n")
        
        print(f"[i] Placeholder creado: {filename}")

def generate_story_images(stories):
    """
    Genera las 6 imágenes para las 2 historias
    """
    # Crear directorio si no existe
    os.makedirs('data/images', exist_ok=True)
    
    generated_images = []
    generation_log = {
        "timestamp": datetime.now().isoformat(),
        "images_generated": [],
        "generation_method": "gemini_with_fallback",
        "stories_processed": list(stories.keys())
    }
    
    # Generar imágenes para cada historia
    for story_num, (story_key, story) in enumerate(stories.items(), 1):
        print(f"\n>> Generando imágenes para: {story['titulo']}")
        
        # Generar 3 imágenes por historia
        for seq_num in range(1, 4):
            seq_key = f'secuencia_{seq_num}'
            
            if seq_key in story:
                sequence = story[seq_key]
                
                # Nombre del archivo
                image_filename = f"story{story_num}_image_{seq_num}.png"
                image_path = f"data/images/{image_filename}"
                
                # Obtener prompt (mejorado si existe, original si no)
                prompt = sequence.get('prompt_imagen_mejorado', 
                                    sequence.get('prompt_imagen', ''))
                
                print(f"   -> Generando {image_filename}...")
                print(f"      Secuencia: {sequence['titulo']}")
                
                # Determinar si hay una imagen previa para dar contexto
                previous_sequence_title = story.get(f'secuencia_{seq_num-1}', {}).get('titulo') if seq_num > 1 else None
                
                # Fallback chain: Gemini 2.5 -> Pollinations
                method = None
                success = False
                # 1. Gemini 2.5 Flash Image Preview
                print(f"   -> [FALLBACK] Intentando Gemini 2.5 Flash Image Preview...")
                success = generate_image_with_gemini(prompt, image_path, "gemini-2.5-flash-image-preview", previous_sequence_title)
                if success:
                    method = "gemini-2.5-flash-image-preview"
                else:
                    print("   -> [!] Gemini 2.5 falló. Usando Pollinations.ai...")
                    time.sleep(1)
                    success = generate_images_pollinations(prompt, image_path)
                    if success:
                        method = "pollinations_fallback"
                if success:
                    generated_images.append(image_filename)
                    generation_log["images_generated"].append({
                        "filename": image_filename,
                        "story": story['titulo'],
                        "method": method,
                        "prompt": prompt,
                        "status": "generated"
                    })
                else:
                    generation_log["images_generated"].append({
                        "filename": image_filename,
                        "method": "all_failed",
                        "sequence": sequence['titulo'],
                        "prompt": prompt,
                        "status": "failed"
                    })
                # Pausa entre generaciones
                time.sleep(2)
    
    # Guardar log de generación
    log_path = 'data/analytics/image_generation_log.json'
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(generation_log, f, indent=2, ensure_ascii=False)
    
    return generated_images, generation_log

def verify_and_report(generated_images, total_expected=6):
    """
    Verifica las imágenes generadas y crea reporte
    """
    print(f"\n[+] REPORTE DE GENERACIÓN:")
    print(f"[+] Imágenes generadas: {len(generated_images)}/{total_expected}")
    
    if len(generated_images) == total_expected:
        print(">> ¡Todas las imágenes fueron generadas exitosamente!")
        print("   Siguiente paso: python select_best_story.py")
        return True
    else:
        print("[!] Algunas imágenes no se pudieron generar")
        missing = total_expected - len(generated_images)
        print(f"[!] Faltantes: {missing} imágenes")
        
        # Crear placeholders para las faltantes si es necesario
        print("[i] Creando placeholders para imágenes faltantes...")
        create_fallback_images()
        
        return False

def main():
    """
    Función principal que ejecuta todo el proceso
    """
    print(">> Iniciando generación de imágenes narrativas...")
    
    # 1. Cargar historias
    print(">> Cargando historias narrativas...")
    stories = load_story_prompts()
    
    if not stories:
        return False
    
    # 2. Mejorar prompts
    print(">> Mejorando prompts de imagen con IA...")
    enhanced_stories = enhance_image_prompts(stories)
    
    # 3. Generar imágenes
    print(">> Generando 6 imágenes (3 por historia)...")
    generated_images, generation_log = generate_story_images(enhanced_stories)
    
    # 4. Verificar resultados
    success = verify_and_report(generated_images)
    
    if success:
        print(f"\n>> ¡Proceso completado exitosamente!")
        print(f"[i] Imágenes en: data/images/")
        print(f"[i] Log en: data/analytics/image_generation_log.json")
    else:
        print(f"\n[!] Proceso completado con advertencias")
        print(f"[i] Revisa el log para detalles")
    
    return success

if __name__ == "__main__":
    main()
