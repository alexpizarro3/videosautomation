import os
import subprocess
import json

def optimizar_con_crop_personalizado(input_path, output_path, video_info, crop_offset_x=0, crop_offset_y=0):
    """Optimizar video con crop personalizado para posicionar mejor el contenido"""
    
    target_width = 720
    target_height = 1280
    
    width = video_info['width']  # 1280
    height = video_info['height']  # 720
    
    print(f"🎯 Usando crop personalizado con offset ({crop_offset_x}, {crop_offset_y})")
    
    # Para capturar mejor la boca del pez, vamos a hacer un crop más amplio
    # En lugar de 405x720, usaremos un crop más ancho para incluir más contenido
    
    # Calculamos un crop que mantenga más proporción horizontal
    target_aspect = target_width / target_height  # 0.5625
    
    # Usar un crop más generoso - tomar 60% del ancho original centrado
    crop_width = int(width * 0.60)  # 768 pixels en lugar de 405
    crop_height = height  # 720 (toda la altura)
    
    # Posición del crop (centrado + offset personalizable)
    base_crop_x = (width - crop_width) // 2  # Centrado
    crop_x = max(0, min(width - crop_width, base_crop_x + crop_offset_x))
    crop_y = crop_offset_y
    
    print(f"📐 Crop personalizado: {crop_width}x{crop_height} desde posición ({crop_x},{crop_y})")
    print(f"📊 Tomando {(crop_width/width)*100:.1f}% del ancho original")
    
    # Filtro que recorta con posición personalizada y luego escala
    video_filter = f"[0:v]crop={crop_width}:{crop_height}:{crop_x}:{crop_y},scale={target_width}:{target_height},format=yuv420p[v]"
    
    # Comando FFmpeg optimizado
    cmd = [
        'ffmpeg', '-y',
        '-i', input_path,
        '-filter_complex', video_filter,
        '-map', '[v]',
        '-map', '0:a?',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-maxrate', '3M',
        '-bufsize', '6M',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',
        '-ac', '2',
        '-movflags', '+faststart',
        '-avoid_negative_ts', 'make_zero',
        '-fflags', '+genpts',
        '-r', '30',
        output_path
    ]
    
    print(f"🚀 Procesando con crop personalizado...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Conversión exitosa con crop personalizado!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en conversión: {e}")
        print(f"❌ stderr: {e.stderr}")
        return False

def analizar_video(video_path):
    """Analizar propiedades del video"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        video_stream = None
        for stream in data['streams']:
            if stream['codec_type'] == 'video':
                video_stream = stream
                break
        
        if not video_stream:
            return None
        
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        aspect_ratio = width / height
        duration = float(video_stream.get('duration', 0))
        
        return {
            'width': width,
            'height': height,
            'aspect_ratio': aspect_ratio,
            'duration': duration
        }
    except Exception as e:
        print(f"❌ Error analizando video: {e}")
        return None

def crear_multiples_versiones():
    """Crear múltiples versiones con diferentes posiciones de crop"""
    
    videos_dir = "data/videos"
    
    # Buscar videos originales
    videos_originales = []
    for file in os.listdir(videos_dir):
        if file.startswith("veo_video_") and file.endswith(".mp4") and "optimized" not in file and "crop" not in file:
            videos_originales.append(file)
    
    videos_originales.sort()
    
    print(f"🎬 GENERADOR DE MÚLTIPLES VERSIONES CROP")
    print(f"📱 Creando diferentes versiones para encontrar la mejor")
    print(f"{'='*60}")
    
    # Diferentes configuraciones de crop para probar
    configuraciones = [
        {"offset_x": 0, "nombre": "centrado"},
        {"offset_x": -100, "nombre": "izquierda"},  # Mover crop hacia la izquierda
        {"offset_x": 100, "nombre": "derecha"},    # Mover crop hacia la derecha
        {"offset_x": -150, "nombre": "mas_izquierda"},  # Aún más a la izquierda
        {"offset_x": 150, "nombre": "mas_derecha"},     # Aún más a la derecha
    ]
    
    for video_file in videos_originales[:1]:  # Solo procesar el primer video para prueba
        input_path = os.path.join(videos_dir, video_file)
        
        print(f"\n{'='*60}")
        print(f"🎬 CREANDO VERSIONES DE: {video_file}")
        print(f"{'='*60}")
        
        # Analizar video
        video_info = analizar_video(input_path)
        if not video_info:
            continue
        
        print(f"📐 Video original: {video_info['width']}x{video_info['height']}")
        
        for config in configuraciones:
            base_name = video_file.replace(".mp4", "")
            output_name = f"{base_name}_crop_{config['nombre']}.mp4"
            output_path = os.path.join(videos_dir, output_name)
            
            print(f"\n📍 Creando versión: {config['nombre']} (offset_x: {config['offset_x']})")
            
            if optimizar_con_crop_personalizado(input_path, output_path, video_info, 
                                               crop_offset_x=config['offset_x']):
                file_size = os.path.getsize(output_path) / (1024*1024)
                print(f"✅ Creado: {output_name} ({file_size:.1f} MB)")
            else:
                print(f"❌ Error creando: {output_name}")
    
    print(f"\n{'='*60}")
    print(f"🎉 VERSIONES CREADAS")
    print(f"{'='*60}")
    print(f"📱 Revisa las diferentes versiones y dime cuál captura mejor la boca del pez:")
    
    for config in configuraciones:
        print(f"   • {video_file.replace('.mp4', '')}_crop_{config['nombre']}.mp4")
    
    print(f"\n💡 Una vez que elijas la mejor, procesaremos los 3 videos con esa configuración")

if __name__ == "__main__":
    crear_multiples_versiones()
