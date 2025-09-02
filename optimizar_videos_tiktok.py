import os
import subprocess
import json

def analizar_video(video_path):
    """Analizar las propiedades del video para determinar el mejor zoom"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # Encontrar el stream de video
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
        
        print(f"📐 Dimensiones: {width}x{height}")
        print(f"📏 Aspect ratio: {aspect_ratio:.3f}")
        print(f"⏱️ Duración: {duration:.1f}s")
        
        return {
            'width': width,
            'height': height,
            'aspect_ratio': aspect_ratio,
            'duration': duration
        }
    except Exception as e:
        print(f"❌ Error analizando video: {e}")
        return None

def optimizar_para_tiktok(input_path, output_path, video_info):
    """Optimizar video para TikTok con zoom inteligente"""
    
    # TikTok target: 720x1280 (9:16)
    target_width = 720
    target_height = 1280
    target_aspect = target_width / target_height  # 0.5625
    
    source_aspect = video_info['aspect_ratio']
    
    print(f"🎯 Aspecto origen: {source_aspect:.3f}")
    print(f"🎯 Aspecto TikTok: {target_aspect:.3f}")
    
    # Determinar estrategia de zoom
    if source_aspect > target_aspect:
        # Video es más ancho que TikTok - necesita crop horizontal y zoom
        print("📱 Video horizontal -> Aplicando zoom y crop inteligente")
        
        # Calcular zoom específico para 0.65x (para capturar boca completa del pez)
        zoom_base = source_aspect / target_aspect
        target_zoom = 0.65
        if zoom_base > 1:
            # Para mostrar la boca completa del pez
            zoom_factor = target_zoom
        else:
            zoom_factor = target_zoom
        print(f"🔍 Factor de zoom máximo: {zoom_base:.2f}x")
        print(f"🔍 Factor de zoom objetivo (0.65x - boca completa): {zoom_factor:.2f}x")
        
        # Filtro corregido para zoom y crop apropiado
        video_filter = f"[0:v]scale={int(video_info['width']*zoom_factor)}:{int(video_info['height']*zoom_factor)},scale={target_width}:{target_height}:force_original_aspect_ratio=increase,crop={target_width}:{target_height}:(in_w-{target_width})/2:(in_h-{target_height})/2,format=yuv420p[v]"
    else:
        # Video ya es vertical - solo ajustar tamaño
        print("📱 Video vertical -> Ajustando escala")
        video_filter = f"[0:v]scale={target_width}:{target_height}:force_original_aspect_ratio=increase,crop={target_width}:{target_height}:(in_w-{target_width})/2:(in_h-{target_height})/2,format=yuv420p[v]"
    
    # Comando FFmpeg optimizado para TikTok
    cmd = [
        'ffmpeg', '-y',
        '-i', input_path,
        '-filter_complex', video_filter,
        '-map', '[v]',
        '-map', '0:a?',  # Audio opcional
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
        '-r', '30',  # 30 FPS para TikTok
        output_path
    ]
    
    print(f"🚀 Iniciando conversión...")
    print(f"📁 Input: {input_path}")
    print(f"📁 Output: {output_path}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Conversión exitosa!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en conversión: {e}")
        print(f"❌ stderr: {e.stderr}")
        return False

def procesar_todos_los_videos():
    """Procesar los 3 videos originales para TikTok"""
    
    videos_dir = "data/videos"
    
    # Buscar videos originales
    videos_originales = []
    for file in os.listdir(videos_dir):
        if file.startswith("veo_video_") and file.endswith(".mp4") and "optimized" not in file:
            videos_originales.append(file)
    
    videos_originales.sort()  # Ordenar por nombre
    
    print(f"🎬 Encontrados {len(videos_originales)} videos originales:")
    for i, video in enumerate(videos_originales, 1):
        print(f"   {i}. {video}")
    
    videos_procesados = []
    
    for i, video_file in enumerate(videos_originales, 1):
        print(f"\n{'='*50}")
        print(f"🎬 PROCESANDO VIDEO {i}/{len(videos_originales)}: {video_file}")
        print(f"{'='*50}")
        
        input_path = os.path.join(videos_dir, video_file)
        
        # Generar nombre de salida
        base_name = video_file.replace(".mp4", "")
        output_name = f"{base_name}_tiktok_optimized.mp4"
        output_path = os.path.join(videos_dir, output_name)
        
        # Analizar video
        print("🔍 Analizando video...")
        video_info = analizar_video(input_path)
        if not video_info:
            print(f"❌ No se pudo analizar {video_file}")
            continue
        
        # Optimizar para TikTok
        print("🎯 Optimizando para TikTok...")
        if optimizar_para_tiktok(input_path, output_path, video_info):
            # Verificar resultado
            print("✅ Verificando resultado...")
            resultado_info = analizar_video(output_path)
            if resultado_info:
                print(f"📱 Video optimizado: {resultado_info['width']}x{resultado_info['height']}")
                print(f"📏 Aspect ratio final: {resultado_info['aspect_ratio']:.3f}")
                videos_procesados.append(output_name)
            else:
                print(f"❌ Error verificando {output_name}")
        else:
            print(f"❌ Error procesando {video_file}")
    
    print(f"\n{'='*50}")
    print(f"🎉 PROCESAMIENTO COMPLETADO")
    print(f"{'='*50}")
    print(f"✅ Videos procesados exitosamente: {len(videos_procesados)}")
    
    for i, video in enumerate(videos_procesados, 1):
        video_path = os.path.join(videos_dir, video)
        file_size = os.path.getsize(video_path) / (1024*1024)  # MB
        print(f"   {i}. {video} ({file_size:.1f} MB)")
    
    if videos_procesados:
        print(f"\n🎬 Videos listos para subir a TikTok en formato perfecto 720x1280!")
        print(f"📱 Optimizados con zoom inteligente para pantalla completa")
    
    return videos_procesados

if __name__ == "__main__":
    print("🎬 OPTIMIZADOR DE VIDEOS PARA TIKTOK")
    print("📱 Conversión a 720x1280 con zoom inteligente")
    print("="*50)
    
    videos_listos = procesar_todos_los_videos()
    
    if videos_listos:
        print(f"\n🚀 ¡Listo! {len(videos_listos)} videos optimizados para TikTok")
    else:
        print("\n❌ No se procesaron videos exitosamente")
