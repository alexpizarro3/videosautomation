#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 EJECUTOR AUTOMÁTICO DEL PIPELINE VIRAL
Script maestro para ejecutar el pipeline completo de generación de videos virales
"""

import os
import sys
import subprocess
import time
from datetime import datetime

class PipelineExecutor:
    """Ejecutor automático del pipeline de videos virales"""
    
    def __init__(self):
        self.python_path = self._get_python_path()
        self.steps = {
            1: {
                "name": "Scraping de TikTok",
                "script": "test_tiktok_scraping.py",
                "description": "Extrae datos y métricas de TikTok"
            },
            2: {
                "name": "Generación de Prompts",
                "script": "generate_prompts_from_scrap.py", 
                "description": "Genera prompts para imágenes"
            },
            3: {
                "name": "Generación de Imágenes",
                "script": "gen_images_from_prompts.py",
                "description": "Crea imágenes con IA"
            },
            4: {
                "name": "Preparación Pipeline Viral",
                "script": "prepare_viral_pipeline.py",
                "description": "Analiza imágenes + genera prompts profesionales"
            },
            5: {
                "name": "Generación de Videos",
                "script": "generate_veo_video_from_image.py",
                "description": "Genera videos virales optimizados"
            },
            6: {
                "name": "Procesamiento Final",
                "script": "procesar_final_tiktok.py",
                "description": "Optimiza videos para TikTok"
            },
            7: {
                "name": "Unión de Videos",
                "script": "unir_videos_simple.py",
                "description": "Combina videos finales"
            }
        }
    
    def _get_python_path(self):
        """Obtiene la ruta correcta de Python"""
        venv_python = "C:/Users/Alexis Pizarro/Documents/Personal/videosautomation/.venv/Scripts/python.exe"
        if os.path.exists(venv_python):
            return f'"{venv_python}"'
        return "python"
    
    def _run_script(self, script_name, step_num):
        """Ejecuta un script individual del pipeline"""
        if not os.path.exists(script_name):
            print(f"❌ Error: Script {script_name} no encontrado")
            return False
        
        print(f"\n🔄 PASO {step_num}: {self.steps[step_num]['name']}")
        print(f"📄 Ejecutando: {script_name}")
        print(f"📝 {self.steps[step_num]['description']}")
        print("-" * 60)
        
        try:
            start_time = time.time()
            result = subprocess.run(
                f"{self.python_path} {script_name}",
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            duration = time.time() - start_time
            
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
    
    def run_full_pipeline(self):
        """Ejecuta el pipeline completo desde cero"""
        print("🚀 INICIANDO PIPELINE COMPLETO DE VIDEOS VIRALES")
        print("=" * 70)
        print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        steps_to_run = [1, 2, 3, 4, 5, 6, 7]
        total_start = time.time()
        failed_steps = []
        
        for step_num in steps_to_run:
            step_info = self.steps[step_num]
            success = self._run_script(step_info["script"], step_num)
            
            if not success:
                failed_steps.append(step_num)
                if step_num in [4, 5]:  # Pasos críticos
                    print(f"❌ PASO {step_num} es crítico. Deteniendo pipeline.")
                    break
        
        total_duration = time.time() - total_start
        
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE EJECUCIÓN DEL PIPELINE")
        print("=" * 70)
        print(f"⏰ Tiempo total: {total_duration:.1f} segundos ({total_duration/60:.1f} minutos)")
        print(f"✅ Pasos exitosos: {len(steps_to_run) - len(failed_steps)}/{len(steps_to_run)}")
        
        if not failed_steps:
            print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
            print("🎬 Videos virales listos para publicación")
        
        return len(failed_steps) == 0
    
    def run_quick_pipeline(self):
        """Ejecuta el pipeline rápido (con imágenes existentes)"""
        print("⚡ INICIANDO PIPELINE RÁPIDO DE VIDEOS VIRALES")
        print("=" * 70)
        
        # Verificar imágenes
        images = [f"data/images/gemini_image_{i+1}.png" for i in range(6)]
        available_images = [img for img in images if os.path.exists(img)]
        
        if not available_images:
            print("❌ No se encontraron imágenes. Ejecutar pipeline completo primero.")
            return False
        
        print(f"✅ Encontradas {len(available_images)} imágenes para procesar")
        
        steps_to_run = [4, 5, 6, 7]
        failed_steps = []
        
        for step_num in steps_to_run:
            step_info = self.steps[step_num]
            success = self._run_script(step_info["script"], step_num)
            
            if not success:
                failed_steps.append(step_num)
                if step_num in [4, 5]:
                    print(f"❌ PASO {step_num} es crítico. Deteniendo pipeline.")
                    break
        
        if not failed_steps:
            print("🎉 PIPELINE RÁPIDO COMPLETADO EXITOSAMENTE")
            print("🎬 Videos virales listos para publicación")
        
        return len(failed_steps) == 0
    
    def show_menu(self):
        """Muestra el menú interactivo"""
        print("🎬 EJECUTOR DEL PIPELINE DE VIDEOS VIRALES")
        print("=" * 60)
        print("Selecciona una opción:")
        print()
        print("1. 🚀 Pipeline Completo (desde scraping)")
        print("2. ⚡ Pipeline Rápido (con imágenes existentes)")  
        print("3. 📋 Ver Descripción de Pasos")
        print("4. ❌ Salir")
        print()

def main():
    """Función principal"""
    executor = PipelineExecutor()
    
    # Argumentos de línea de comandos
    if len(sys.argv) > 1:
        if sys.argv[1] == "full":
            return executor.run_full_pipeline()
        elif sys.argv[1] == "quick":
            return executor.run_quick_pipeline()
    
    # Menú interactivo
    while True:
        executor.show_menu()
        
        try:
            choice = input("👉 Ingresa tu opción (1-4): ").strip()
            
            if choice == "1":
                print("\n🚀 Iniciando Pipeline Completo...")
                time.sleep(1)
                executor.run_full_pipeline()
                
            elif choice == "2":
                print("\n⚡ Iniciando Pipeline Rápido...")
                time.sleep(1)
                executor.run_quick_pipeline()
                
            elif choice == "3":
                print("\n📋 DESCRIPCIÓN DE PASOS DEL PIPELINE:")
                print("=" * 60)
                for num, step in executor.steps.items():
                    print(f"{num}. {step['name']}")
                    print(f"   📄 Script: {step['script']}")
                    print(f"   📝 {step['description']}")
                    print()
                
            elif choice == "4":
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción inválida. Selecciona 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Ejecución cancelada por el usuario")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        input("\n📱 Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
