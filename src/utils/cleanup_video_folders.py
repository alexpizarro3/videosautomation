#!/usr/bin/env python3
"""
Utilidad para limpiar carpetas de videos procesados y originales.
"""
import os
from pathlib import Path

def clean_video_folders():
    """Elimina todos los archivos de video de las carpetas 'processed' y 'original'."""
    print("🧹 Iniciando limpieza de carpetas de videos...")
    
    # Obtener el path del directorio raíz del proyecto
    project_root = Path(__file__).parent.parent.parent
    
    video_folders = [
        project_root / "data" / "videos" / "processed",
        project_root / "data" / "videos" / "original"
    ]
    
    total_deleted = 0
    for folder in video_folders:
        if not folder.exists() or not folder.is_dir():
            print(f"⚠️  La carpeta no existe, saltando: {folder}")
            continue

        files_to_delete = list(folder.glob("*.mp4"))
        
        if not files_to_delete:
            print(f"✅ Carpeta ya está limpia: {folder.name}")
            continue
            
        print(f"🗑️  Eliminando {len(files_to_delete)} videos de la carpeta: {folder.name}")
        
        for f in files_to_delete:
            try:
                f.unlink() # Elimina el archivo
                total_deleted += 1
            except OSError as e:
                print(f"❌ Error eliminando el archivo {f}: {e}")

    if total_deleted > 0:
        print(f"🧼 Limpieza completada. Se eliminaron {total_deleted} archivos de video.")
    else:
        print("✨ No se encontraron archivos de video para eliminar.")

if __name__ == "__main__":
    # Permite ejecutar este script de forma independiente para pruebas
    clean_video_folders()
