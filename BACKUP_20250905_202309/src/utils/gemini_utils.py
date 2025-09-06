"""
Utilidades para trabajar con Google Generative AI (Gemini/Veo3)
"""

import os
from typing import Optional


def get_gemini_api_key() -> str:
    """
    Obtener API key de Gemini desde variables de entorno
    Compatible con diferentes formas de configuración
    """
    # Intentar diferentes nombres de variables de entorno
    api_key = (
        os.getenv('GEMINI_API_KEY') or 
        os.getenv('GOOGLE_API_KEY') or 
        os.getenv('GENAI_API_KEY')
    )
    
    if not api_key:
        raise ValueError(
            "No se encontró API key de Gemini. "
            "Configura GEMINI_API_KEY en tus variables de entorno."
        )
    
    return api_key


def validate_api_key(api_key: str) -> bool:
    """
    Validar formato básico de API key de Google
    """
    if not api_key:
        return False
    
    # Las API keys de Google suelen empezar con ciertos prefijos
    if api_key.startswith('AIza') and len(api_key) == 39:
        return True
    
    # Otras validaciones básicas
    if len(api_key) > 20 and api_key.replace('-', '').replace('_', '').isalnum():
        return True
    
    return False


def optimize_prompt_for_tiktok(prompt: str, content_type: str = "video") -> str:
    """
    Optimizar prompt para contenido de TikTok
    """
    if content_type == "video":
        # Prefijos para videos verticales de TikTok
        tiktok_prefixes = [
            "Vertical 9:16 video format.",
            "TikTok-style content.",
            "Mobile-optimized vertical video.",
        ]
        
        # Sufijos para mejorar calidad
        quality_suffixes = [
            "High quality, crisp details.",
            "Trending social media style.",
            "Eye-catching and engaging.",
        ]
        
        # Combinar
        optimized = f"{tiktok_prefixes[0]} {prompt} {quality_suffixes[0]}"
        
    elif content_type == "image":
        # Optimización para imágenes
        image_prefixes = [
            "Vertical 9:16 aspect ratio.",
            "High-resolution mobile image.",
            "TikTok thumbnail style.",
        ]
        
        quality_suffixes = [
            "Vibrant colors, sharp details.",
            "Social media optimized.",
            "Eye-catching composition.",
        ]
        
        optimized = f"{image_prefixes[0]} {prompt} {quality_suffixes[0]}"
    
    else:
        optimized = prompt
    
    return optimized


def get_model_config(model_type: str = "veo3") -> dict:
    """
    Obtener configuración recomendada para diferentes modelos
    """
    configs = {
        "veo3": {
            "model": "models/veo-3.0-generate-preview",
            "fast_model": "models/veo-3.0-fast-generate-preview",
            "max_duration": 15,  # segundos
            "recommended_resolution": "1080x1920",
        },
        "veo2": {
            "model": "veo-2.0-generate-001",
            "max_duration": 8,  # segundos
            "recommended_resolution": "1080x1920",
        },
        "gemini_image": {
            "model": "gemini-2.0-flash-preview-image-generation",
            "response_modalities": ['TEXT', 'IMAGE'],
        }
    }
    
    return configs.get(model_type, {})


def format_duration_for_veo(seconds: int) -> int:
    """
    Formatear duración para Veo3 (validar límites)
    """
    # Veo3 tiene límites de duración
    min_duration = 3
    max_duration = 15  # Para cuenta educativa gratuita
    
    if seconds < min_duration:
        return min_duration
    elif seconds > max_duration:
        return max_duration
    else:
        return seconds


def check_daily_limits(videos_generated_today: int, max_daily_videos: int = 3) -> bool:
    """
    Verificar si se pueden generar más videos hoy
    """
    return videos_generated_today < max_daily_videos


def create_negative_prompt(content_type: str = "general") -> str:
    """
    Crear prompt negativo para mejorar calidad
    """
    base_negative = "low quality, blurry, distorted, pixelated, amateur"
    
    if content_type == "tiktok":
        return f"{base_negative}, horizontal format, landscape, watermarks, logos"
    elif content_type == "professional":
        return f"{base_negative}, cartoon, anime, unrealistic"
    else:
        return base_negative
