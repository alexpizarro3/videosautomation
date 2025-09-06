#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 VERIFICADOR RÁPIDO DE PIPELINE
Verifica que todos los archivos necesarios para el pipeline estén presentes
"""

import os
import sys

def verify_pipeline_files():
    """Verifica que todos los archivos del pipeline estén presentes"""
    print("🔧 VERIFICADOR DE PIPELINE")
    print("=" * 50)
    
    # Lista de archivos críticos del pipeline
    critical_files = [
        "test_tiktok_scraping.py",
        "generate_prompts_from_scrap.py", 
        "gen_images_from_prompts.py",
        "prepare_viral_pipeline.py",
        "generate_veo_video_from_image.py",
        "optimizar_videos_tiktok.py",
        "procesar_final_tiktok.py",
        "subir_tiktok_selenium_final_v5.py"
    ]
    
    # Archivos de soporte necesarios
    support_files = [
        "image_metadata_analyzer.py",
        "viral_video_prompt_generator.py",
        "run_automated_pipeline.py",
        "run_pipeline_orchestrator.py",
        "run_pipeline.py"
    ]
    
    # Archivos de configuración
    config_files = [
        ".env",
        "requirements.txt",
        "config/upload_cookies_playwright.json"
    ]
    
    # Verificar archivos críticos
    print("📋 Verificando archivos críticos del pipeline:")
    missing_critical = []
    for file in critical_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - FALTANTE")
            missing_critical.append(file)
    
    # Verificar archivos de soporte
    print("\n🔧 Verificando archivos de soporte:")
    missing_support = []
    for file in support_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - FALTANTE")
            missing_support.append(file)
    
    # Verificar configuración
    print("\n⚙️ Verificando configuración:")
    missing_config = []
    for file in config_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - FALTANTE")
            missing_config.append(file)
    
    # Verificar directorios
    print("\n📁 Verificando directorios:")
    required_dirs = ["data", "data/images", "data/analytics", "config"]
    missing_dirs = []
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/ - FALTANTE")
            missing_dirs.append(dir_path)
    
    # Resumen
    print("\n" + "=" * 50)
    total_missing = len(missing_critical) + len(missing_support) + len(missing_config) + len(missing_dirs)
    
    if total_missing == 0:
        print("🎉 ¡PIPELINE COMPLETAMENTE CONFIGURADO!")
        print("✅ Todos los archivos necesarios están presentes")
        print("🚀 El pipeline está listo para ejecutarse")
        return True
    else:
        print(f"⚠️ FALTAN {total_missing} ELEMENTOS")
        
        if missing_critical:
            print(f"❌ Archivos críticos faltantes: {len(missing_critical)}")
            for file in missing_critical:
                print(f"   • {file}")
        
        if missing_support:
            print(f"🔧 Archivos de soporte faltantes: {len(missing_support)}")
            for file in missing_support:
                print(f"   • {file}")
        
        if missing_config:
            print(f"⚙️ Configuración faltante: {len(missing_config)}")
            for file in missing_config:
                print(f"   • {file}")
        
        if missing_dirs:
            print(f"📁 Directorios faltantes: {len(missing_dirs)}")
            for dir_path in missing_dirs:
                print(f"   • {dir_path}/")
        
        return False

def check_python_dependencies():
    """Verifica las dependencias de Python"""
    print("\n🐍 Verificando dependencias de Python:")
    
    required_packages = [
        "selenium", "requests", "beautifulsoup4", "google.generativeai",
        "dotenv", "yaml", "PIL", "cv2", "numpy", "undetected_chromedriver"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == "dotenv":
                import dotenv
            elif package == "yaml":
                import yaml
            elif package == "PIL":
                import PIL
            elif package == "cv2":
                import cv2
            elif package == "google.generativeai":
                import google.generativeai
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Faltan {len(missing_packages)} paquetes:")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    else:
        print("✅ Todas las dependencias están instaladas")
        return True

if __name__ == "__main__":
    print("🔧 VERIFICACIÓN COMPLETA DEL PIPELINE")
    print("=" * 60)
    
    # Verificar archivos
    files_ok = verify_pipeline_files()
    
    # Verificar dependencias
    deps_ok = check_python_dependencies()
    
    # Resultado final
    print("\n" + "=" * 60)
    if files_ok and deps_ok:
        print("🎉 ¡PIPELINE LISTO PARA EJECUTAR!")
        print("🚀 Puedes ejecutar: python run_automated_pipeline.py")
    else:
        print("❌ Pipeline necesita configuración adicional")
        print("🔧 Revisa los elementos faltantes arriba")
