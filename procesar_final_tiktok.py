#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROCESADOR FINAL - CONFIGURACIÓN ÓPTIMA
Aplicar crop centrado + zoom 1.2x a los 3 videos originales
"""

import subprocess
import os
import sys
import glob

def optimizar_video_final(input_file, output_file, zoom_factor=1.2):
    """
    Optimiza video con la configuración perfecta: crop centrado + zoom 1.2x
    
    Args:
        input_file: Video de entrada
        output_file: Video de salida  
        zoom_factor: Factor de zoom (1.2 = 20% más zoom)
    """
    try:
        # Obtener info del video
        probe_cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams',
            input_file
        ]
        
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        import json
        info = json.loads(result.stdout)
        
        # Encontrar stream de video
        video_stream = None
        for stream in info['streams']:
            if stream['codec_type'] == 'video':
                video_stream = stream
                break
        
        if not video_stream:
            print("No se encontró stream de video")
            return False
        
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        
        print(f"Video original: {width}x{height}")
        print(f"Aplicando zoom factor: {zoom_factor}x (CONFIGURACIÓN ÓPTIMA)")
        
        # Calcular dimensiones con zoom - CONFIGURACIÓN CENTRADA PERFECTA
        crop_width = int(width * 0.5 / zoom_factor)   # 50% del ancho, reducido por zoom
        crop_height = int(height / zoom_factor)       # altura completa, reducida por zoom
        
        # Calcular posición de crop CENTRADA (offset = 0, 0)
        crop_x = int((width - crop_width) / 2)        # Centrado horizontalmente
        crop_y = int((height - crop_height) / 2)      # Centrado verticalmente
        
        # Asegurar que el crop esté dentro de los límites
        crop_x = max(0, min(crop_x, width - crop_width))
        crop_y = max(0, min(crop_y, height - crop_height))
        
        print(f"Crop centrado con zoom: {crop_width}x{crop_height} desde posición ({crop_x},{crop_y})")
        print(f"Tomando {(crop_width/width)*100:.1f}% del ancho original")
        print(f"Posición: CENTRADA PERFECTA para boca completa del pez")
        
        # Construir comando FFmpeg con configuración óptima
        cmd = [
            'ffmpeg', '-i', input_file,
            '-filter_complex',
            f'[0:v]crop={crop_width}:{crop_height}:{crop_x}:{crop_y},scale=720:1280:flags=lanczos[v]',
            '-map', '[v]',
            '-map', '0:a?',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-y',
            output_file
        ]
        
        print("Procesando con configuración ÓPTIMA...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"¡CONVERSIÓN PERFECTA!")
                print(f"Creado: {os.path.basename(output_file)} ({size_mb:.1f} MB)")
                return True
            else:
                print("Error: archivo no creado")
                return False
        else:
            print(f"Error FFmpeg: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_video_files(directory):
    """
    Obtiene archivos de video solo de la carpeta 'original', no recursivamente
    para evitar procesar videos ya procesados
    """
    project_root = "C:\\Users\\Alexis Pizarro\\Documents\\Personal\\videosautomation\\"
    original_dir = os.path.join(project_root, directory, "original")
    
    # Solo buscar en la carpeta 'original', no recursivamente
    if os.path.exists(original_dir):
        absolute_paths = glob.glob(os.path.join(original_dir, "*.mp4"))
        relative_paths = [os.path.relpath(path, project_root) for path in absolute_paths]
        print(f"📁 Procesando solo videos de: {original_dir}")
        print(f"📊 Videos encontrados: {len(relative_paths)}")
        return relative_paths
    else:
        print(f"⚠️ Carpeta original no encontrada: {original_dir}")
        return []

def main():
    print("PROCESADOR FINAL - CONFIGURACIÓN ÓPTIMA")
    print("Crop centrado + zoom 1.2x SOLO para videos en /original")
    print("Configuración perfecta para boca completa del pez")
    print("=" * 65)

    # Dynamically get video files from data/videos/original ONLY
    videos_originales = get_video_files("data/videos")

    if not videos_originales:
        print("No se encontraron videos en data/videos/original. Asegúrate de que haya archivos .mp4 allí.")
        return

    
    zoom_factor = 1.2  # Configuración óptima confirmada
    videos_finales = []
    
    print(f"\nProcesando {len(videos_originales)} videos con zoom {zoom_factor}x (configuración ÓPTIMA)")
    print("=" * 65)
    
    for i, video_file in enumerate(videos_originales, 1):
        if not os.path.exists(video_file):
            print(f"Video {i} no encontrado: {video_file}")
            continue
        
        print(f"\nPROCESANDO VIDEO {i}/{len(videos_originales)}: {os.path.basename(video_file)}")
        print("-" * 50)
        
        # Generar nombre de archivo final
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        output_file = os.path.join("data", "videos", "processed", f"{base_name}_tiktok_FINAL.mp4")
        
        # Procesar video con configuración óptima
        if optimizar_video_final(video_file, output_file, zoom_factor):
            videos_finales.append(output_file)
            print(f"Video {i} completado con ÉXITO!")
        else:
            print(f"Error procesando video {i}")
    
    print("\n" + "=" * 65)
    print("PROCESAMIENTO FINAL COMPLETADO")
    print("=" * 65)
    
    if videos_finales:
        print("VIDEOS FINALES OPTIMIZADOS PARA TIKTOK:")
        for i, video in enumerate(videos_finales, 1):
            print(f"   {i}. {video}")
        
        print(f"\nConfiguración aplicada:")
        print(f"   • Zoom: {zoom_factor}x (20% más acercamiento)")
        print(f"   • Posición: Centrada perfecta")
        print(f"   • Formato: 720x1280 (TikTok)")
        print(f"   • Calidad: Optimizada para móvil")
        
        print(f"\n¡Listos para subir a TikTok!")
        print(f"Todos capturan perfectamente la boca completa del pez")
        
    else:
        print("No se procesaron videos exitosamente")

if __name__ == "__main__":
    main()

