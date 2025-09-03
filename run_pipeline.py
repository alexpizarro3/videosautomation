#!/usr/bin/env python3
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
    print(f"\n🎯 PASO {step_num}: {step_name}")
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
        print("\n🎉 ¡Pipeline completado exitosamente!")
        
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
            print("\n🎉 ¡Pasos completados exitosamente!")
        except ValueError:
            print("❌ Formato de pasos inválido. Usa: --steps 1-4")
    else:
        print("ℹ️  Uso:")
        print("  python run_pipeline.py --all           # Pipeline completo")
        print("  python run_pipeline.py --steps 1-4     # Pasos 1 al 4") 
        print("  python run_pipeline.py --step 5        # Solo paso 5")
        print("\n📋 Pasos disponibles:")
        for step_num, step_name, _ in steps:
            print(f"  {step_num}. {step_name}")

if __name__ == "__main__":
    main()
