import os
import subprocess
import json

def optimizar_con_crop_inteligente(input_path, output_path, video_info):
    """Optimizar video usando crop inteligente centrado en el contenido principal"""
    
    target_width = 720
    target_height = 1280
    
    width = video_info['width']
    height = video_info['height']
    
    print(f"🎯 Usando crop inteligente centrado en contenido principal")
    
    # Método 1: Crop inteligente que mantiene proporción y centra contenido
    # Calculamos el área óptima para capturar el pez completo
    
    # Para un video 1280x720, queremos tomar una sección central que capture todo el pez
    # Usaremos una ventana cuadrada centrada y luego la escalamos a formato TikTok
    
    source_aspect = width / height  # 1.778
    target_aspect = target_width / target_height  # 0.5625
    
    if source_aspect > target_aspect:
        # Video horizontal - necesitamos recortar horizontalmente
        # Calculamos el ancho que necesitamos para mantener el aspect ratio de TikTok
        new_width = int(height * target_aspect)
        crop_x = (width - new_width) // 2  # Centrar horizontalmente
        crop_y = 0
        crop_w = new_width
        crop_h = height
        
        print(f"📐 Crop horizontal: {crop_w}x{crop_h} desde posición ({crop_x},{crop_y})")
        
        # Filtro que recorta y luego escala
        video_filter = f"[0:v]crop={crop_w}:{crop_h}:{crop_x}:{crop_y},scale={target_width}:{target_height},format=yuv420p[v]"
        
    else:
        # Video vertical - necesitamos recortar verticalmente o añadir padding
        new_height = int(width / target_aspect)
        if new_height <= height:
            # Recortar verticalmente
            crop_x = 0
            crop_y = (height - new_height) // 2
            crop_w = width
            crop_h = new_height
            
            video_filter = f"[0:v]crop={crop_w}:{crop_h}:{crop_x}:{crop_y},scale={target_width}:{target_height},format=yuv420p[v]"
        else:
            # Añadir padding
            video_filter = f"[0:v]scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:black,format=yuv420p[v]"
    
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
    
    print(f"🚀 Procesando con crop inteligente...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Conversión exitosa con crop inteligente!")
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

def procesar_con_crop_inteligente():
    """Procesar videos con crop inteligente"""
    
    videos_dir = "data/videos"
    
    # Buscar videos originales
    videos_originales = []
    for file in os.listdir(videos_dir):
        if file.startswith("veo_video_") and file.endswith(".mp4") and "optimized" not in file:
            videos_originales.append(file)
    
    videos_originales.sort()
    
    print(f"🎬 OPTIMIZADOR CON CROP INTELIGENTE")
    print(f"📱 Procesando {len(videos_originales)} videos")
    print(f"{'='*60}")
    
    videos_procesados = []
    
    for i, video_file in enumerate(videos_originales, 1):
        print(f"\n{'='*60}")
        print(f"🎬 PROCESANDO VIDEO {i}/{len(videos_originales)}: {video_file}")
        print(f"{'='*60}")
        
        input_path = os.path.join(videos_dir, video_file)
        
        # Generar nombre de salida
        base_name = video_file.replace(".mp4", "")
        output_name = f"{base_name}_tiktok_crop_inteligente.mp4"
        output_path = os.path.join(videos_dir, output_name)
        
        # Analizar video
        print("🔍 Analizando video...")
        video_info = analizar_video(input_path)
        if not video_info:
            print(f"❌ No se pudo analizar {video_file}")
            continue
        
        print(f"📐 Dimensiones originales: {video_info['width']}x{video_info['height']}")
        print(f"📏 Aspect ratio: {video_info['aspect_ratio']:.3f}")
        
        # Optimizar con crop inteligente
        if optimizar_con_crop_inteligente(input_path, output_path, video_info):
            # Verificar resultado
            resultado_info = analizar_video(output_path)
            if resultado_info:
                print(f"📱 Video optimizado: {resultado_info['width']}x{resultado_info['height']}")
                print(f"📏 Aspect ratio final: {resultado_info['aspect_ratio']:.3f}")
                print(f"💾 Tamaño: {os.path.getsize(output_path) / (1024*1024):.1f} MB")
                videos_procesados.append(output_name)
            else:
                print(f"❌ Error verificando {output_name}")
        else:
            print(f"❌ Error procesando {video_file}")
    
    print(f"\n{'='*60}")
    print(f"🎉 PROCESAMIENTO COMPLETADO")
    print(f"{'='*60}")
    print(f"✅ Videos procesados exitosamente: {len(videos_procesados)}")
    
    for i, video in enumerate(videos_procesados, 1):
        video_path = os.path.join(videos_dir, video)
        file_size = os.path.getsize(video_path) / (1024*1024)
        print(f"   {i}. {video} ({file_size:.1f} MB)")
    
    if videos_procesados:
        print(f"\n🎬 Videos con crop inteligente listos para TikTok!")
        print(f"📱 Optimizados para mostrar el contenido principal completo")
    
    return videos_procesados

if __name__ == "__main__":
    procesar_con_crop_inteligente()
