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

IMAGE_PATH = "gemini_image_3.png"  # Cambia por tu imagen (.png/.jpg)
PROMPT = (
    "Vertical 9:16 ASMR loop. Un dragón de cristal azul vuela sobre un lago de neón, lanzando destellos y burbujas. Fondo: montañas brillantes, reflejos acuáticos y niebla digital. Sonido envolvente: aleteo, burbujeo, ecos hipnóticos y efectos de sonido adictivos. Transiciones suaves, zoom progresivo y ambiente fantástico. #DragonCore #ASMR #ViralTikTok. ~8s"
)
OUT_MP4 = "veo_video_3.mp4"

client = genai.Client(api_key=GEMINI_API_KEY)

# Leer la imagen como bytes y detectar MIME
mime, _ = mimetypes.guess_type(IMAGE_PATH)
if not mime:
    mime = "image/png"

if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"No se encontró la imagen en: {IMAGE_PATH}")

with open(IMAGE_PATH, "rb") as f:
    img_bytes = f.read()

# Construir objeto de imagen compatible
image = types.Image(image_bytes=img_bytes, mime_type=mime)

# 1) Crear la operación
operation = client.models.generate_videos(
    model=VEO_MODEL,
    prompt=PROMPT,
    image=image,
    config=types.GenerateVideosConfig(
        #duration_seconds=8,      # usa duration_seconds si tu cuenta lo permite
        # number_of_videos=1,     # opcional
        # negative_prompt="cartoon, low quality",  # opcional
    )
)

# 2) Polling hasta que termine
while not operation.done:
    print("Esperando que termine la generación...")
    time.sleep(10)
    operation = client.operations.get(operation)
    # Intentar descargar el video si ya está disponible
    try:
        videos = getattr(getattr(operation, 'response', None), 'generated_videos', None)
        if videos and len(videos) > 0:
            generated = videos[0]
            client.files.download(file=generated.video)
            generated.video.save(OUT_MP4)
            print(f"✅ Guardado: {OUT_MP4}")
            break  # Detener el bucle y finalizar el script
    except Exception as e:
        print(f"❌ Error al descargar el video: {e}")
"""
Genera un video viral usando Veo 3 a partir de una imagen y un prompt detallado (con sonido envolvente y efectos ASMR)
"""





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
                    break
                print(f"⏳ Esperando... (intento {attempt + 1}/{max_attempts})")
                time.sleep(5)
                attempt += 1
            except Exception as e:
                print(f"⚠️  Error verificando estado: {e}")
                time.sleep(5)
                attempt += 1

        if attempt >= max_attempts:
            print("⏰ Timeout: La generación está tardando más de lo esperado")
            print("💡 Tu video se está generando en background")
            return None

        print("✅ ¡Video generado exitosamente!")
        os.makedirs('data/videos', exist_ok=True)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"veo_video_{timestamp}.mp4"
        filepath = os.path.join('data/videos', filename)

        try:
            if hasattr(operation, 'result') and operation.result:
                result = operation.result
                if hasattr(result, 'video'):
                    client.files.download(file=result.video)
                    result.video.save(filepath)
                    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                        file_size = os.path.getsize(filepath)
                        print(f"🎉 ¡VIDEO GENERADO EXITOSAMENTE!")
                        print(f"📁 Archivo: {filepath}")
                        print(f"📦 Tamaño: {file_size:,} bytes")
                        return filepath
            print("💡 Video generado pero necesita descarga manual")
            print("💡 Usar el sistema completo para descarga automática")
        except Exception as e:
            print(f"⚠️  Error descargando video: {e}")
            print("💡 Video generado correctamente en Google Cloud")
            print("💡 Usar el sistema completo para gestión de descargas")
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
