"""
Genera imágenes usando Gemini Web UI (Selenium) a partir de los prompts generados automáticamente
CON FALLBACK AUTOMÁTICO 100% GRATUITO (Pollinations.AI + HuggingFace) si Gemini no está disponible
"""

import json
import os
import logging
import time
from dotenv import load_dotenv
from src.utils.gemini_web_client import GeminiWebClient
from free_fallback_generator import PollinationsFallbackGenerator, HuggingFaceFallbackGenerator

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializar fallbacks gratuitos
pollinations_fallback = PollinationsFallbackGenerator()
huggingface_fallback = HuggingFaceFallbackGenerator()

# Verificar disponibilidad de fallbacks
pollinations_available = pollinations_fallback.is_available()
huggingface_available = huggingface_fallback.is_available()

logger.info(f"✅ Pollinations fallback: {'Disponible' if pollinations_available else 'No disponible'}")
logger.info(f"✅ HuggingFace fallback: {'Disponible' if huggingface_available else 'No disponible'}")

if not pollinations_available and not huggingface_available:
    logger.warning("⚠️ NO hay fallbacks gratuitos disponibles - solo el método principal funcionará")
else:
    logger.info("🛡️ Fallbacks gratuitos configurados correctamente")

def generate_image_with_selenium(prompt: str, image_path: str) -> bool:
    """
    Genera imagen usando Gemini Web UI con Selenium.
    """
    client = None
    try:
        logger.info(f"🎨 Generando con Gemini (Selenium): {prompt[:50]}...")
        client = GeminiWebClient()
        output_dir = os.path.dirname(image_path)
        downloaded_image_path = client.generate_image(prompt, output_dir=output_dir)

        wait_time = 0
        while downloaded_image_path and not os.path.exists(downloaded_image_path) and wait_time < 20:
            time.sleep(1)
            wait_time += 1

        image_to_rename = downloaded_image_path
        if not (image_to_rename and os.path.exists(image_to_rename)):
            logger.warning("Archivo esperado no encontrado. Buscando el más reciente en la carpeta de descargas...")
            downloads_dir = os.path.dirname(downloaded_image_path)
            files = [os.path.join(downloads_dir, f) for f in os.listdir(downloads_dir) if f.endswith('.tmp') or f.endswith('.png')]
            if files:
                image_to_rename = max(files, key=os.path.getmtime)
                logger.info(f"Usando archivo más reciente: {os.path.basename(image_to_rename)}")
            else:
                logger.warning("No se encontró ningún archivo reciente en la carpeta de descargas.")

        if image_to_rename and image_to_rename.endswith('.tmp'):
            logger.info(f"Esperando a que el archivo {os.path.basename(image_to_rename)} se convierta en imagen final...")
            tmp_wait_time = 0
            final_candidate = image_to_rename[:-4] + '.png'
            while os.path.exists(image_to_rename) and not os.path.exists(final_candidate) and tmp_wait_time < 20:
                time.sleep(1)
                tmp_wait_time += 1
            if os.path.exists(final_candidate):
                image_to_rename = final_candidate
                logger.info(f"Descarga finalizada: {os.path.basename(image_to_rename)}")
            else:
                logger.warning("El archivo .tmp no se convirtió en imagen final tras esperar 20s.")

        if image_to_rename and os.path.exists(image_to_rename):
            logger.info("Esperando 5 segundos antes de renombrar la imagen...")
            time.sleep(5)
            if os.path.exists(image_path):
                os.remove(image_path)
            os.rename(image_to_rename, image_path)
            logger.info(f"Imagen renombrada y guardada como: {os.path.basename(image_path)}")
            return True
        else:
            raise Exception("No se encontró ningún archivo de imagen descargado para renombrar.")

    except Exception as e:
        logger.error(f"❌ Error en la generación con Selenium: {e}")
        return False
    finally:
        if client:
            client.close()

def generate_image_with_fallback(prompt: str, image_path: str) -> bool:
    """
    Genera imagen con Selenium, usando fallbacks gratuitos si falla.
    """
    # Intentar primero con Selenium
    success = generate_image_with_selenium(prompt, image_path)
    
    if success:
        return True
    
    logger.info("🔄 Falló la generación con Selenium. Probando fallbacks gratuitos...")
    
    # Fallback 1: Pollinations.AI
    if pollinations_available:
        logger.info("🌸 Intentando con Pollinations.AI...")
        success = pollinations_fallback.generate_viral_image(prompt, image_path)
        if success:
            logger.info(f"✅ Imagen generada con Pollinations fallback: {image_path}")
            return True
        else:
            logger.warning("⚠️ Pollinations también falló")
    
    # Fallback 2: HuggingFace
    if huggingface_available:
        logger.info("🤗 Intentando con HuggingFace...")
        success = huggingface_fallback.generate_image(prompt, image_path)
        if success:
            logger.info(f"✅ Imagen generada con HuggingFace fallback: {image_path}")
            return True
        else:
            logger.warning("⚠️ HuggingFace también falló")
    
    logger.error("❌ Todos los métodos de generación de imagen fallaron.")
    return False

# Cargar prompts generados automáticamente
prompts_path = os.getenv('PROMPTS_JSON', 'data/analytics/fusion_prompts_auto.json')
with open(prompts_path, 'r', encoding='utf-8') as f:
    prompts = json.load(f).get('prompts', [])

logger.info(f"📁 Cargados {len(prompts)} prompts desde {prompts_path}")

# Determinar fallbacks disponibles para logging
fallback_systems = []
if pollinations_available:
    fallback_systems.append("Pollinations.AI")
if huggingface_available:
    fallback_systems.append("HuggingFace")

fallback_info = " → ".join(fallback_systems) if fallback_systems else "Sin fallback"
logger.info(f"🔄 Sistema de fallback: Gemini (Selenium) → {fallback_info}")

for idx, prompt in enumerate(prompts):
    print(f"\n{'='*60}")
    print(f"🎯 GENERANDO IMAGEN {idx+1}/{len(prompts)}")
    print(f"📝 Prompt: {prompt}")
    print(f"{'='*60}")
    
    image_path = f'data/images/viral_image_{idx+1}.png'
    
    # Generar imagen con sistema de fallback
    success = generate_image_with_fallback(prompt, image_path)
    
    if success:
        print(f"✅ ÉXITO: Imagen {idx+1} generada correctamente")
    else:
        print(f"❌ ERROR: No se pudo generar imagen {idx+1}")
    
    print(f"📁 Ubicación: {image_path}")

print(f"\n{'='*60}")
print("🎉 PROCESO COMPLETADO")
print(f"📊 Total prompts procesados: {len(prompts)}")
print(f"{'='*60}")