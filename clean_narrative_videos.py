"""
Script para regenerar pipeline narrativo con consistencia en español
"""
import os
import shutil

def clean_and_regenerate():
    """
    Limpia archivos inconsistentes y prepara regeneración en español
    """
    print("🧹 Limpiando archivos inconsistentes...")
    
    # Limpiar videos narrativos existentes
    narrative_videos = [
        'data/videos/original/narrative_video_1.mp4',
        'data/videos/original/narrative_video_2.mp4', 
        'data/videos/original/narrative_video_3.mp4'
    ]
    
    for video in narrative_videos:
        if os.path.exists(video):
            print(f"🗑️ Eliminando: {video}")
            os.remove(video)
    
    # Limpiar archivos de información inconsistentes
    info_files = [
        'data/videos/narrative_video_1_info.json',
        'data/videos/narrative_video_2_info.json',
        'data/videos/narrative_video_3_info.json'
    ]
    
    for info_file in info_files:
        if os.path.exists(info_file):
            print(f"🗑️ Eliminando: {info_file}")
            os.remove(info_file)
    
    print("✅ Limpieza completada")
    print("📋 Listo para regenerar con consistencia en español")
    print("🎬 Ejecuta: python generate_narrative_videos_veo3.py")

if __name__ == "__main__":
    clean_and_regenerate()
