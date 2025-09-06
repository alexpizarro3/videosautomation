import asyncio
import os
import subprocess
from datetime import datetime

def analyze_video_file(video_path):
    """Analizar archivo de video para detectar posibles problemas"""
    
    print(f"\n🔍 Analizando archivo: {video_path}")
    
    if not os.path.exists(video_path):
        print("❌ Archivo no existe")
        return False
    
    # Información básica del archivo
    file_size = os.path.getsize(video_path)
    file_size_mb = file_size / (1024 * 1024)
    print(f"📊 Tamaño: {file_size_mb:.2f} MB ({file_size} bytes)")
    
    # Verificar con ffprobe
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json', 
            '-show_format', '-show_streams', video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            
            print("✅ Archivo de video válido")
            
            # Información del formato
            format_info = data.get('format', {})
            print(f"📁 Formato: {format_info.get('format_name', 'Desconocido')}")
            print(f"⏱️ Duración: {float(format_info.get('duration', 0)):.2f} segundos")
            print(f"📏 Bitrate: {int(format_info.get('bit_rate', 0))} bps")
            
            # Información de streams
            streams = data.get('streams', [])
            for i, stream in enumerate(streams):
                stream_type = stream.get('codec_type', 'unknown')
                codec_name = stream.get('codec_name', 'unknown')
                
                if stream_type == 'video':
                    width = stream.get('width', 0)
                    height = stream.get('height', 0)
                    fps = stream.get('avg_frame_rate', '0/1')
                    if '/' in fps:
                        num, den = fps.split('/')
                        fps_val = float(num) / float(den) if float(den) != 0 else 0
                    else:
                        fps_val = float(fps)
                    
                    print(f"🎥 Video Stream {i}: {codec_name}, {width}x{height}, {fps_val:.2f} FPS")
                    
                    # Verificar si las dimensiones son problemáticas
                    if width == 0 or height == 0:
                        print("⚠️ Dimensiones de video inválidas")
                        return False
                    
                    aspect_ratio = width / height
                    print(f"📐 Aspect ratio: {aspect_ratio:.3f}")
                    
                    # TikTok prefiere 9:16 (0.5625)
                    if abs(aspect_ratio - 0.5625) > 0.1:
                        print(f"⚠️ Aspect ratio no óptimo para TikTok (ideal: 0.563)")
                    
                elif stream_type == 'audio':
                    sample_rate = stream.get('sample_rate', 0)
                    channels = stream.get('channels', 0)
                    print(f"🔊 Audio Stream {i}: {codec_name}, {sample_rate} Hz, {channels} canales")
            
            # Verificar metadatos
            metadata = format_info.get('tags', {})
            if metadata:
                print("🏷️ Metadatos encontrados:")
                for key, value in metadata.items():
                    print(f"   {key}: {value}")
                    
                # Buscar metadatos problemáticos
                problematic_tags = ['creation_time', 'encoder', 'major_brand', 'minor_version']
                for tag in problematic_tags:
                    if tag in metadata:
                        print(f"⚠️ Metadato potencialmente problemático: {tag} = {metadata[tag]}")
            
            return True
            
        else:
            print(f"❌ Error analizando con ffprobe: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando ffprobe: {e}")
        return False

def check_browser_compatibility():
    """Verificar compatibilidad del navegador"""
    
    print("\n🌐 Verificando compatibilidad del navegador...")
    
    # Crear un archivo HTML de prueba para cargar un video
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Video Upload</title>
    </head>
    <body>
        <h1>Test de carga de video</h1>
        <input type="file" id="videoInput" accept="video/*" />
        <video id="videoPreview" width="320" height="240" controls style="display:none;">
            Tu navegador no soporta el elemento video.
        </video>
        
        <script>
            document.getElementById('videoInput').addEventListener('change', function(e) {
                var file = e.target.files[0];
                if (file) {
                    console.log('Archivo seleccionado:', file.name, file.size, file.type);
                    
                    var video = document.getElementById('videoPreview');
                    var url = URL.createObjectURL(file);
                    video.src = url;
                    video.style.display = 'block';
                    
                    video.addEventListener('loadedmetadata', function() {
                        console.log('Metadatos cargados:', {
                            duration: video.duration,
                            width: video.videoWidth,
                            height: video.videoHeight
                        });
                    });
                    
                    video.addEventListener('error', function(err) {
                        console.error('Error cargando video:', err);
                    });
                }
            });
        </script>
    </body>
    </html>
    """
    
    with open("test_video_upload.html", "w", encoding="utf-8") as f:
        f.write(test_html)
    
    print("✅ Archivo de prueba creado: test_video_upload.html")
    print("💡 Abre este archivo en tu navegador y prueba cargar el video manualmente")

def suggest_solutions():
    """Sugerir posibles soluciones"""
    
    print("\n💡 Posibles soluciones a probar:")
    print("1. 🔄 Convertir el video a un formato más compatible:")
    print("   ffmpeg -i input.mp4 -c:v libx264 -c:a aac -preset fast -crf 23 output.mp4")
    
    print("\n2. 🗂️ Crear video con configuración específica para TikTok:")
    print("   ffmpeg -i input.mp4 -vf 'scale=720:1280' -c:v libx264 -c:a aac -b:v 2M -b:a 128k output.mp4")
    
    print("\n3. 🧹 Limpiar completamente metadatos:")
    print("   ffmpeg -i input.mp4 -map_metadata -1 -c copy output.mp4")
    
    print("\n4. 🔍 Verificar si TikTok tiene problemas temporales:")
    print("   - Probar en modo incógnito")
    print("   - Limpiar cache del navegador")
    print("   - Probar con otro navegador")
    
    print("\n5. 📱 Probar subir desde dispositivo móvil para comparar")

async def test_tiktok_upload_page():
    """Probar la página de upload de TikTok para detectar cambios"""
    
    from playwright.async_api import async_playwright
    import json
    
    print("\n🔍 Analizando página de upload de TikTok...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Cargar cookies si existen
        try:
            with open("config/upload_cookies_playwright.json", 'r') as f:
                cookies = json.load(f)
            
            for cookie in cookies:
                if 'sameSite' in cookie:
                    val = cookie['sameSite']
                    if val not in ["Strict", "Lax", "None"]:
                        cookie["sameSite"] = "None"
            
            await context.add_cookies(cookies)
        except:
            print("⚠️ No se pudieron cargar cookies")
        
        await page.goto("https://www.tiktok.com/upload")
        await page.wait_for_load_state('networkidle')
        
        # Analizar elementos en la página
        print("📋 Elementos de upload encontrados:")
        
        # Buscar inputs de archivo
        file_inputs = await page.query_selector_all('input[type="file"]')
        print(f"📁 Inputs de archivo encontrados: {len(file_inputs)}")
        
        for i, input_elem in enumerate(file_inputs):
            try:
                accept = await input_elem.get_attribute('accept')
                class_name = await input_elem.get_attribute('class')
                style = await input_elem.get_attribute('style')
                is_visible = await input_elem.is_visible()
                
                print(f"  Input #{i+1}:")
                print(f"    Accept: {accept}")
                print(f"    Class: {class_name}")
                print(f"    Style: {style}")
                print(f"    Visible: {is_visible}")
            except Exception as e:
                print(f"    Error analizando input #{i+1}: {e}")
        
        # Buscar dropzones
        dropzones = await page.query_selector_all('[data-e2e*="upload"], .upload-area, .drop-zone')
        print(f"📤 Dropzones encontradas: {len(dropzones)}")
        
        # Screenshot de la página
        await page.screenshot(path="tiktok_upload_page_analysis.png")
        print("📸 Screenshot guardado: tiktok_upload_page_analysis.png")
        
        await browser.close()

def main():
    print("🔧 Diagnóstico completo del problema de upload")
    print("=" * 50)
    
    # Analizar archivos de video
    video_files = [
        "data/videos/veo_video_20250901_190803.mp4",
        "data/videos/veo_video_20250901_190803_clean.mp4"
    ]
    
    for video_file in video_files:
        if os.path.exists(video_file):
            analyze_video_file(video_file)
    
    # Verificar herramientas
    print("\n🛠️ Verificando herramientas disponibles:")
    try:
        result = subprocess.run(['ffprobe', '-version'], capture_output=True)
        if result.returncode == 0:
            print("✅ FFprobe disponible")
        else:
            print("❌ FFprobe no disponible")
    except:
        print("❌ FFprobe no encontrado")
    
    # Crear archivo de prueba HTML
    check_browser_compatibility()
    
    # Sugerir soluciones
    suggest_solutions()
    
    # Probar página de TikTok
    print("\n🔍 ¿Quieres analizar la página de upload de TikTok? (y/n)")
    # response = input().lower()
    # if response == 'y':
    #     asyncio.run(test_tiktok_upload_page())

if __name__ == "__main__":
    main()
