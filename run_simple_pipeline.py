#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 EJECUTOR SIMPLE DEL PIPELINE VIRAL
"""

import os
import subprocess
import time
from datetime import datetime

def get_python_path():
    """Obtiene la ruta correcta de Python"""
    venv_python = "C:/Users/Alexis Pizarro/Documents/Personal/videosautomation/.venv/Scripts/python.exe"
    if os.path.exists(venv_python):
        return f'"{venv_python}"'
    return "python"

def run_script(script_name, step_num, description):
    """Ejecuta un script individual del pipeline"""
    if not os.path.exists(script_name):
        print(f"❌ Error: Script {script_name} no encontrado")
        return False
    
    print(f"\n🔄 PASO {step_num}: {description}")
    print(f"📄 Ejecutando: {script_name}")
    print("-" * 60)
    
    try:
        python_path = get_python_path()
        start_time = time.time()
        
        result = subprocess.run(
            f"{python_path} {script_name}",
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        duration = time.time() - start_time
        
        print(f"📤 Output:")
        if result.stdout:
            print(result.stdout[-500:])  # Últimas 500 chars
        
        if result.returncode == 0:
            print(f"✅ PASO {step_num} completado exitosamente")
            print(f"⏱️ Duración: {duration:.1f} segundos")
            return True
        else:
            print(f"❌ PASO {step_num} falló")
            print(f"💥 Código de error: {result.returncode}")
            if result.stderr:
                print("📤 Error:")
                print(result.stderr[-300:])
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        return False

def main():
    """Ejecuta el pipeline completo"""
    print("🚀 INICIANDO PIPELINE COMPLETO DE VIDEOS VIRALES")
    print("=" * 70)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    steps = [
        (1, "test_tiktok_scraping.py", "Scraping de TikTok"),
        (2, "generate_prompts_from_scrap.py", "Generación de Prompts"),
        (3, "gen_images_from_prompts.py", "Generación de Imágenes"),
        (4, "prepare_viral_pipeline.py", "Preparación Pipeline Viral"),
        (5, "generate_veo_video_from_image.py", "Generación de Videos"),
        (6, "procesar_final_tiktok.py", "Procesamiento Final"),
        (7, "unir_videos_simple.py", "Unión de Videos")
    ]
    
    total_start = time.time()
    failed_steps = []
    
    for step_num, script, description in steps:
        success = run_script(script, step_num, description)
        
        if not success:
            failed_steps.append(step_num)
            print(f"\n⚠️ PASO {step_num} falló. ¿Continuar? (s/n): ", end='')
            continue_choice = input().lower().strip()
            if continue_choice != 's':
                print("🛑 Pipeline detenido por el usuario")
                break
    
    total_duration = time.time() - total_start
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE EJECUCIÓN DEL PIPELINE")
    print("=" * 70)
    print(f"⏰ Tiempo total: {total_duration:.1f} segundos ({total_duration/60:.1f} minutos)")
    print(f"✅ Pasos exitosos: {len(steps) - len(failed_steps)}/{len(steps)}")
    
    if not failed_steps:
        print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
        print("🎬 Videos virales listos para publicación")
    else:
        print(f"⚠️ Pasos fallidos: {failed_steps}")

if __name__ == "__main__":
    main()
