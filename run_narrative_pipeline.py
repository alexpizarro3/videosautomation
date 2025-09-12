#!/usr/bin/env python3
"""
Orquestador del PIPELINE NARRATIVO ASMR
========================================

Este script ejecuta de forma secuencial todos los pasos necesarios para el pipeline
narrativo, desde el análisis de tendencias hasta la subida final del contenido.

Permite dos modos de ejecución:
1.  **Automático**: Ejecuta todos los pasos en orden, ideal para producción.
2.  **Manual**: Permite seleccionar y ejecutar pasos individuales, útil para depuración
    o ejecuciones parciales.

El script también incluye una limpieza inicial de las carpetas de video para
asegurar que cada ejecución comience desde un estado limpio.
"""
import os
import subprocess
import sys
import glob
from src.utils.cleanup_video_folders import clean_video_folders

# Definición de los pasos del pipeline según PIPELINE_NARRATIVO_EXECUTION_ORDER.md
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

def clean_image_folder(image_dir: str = "data/images"):
    """Elimina todas las imágenes (.png, .jpg, .jpeg) de la carpeta de imágenes."""
    if not os.path.exists(image_dir):
        print(f"   -> La carpeta '{image_dir}' no existe, no se necesita limpieza.")
        return

    files_to_delete = glob.glob(os.path.join(image_dir, "*.png")) + \
                      glob.glob(os.path.join(image_dir, "*.jpg")) + \
                      glob.glob(os.path.join(image_dir, "*.jpeg"))
    
    if not files_to_delete:
        return

    deleted_count = 0
    for f in files_to_delete:
        try:
            os.remove(f)
            deleted_count += 1
        except Exception as e:
            print(f"   -> Error al eliminar {f}: {e}")

def run_step(script_name: str) -> bool:
    """Ejecuta un script de Python y maneja los errores."""
    print(f"\n>> Ejecutando: {script_name}")
    try:
        # Usamos subprocess.run para un mejor control y captura de errores
        result = subprocess.run([sys.executable, script_name], check=True, text=True, capture_output=True)
        print(f"[+] Completado: {script_name}")
        return True
    except FileNotFoundError:
        print(f"[!] Error: El script '{script_name}' no fue encontrado.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[!] Error ejecutando {script_name} (código de salida: {e.returncode})")
        print("   --- Salida de error ---")
        print(e.stderr)
        print("   -----------------------")
        return False
    except Exception as e:
        print(f"[!] Ocurrió un error inesperado ejecutando {script_name}: {e}")
        return False

def run_pipeline(auto: bool = True):
    """Ejecuta el pipeline en modo automático o manual."""
    print("\n=== INICIO DEL PIPELINE NARRATIVO ASMR ===")
    if auto:
        print(">> Modo automático: ejecutando todos los pasos...")
        for i, (name, script) in enumerate(PIPELINE_STEPS, 1):
            print(f"\n-> Paso {i}/{len(PIPELINE_STEPS)}: {name}")
            if not run_step(script):
                print(f"\n[!] El pipeline se detuvo debido a un error en el paso '{name}'.")
                return
        print("\n[+] ¡Pipeline narrativo completado exitosamente!")
    else:
        print(">> Modo manual: selecciona los pasos a ejecutar.")
        while True:
            print("\n--- Pasos Disponibles ---")
            for idx, (name, script) in enumerate(PIPELINE_STEPS, 1):
                print(f"{idx}. {name} ({script})")
            print("0. Salir del modo manual")
            try:
                choice = int(input("\nSelecciona el número del paso a ejecutar: "))
                if choice == 0:
                    break
                if 1 <= choice <= len(PIPELINE_STEPS):
                    name, script = PIPELINE_STEPS[choice - 1]
                    run_step(script)
                else:
                    print("Opción inválida. Por favor, elige un número de la lista.")
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número.")
            except KeyboardInterrupt:
                break
    print("\n[+] Orquestador narrativo finalizado.")

def main():
    """Función principal para seleccionar el modo de ejecución del orquestador."""
    # Limpiar carpetas de videos antes de iniciar para evitar conflictos
    print(">> Limpiando carpetas de videos de ejecuciones anteriores...")
    clean_video_folders()
    print("[+] Carpetas de video limpias.")

    print(">> Limpiando carpeta de imágenes...")
    clean_image_folder()
    print("[+] Carpeta de imágenes limpia.")

    print("\n=== ORQUESTADOR DEL PIPELINE NARRATIVO ASMR ===")
    print("1. Ejecutar pipeline completo (Automático)")
    print("2. Ejecutar pasos individuales (Manual)")
    print("0. Salir")

    try:
        mode = input("\nSelecciona un modo de ejecución (1, 2, o 0): ")
        if mode == '1':
            run_pipeline(auto=True)
        elif mode == '2':
            run_pipeline(auto=False)
        elif mode == '0':
            pass
        else:
            print("Opción inválida.")
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

    print("\n>> Orquestador narrativo cerrado.")

if __name__ == "__main__":
    main()
