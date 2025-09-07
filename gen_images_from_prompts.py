"""
Genera imágenes usando Gemini 2.5 Flash Preview a partir de los prompts generados automáticamente
CON FALLBACK AUTOMÁTICO 100% GRATUITO (Pollinations.AI + HuggingFace) si Gemini no está disponible
"""

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import json
import os
import logging
from dotenv import load_dotenv
from free_fallback_generator import PollinationsFallbackGenerator, HuggingFaceFallbackGenerator

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar APIs
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No se encontró GEMINI_API_KEY en las variables de entorno. Verifica tu archivo .env.")

client = genai.Client(api_key=api_key)

# Inicializar fallbacks gratuitos
pollinations_fallback = PollinationsFallbackGenerator()
huggingface_fallback = HuggingFaceFallbackGenerator()

# Verificar disponibilidad de fallbacks
pollinations_available = pollinations_fallback.is_available()
huggingface_available = huggingface_fallback.is_available()

logger.info(f"✅ Pollinations fallback: {'Disponible' if pollinations_available else 'No disponible'}")
logger.info(f"✅ HuggingFace fallback: {'Disponible' if huggingface_available else 'No disponible'}")

if not pollinations_available and not huggingface_available:
    logger.warning("⚠️ NO hay fallbacks disponibles - solo Gemini funcionará")
else:
    logger.info("🛡️ Fallbacks gratuitos configurados correctamente")

def generate_image_with_gemini(prompt: str, image_path: str) -> bool:
    """
    Genera imagen usando Gemini API
    """
    try:
        logger.info(f"🎨 Generando con Gemini: {prompt[:50]}...")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        if response and response.candidates:
            candidate = response.candidates[0]
            if candidate and candidate.content and hasattr(candidate.content, 'parts'):
                for part in candidate.content.parts:
                    if getattr(part, 'inline_data', None) is not None and getattr(part.inline_data, 'data', None) is not None:
                        image = Image.open(BytesIO(part.inline_data.data))
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)
                        image.save(image_path)
                        logger.info(f"✅ Imagen Gemini guardada: {image_path}")
                        return True
        
        logger.warning("⚠️ Gemini no generó imagen válida")
        return False
        
    except Exception as e:
        logger.error(f"❌ Error en Gemini API: {e}")
        return False

def generate_image_with_fallback(prompt: str, image_path: str) -> bool:
    """
    Genera imagen con Gemini, usando fallbacks gratuitos si falla
    """
    # Intentar primero con Gemini
    success = generate_image_with_gemini(prompt, image_path)
    
    if success:
        return True
    
    # Si Gemini falla, usar fallbacks gratuitos en orden de preferencia
    logger.info("🔄 Gemini falló. Probando fallbacks gratuitos...")
    
    # Fallback 1: Pollinations.AI (más rápido y confiable)
    if pollinations_available:
        logger.info("🌸 Intentando con Pollinations.AI...")
        success = pollinations_fallback.generate_viral_image(prompt, image_path)
        
        if success:
            logger.info(f"✅ Imagen generada con Pollinations fallback: {image_path}")
            return True
        else:
            logger.warning("⚠️ Pollinations también falló")
    
    # Fallback 2: HuggingFace (requiere token opcional pero funciona sin él)
    if huggingface_available:
        logger.info("🤗 Intentando con HuggingFace...")
        success = huggingface_fallback.generate_image(prompt, image_path)
        
        if success:
            logger.info(f"✅ Imagen generada con HuggingFace fallback: {image_path}")
            return True
        else:
            logger.warning("⚠️ HuggingFace también falló")
    
    logger.error("❌ Todos los fallbacks fallaron - no se pudo generar imagen")
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
logger.info(f"🔄 Sistema de fallback: Gemini → {fallback_info}")

for idx, prompt in enumerate(prompts):
    print(f"\n{'='*60}")
    print(f"🎯 GENERANDO IMAGEN {idx+1}/{len(prompts)}")
    print(f"📝 Prompt: {prompt}")
    print(f"{'='*60}")
    
    image_path = f'data/images/gemini_image_{idx+1}.png'
    
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
