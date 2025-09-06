#!/usr/bin/env python3
"""
Script de prueba simple para validar la configuración
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_configuration():
    """Probar que la configuración esté correcta"""
    print("🚀 PRUEBA DE CONFIGURACIÓN")
    print("=" * 50)
    
    # Verificar API keys
    gemini_key = os.getenv('GEMINI_API_KEY')
    veo3_key = os.getenv('VEO3_API_KEY')
    
    if gemini_key:
        print(f"✅ GEMINI_API_KEY: {gemini_key[:20]}...")
    else:
        print("❌ GEMINI_API_KEY: No configurada")
    
    if veo3_key:
        print(f"✅ VEO3_API_KEY: {veo3_key[:20]}...")
    else:
        print("❌ VEO3_API_KEY: No configurada")
    
    # Verificar modelos
    gemini_model = os.getenv('GEMINI_MODEL')
    veo3_model = os.getenv('VEO3_MODEL')
    
    print(f"📋 GEMINI_MODEL: {gemini_model}")
    print(f"📋 VEO3_MODEL: {veo3_model}")
    
    # Verificar TikTok
    tiktok_user = os.getenv('TIKTOK_USERNAME')
    tiktok_email = os.getenv('TIKTOK_EMAIL')
    
    print(f"👤 TIKTOK_USERNAME: {tiktok_user}")
    print(f"📧 TIKTOK_EMAIL: {tiktok_email}")
    
    # Verificar importaciones básicas
    print("\n🧪 PROBANDO IMPORTACIONES...")
    
    try:
        import google.genai as genai
        print("✅ google.genai")
    except ImportError as e:
        print(f"❌ google.genai: {e}")
    
    try:
        from PIL import Image
        print("✅ PIL")
    except ImportError as e:
        print(f"❌ PIL: {e}")
    
    try:
        import cv2
        print("✅ opencv-python")
    except ImportError as e:
        print(f"❌ opencv-python: {e}")
    
    try:
        import numpy as np
        print("✅ numpy")
    except ImportError as e:
        print(f"❌ numpy: {e}")
    
    print("\n🎯 PRÓXIMOS PASOS:")
    if gemini_key and veo3_key:
        print("1. ✅ APIs configuradas - Puedes probar generación")
        print("2. 🧪 Ejecuta: python -m src.main --test")
        print("3. 🚀 Sistema listo para automatización")
    else:
        print("1. ❌ Configura tus API keys en el archivo .env")
        print("2. 🔑 GEMINI_API_KEY desde: https://makersuite.google.com/app/apikey")
        print("3. 🔑 VEO3_API_KEY: Tu cuenta de estudiante de Google")

def test_simple_generation():
    """Prueba simple de generación"""
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_key:
        print("⚠️  No se puede probar generación sin GEMINI_API_KEY")
        return
    
    print("\n🧪 PRUEBA SIMPLE DE GEMINI...")
    
    try:
        import google.genai as genai
        
        # Configurar cliente
        client = genai.Client(api_key=gemini_key)
        
        # Crear prompt simple
        prompt = "Create a motivational image with the text 'Success starts today!'"
        
        # Probar generación (sin ejecutar realmente para evitar costos)
        print(f"✅ Cliente configurado correctamente")
        print(f"📝 Prompt de prueba: {prompt}")
        print("💡 Para ejecutar generación real, usa el sistema completo")
        
    except Exception as e:
        print(f"❌ Error en prueba de Gemini: {e}")

if __name__ == "__main__":
    test_configuration()
    test_simple_generation()
    
    print("\n" + "=" * 50)
    print("🏁 PRUEBA COMPLETADA")
    print("💡 Ejecuta 'python src/main.py' para usar el sistema completo")
