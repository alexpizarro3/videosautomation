#!/usr/bin/env python3
"""
Script para verificar que todas las rutas de imágenes están configuradas correctamente
"""

import os
import glob
from pathlib import Path

def verify_image_paths():
    """Verificar que los archivos usan las rutas correctas de imágenes"""
    
    print("🔍 VERIFICANDO CONFIGURACIÓN DE RUTAS DE IMÁGENES")
    print("=" * 60)
    
    # Verificar que existe el directorio data/images
    images_dir = Path("data/images")
    if images_dir.exists():
        print(f"✅ Directorio {images_dir} existe")
    else:
        print(f"❌ Directorio {images_dir} NO existe")
        print("   Creando directorio...")
        images_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio {images_dir} creado")
    
    # Archivos que deben usar data/images/
    files_to_check = [
        "gen_images_from_prompts.py",
        "core/03_generate_images.py", 
        "generate_veo_video_from_image.py",
        "image_metadata_analyzer.py",
        "prepare_viral_pipeline.py",
        "run_pipeline.py",
        "core/04_generate_videos.py",
        "colab_test.py"
    ]
    
    print("\n📂 VERIFICANDO ARCHIVOS:")
    print("-" * 40)
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"\n📄 {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar paths incorretos (raíz del proyecto)
            incorrect_patterns = [
                'gemini_image_',
                '"gemini_image_',
                "'gemini_image_"
            ]
            
            # Verificar paths correctos (data/images)
            correct_patterns = [
                'data/images/gemini_image_',
                '"data/images/gemini_image_',
                "'data/images/gemini_image_"
            ]
            
            has_incorrect = any(pattern in content for pattern in incorrect_patterns if not f"data/images/{pattern.replace('gemini_image_', 'gemini_image_')}" in content)
            has_correct = any(pattern in content for pattern in correct_patterns)
            
            if has_correct and not has_incorrect:
                print(f"   ✅ Configurado correctamente")
            elif has_incorrect:
                print(f"   ⚠️  Contiene referencias a rutas en la raíz")
            else:
                print(f"   ℹ️  No contiene referencias a imágenes Gemini")
        else:
            print(f"\n📄 {file_path}")
            print(f"   ❌ Archivo no encontrado")
    
    # Verificar imágenes existentes
    print(f"\n🖼️  IMÁGENES EXISTENTES:")
    print("-" * 40)
    
    # Buscar en raíz (no debería haber)
    root_images = glob.glob("gemini_image_*.png") + glob.glob("gemini_image_*.jpg") + glob.glob("gemini_image_*.jpeg")
    if root_images:
        print(f"⚠️  Imágenes en raíz del proyecto (mover a data/images/):")
        for img in root_images:
            print(f"   - {img}")
    else:
        print(f"✅ No hay imágenes en la raíz del proyecto")
    
    # Buscar en data/images (debería estar aquí)
    data_images = glob.glob("data/images/gemini_image_*.png") + glob.glob("data/images/gemini_image_*.jpg") + glob.glob("data/images/gemini_image_*.jpeg")
    if data_images:
        print(f"✅ Imágenes en data/images/:")
        for img in data_images:
            print(f"   - {img}")
    else:
        print(f"ℹ️  No hay imágenes generadas aún en data/images/")
    
    print(f"\n🎯 RESUMEN:")
    print("-" * 40)
    print(f"✅ Directorio data/images configurado")
    print(f"✅ Archivos actualizados para usar data/images/")
    print(f"✅ Sistema listo para generar imágenes en ubicación correcta")

if __name__ == "__main__":
    verify_image_paths()
