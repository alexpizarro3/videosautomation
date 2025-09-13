import json
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
import urllib.parse
import time
from src.utils.gemini_web_client import GeminiWebClient

# Cargar variables de entorno
load_dotenv()

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

def enhance_image_prompts_selenium(stories):
    """
    Mejora los prompts de imagen usando la UI de Gemini con Selenium.
    """
    enhanced_stories = stories.copy()
    
    enhancement_prompt_template = """
    Eres un experto en la creación de prompts para IA generativa de imágenes.
    Tu tarea es mejorar un prompt básico para que produzca imágenes de alta calidad,
    fotorrealistas y con una estética ASMR específica.

    PROMPT ORIGINAL:
    "{original_prompt}"

    MEJORAS REQUERIDAS:
    1.  **Detalles Técnicos:** Incorpora términos como "hyperrealistic", "4K", "8K", "cinematic lighting", "professional photography", "octane render".
    2.  **Estética ASMR:** Añade elementos visuales que evoquen sensaciones ASMR, como "satisfying textures", "glossy surfaces", "soft focus", "intricate details".
    3.  **Composición y Color:** Especifica una paleta de colores vibrante y una composición visualmente atractiva (ej. "dynamic composition", "vibrant color palette", "strong contrast").
    4.  **Claridad y Concisión:** El prompt final debe ser claro, directo y estar en inglés para maximizar la compatibilidad con los modelos de IA.

    RESPONDE ÚNICAMENTE CON UN OBJETO JSON que contenga una sola clave, "enhanced_prompt".
    No incluyas explicaciones, texto introductorio ni marcadores de código como ```json

    Ejemplo de respuesta:
    {
        "enhanced_prompt": "A hyperrealistic 4K image of a glossy, vibrant blue crystal being cut with a glowing laser, casting cinematic lighting and intricate details on a dark, satisfyingly textured surface, professional photography, octane render."
    }
    """
    
    client = None
    try:
        client = GeminiWebClient()
        
        for story_key, story in stories.items():
            print(f">> Mejorando prompts para: {story['titulo']}...")
            
            for seq_num in range(1, 4):
                seq_key = f'secuencia_{seq_num}'
                if seq_key in story:
                    original_prompt = story[seq_key]['prompt_imagen']
                    
                    # Formatear el prompt para la solicitud de mejora
                    current_prompt = enhancement_prompt_template.format(original_prompt=original_prompt)
                    
                    # Generar prompt mejorado usando Selenium
                    response_text = client.generate_text(current_prompt)
                    print(f"   -> Respuesta recibida: {response_text}")

                    if not response_text:
                        print(f"   -> [!] No se recibió respuesta para la secuencia {seq_num}. Usando prompt original.")
                        continue

                    try:
                        # La respuesta esperada es un JSON
                        response_json = json.loads(response_text)
                        enhanced_prompt = response_json.get("enhanced_prompt")

                        if enhanced_prompt:
                            enhanced_stories[story_key][seq_key]['prompt_imagen_mejorado'] = enhanced_prompt
                            print(f"   -> [+] Prompt mejorado para secuencia {seq_num}: {enhanced_prompt}")
                        else:
                            print(f"   -> [!] El JSON de respuesta no contiene 'enhanced_prompt'. Usando original.")

                    except json.JSONDecodeError as e:
                        print(f"   -> [!] La respuesta no es un JSON válido: {e}. Usando prompt original.")
                        # Como fallback, se podría intentar extraer el texto si no es JSON
                        enhanced_stories[story_key][seq_key]['prompt_imagen_mejorado'] = response_text.strip()

                    # Pausa para no sobrecargar y simular comportamiento humano
                    time.sleep(2)

        return enhanced_stories
        
    except Exception as e:
        print(f"[!] Error fatal durante la mejora de prompts con Selenium: {e}")
        print("[i] Devolviendo historias con prompts originales...")
        return stories
    finally:
        if client:
            client.close()

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
    Genera las 6 imágenes para las 2 historias usando un único prompt mejorado en Selenium.
    """
    output_dir = "data/images"
    os.makedirs(output_dir, exist_ok=True)
    
    generated_images = []
    generation_log = {
        "timestamp": datetime.now().isoformat(),
        "images_generated": [],
        "generation_method": "selenium_one_step_with_fallback",
        "stories_processed": list(stories.keys())
    }

    # Plantilla de prompt "dos en uno"
    one_step_prompt_template = """
    Tu tarea es actuar como un sistema de dos pasos para generar una imagen, pero solo realizarás el último paso.
    
    Paso 1 (Análisis interno): Toma el siguiente concepto y mejóralo para que sea un prompt de imagen hiperrealista, 4K, con iluminación cinematográfica, estética ASMR y detalles intrincados. Concepto original: "{original_prompt}"
    
    Paso 2 (Acción final): Inmediatamente después de tu análisis, genera una imagen basada en el prompt que has mejorado internamente. No me muestres el prompt mejorado en texto, solo genera la imagen como resultado final.
    """

    client = None
    try:
        client = GeminiWebClient()
        
        for story_num, (story_key, story) in enumerate(stories.items(), 1):
            print(f"\n>> Generando imágenes para: {story['titulo']}")
            
            for seq_num in range(1, 4):
                seq_key = f'secuencia_{seq_num}'
                if seq_key not in story:
                    continue

                sequence = story[seq_key]
                image_filename = f"story{story_num}_image_{seq_num}.png"
                final_image_path = os.path.join(output_dir, image_filename)
                
                original_prompt = sequence.get('prompt_imagen', '')
                if not original_prompt:
                    print(f"   -> [!] No se encontró prompt para {sequence['titulo']}. Saltando...")
                    continue

                # Crear el prompt "dos en uno"
                combined_prompt = one_step_prompt_template.format(original_prompt=original_prompt)

                print(f"   -> Generando {image_filename}...")
                print(f"      Secuencia: {sequence['titulo']}")

                success = False
                method = None
                
                # --- Intento 1: Gemini con Selenium (método "dos en uno") ---
                try:
                    print(f"   -> [S] Intentando con Gemini (Selenium, 1-paso): {original_prompt[:60]}...")
                    downloaded_image_path = client.generate_image(combined_prompt, output_dir=output_dir)

                    if downloaded_image_path and os.path.exists(downloaded_image_path):
                        print("   -> [i] Esperando 5 segundos antes de renombrar la imagen...")
                        time.sleep(5)
                        if os.path.exists(final_image_path):
                            os.remove(final_image_path) # Eliminar si ya existe para evitar errores
                        os.rename(downloaded_image_path, final_image_path)
                        
                        print(f"   -> [+] Imagen renombrada y guardada como: {image_filename}")
                        success = True
                        method = "gemini_selenium_one_step"
                    else:
                        raise Exception("El método generate_image no devolvió una ruta de archivo válida.")

                except Exception as e:
                    print(f"   -> [!] Falló la generación con Selenium: {e}")
                    success = False

                # --- Intento 2: Fallback a Pollinations ---
                if not success:
                    print("   -> [!] Falló Gemini (Selenium). Usando Pollinations.ai...")
                    time.sleep(1)
                    # Usamos el prompt original para el fallback
                    success = generate_images_pollinations(original_prompt, final_image_path)
                    if success:
                        method = "pollinations_fallback"

                # --- Registrar resultado ---
                log_entry = {
                    "filename": image_filename,
                    "story": story['titulo'],
                    "method": method if success else "all_failed",
                    "prompt": original_prompt,
                    "status": "generated" if success else "failed"
                }
                generation_log["images_generated"].append(log_entry)
                
                if success:
                    generated_images.append(image_filename)
                
                time.sleep(2) # Pausa entre generaciones

    except Exception as e:
        print(f"\n[!] Error fatal en el proceso de generación de imágenes: {e}")
    finally:
        if client:
            client.close()

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
    
    # 2. Generar imágenes (proceso unificado)
    print(">> Generando 6 imágenes (3 por historia) con método de 1 solo paso...")
    generated_images, generation_log = generate_story_images(stories)
    
    # 3. Verificar resultados
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
