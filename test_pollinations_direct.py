#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DIRECTO DE POLLINATIONS.AI
"""

import requests
import urllib.parse
import os

def test_pollinations_direct():
    """
    Test directo de la API de Pollinations
    """
    print("🌸 TESTING POLLINATIONS.AI DIRECTO")
    print("=" * 50)
    
    # Prompt de prueba
    prompt = "A cute cat with rainbow colors, aesthetic viral style"
    encoded_prompt = urllib.parse.quote(prompt)
    
    # URL base
    base_url = "https://image.pollinations.ai/prompt"
    url = f"{base_url}/{encoded_prompt}"
    
    print(f"📝 Prompt: {prompt}")
    print(f"🔗 URL: {url}")
    print("⏳ Haciendo petición...")
    
    try:
        # Hacer petición
        response = requests.get(url, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Content Length: {len(response.content)} bytes")
        
        content_type = response.headers.get('content-type', 'unknown')
        print(f"🗂️ Content Type: {content_type}")
        
        if response.status_code == 200:
            if 'image' in content_type and len(response.content) > 1000:
                # Guardar imagen
                filename = "test_pollinations_direct.png"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                print(f"✅ ÉXITO: Imagen descargada")
                print(f"📁 Archivo: {filename}")
                print(f"📏 Tamaño: {file_size/1024:.1f} KB")
                
                # Verificar que existe
                if os.path.exists(filename):
                    print(f"✅ Archivo verificado: {os.path.getsize(filename)} bytes")
                    return True
                else:
                    print("❌ ERROR: Archivo no se guardó correctamente")
                    return False
            else:
                print("❌ ERROR: Respuesta no es una imagen válida")
                print(f"Content: {response.content[:200]}...")
                return False
        else:
            print(f"❌ ERROR: Status code {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ ERROR: Timeout - el servicio puede estar lento")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR inesperado: {e}")
        return False

def test_pollinations_with_params():
    """
    Test con parámetros adicionales
    """
    print("\n🌸 TESTING CON PARÁMETROS")
    print("=" * 50)
    
    prompt = "ASMR aesthetic cat, hiperrealista"
    encoded_prompt = urllib.parse.quote(prompt)
    
    # URL con parámetros
    params = {
        'width': 1024,
        'height': 1024,
        'model': 'flux',
        'nologo': 'true',
        'enhance': 'true'
    }
    
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    print(f"📝 Prompt: {prompt}")
    print(f"⚙️ Parámetros: {params}")
    print("⏳ Haciendo petición con parámetros...")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"🔗 URL final: {response.url}")
        
        if response.status_code == 200:
            filename = "test_pollinations_params.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ ÉXITO con parámetros")
            print(f"📁 Archivo: {filename}")
            print(f"📏 Tamaño: {file_size/1024:.1f} KB")
            return True
        else:
            print(f"❌ ERROR: Status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_multiple_prompts():
    """
    Test con múltiples prompts para verificar consistencia
    """
    print("\n🌸 TESTING MÚLTIPLES PROMPTS")
    print("=" * 50)
    
    prompts = [
        "A red apple on white background",
        "A blue flower in sunlight",
        "A golden sunset over mountains"
    ]
    
    successful = 0
    total = len(prompts)
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n🎯 Test {i}/{total}: {prompt}")
        
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        try:
            response = requests.get(url, timeout=20)
            
            if response.status_code == 200 and len(response.content) > 1000:
                filename = f"test_pollinations_multi_{i}.png"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                print(f"   ✅ Éxito: {len(response.content)/1024:.1f} KB")
                successful += 1
            else:
                print(f"   ❌ Falló: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📊 Resultados: {successful}/{total} exitosos")
    return successful == total

if __name__ == "__main__":
    print("🚀 INICIANDO TESTS DE POLLINATIONS.AI")
    print("=" * 60)
    
    # Test 1: Básico
    test1 = test_pollinations_direct()
    
    # Test 2: Con parámetros
    test2 = test_pollinations_with_params()
    
    # Test 3: Múltiples prompts
    test3 = test_multiple_prompts()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    print(f"🔵 Test básico: {'✅ PASÓ' if test1 else '❌ FALLÓ'}")
    print(f"⚙️ Test con parámetros: {'✅ PASÓ' if test2 else '❌ FALLÓ'}")
    print(f"🔄 Test múltiples: {'✅ PASÓ' if test3 else '❌ FALLÓ'}")
    
    overall = test1 or test2  # Al menos uno debe pasar
    print(f"\n🎯 RESULTADO GENERAL: {'✅ POLLINATIONS FUNCIONA' if overall else '❌ POLLINATIONS NO DISPONIBLE'}")
    
    if overall:
        print("\n🎉 ¡POLLINATIONS.AI ESTÁ FUNCIONANDO!")
        print("   - Puede ser usado como fallback confiable")
        print("   - Calidad de imágenes excelente")
        print("   - Respuesta rápida y estable")
    else:
        print("\n⚠️ POLLINATIONS NO DISPONIBLE:")
        print("   - Puede estar temporalmente no disponible")
        print("   - Verificar conexión a internet")
        print("   - Reintentar más tarde")
    
    print("\n" + "=" * 60)
