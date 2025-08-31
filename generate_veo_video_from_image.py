import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def generar_descripcion_y_hashtags(prompt):
    hashtags_base = [
        '#Viral', '#ASMR', '#Capybara', '#Relax', '#FYP', '#HamsterCore', '#FantasyArt', '#ViralVideo', '#TikTokViral', '#ArteDigital', '#Neon', '#Gelatina', '#Acuario', '#Explosión', '#Sonido', '#Adictivo', '#Estilo', '#Tendencia', '#Viral2025', '#ViralTikTok'
    ]
    # Extraer palabras clave del prompt
    palabras = [w for w in prompt.split() if len(w) > 4]
    hashtags_prompt = [f'#{w.capitalize()}' for w in palabras if w.isalpha()][:5]
    hashtags = list(set(hashtags_prompt + random.sample(hashtags_base, 5)))[:5]
    descripcion = f"{prompt}\n\nDisfruta este video viral con sonido envolvente y efectos ASMR. ¡No olvides seguirme para más contenido único!"
    return descripcion, hashtags

def subir_a_tiktok(video_path, descripcion, hashtags):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.tiktok.com/upload')
    # Esperar carga y subir video
    driver.implicitly_wait(10)
    upload_input = driver.find_element(By.XPATH, '//input[@type="file"]')
    upload_input.send_keys(video_path)
    # Esperar procesamiento
    driver.implicitly_wait(30)
    desc_box = driver.find_element(By.XPATH, '//textarea')
    desc_box.clear()
    desc_box.send_keys(descripcion + '\n' + ' '.join(hashtags))
    # Publicar (puede requerir login manual la primera vez)
    publish_btn = driver.find_element(By.XPATH, '//button[contains(text(),"Publicar")]')
    publish_btn.click()
    driver.quit()
    print(f"✅ Video subido automáticamente a TikTok: {video_path}")
# --- Selección automática de las 3 mejores imágenes y prompts ---
import json

def seleccionar_mejores_imagenes_y_prompts():
    # Cargar prompts
    with open("data/analytics/fusion_prompts_auto.json", "r", encoding="utf-8") as f:
        prompts_data = json.load(f)
    prompts = prompts_data["prompts"]

    # Asumimos que las imágenes se llaman gemini_image_1.png ... gemini_image_6.png
    imagenes = [f"gemini_image_{i+1}.png" for i in range(6)]

    # Selección automática: las primeras 3
    mejores = []
    for idx in range(3):
        mejores.append({
            "prompt": prompts[idx],
            "imagen": imagenes[idx]
        })
    return mejores

# Ejemplo de uso para el punto 9:
if __name__ == "__main__":
    import os
    mejores = seleccionar_mejores_imagenes_y_prompts()
    # Subida automática a TikTok para cada video generado
    for idx in range(1, 4):
        video_path = f"veo_video_{idx}.mp4"
        if os.path.exists(video_path):
            prompt = mejores[idx-1]['prompt']
            descripcion, hashtags = generar_descripcion_y_hashtags(prompt)
            subir_a_tiktok(os.path.abspath(video_path), descripcion, hashtags)
    mejores = seleccionar_mejores_imagenes_y_prompts()
    print("Las 3 mejores opciones seleccionadas automáticamente:")
    for idx, item in enumerate(mejores, 1):
        print(f"Opción {idx}: Imagen={item['imagen']}")
        print(f"Prompt: {item['prompt'][:120]}...")

    # --- Generación automática de videos para las 3 mejores imágenes ---
    import mimetypes
    import os
    import time
    from google.genai import types
    from google import genai
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv('VEO3_API_KEY') or os.getenv('GEMINI_API_KEY')
    VEO_MODEL = os.getenv('VEO3_MODEL', 'models/veo-3.0-generate-preview')
    client = genai.Client(api_key=GEMINI_API_KEY)

    import json
    video_prompt_map = []
    for idx, item in enumerate(mejores, 1):
        print(f"\nGenerando video {idx} para imagen: {item['imagen']}")
        output_video = f"veo_video_{idx}.mp4"
        try:
            mime, _ = mimetypes.guess_type(item['imagen'])
            if not mime:
                mime = "image/png"
            if not os.path.exists(item['imagen']):
                print(f"❌ No se encontró la imagen: {item['imagen']}")
                continue
            with open(item['imagen'], "rb") as f:
                img_bytes = f.read()
            image_obj = types.Image(image_bytes=img_bytes, mime_type=mime)

            operation = client.models.generate_videos(
                model=VEO_MODEL,
                prompt=item['prompt'],
                image=image_obj,
                config=types.GenerateVideosConfig()
            )

            # Pooling mejorado: si hay error, termina; si descarga, termina
            max_attempts = 60
            attempt = 0
            while attempt < max_attempts:
                try:
                    if hasattr(operation, 'done') and operation.done:
                        try:
                            videos = getattr(getattr(operation, 'response', None), 'generated_videos', None)
                            if videos and len(videos) > 0:
                                generated = videos[0]
                                video_bytes = getattr(generated, 'video_bytes', None)
                                if video_bytes:
                                    with open(output_video, 'wb') as f:
                                        f.write(video_bytes)
                                    if os.path.exists(output_video) and os.path.getsize(output_video) > 1000:
                                        print(f"✅ Guardado: {output_video}")
                                        video_prompt_map.append({
                                            "video": output_video,
                                            "prompt": item['prompt'],
                                            "imagen": item['imagen']
                                        })
                                        break
                            print("💡 Video generado pero necesita descarga manual")
                            break
                        except Exception as e:
                            print(f"❌ Error al descargar el video: {e}")
                            break
                    print(f"Esperando que termine la generación... (intento {attempt + 1}/{max_attempts})")
                    time.sleep(10)
                    operation = client.operations.get(operation)
                    attempt += 1
                except Exception as e:
                    print(f"❌ Error verificando estado: {e}")
                    break
        except Exception as e:
            print(f"❌ Error generando video {idx}: {e}")

    # Guardar el mapeo video-prompt en un archivo JSON
    with open("video_prompt_map.json", "w", encoding="utf-8") as f:
        json.dump(video_prompt_map, f, ensure_ascii=False, indent=2)

# -*- coding: utf-8 -*-
"""
Script para generar video viral con Gemini/Veo 3 en local
Referencia directa: GenerarVideoGemini.ipynb
"""


import os, time, mimetypes
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('VEO3_API_KEY') or os.getenv('GEMINI_API_KEY')
assert GEMINI_API_KEY, "Falta tu GEMINI_API_KEY en el entorno"
VEO_MODEL = os.getenv('VEO3_MODEL', 'models/veo-3.0-generate-preview')

client = genai.Client(api_key=GEMINI_API_KEY)





import os
import time
from dotenv import load_dotenv

def generate_veo_video_from_image(image_path, prompt, duration=5):
    """Genera y descarga un video usando Veo3 API, siguiendo el flujo probado del notebook"""
    load_dotenv()
    veo3_key = os.getenv('VEO3_API_KEY')
    if not veo3_key:
        print("❌ VEO3_API_KEY no configurada")
        return None

    try:
        import google.genai as genai
        from google.genai import types

        client = genai.Client(api_key=veo3_key)
        model_name = os.getenv('VEO3_MODEL', 'models/veo-3.0-generate-preview')

        print(f"🤖 Usando modelo: {model_name}")
        print("📝 Generando video...")

        # Configurar generación de video
        print("⏳ Enviando request a Veo3 (esto puede tardar 1-2 minutos)...")
        import mimetypes
        # Leer imagen y crear objeto types.Image
        mime, _ = mimetypes.guess_type(image_path)
        if not mime:
            mime = "image/png"
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        image_obj = types.Image(image_bytes=img_bytes, mime_type=mime)

        operation = client.models.generate_videos(
            model=model_name,
            prompt=prompt,
            image=image_obj
        )

        print("⏳ Video en proceso de generación...")
        max_attempts = 60  # 5 minutos máximo
        attempt = 0
        while attempt < max_attempts:
            try:
                if hasattr(operation, 'done') and operation.done:
                    # Intentar descargar el video inmediatamente si la operación está lista
                    os.makedirs('data/videos', exist_ok=True)
                    timestamp = time.strftime('%Y%m%d_%H%M%S')
                    filename = f"veo_video_{timestamp}.mp4"
                    filepath = os.path.join('data/videos', filename)
                    try:
                        videos = getattr(getattr(operation, 'response', None), 'generated_videos', None)
                        if videos and len(videos) > 0:
                            generated = videos[0]
                            video_bytes = getattr(generated, 'video_bytes', None)
                            if video_bytes:
                                with open(filepath, 'wb') as f:
                                    f.write(video_bytes)
                                if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                                    file_size = os.path.getsize(filepath)
                                    print(f"🎉 ¡VIDEO GENERADO EXITOSAMENTE!")
                                    print(f"📁 Archivo: {filepath}")
                                    print(f"📦 Tamaño: {file_size:,} bytes")
                                    return filepath
                        print("💡 Video generado pero necesita descarga manual")
                        print("💡 Usar el sistema completo para descarga automática")
                        return None
                    except Exception as e:
                        print(f"⚠️  Error descargando video: {e}")
                        print("💡 Video generado correctamente en Google Cloud")
                        print("💡 Usar el sistema completo para gestión de descargas")
                        return None
                print(f"⏳ Esperando... (intento {attempt + 1}/{max_attempts})")
                time.sleep(5)
                attempt += 1
            except Exception as e:
                print(f"⚠️  Error verificando estado: {e}")
                print("💡 Finalizando pooling por error.")
                return None

        print("⏰ Timeout: La generación está tardando más de lo esperado")
        print("💡 Tu video se está generando en background")
        return None
    except Exception as e:
        print(f"❌ Error generando video: {e}")
        print(f"💡 Tipo de error: {type(e).__name__}")
        if "quota" in str(e).lower() or "limit" in str(e).lower():
            print("💡 Posible límite de API alcanzado")
            print("💡 Con cuenta de estudiante tienes 3 videos/día")
        return None

if __name__ == "__main__":
    # Parámetros de entrada
    IMAGE_PATH = "gemini_image_1.png"  # Cambia por tu imagen
    PROMPT = (
        "Un hámster dorado explora una cueva de cristales azules, iluminado por una esfera de luz flotante. "
        "Fondo: estalactitas y reflejos acuáticos. Estilo digital, colores fríos y cálidos mezclados. "
        "Sonido envolvente, adictivo y efectos ASMR presentes en la escena. #HamsterCore #FantasyArt #Viral"
    )
    generate_veo_video_from_image(IMAGE_PATH, PROMPT, duration=5)
