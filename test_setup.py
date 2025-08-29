#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración del sistema
"""

import os
import sys
import json
from datetime import datetime

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def test_imports():
    """Probar que todas las dependencias se pueden importar"""
    print("🔍 Probando imports...")
    
    try:
        import requests
        print("✅ requests")
    except ImportError:
        print("❌ requests - Run: pip install requests")
        return False
    
    try:
        import yaml
        print("✅ pyyaml")
    except ImportError:
        print("❌ pyyaml - Run: pip install pyyaml")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow")
    except ImportError:
        print("❌ Pillow - Run: pip install Pillow")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv")
    except ImportError:
        print("❌ python-dotenv - Run: pip install python-dotenv")
        return False
    
    # Opcional: estos pueden fallar en desarrollo
    try:
        import cv2
        print("✅ opencv-python")
    except ImportError:
        print("⚠️ opencv-python - Run: pip install opencv-python")
    
    try:
        import pandas as pd
        print("✅ pandas")
    except ImportError:
        print("⚠️ pandas - Run: pip install pandas")
    
    try:
        import numpy as np
        print("✅ numpy")
    except ImportError:
        print("⚠️ numpy - Run: pip install numpy")
    
    return True

def test_configuration():
    """Probar configuración del proyecto"""
    print("\n🔧 Probando configuración...")
    
    # Probar que se puede cargar la configuración
    try:
        from src.utils.config import config
        print("✅ Configuración cargada")
        
        # Verificar directorios
        data_dir = config.get_project_root()
        print(f"📁 Directorio del proyecto: {data_dir}")
        
        # Crear directorios de datos
        for subdir in ['metrics', 'images', 'videos', 'prompts', 'sessions']:
            dir_path = config.get_data_dir(subdir)
            print(f"📁 Directorio {subdir}: {dir_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_environment_variables():
    """Probar variables de entorno"""
    print("\n🔑 Probando variables de entorno...")
    
    try:
        from src.utils.config import config
        
        # Verificar API keys (sin mostrar los valores)
        if config.gemini_api_key:
            print("✅ GEMINI_API_KEY configurada")
        else:
            print("⚠️ GEMINI_API_KEY no configurada")
        
        if config.veo3_api_key:
            print("✅ VEO3_API_KEY configurada")
        else:
            print("⚠️ VEO3_API_KEY no configurada")
        
        if config.tiktok_username:
            print("✅ TIKTOK_USERNAME configurado")
        else:
            print("⚠️ TIKTOK_USERNAME no configurado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando variables: {e}")
        return False

def test_cookies():
    """Probar configuración de cookies de TikTok"""
    print("\n🍪 Probando cookies de TikTok...")
    
    try:
        from src.utils.config import config
        cookies_path = config.get_cookies_path()
        
        if os.path.exists(cookies_path):
            print(f"✅ Archivo de cookies encontrado: {cookies_path}")
            
            # Verificar formato
            with open(cookies_path, 'r') as f:
                cookies_data = json.load(f)
                
            if 'cookies' in cookies_data and isinstance(cookies_data['cookies'], list):
                print(f"✅ Formato de cookies válido ({len(cookies_data['cookies'])} cookies)")
                
                # Verificar cookies importantes
                cookie_names = [cookie.get('name', '') for cookie in cookies_data['cookies']]
                
                important_cookies = ['sessionid', 'csrf_token']
                for cookie_name in important_cookies:
                    if cookie_name in cookie_names:
                        print(f"✅ Cookie {cookie_name} encontrada")
                    else:
                        print(f"⚠️ Cookie {cookie_name} no encontrada")
                
                return True
            else:
                print("❌ Formato de cookies inválido")
                return False
        else:
            print(f"⚠️ Archivo de cookies no encontrado: {cookies_path}")
            print("💡 Copia config/tiktok_cookies.json.example y configura tus cookies reales")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando cookies: {e}")
        return False

def test_basic_functionality():
    """Probar funcionalidad básica"""
    print("\n⚙️ Probando funcionalidad básica...")
    
    try:
        # Probar logger
        from src.utils.logger import get_logger
        logger = get_logger("test")
        logger.info("Test de logging")
        print("✅ Sistema de logging")
        
        # Probar helpers
        from src.utils.helpers import sanitize_filename, get_trending_hashtags
        test_filename = sanitize_filename("test/file<>name.txt")
        print(f"✅ Sanitización de archivos: {test_filename}")
        
        hashtags = get_trending_hashtags()
        print(f"✅ Hashtags trending: {len(hashtags)} hashtags")
        
        # Probar generador de prompts (sin APIs)
        from src.generation.prompt_generator import PromptGenerator
        generator = PromptGenerator()
        print("✅ Generador de prompts")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad básica: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 TikTok Video Automation - Test de Configuración")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuración", test_configuration),
        ("Variables de entorno", test_environment_variables),
        ("Cookies de TikTok", test_cookies),
        ("Funcionalidad básica", test_basic_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Configuración completa! El sistema está listo para usar.")
        print("\n📝 Próximos pasos:")
        print("1. Ejecuta: python src/main.py --username tu_usuario --dry-run")
        print("2. Revisa los logs en la carpeta logs/")
        print("3. Si todo funciona, quita --dry-run para subir videos reales")
    else:
        print("⚠️ Hay problemas en la configuración. Revisa los errores arriba.")
        print("\n📝 Para obtener ayuda:")
        print("1. Revisa SETUP.md para instrucciones detalladas")
        print("2. Verifica que todas las dependencias están instaladas")
        print("3. Configura las variables de entorno en .env")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
