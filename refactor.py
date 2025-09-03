#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 SCRIPT DE REFACTORIZACIÓN AUTOMÁTICA
📁 Reorganiza todo el proyecto videosautomation
"""

import os
import shutil
import json
from pathlib import Path

def create_new_structure():
    """Crea la nueva estructura de carpetas"""
    print("🏗️  CREANDO NUEVA ESTRUCTURA...")
    
    folders = [
        "core",
        "utils", 
        "data/analytics",
        "data/images", 
        "data/videos/original",
        "data/videos/processed", 
        "data/videos/final",
        "data/logs",
        "config",
        "archive/old_scripts",
        "archive/testing",
        "archive/experiments",
        "archive/debug_files"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Creada: {folder}/")
    
    print("✅ Estructura de carpetas creada\n")

def migrate_core_scripts():
    """Migra y renombra los scripts principales"""
    print("📦 MIGRANDO SCRIPTS PRINCIPALES...")
    
    migrations = {
        # Script original → Nuevo nombre y ubicación
        "test_tiktok_scraping.py": "core/01_scrape_analytics.py",
        "generate_prompts_from_scrap.py": "core/02_generate_prompts.py",
        "gen_images_from_prompts.py": "core/03_generate_images.py", 
        "generate_veo_video_from_image.py": "core/04_generate_videos.py",
        "procesar_final_tiktok.py": "core/05_optimize_videos.py",
        "unir_videos_simple.py": "core/06_unite_videos.py",
        "subir_tiktok_playwright.py": "core/07_upload_tiktok.py"
    }
    
    for old_file, new_file in migrations.items():
        if os.path.exists(old_file):
            shutil.copy2(old_file, new_file)
            print(f"✅ {old_file} → {new_file}")
        else:
            print(f"⚠️  No encontrado: {old_file}")
    
    print("✅ Scripts principales migrados\n")

def migrate_utils():
    """Migra archivos de utilidades"""
    print("🔧 MIGRANDO UTILIDADES...")
    
    utils_files = [
        "gemini_utils.py",
        # Otros archivos utils se crearán consolidando funciones
    ]
    
    for file in utils_files:
        if os.path.exists(file):
            shutil.copy2(file, f"utils/{file}")
            print(f"✅ {file} → utils/{file}")
    
    print("✅ Utilidades migradas\n")

def archive_test_files():
    """Archiva todos los archivos de testing"""
    print("📦 ARCHIVANDO ARCHIVOS DE TESTING...")
    
    test_patterns = [
        "test_*.py",
        "*_test.py", 
        "*_debug.py",
        "diagnostic_*.py"
    ]
    
    import glob
    archived_count = 0
    
    for pattern in test_patterns:
        for file in glob.glob(pattern):
            if os.path.isfile(file):
                shutil.move(file, f"archive/testing/{file}")
                print(f"📦 {file} → archive/testing/")
                archived_count += 1
    
    print(f"✅ {archived_count} archivos de testing archivados\n")

def archive_experimental_files():
    """Archiva scripts experimentales"""
    print("🧪 ARCHIVANDO SCRIPTS EXPERIMENTALES...")
    
    experimental_files = [
        "advanced_visual_analyzer.py",
        "authentic_viral_fusion.py", 
        "create_visual_concept.py",
        "definitive_viral_generator.py",
        "final_authentic_concept.py",
        "final_viral_video_generator.py",
        "intelligent_*.py",
        "viral_*.py",
        "real_*.py"
    ]
    
    import glob
    archived_count = 0
    
    for pattern in experimental_files:
        for file in glob.glob(pattern):
            if os.path.isfile(file):
                shutil.move(file, f"archive/experiments/{file}")
                print(f"🧪 {file} → archive/experiments/")
                archived_count += 1
    
    print(f"✅ {archived_count} scripts experimentales archivados\n")

def clean_debug_files():
    """Limpia archivos de debug temporales"""
    print("🗑️  LIMPIANDO ARCHIVOS DE DEBUG...")
    
    debug_patterns = [
        "debug_*.png",
        "debug_*.html", 
        "dragdrop_*.png",
        "test_*.png",
        "anti_bot_*.png",
        "gemini_image_*.png"
    ]
    
    import glob
    deleted_count = 0
    archived_count = 0
    
    for pattern in debug_patterns:
        for file in glob.glob(pattern):
            if os.path.isfile(file):
                # Algunos archivos importantes se archivan, otros se eliminan
                if "important" in file or file.startswith("final_"):
                    shutil.move(file, f"archive/debug_files/{file}")
                    archived_count += 1
                else:
                    os.remove(file)
                    deleted_count += 1
    
    print(f"🗑️  {deleted_count} archivos temporales eliminados")
    print(f"📦 {archived_count} archivos debug archivados\n")

def organize_videos():
    """Organiza los videos por categorías"""
    print("🎬 ORGANIZANDO VIDEOS...")
    
    import glob
    
    # Videos originales de Veo 3
    for file in glob.glob("data/videos/veo_video_*.mp4"):
        if "_tiktok_FINAL" not in file and "_crop" not in file:
            filename = os.path.basename(file)
            shutil.move(file, f"data/videos/original/{filename}")
            print(f"📁 {filename} → data/videos/original/")
    
    # Videos procesados (crop, zoom, etc.)
    processed_patterns = ["*_crop*.mp4", "*_tiktok_FINAL.mp4"]
    for pattern in processed_patterns:
        for file in glob.glob(pattern):
            if os.path.isfile(file):
                filename = os.path.basename(file)
                shutil.move(file, f"data/videos/processed/{filename}")
                print(f"🔧 {filename} → data/videos/processed/")
    
    # Videos finales unidos
    final_patterns = ["videos_unidos_*.mp4"]
    for pattern in final_patterns:
        for file in glob.glob(pattern):
            if os.path.isfile(file):
                filename = os.path.basename(file)
                shutil.move(file, f"data/videos/final/{filename}")
                print(f"🎯 {filename} → data/videos/final/")
    
    print("✅ Videos organizados\n")

def clean_pycache():
    """Elimina archivos __pycache__"""
    print("🧹 LIMPIANDO __pycache__...")
    
    import glob
    for pycache_dir in glob.glob("**/__pycache__", recursive=True):
        shutil.rmtree(pycache_dir)
        print(f"🗑️  Eliminado: {pycache_dir}")
    
    print("✅ Cache limpio\n")

def create_pipeline_runner():
    """Crea el script principal del pipeline"""
    print("🚀 CREANDO SCRIPT PRINCIPAL DEL PIPELINE...")
    
    pipeline_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 PIPELINE PRINCIPAL VIDEOSAUTOMATION
📱 Ejecuta el pipeline completo de generación de videos TikTok
"""

import sys
import os
import subprocess
import argparse

def run_step(step_num, step_name, script_path):
    """Ejecuta un paso del pipeline"""
    print(f"\\n🎯 PASO {step_num}: {step_name}")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                               capture_output=True, text=True, check=True)
        print(f"✅ Paso {step_num} completado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en paso {step_num}: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Pipeline de generación de videos TikTok")
    parser.add_argument("--all", action="store_true", help="Ejecutar pipeline completo")
    parser.add_argument("--steps", help="Rango de pasos (ej: 1-4)")
    parser.add_argument("--step", type=int, help="Ejecutar paso específico")
    
    args = parser.parse_args()
    
    # Definir pasos del pipeline
    steps = [
        (1, "Análisis TikTok", "core/01_scrape_analytics.py"),
        (2, "Generación Prompts", "core/02_generate_prompts.py"), 
        (3, "Generación Imágenes", "core/03_generate_images.py"),
        (4, "Generación Videos", "core/04_generate_videos.py"),
        (5, "Optimización Videos", "core/05_optimize_videos.py"),
        (6, "Unir Videos", "core/06_unite_videos.py"),
        (7, "Subida TikTok", "core/07_upload_tiktok.py")
    ]
    
    print("🎬 PIPELINE VIDEOSAUTOMATION")
    print("=" * 40)
    
    if args.all:
        print("🚀 Ejecutando pipeline completo...")
        for step_num, step_name, script_path in steps:
            if not run_step(step_num, step_name, script_path):
                print(f"💥 Pipeline detenido en paso {step_num}")
                sys.exit(1)
        print("\\n🎉 ¡Pipeline completado exitosamente!")
        
    elif args.step:
        step_num = args.step
        if 1 <= step_num <= len(steps):
            _, step_name, script_path = steps[step_num - 1]
            run_step(step_num, step_name, script_path)
        else:
            print(f"❌ Paso {step_num} no válido. Usa 1-{len(steps)}")
            
    elif args.steps:
        try:
            start, end = map(int, args.steps.split("-"))
            print(f"🚀 Ejecutando pasos {start}-{end}...")
            for i in range(start - 1, end):
                step_num, step_name, script_path = steps[i]
                if not run_step(step_num, step_name, script_path):
                    print(f"💥 Pipeline detenido en paso {step_num}")
                    sys.exit(1)
            print("\\n🎉 ¡Pasos completados exitosamente!")
        except ValueError:
            print("❌ Formato de pasos inválido. Usa: --steps 1-4")
    else:
        print("ℹ️  Uso:")
        print("  python run_pipeline.py --all           # Pipeline completo")
        print("  python run_pipeline.py --steps 1-4     # Pasos 1 al 4") 
        print("  python run_pipeline.py --step 5        # Solo paso 5")
        print("\\n📋 Pasos disponibles:")
        for step_num, step_name, _ in steps:
            print(f"  {step_num}. {step_name}")

if __name__ == "__main__":
    main()
'''
    
    with open("run_pipeline.py", "w", encoding="utf-8") as f:
        f.write(pipeline_script)
    
    print("✅ Script principal creado: run_pipeline.py\n")

def create_summary():
    """Crea resumen de la refactorización"""
    print("📊 CREANDO RESUMEN...")
    
    summary = {
        "refactoring_date": "2025-09-01",
        "files_before": len([f for f in os.listdir(".") if os.path.isfile(f)]),
        "structure": {
            "core_scripts": 7,
            "utils": ["gemini_utils.py", "video_utils.py", "tiktok_utils.py"],
            "archived_tests": "archive/testing/",
            "archived_experiments": "archive/experiments/", 
            "videos_organized": {
                "original": "data/videos/original/",
                "processed": "data/videos/processed/",
                "final": "data/videos/final/"
            }
        },
        "pipeline_steps": [
            "01_scrape_analytics.py",
            "02_generate_prompts.py", 
            "03_generate_images.py",
            "04_generate_videos.py",
            "05_optimize_videos.py",
            "06_unite_videos.py", 
            "07_upload_tiktok.py"
        ]
    }
    
    with open("REFACTORING_SUMMARY.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("✅ Resumen guardado: REFACTORING_SUMMARY.json\n")

def main():
    print("🧹 INICIANDO REFACTORIZACIÓN AUTOMÁTICA")
    print("=" * 50)
    print("⚠️  ASEGÚRATE DE HABER HECHO git push ANTES!")
    
    response = input("\\n¿Continuar con la refactorización? (y/N): ")
    if response.lower() != 'y':
        print("❌ Refactorización cancelada")
        return
    
    # Ejecutar refactorización
    create_new_structure()
    migrate_core_scripts()
    migrate_utils()
    archive_test_files()
    archive_experimental_files() 
    clean_debug_files()
    organize_videos()
    clean_pycache()
    create_pipeline_runner()
    create_summary()
    
    print("🎉 ¡REFACTORIZACIÓN COMPLETADA!")
    print("=" * 50)
    print("✅ Estructura organizada")
    print("✅ Scripts principales numerados") 
    print("✅ Archivos antiguos archivados")
    print("✅ Videos organizados por categoría")
    print("✅ Pipeline principal creado")
    print("\\n🚀 Nuevo uso:")
    print("  python run_pipeline.py --all")
    print("  python core/05_optimize_videos.py")

if __name__ == "__main__":
    main()
