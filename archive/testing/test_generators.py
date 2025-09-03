#!/usr/bin/env python3
"""
Script de prueba para validar los generadores de imagen y video
usando las APIs de Gemini y Veo3 con tu código funcional integrado.
"""

import os
import sys
import time
from dotenv import load_dotenv

# Añadir el directorio src al path ANTES de las importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Ahora podemos importar desde src
from generation.image_generator import GeminiImageGenerator
from generation.video_generator import Veo3VideoGenerator
from utils.logger import get_logger

def test_image_generation():
    """Probar generación de imágenes con Gemini"""
    print("\n🖼️  PROBANDO GENERACIÓN DE IMÁGENES CON GEMINI...")
    
    # Configurar generador
    image_gen = GeminiImageGenerator()
    
    # Datos de prueba
    test_prompt = {
        'id': 'test_001',
        'tema': 'motivación',
        'subtema': 'éxito personal',
        'texto_principal': 'El éxito se construye día a día',
        'texto_secundario': 'Cada pequeño paso cuenta',
        'categoria': 'motivacion',
        'sentimiento': 'inspiracional',
        'palabras_clave': ['éxito', 'motivación', 'crecimiento'],
        'style_context': {
            'background': 'gradient',
            'mood': 'energetic',
            'color_scheme': 'vibrant'
        }
    }
    
    try:
        # Generar imagen
        print(f"Generando imagen para: {test_prompt['texto_principal']}")
        result = image_gen.generate_images_from_prompts([test_prompt])
        
        if result and len(result) > 0:
            # El resultado es una lista de diccionarios con información
            image_info = result[0]
            image_path = image_info.get('path') if isinstance(image_info, dict) else image_info
            print(f"✅ Imagen generada exitosamente: {image_path}")
            
            # Verificar que el archivo existe
            if image_path and os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                print(f"   📁 Tamaño del archivo: {file_size:,} bytes")
                return image_path
            else:
                print("❌ Error: Archivo de imagen no encontrado")
                return None
        else:
            print("❌ Error: No se pudo generar la imagen")
            return None
            
    except Exception as e:
        print(f"❌ Error en generación de imagen: {e}")
        return None

def test_video_generation(image_path=None):
    """Probar generación de videos con Veo3"""
    print("\n🎬 PROBANDO GENERACIÓN DE VIDEOS CON VEO3...")
    
    # Configurar generador
    video_gen = Veo3VideoGenerator()
    
    # Datos de prueba
    test_prompt = {
        'id': 'test_video_001',
        'tema': 'motivación',
        'texto_principal': 'El éxito se construye día a día',
        'duration': 5,  # 5 segundos para prueba rápida
        'style_context': {
            'movement': 'subtle',
            'transition': 'smooth',
            'mood': 'inspirational'
        },
        'video_specs': {
            'aspect_ratio': '9:16',
            'resolution': '1080x1920',
            'duration_seconds': 5
        }
    }
    
    try:
        # Si tenemos una imagen base, úsala
        if image_path and os.path.exists(image_path):
            print(f"Usando imagen base: {image_path}")
            test_prompt['base_image'] = image_path
        
        # Generar video
        print(f"Generando video para: {test_prompt['texto_principal']}")
        
        # Para video necesitamos pasar las imágenes base
        image_paths = [image_path] if image_path else []
        result = video_gen.generate_videos_from_images([test_prompt], image_paths)
        
        if result and len(result) > 0:
            # El resultado es una lista de diccionarios con información
            video_info = result[0]
            video_path = video_info.get('path') if isinstance(video_info, dict) else video_info
            print(f"✅ Video generado exitosamente: {video_path}")
            
            # Verificar que el archivo existe
            if video_path and os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                print(f"   📁 Tamaño del archivo: {file_size:,} bytes")
                return video_path
            else:
                print("❌ Error: Archivo de video no encontrado")
                return None
        else:
            print("❌ Error: No se pudo generar el video")
            return None
            
    except Exception as e:
        print(f"❌ Error en generación de video: {e}")
        return None

def main():
    """Función principal de prueba"""
    print("🚀 INICIANDO PRUEBAS DE GENERADORES")
    print("=" * 50)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar API keys
    gemini_key = os.getenv('GEMINI_API_KEY')
    veo3_key = os.getenv('VEO3_API_KEY')
    
    if not gemini_key:
        print("⚠️  AVISO: GEMINI_API_KEY no encontrada en .env")
        print("   Las pruebas de imagen pueden fallar")
    else:
        print(f"✅ GEMINI_API_KEY configurada: {gemini_key[:10]}...")
    
    if not veo3_key:
        print("⚠️  AVISO: VEO3_API_KEY no encontrada en .env")
        print("   Las pruebas de video pueden fallar")
    else:
        print(f"✅ VEO3_API_KEY configurada: {veo3_key[:10]}...")
    
    # Ejecutar pruebas
    image_path = None
    
    # Prueba 1: Generación de imágenes
    if gemini_key:
        image_path = test_image_generation()
        time.sleep(2)  # Pausa entre pruebas
    
    # Prueba 2: Generación de videos
    if veo3_key:
        video_path = test_video_generation(image_path)
    
    print("\n" + "=" * 50)
    print("🏁 PRUEBAS COMPLETADAS")
    
    if gemini_key and veo3_key:
        print("💡 PRÓXIMOS PASOS:")
        print("   1. Verifica que las imágenes y videos se generaron correctamente")
        print("   2. Ejecuta el sistema completo con: python src/main.py")
        print("   3. Configura GitHub Actions para automatización")
    else:
        print("💡 CONFIGURACIÓN PENDIENTE:")
        if not gemini_key:
            print("   - Añade GEMINI_API_KEY a tu archivo .env")
        if not veo3_key:
            print("   - Añade VEO3_API_KEY a tu archivo .env")

if __name__ == "__main__":
    main()
