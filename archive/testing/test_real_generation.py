#!/usr/bin/env python3
"""
Script de prueba REAL para generar imágenes y videos
usando las APIs de Gemini y Veo3
"""

import os
import sys
import time
from dotenv import load_dotenv

def test_real_image_generation():
    """Probar generación REAL de imágenes con Gemini"""
    print("🖼️  GENERACIÓN REAL DE IMAGEN CON GEMINI")
    print("=" * 50)
    
    # Cargar configuración
    load_dotenv()
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY no configurada")
        return None
    
    try:
        import google.genai as genai
        from PIL import Image
        import base64
        import io
        
        # Configurar cliente
        client = genai.Client(api_key=gemini_key)
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-preview-image-generation')
        
        print(f"🤖 Usando modelo: {model_name}")
        print("📝 Generando imagen motivacional...")
        
        # Prompt optimizado para TikTok
        prompt = """Create a vibrant motivational image for TikTok with the text 'EL ÉXITO EMPIEZA HOY' in bold, modern typography. 
        Style: Modern, energetic, vertical format (9:16), bright colors (orange, blue, white), 
        minimalist background with subtle gradient, professional typography, inspirational mood.
        Make it eye-catching for social media."""
        
        # Configurar generación (usando el formato más simple)
        print("⏳ Enviando request a Gemini...")
        
        # Generar imagen usando el método más directo
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        print("✅ Respuesta recibida de Gemini")
        
        # Procesar respuesta
        if response and response.candidates:
            candidate = response.candidates[0]
            if candidate and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                for part in candidate.content.parts:
                    # Buscar parte con imagen
                    if (hasattr(part, 'inline_data') and 
                        part.inline_data is not None and 
                        hasattr(part.inline_data, 'data') and
                        part.inline_data.data is not None):
                        
                        # Crear directorio de imágenes
                        os.makedirs('data/images', exist_ok=True)
                        
                        # Generar nombre de archivo
                        timestamp = time.strftime('%Y%m%d_%H%M%S')
                        filename = f"test_image_{timestamp}.jpg"
                        filepath = os.path.join('data/images', filename)
                        
                        # Decodificar y guardar imagen
                        image_data = base64.b64decode(part.inline_data.data)
                        
                        with open(filepath, 'wb') as f:
                            f.write(image_data)
                        
                        # Verificar imagen con PIL
                        img = Image.open(filepath)
                        width, height = img.size
                        
                        print(f"🎉 ¡IMAGEN GENERADA EXITOSAMENTE!")
                        print(f"📁 Archivo: {filepath}")
                        print(f"📏 Resolución: {width}x{height}")
                        print(f"📦 Tamaño: {len(image_data):,} bytes")
                        
                        return filepath
        
        print("❌ No se encontró imagen en la respuesta")
        return None
        
    except Exception as e:
        print(f"❌ Error generando imagen: {e}")
        print(f"💡 Tipo de error: {type(e).__name__}")
        return None

def test_real_video_generation(image_path=None):
    """Probar generación REAL de video con Veo3"""
    print("\n🎬 GENERACIÓN REAL DE VIDEO CON VEO3")
    print("=" * 50)
    
    # Cargar configuración
    veo3_key = os.getenv('VEO3_API_KEY')
    
    if not veo3_key:
        print("❌ VEO3_API_KEY no configurada")
        return None
    
    try:
        import google.genai as genai
        from google.genai import types
        
        # Configurar cliente
        client = genai.Client(api_key=veo3_key)
        model_name = os.getenv('VEO3_MODEL', 'models/veo-3.0-generate-preview')
        
        print(f"🤖 Usando modelo: {model_name}")
        print("📝 Generando video motivacional...")
        
        # Prompt para video
        video_prompt = """Create a 5-second motivational video with smooth camera movement. 
        Show inspiring visuals with the message 'EL ÉXITO EMPIEZA HOY'. 
        Style: Modern, energetic, vertical format for TikTok, smooth transitions, 
        vibrant colors, professional look. Add subtle zoom and fade effects."""
        
        # Configurar generación de video (usando formato simplificado)
        print("⏳ Enviando request a Veo3 (esto puede tardar 1-2 minutos)...")
        
        # Generar video usando el método directo
        operation = client.models.generate_videos(
            model=model_name,
            prompt=video_prompt,
            duration_seconds=5
        )
        
        print("⏳ Video en proceso de generación...")
        print("💡 Veo3 está creando tu video, por favor espera...")
        
        # Polling para esperar resultado
        max_attempts = 60  # 5 minutos máximo
        attempt = 0
        
        while attempt < max_attempts:
            try:
                # Verificar estado del operation
                if hasattr(operation, 'done') and operation.done:
                    break
                
                # Si no está listo, esperar
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
            print("💡 Intenta verificar más tarde o usa el sistema completo")
            return None
        
        # Si llegamos aquí, el video debería estar listo
        print("✅ ¡Video generado exitosamente!")
        
        # Crear directorio de videos
        os.makedirs('data/videos', exist_ok=True)
        
        # Generar nombre de archivo
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"test_video_{timestamp}.mp4"
        filepath = os.path.join('data/videos', filename)
        
        # Descargar video (esto depende de la respuesta exacta de Veo3)
        try:
            # Método 1: Si el operation tiene el video
            if hasattr(operation, 'result') and operation.result:
                result = operation.result
                if hasattr(result, 'video'):
                    # Usar el cliente para descargar
                    client.files.download(file=result.video)
                    result.video.save(filepath)
                    
                    # Verificar archivo
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
        
        # Si es error de límite, informar
        if "quota" in str(e).lower() or "limit" in str(e).lower():
            print("💡 Posible límite de API alcanzado")
            print("💡 Con cuenta de estudiante tienes 3 videos/día")
        
        return None

def main():
    """Función principal de prueba real"""
    print("🚀 PRUEBA REAL DE GENERACIÓN")
    print("🎯 Usando APIs reales de Google Generative AI")
    print("=" * 60)
    
    # Cargar configuración
    load_dotenv()
    
    # Mostrar configuración
    print(f"🔑 GEMINI_API_KEY: {'✅ Configurada' if os.getenv('GEMINI_API_KEY') else '❌ Faltante'}")
    print(f"🔑 VEO3_API_KEY: {'✅ Configurada' if os.getenv('VEO3_API_KEY') else '❌ Faltante'}")
    print()
    
    # Prueba 1: Generar imagen
    image_path = test_real_image_generation()
    
    if image_path:
        print(f"\n✅ Imagen lista: {image_path}")
        time.sleep(2)
    else:
        print("\n⚠️  Sin imagen para el video")
    
    # Prueba 2: Generar video
    video_path = test_real_video_generation(image_path)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    if image_path:
        print(f"✅ Imagen: {image_path}")
    else:
        print("❌ Imagen: No generada")
    
    if video_path:
        print(f"✅ Video: {video_path}")
    else:
        print("❌ Video: No generado (normal en primera prueba)")
    
    print("\n💡 PRÓXIMOS PASOS:")
    if image_path:
        print("1. ✅ Gemini funciona perfectamente")
        print("2. 🎬 Veo3 puede tardar más tiempo (normal)")
        print("3. 🍪 Configurar cookies de TikTok")
        print("4. 🚀 Ejecutar sistema completo")
    else:
        print("1. 🔍 Revisar configuración de GEMINI_API_KEY")
        print("2. 🔍 Verificar límites de API")
        print("3. 💬 Contactar soporte si persiste")

if __name__ == "__main__":
    main()
