#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 TEST TIKTOK UPLOAD
Prueba rápida de subida a TikTok para verificar funcionamiento
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_tiktok_upload():
    """
    Probar upload a TikTok con el primer video disponible
    """
    print("📱 TEST TIKTOK UPLOAD")
    print("Verificación de funcionamiento")
    print("=" * 60)
    
    try:
        # Verificar carpeta de videos
        tiktok_folder = "data/videos/processed"
        
        if not os.path.exists(tiktok_folder):
            print(f"❌ Carpeta no encontrada: {tiktok_folder}")
            return False
        
        # Buscar videos disponibles
        videos_available = list(Path(tiktok_folder).glob("*.mp4"))
        
        if not videos_available:
            print(f"❌ No hay videos .mp4 en {tiktok_folder}")
            return False
        
        print(f"📁 VIDEOS ENCONTRADOS: {len(videos_available)}")
        for i, video in enumerate(videos_available, 1):
            size_mb = video.stat().st_size / 1024 / 1024
            print(f"   {i}. {video.name} ({size_mb:.1f} MB)")
        
        # Verificar script de TikTok
        tiktok_script = "subir_tiktok_selenium_final_v5.py"
        if not os.path.exists(tiktok_script):
            print(f"❌ Script TikTok no encontrado: {tiktok_script}")
            return False
        
        print(f"✅ Script TikTok encontrado: {tiktok_script}")
        
        # Importar funciones necesarias
        print(f"\n🔧 Verificando imports...")
        
        try:
            from subir_tiktok_selenium_final_v5 import subir_video_selenium_xpaths_definitivos, generar_descripcion_dinamica
            print("✅ Funciones de TikTok importadas correctamente")
        except ImportError as e:
            print(f"❌ Error importando funciones TikTok: {e}")
            return False
        except Exception as e:
            print(f"❌ Error en importación: {e}")
            return False
        
        # Seleccionar primer video para prueba
        test_video = videos_available[0]
        
        print(f"\n📱 PREPARANDO TEST:")
        print(f"   📁 Archivo: {test_video.name}")
        print(f"   📊 Tamaño: {test_video.stat().st_size/1024/1024:.1f} MB")
        print(f"   📍 Ruta: {test_video}")
        
        # Generar descripción de prueba
        print(f"\n🤖 Generando descripción...")
        try:
            descripcion = generar_descripcion_dinamica(str(test_video))
            print(f"✅ Descripción generada: {descripcion[:50]}...")
        except Exception as e:
            print(f"⚠️ Error generando descripción, usando básica: {e}")
            descripcion = "🔥 Contenido viral increíble! #viral #trending #fyp"
        
        print(f"\n🚀 INICIANDO TEST DE UPLOAD...")
        print("⚠️ Se abrirá navegador automatizado")
        print("⚠️ PRESIONA CTRL+C SI QUIERES CANCELAR")
        
        # Esperar confirmación
        input("\n📌 Presiona ENTER para continuar o CTRL+C para cancelar...")
        
        # Ejecutar upload de prueba
        try:
            result = subir_video_selenium_xpaths_definitivos(str(test_video), descripcion)
            
            if result:
                print(f"\n🎉 ¡TEST DE TIKTOK EXITOSO!")
                print(f"   ✅ Video subido: {test_video.name}")
                print(f"   📝 Descripción: {descripcion}")
                print(f"   ⏰ Completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                return True
            else:
                print(f"\n❌ Test de TikTok falló")
                print(f"   📁 Video: {test_video.name}")
                print(f"   🔍 Revisar logs del navegador")
                return False
                
        except KeyboardInterrupt:
            print(f"\n⚠️ Test cancelado por el usuario")
            return False
        except Exception as e:
            print(f"\n❌ Error durante test: {e}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error en test de TikTok: {e}")
        logger.error(f"Error en test: {e}")
        return False

def show_tiktok_requirements():
    """
    Mostrar requisitos para TikTok
    """
    print("\n📋 REQUISITOS PARA TIKTOK:")
    print("=" * 50)
    
    print("🔧 CONFIGURACIÓN:")
    print("   ✅ Chrome instalado")
    print("   ✅ ChromeDriver configurado")
    print("   ✅ Selenium instalado")
    print("   ✅ Scripts anti-detección activos")
    
    print("\n📱 CUENTA TIKTOK:")
    print("   📧 Cuenta activa requerida")
    print("   🔑 Login manual en primera ejecución")
    print("   🍪 Cookies guardadas automáticamente")
    
    print("\n📹 VIDEOS:")
    print("   📏 Máximo 60 segundos")
    print("   📐 Formato vertical preferido (9:16)")
    print("   📊 Tamaño máximo ~100MB")

def main():
    """
    Función principal
    """
    print("📱 TEST TIKTOK UPLOADER")
    print("=" * 50)
    
    show_tiktok_requirements()
    
    print(f"\n🚀 Iniciando test de TikTok...")
    
    success = test_tiktok_upload()
    
    if success:
        print(f"\n🎉 ¡TEST COMPLETADO EXITOSAMENTE!")
        print(f"✅ El sistema TikTok está funcionando correctamente")
        print(f"🔄 Puedes usar upload_tiktok_masivo.py para subir todos")
    else:
        print(f"\n❌ Test falló")
        print(f"🔍 Revisar configuración y dependencias")

if __name__ == "__main__":
    main()
