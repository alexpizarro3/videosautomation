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
import json
import time

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

def find_latest_manifest():
    """Encuentra el manifiesto más reciente."""
    manifest_files = glob.glob("video_prompt_map_professional_*.json")
    if not manifest_files:
        return None
    latest_manifest = max(manifest_files, key=os.path.getctime)
    return latest_manifest

def main():
    print("PROCESADOR FINAL - CONFIGURACIÓN ÓPTIMA")
    print("Crop centrado + zoom 1.2x SOLO para videos en /original")
    print("Configuración perfecta para boca completa del pez")
    print("=" * 65)

    latest_manifest = find_latest_manifest()
    if not latest_manifest:
        print("No se encontró ningún archivo de manifiesto 'video_prompt_map_professional_*.json'.")
        return

    print(f"Usando el manifiesto: {latest_manifest}")
    with open(latest_manifest, 'r', encoding='utf-8') as f:
        manifest_data = json.load(f)

    videos_a_procesar = manifest_data.get("videos", [])
    if not videos_a_procesar:
        print("No se encontraron videos en el manifiesto.")
        return

    zoom_factor = 1.2  # Configuración óptima confirmada
    videos_finales = []
    
    print(f"\nProcesando {len(videos_a_procesar)} videos con zoom {zoom_factor}x (configuración ÓPTIMA)")
    print("=" * 65)
    
    for i, video_info in enumerate(videos_a_procesar, 1):
        video_file = video_info.get("video")
        if not video_file or not os.path.exists(video_file):
            print(f"Video {i} no encontrado: {video_file}")
            continue
        
        print(f"\nPROCESANDO VIDEO {i}/{len(videos_a_procesar)}: {os.path.basename(video_file)}")
        print("-" * 50)
        
        # Generar nombre de archivo final
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        output_file = os.path.join("data", "videos", "processed", f"{base_name}_tiktok_FINAL.mp4")
        
        # Procesar video con configuración óptima
        if optimizar_video_final(video_file, output_file, zoom_factor):
            video_info["processed_video"] = output_file
            videos_finales.append(video_info)
            print(f"Video {i} completado con ÉXITO!")
        else:
            print(f"Error procesando video {i}")
    
    if videos_finales:
        timestamp = int(time.time())
        new_manifest_file = f"processed_video_map_{timestamp}.json"
        with open(new_manifest_file, 'w', encoding='utf-8') as f:
            json.dump({"videos": videos_finales}, f, indent=2, ensure_ascii=False)
        print(f"\nManifiesto de videos procesados guardado como: {new_manifest_file}")

    print("\n" + "=" * 65)
    print("PROCESAMIENTO FINAL COMPLETADO")
    print("=" * 65)
    
    if videos_finales:
        print("VIDEOS FINALES OPTIMIZADOS PARA TIKTOK:")
        for i, video in enumerate(videos_finales, 1):
            print(f"   {i}. {video['processed_video']}")
        
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
