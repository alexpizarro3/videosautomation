#!/usr/bin/env python3
"""
Orquestador PIPELINE NARRATIVO ASMR
Permite ejecutar el pipeline narrativo de forma manual o automática.
"""
import os
import sys
from pathlib import Path
from src.utils.cleanup_video_folders import clean_video_folders

PIPELINE_STEPS = [
    ("Extracción de datos y tendencias", "test_tiktok_scraping.py"),
    ("Generación de historias narrativas ASMR", "generate_story_prompts_from_scrap.py"),
    ("Generación de imágenes por historia", "generate_story_images.py"),
    ("Selección de la mejor historia", "select_best_story.py"),
    ("Generación de videos narrativos secuenciales", "generate_narrative_videos_veo3.py"),
    ("Procesamiento final de videos", "procesar_final_tiktok.py"),
    ("Unión de videos narrativos", "unir_videos_simple.py"),
    ("Upload dual TikTok + YouTube Shorts", "dual_uploader_automatic.py"),
    ("Backup en la nube", "upload_to_drive.py")
]

def run_step(script):
    print(f"\n🚀 Ejecutando: {script}")
    exit_code = os.system(f"python {script}")
    if exit_code != 0:
        print(f"❌ Error ejecutando {script}")
    else:
        print(f"✅ Completado: {script}")

def run_pipeline(auto=True):
    print("\n=== PIPELINE NARRATIVO ASMR ===")
    if auto:
        print("Modo automático: ejecutando todos los pasos...")
        for name, script in PIPELINE_STEPS:
            print(f"\n➡️ {name}")
            run_step(script)
        print("\n🎉 Pipeline narrativo completado!")
    else:
        print("Modo manual: selecciona los pasos a ejecutar.")
        for idx, (name, script) in enumerate(PIPELINE_STEPS, 1):
            print(f"{idx}. {name} ({script})")
        print("0. Salir")
        while True:
            try:
                sel = int(input("\nSelecciona el paso a ejecutar (0 para salir): "))
                if sel == 0:
                    break
                if 1 <= sel <= len(PIPELINE_STEPS):
                    name, script = PIPELINE_STEPS[sel-1]
                    print(f"\n➡️ {name}")
                    run_step(script)
                else:
                    print("Opción inválida.")
            except KeyboardInterrupt:
                break
            except Exception:
                print("Opción inválida.")
    print("\n✅ Orquestador narrativo finalizado.")

def main():
    # Limpiar carpetas de videos antes de iniciar
    clean_video_folders()

    print("\n=== ORQUESTADOR PIPELINE NARRATIVO ASMR ===")
    print("1. Ejecutar pipeline completo (automático)")
    print("2. Ejecutar pasos manualmente")
    print("0. Salir")
    try:
        sel = int(input("\nSelecciona modo: "))
        if sel == 1:
            run_pipeline(auto=True)
        elif sel == 2:
            run_pipeline(auto=False)
    except KeyboardInterrupt:
        pass
    except Exception:
        print("Opción inválida.")
    print("\n👋 Orquestador narrativo cerrado.")

if __name__ == "__main__":
    main()
