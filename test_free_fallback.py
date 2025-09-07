#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DEL SISTEMA DE FALLBACK GRATUITO
Valida que Pollinations.AI y HuggingFace funcionan como fallback
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_pollinations_fallback():
    """
    Test completo de Pollinations.AI
    """
    print("🌸 TESTING POLLINATIONS.AI FALLBACK")
    print("=" * 60)
    
    # Test 1: Importar módulo
    print("\n🔍 Test 1: Importando módulo...")
    try:
        from free_fallback_generator import PollinationsFallbackGenerator
        print("   ✅ Módulo importado correctamente")
    except ImportError as e:
        print(f"   ❌ Error importando módulo: {e}")
        return False
    
    # Test 2: Inicializar generador
    print("\n🔍 Test 2: Inicializando generador...")
    try:
        generator = PollinationsFallbackGenerator()
        print("   ✅ Generador inicializado")
    except Exception as e:
        print(f"   ❌ Error inicializando: {e}")
        return False
    
    # Test 3: Verificar disponibilidad
    print("\n🔍 Test 3: Verificando disponibilidad...")
    try:
        available = generator.is_available()
        print(f"   {'✅' if available else '⚠️'} Pollinations disponible: {available}")
        
        if not available:
            print("   💡 Posibles causas:")
            print("      - Sin conexión a internet")
            print("      - Servicio temporalmente no disponible")
            return False
    except Exception as e:
        print(f"   ❌ Error verificando disponibilidad: {e}")
        return False
    
    # Test 4: Test de conexión completa
    print("\n🔍 Test 4: Test de conexión completa...")
    try:
        test_result = generator.test_connection()
        print(f"   Disponible: {test_result.get('available', False)}")
        print(f"   Test generación: {test_result.get('test_generation', False)}")
        
        if test_result.get('error'):
            print(f"   Error: {test_result['error']}")
            return False
            
        if not test_result.get('available'):
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de conexión: {e}")
        return False
    
    # Test 5: Generación real
    print("\n🔍 Test 5: Generación de imagen real...")
    try:
        test_prompt = "A cute cat with rainbow colors, aesthetic viral style"
        test_path = "test_pollinations_real.png"
        
        print(f"   Prompt: {test_prompt}")
        print(f"   Guardando en: {test_path}")
        
        success = generator.generate_viral_image(test_prompt, test_path)
        
        if success and os.path.exists(test_path):
            file_size = os.path.getsize(test_path)
            print(f"   ✅ Imagen generada exitosamente")
            print(f"   📁 Archivo: {test_path}")
            print(f"   📏 Tamaño: {file_size/1024:.1f} KB")
            
            # Limpiar archivo de prueba
            try:
                os.remove(test_path)
                print("   🧹 Archivo de prueba eliminado")
            except:
                pass
                
            return True
        else:
            print("   ❌ Fallo en generación de imagen")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en generación: {e}")
        return False

def test_huggingface_fallback():
    """
    Test de HuggingFace Inference API
    """
    print("\n🤗 TESTING HUGGINGFACE FALLBACK")
    print("=" * 60)
    
    # Test 1: Importar módulo
    print("\n🔍 Test 1: Importando módulo...")
    try:
        from free_fallback_generator import HuggingFaceFallbackGenerator
        print("   ✅ Módulo importado correctamente")
    except ImportError as e:
        print(f"   ❌ Error importando módulo: {e}")
        return False
    
    # Test 2: Inicializar generador
    print("\n🔍 Test 2: Inicializando generador...")
    try:
        generator = HuggingFaceFallbackGenerator()
        print("   ✅ Generador inicializado")
        
        # Verificar si hay token configurado
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
        print(f"   🔑 Token HF: {'Configurado' if hf_token else 'No configurado (OK)'}")
        
    except Exception as e:
        print(f"   ❌ Error inicializando: {e}")
        return False
    
    # Test 3: Verificar disponibilidad
    print("\n🔍 Test 3: Verificando disponibilidad...")
    try:
        available = generator.is_available()
        print(f"   {'✅' if available else '⚠️'} HuggingFace disponible: {available}")
        
        if not available:
            print("   💡 Posibles causas:")
            print("      - Sin conexión a internet")
            print("      - Modelo en mantenimiento")
            return False
    except Exception as e:
        print(f"   ❌ Error verificando disponibilidad: {e}")
        return False
    
    # Test 4: Generación de prueba (rápida)
    print("\n🔍 Test 4: Generación de imagen (puede tomar tiempo)...")
    try:
        test_prompt = "A simple blue flower"
        test_path = "test_huggingface_real.png"
        
        print(f"   Prompt: {test_prompt}")
        print(f"   ⏳ Generando... (esto puede tomar 30-60 segundos)")
        
        success = generator.generate_image(test_prompt, test_path)
        
        if success and os.path.exists(test_path):
            file_size = os.path.getsize(test_path)
            print(f"   ✅ Imagen generada exitosamente")
            print(f"   📁 Archivo: {test_path}")
            print(f"   📏 Tamaño: {file_size/1024:.1f} KB")
            
            # Limpiar archivo de prueba
            try:
                os.remove(test_path)
                print("   🧹 Archivo de prueba eliminado")
            except:
                pass
                
            return True
        else:
            print("   ⚠️ Fallo en generación (normal en tier gratuito)")
            print("   💡 HuggingFace puede tener colas en horas pico")
            return False
            
    except Exception as e:
        print(f"   ⚠️ Error en generación: {e}")
        print("   💡 Esto es normal - HuggingFace puede estar ocupado")
        return False

def test_integration():
    """
    Test de integración con el script principal
    """
    print("\n🔗 TESTING INTEGRACIÓN")
    print("=" * 60)
    
    try:
        # Verificar que el script principal puede importar los fallbacks
        import gen_images_from_prompts
        print("   ✅ Script principal importado correctamente")
        
        # Verificar que las funciones están disponibles
        if hasattr(gen_images_from_prompts, 'generate_image_with_fallback'):
            print("   ✅ Función de fallback disponible")
        else:
            print("   ❌ Función de fallback no encontrada")
            return False
        
        # Verificar que los generadores están inicializados
        if hasattr(gen_images_from_prompts, 'pollinations_fallback'):
            print("   ✅ Pollinations fallback integrado")
        else:
            print("   ❌ Pollinations fallback no integrado")
            return False
        
        if hasattr(gen_images_from_prompts, 'huggingface_fallback'):
            print("   ✅ HuggingFace fallback integrado")
        else:
            print("   ❌ HuggingFace fallback no integrado")
            return False
            
        return True
        
    except Exception as e:
        print(f"   ❌ Error en integración: {e}")
        return False

def main():
    """
    Ejecutar todos los tests
    """
    print("🚀 INICIANDO TESTS DEL SISTEMA DE FALLBACK GRATUITO")
    print("=" * 70)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Test de Pollinations
    test1_passed = test_pollinations_fallback()
    
    # Test de HuggingFace
    test2_passed = test_huggingface_fallback()
    
    # Test de integración
    test3_passed = test_integration()
    
    # Resultado final
    print("\n" + "=" * 70)
    print("📊 RESULTADOS FINALES")
    print("=" * 70)
    print(f"🌸 Test Pollinations: {'✅ PASÓ' if test1_passed else '❌ FALLÓ'}")
    print(f"🤗 Test HuggingFace: {'✅ PASÓ' if test2_passed else '⚠️ NO DISPONIBLE'}")
    print(f"🔗 Test Integración: {'✅ PASÓ' if test3_passed else '❌ FALLÓ'}")
    
    # Al menos un fallback debe funcionar
    at_least_one_fallback = test1_passed or test2_passed
    overall_success = at_least_one_fallback and test3_passed
    
    print(f"\n🎯 RESULTADO GENERAL: {'✅ SISTEMA FUNCIONAL' if overall_success else '❌ CONFIGURACIÓN REQUERIDA'}")
    
    if overall_success:
        print("\n🎉 ¡SISTEMA DE FALLBACK GRATUITO FUNCIONANDO!")
        if test1_passed and test2_passed:
            print("   - AMBOS fallbacks funcionando (máxima robustez)")
        elif test1_passed:
            print("   - Pollinations.AI funcionando (excelente)")
        elif test2_passed:
            print("   - HuggingFace funcionando (bueno)")
        print("   - Tu pipeline ahora es ultra-robusto y 100% gratuito")
        print("   - Se activará automáticamente si Gemini falla")
    else:
        print("\n⚠️ ACCIÓN REQUERIDA:")
        if not at_least_one_fallback:
            print("   - Verificar conexión a internet")
            print("   - Reintentar más tarde si servicios están ocupados")
        if not test3_passed:
            print("   - Revisar importaciones en script principal")
    
    print("\n" + "=" * 70)
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
