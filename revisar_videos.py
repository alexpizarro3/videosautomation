import os
import subprocess
import json
from datetime import datetime

def crear_preview_video(video_path, output_path, timestamp=""):
    """Crear un preview del video optimizado"""
    try:
        # Crear thumbnail del primer frame
        thumbnail_path = output_path.replace('.mp4', f'_preview{timestamp}.jpg')
        
        cmd_thumb = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vf', 'scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280',
            '-vframes', '1',
            '-q:v', '2',
            thumbnail_path
        ]
        
        subprocess.run(cmd_thumb, capture_output=True, check=True)
        
        # Crear video corto de preview (primeros 3 segundos)
        preview_video_path = output_path.replace('.mp4', f'_preview{timestamp}.mp4')
        
        cmd_preview = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-t', '3',
            '-c', 'copy',
            preview_video_path
        ]
        
        subprocess.run(cmd_preview, capture_output=True, check=True)
        
        return thumbnail_path, preview_video_path
        
    except Exception as e:
        print(f"❌ Error creando preview: {e}")
        return None, None

def revisar_videos_optimizados():
    """Revisar y mostrar información de los videos optimizados"""
    
    videos_dir = "data/videos"
    timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
    
    print("🔍 REVISIÓN DE VIDEOS OPTIMIZADOS")
    print("="*50)
    
    # Buscar videos originales
    videos_originales = []
    for file in os.listdir(videos_dir):
        if file.startswith("veo_video_") and file.endswith(".mp4") and "optimized" not in file and "preview" not in file:
            videos_originales.append(file)
    
    videos_originales.sort()
    
    if not videos_originales:
        print("❌ No se encontraron videos originales")
        return
    
    # Procesar cada video para revisión
    for i, video_file in enumerate(videos_originales, 1):
        print(f"\n{'='*60}")
        print(f"🎬 REVISANDO VIDEO {i}: {video_file}")
        print(f"{'='*60}")
        
        input_path = os.path.join(videos_dir, video_file)
        
        # Analizar video original
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                '-show_format', '-show_streams', input_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            video_stream = None
            for stream in data['streams']:
                if stream['codec_type'] == 'video':
                    video_stream = stream
                    break
            
            if video_stream:
                width = int(video_stream['width'])
                height = int(video_stream['height'])
                aspect_ratio = width / height
                duration = float(video_stream.get('duration', 0))
                
                print(f"📊 ORIGINAL:")
                print(f"   📐 Dimensiones: {width}x{height}")
                print(f"   📏 Aspect ratio: {aspect_ratio:.3f}")
                print(f"   ⏱️ Duración: {duration:.1f}s")
                print(f"   💾 Tamaño: {os.path.getsize(input_path) / (1024*1024):.1f} MB")
                
                # Calcular zoom al 35%
                target_aspect = 720 / 1280  # 0.5625
                zoom_base = aspect_ratio / target_aspect
                zoom_actual = 1 + (zoom_base - 1) * 0.35
                
                print(f"\n🔍 ZOOM APLICADO:")
                print(f"   🎯 Factor máximo: {zoom_base:.2f}x")
                print(f"   🎯 Factor final (35%): {zoom_actual:.2f}x")
                
                # Crear preview temporal con el zoom actual
                temp_optimized = os.path.join(videos_dir, f"temp_optimized{timestamp}.mp4")
                
                print(f"\n⚙️ Generando preview optimizado...")
                
                # Comando FFmpeg con zoom actual
                cmd_opt = [
                    'ffmpeg', '-y',
                    '-i', input_path,
                    '-filter_complex', f'''
                    [0:v]scale={int(width*zoom_actual)}:{int(height*zoom_actual)},
                    crop=720:1280:(in_w-720)/2:(in_h-1280)/2,
                    format=yuv420p[v]
                    ''',
                    '-map', '[v]',
                    '-map', '0:a?',
                    '-c:v', 'libx264',
                    '-preset', 'fast',
                    '-crf', '23',
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-t', '3',  # Solo 3 segundos para preview
                    temp_optimized
                ]
                
                try:
                    subprocess.run(cmd_opt, capture_output=True, text=True, check=True)
                    
                    # Analizar resultado
                    cmd_check = [
                        'ffprobe', '-v', 'quiet', '-print_format', 'json',
                        '-show_format', '-show_streams', temp_optimized
                    ]
                    result_opt = subprocess.run(cmd_check, capture_output=True, text=True, check=True)
                    data_opt = json.loads(result_opt.stdout)
                    
                    video_stream_opt = None
                    for stream in data_opt['streams']:
                        if stream['codec_type'] == 'video':
                            video_stream_opt = stream
                            break
                    
                    if video_stream_opt:
                        width_opt = int(video_stream_opt['width'])
                        height_opt = int(video_stream_opt['height'])
                        aspect_opt = width_opt / height_opt
                        
                        print(f"📊 OPTIMIZADO:")
                        print(f"   📐 Dimensiones: {width_opt}x{height_opt}")
                        print(f"   📏 Aspect ratio: {aspect_opt:.3f}")
                        print(f"   💾 Tamaño preview: {os.path.getsize(temp_optimized) / (1024*1024):.1f} MB")
                        
                        # Crear thumbnail
                        thumbnail_path = temp_optimized.replace('.mp4', '_thumb.jpg')
                        cmd_thumb = [
                            'ffmpeg', '-y',
                            '-i', temp_optimized,
                            '-vframes', '1',
                            '-q:v', '2',
                            thumbnail_path
                        ]
                        subprocess.run(cmd_thumb, capture_output=True)
                        
                        if os.path.exists(thumbnail_path):
                            print(f"   🖼️ Thumbnail: {thumbnail_path}")
                        
                        print(f"   🎬 Preview: {temp_optimized}")
                        
                        if width_opt == 720 and height_opt == 1280:
                            print("   ✅ Formato TikTok PERFECTO")
                        else:
                            print("   ⚠️ Formato no coincide con TikTok")
                    
                except subprocess.CalledProcessError as e:
                    print(f"   ❌ Error generando preview: {e}")
                
        except Exception as e:
            print(f"❌ Error analizando {video_file}: {e}")
    
    print(f"\n{'='*60}")
    print("🎯 REVISIÓN COMPLETADA")
    print(f"{'='*60}")
    print("📁 Archivos temporales generados para revisión:")
    
    # Listar archivos temporales
    for file in os.listdir(videos_dir):
        if f"temp_optimized{timestamp}" in file:
            file_path = os.path.join(videos_dir, file)
            size_mb = os.path.getsize(file_path) / (1024*1024)
            print(f"   📄 {file} ({size_mb:.1f} MB)")
    
    print(f"\n💡 Revisa los archivos preview para verificar el zoom")
    print(f"🗑️ Los archivos temporales se pueden eliminar después de revisar")

if __name__ == "__main__":
    revisar_videos_optimizados()
