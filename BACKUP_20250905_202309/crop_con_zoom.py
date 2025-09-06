#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 GENERADOR DE VERSIONES CON CROP + ZOOM
📱 Optimización avanzada para TikTok con zoom ligero
"""

import subprocess
import os
import sys

def optimizar_video_crop_zoom(input_file, output_file, offset_x=0, offset_y=0, zoom_factor=1.2):
    """
    Optimiza video con crop personalizado + zoom ligero
    
    Args:
        input_file: Video de entrada
        output_file: Video de salida
        offset_x: Desplazamiento horizontal del crop (-/+)
        offset_y: Desplazamiento vertical del crop (-/+)
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
            print("❌ No se encontró stream de video")
            return False
        
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        
        print(f"📐 Video original: {width}x{height}")
        print(f"🔍 Aplicando zoom factor: {zoom_factor}x")
        print(f"📍 Offset: ({offset_x}, {offset_y})")
        
        # Calcular dimensiones con zoom
        # Zoom se aplica reduciendo el área de captura
        crop_width = int(width * 0.6 / zoom_factor)  # 60% del ancho, reducido por zoom
        crop_height = int(height / zoom_factor)      # altura completa, reducida por zoom
        
        # Calcular posición de crop centrada + offset
        crop_x = int((width - crop_width) / 2) + offset_x
        crop_y = int((height - crop_height) / 2) + offset_y
        
        # Asegurar que el crop esté dentro de los límites
        crop_x = max(0, min(crop_x, width - crop_width))
        crop_y = max(0, min(crop_y, height - crop_height))
        
        print(f"📐 Crop con zoom: {crop_width}x{crop_height} desde posición ({crop_x},{crop_y})")
        print(f"📊 Tomando {(crop_width/width)*100:.1f}% del ancho original")
        
        # Construir comando FFmpeg
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
        
        print("🚀 Procesando con crop + zoom...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ Conversión exitosa con crop + zoom!")
                print(f"✅ Creado: {os.path.basename(output_file)} ({size_mb:.1f} MB)")
                return True
            else:
                print("❌ Error: archivo no creado")
                return False
        else:
            print(f"❌ Error FFmpeg: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎬 GENERADOR DE MÚLTIPLES VERSIONES CROP + ZOOM")
    print("📱 Creando diferentes versiones con zoom ligero")
    print("=" * 60)
    
    # Buscar video con 190857 en el nombre o usar el disponible
    video_patterns = [
        "data/videos/veo_video_20250901_190857.mp4",
        "veo_video_20250901_190857.mp4",
        "data/videos/*190857*.mp4",
        "*190857*.mp4",
        "*19087*.mp4",
        "Fruta.mp4"  # Video de prueba disponible
    ]
    
    video_file = None
    for pattern in video_patterns:
        if "*" in pattern:
            import glob
            matches = glob.glob(pattern)
            if matches:
                video_file = matches[0]
                break
        else:
            if os.path.exists(pattern):
                video_file = pattern
                break
    
    if not video_file:
        print(f"❌ No se encontró ningún video. Patrones buscados: {video_patterns}")
        return
    
    print(f"📹 Usando video: {video_file}")
    
    print(f"\n🎬 CREANDO VERSIONES DE: {video_file}")
    print("=" * 60)
    
    # Configuraciones con zoom ligero (1.2x = 20% más zoom)
    configuraciones = [
        ("centrado", 0, 0),
        ("izquierda", -80, 0),      # Menos desplazamiento debido al zoom
        ("derecha", 80, 0),
        ("mas_izquierda", -120, 0),
        ("mas_derecha", 120, 0),
    ]
    
    zoom_factor = 1.2  # 20% más zoom
    
    videos_creados = []
    
    for nombre, offset_x, offset_y in configuraciones:
        print(f"\n📍 Creando versión: {nombre} (offset_x: {offset_x})")
        print(f"🎯 Usando crop + zoom {zoom_factor}x con offset ({offset_x}, {offset_y})")
        
        # Generar nombre de archivo
        base_name = os.path.splitext(video_file)[0]
        output_file = f"{base_name}_cropzoom_{nombre}.mp4"
        
        # Procesar video
        if optimizar_video_crop_zoom(video_file, output_file, offset_x, offset_y, zoom_factor):
            videos_creados.append(output_file)
        else:
            print(f"❌ Error creando versión: {nombre}")
    
    print("\n" + "=" * 60)
    print("🎉 VERSIONES CREADAS CON CROP + ZOOM")
    print("=" * 60)
    
    if videos_creados:
        print("📱 Revisa las diferentes versiones y dime cuál captura mejor la boca del pez:")
        for video in videos_creados:
            print(f"   • {video}")
        
        print(f"\n💡 Todas con zoom {zoom_factor}x para mejor captura de detalles")
        print("💡 Una vez que elijas la mejor, procesaremos los 3 videos con esa configuración")
    else:
        print("❌ No se crearon videos")

if __name__ == "__main__":
    main()
