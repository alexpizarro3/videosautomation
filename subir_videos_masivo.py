import asyncio
import os
from playwright.async_api import async_playwright
import json
import base64
import time

async def subir_video_individual(browser, video_path, video_numero, total_videos):
    """Subir un video individual a TikTok"""
    
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    
    page = await context.new_page()
    
    # Anti-detección
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
    """)
    
    try:
        # Cargar cookies
        with open("config/upload_cookies_playwright.json", 'r') as f:
            cookies = json.load(f)
        
        for cookie in cookies:
            if 'sameSite' in cookie:
                val = cookie['sameSite']
                if val not in ["Strict", "Lax", "None"]:
                    cookie["sameSite"] = "None"
        
        await context.add_cookies(cookies)
        
        print(f"\n{'='*60}")
        print(f"🎬 SUBIENDO VIDEO {video_numero}/{total_videos}")
        print(f"📁 {os.path.basename(video_path)}")
        print(f"{'='*60}")
        
        # Ir a upload
        await page.goto("https://www.tiktok.com/upload")
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)
        
        # Buscar dropzone
        dropzone = await page.query_selector('div:has-text("Select video")')
        if not dropzone:
            print("❌ Dropzone no encontrado")
            return False
        
        # Cargar video
        with open(video_path, 'rb') as f:
            video_data = f.read()
        
        video_base64 = base64.b64encode(video_data).decode()
        file_size_mb = len(video_data) / (1024*1024)
        print(f"📁 Video cargado: {file_size_mb:.1f} MB")
        
        # Obtener coordenadas
        dropzone_box = await dropzone.bounding_box()
        if dropzone_box:
            center_x = dropzone_box['x'] + dropzone_box['width'] / 2
            center_y = dropzone_box['y'] + dropzone_box['height'] / 2
        else:
            center_x = 960
            center_y = 540
        
        # Simular drag & drop
        await page.evaluate(f"""
            async (data) => {{
                const {{ centerX, centerY, videoBase64, fileName }} = data;
                
                const byteCharacters = atob(videoBase64);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {{
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }}
                const byteArray = new Uint8Array(byteNumbers);
                const blob = new Blob([byteArray], {{ type: 'video/mp4' }});
                const file = new File([blob], fileName, {{ type: 'video/mp4' }});
                
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                
                const dropzone = document.elementFromPoint(centerX, centerY) || document.body;
                
                const dragEnterEvent = new DragEvent('dragenter', {{
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                }});
                
                const dragOverEvent = new DragEvent('dragover', {{
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                }});
                
                const dropEvent = new DragEvent('drop', {{
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                }});
                
                dropzone.dispatchEvent(dragEnterEvent);
                await new Promise(resolve => setTimeout(resolve, 100));
                dropzone.dispatchEvent(dragOverEvent);
                await new Promise(resolve => setTimeout(resolve, 100));
                dropzone.dispatchEvent(dropEvent);
                
                const fileInput = document.querySelector('input[type="file"]');
                if (fileInput) {{
                    const changeEvent = new Event('change', {{ bubbles: true }});
                    Object.defineProperty(fileInput, 'files', {{
                        value: dataTransfer.files,
                        configurable: true
                    }});
                    fileInput.dispatchEvent(changeEvent);
                }}
                
                return true;
            }}
        """, {
            'centerX': center_x,
            'centerY': center_y,
            'videoBase64': video_base64,
            'fileName': os.path.basename(video_path)
        })
        
        # Verificar carga
        print("⏳ Verificando carga del video...")
        video_loaded = False
        for i in range(15):
            await page.wait_for_timeout(2000)
            select_btn = await page.query_selector('[data-e2e="select_video_button"]')
            if not (select_btn and await select_btn.is_visible()):
                print("✅ Video cargado exitosamente")
                video_loaded = True
                break
            print(f"⏳ Esperando carga... {i+1}/15")
        
        if not video_loaded:
            print("❌ Video no se cargó")
            return False
        
        # Escribir descripción personalizada por video
        print("✏️ Escribiendo descripción...")
        
        descripciones = [
            """🔥 ¿Sabías que puedes crear contenido viral con IA? 

🎬 Este truco te va a cambiar la forma de crear videos
💡 Guarda este post para no olvidarlo
✨ #IA #ContentCreator #Viral #Tips #VideoMarketing""",
            
            """💡 La IA está revolucionando la creación de contenido

🚀 En segundos puedes generar ideas increíbles
🎯 Perfecto para creators que buscan destacar
📱 #CreadorDeContenido #IA #Viral #TikTokTips #Marketing""",
            
            """🎯 El secreto que usan los creators exitosos

⚡ Herramientas de IA que transforman tu contenido  
🔝 Lleva tu creatividad al siguiente nivel
💪 #ViralContent #IA #Creator #Tips #Success"""
        ]
        
        # Usar descripción según el número de video
        descripcion = descripciones[(video_numero - 1) % len(descripciones)]
        
        # Encontrar editor
        editor_selectors = [
            '[contenteditable="true"]',
            '[data-e2e="editor-placeholder"]',
            'div[contenteditable]',
            '[role="textbox"]'
        ]
        
        editor = None
        for selector in editor_selectors:
            try:
                editor = await page.wait_for_selector(selector, timeout=5000)
                if editor and await editor.is_visible():
                    break
            except:
                continue
        
        if not editor:
            print("❌ Editor no encontrado")
            return False
        
        # Escribir descripción
        await editor.click()
        await page.keyboard.press('Control+a')
        await page.keyboard.press('Delete')
        await editor.type(descripcion, delay=30)
        print("✅ Descripción escrita")
        
        # Manejar modal de IA
        await page.wait_for_timeout(2000)
        try:
            ai_modal = await page.query_selector('[data-e2e="ai-modal-close"]')
            if ai_modal and await ai_modal.is_visible():
                await ai_modal.click()
                print("✅ Modal IA cerrado")
                await page.wait_for_timeout(1000)
        except:
            pass
        
        # Publicar
        print("🚀 Publicando video...")
        
        publish_selectors = [
            '[data-e2e="post-button"]',
            'button:has-text("Post")',
            '[data-e2e="submit-post"]',
            'button[type="submit"]'
        ]
        
        publish_btn = None
        for selector in publish_selectors:
            try:
                btn = await page.query_selector(selector)
                if btn and await btn.is_visible() and not await btn.is_disabled():
                    publish_btn = btn
                    break
            except:
                continue
        
        if not publish_btn:
            print("❌ Botón de publicar no encontrado")
            return False
        
        await publish_btn.click()
        print("✅ Video enviado para publicación")
        
        # Verificar éxito
        print("⏳ Verificando publicación...")
        success = False
        
        for i in range(15):
            await page.wait_for_timeout(2000)
            
            success_indicators = [
                'text="Your video is being uploaded"',
                'text="Uploading"', 
                'text="Processing"',
                'text="Your video has been uploaded"',
                '[data-e2e="upload-success"]'
            ]
            
            for indicator in success_indicators:
                try:
                    element = await page.query_selector(indicator)
                    if element and await element.is_visible():
                        print(f"✅ ¡ÉXITO! Video en proceso")
                        success = True
                        break
                except:
                    continue
            
            if success:
                break
            
            if "upload" not in page.url:
                print("✅ ¡ÉXITO! Redirigido fuera de upload")
                success = True
                break
            
            print(f"⏳ Verificando... {i+1}/15")
        
        if success:
            print(f"🎉 ¡VIDEO {video_numero} SUBIDO EXITOSAMENTE!")
        else:
            print(f"⚠️ Video {video_numero} enviado (verificar manualmente)")
        
        return success
        
    except Exception as e:
        print(f"❌ Error subiendo video {video_numero}: {e}")
        return False
    
    finally:
        await context.close()

async def subir_todos_los_videos_optimizados():
    """Subir los 3 videos optimizados secuencialmente"""
    
    # Buscar videos optimizados
    videos_dir = "data/videos"
    videos_optimizados = []
    
    for file in os.listdir(videos_dir):
        if file.endswith("_tiktok_optimized.mp4"):
            videos_optimizados.append(os.path.join(videos_dir, file))
    
    videos_optimizados.sort()
    
    if not videos_optimizados:
        print("❌ No se encontraron videos optimizados")
        return
    
    print(f"🎬 SUBIDA MASIVA DE VIDEOS OPTIMIZADOS")
    print(f"📱 {len(videos_optimizados)} videos listos para TikTok")
    print(f"{'='*60}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        videos_subidos = 0
        
        try:
            for i, video_path in enumerate(videos_optimizados, 1):
                print(f"\n⏳ Esperando 10 segundos entre videos...")
                if i > 1:  # No esperar antes del primer video
                    await asyncio.sleep(10)
                
                success = await subir_video_individual(browser, video_path, i, len(videos_optimizados))
                if success:
                    videos_subidos += 1
                
                print(f"📊 Progreso: {i}/{len(videos_optimizados)} procesados, {videos_subidos} exitosos")
        
        finally:
            await browser.close()
        
        print(f"\n{'='*60}")
        print(f"🎉 SUBIDA MASIVA COMPLETADA")
        print(f"{'='*60}")
        print(f"✅ Videos subidos exitosamente: {videos_subidos}/{len(videos_optimizados)}")
        print(f"📱 Los videos aparecerán en tu perfil en unos minutos")
        
        if videos_subidos > 0:
            print(f"🚀 ¡MISIÓN CUMPLIDA! {videos_subidos} videos optimizados subidos a TikTok")

if __name__ == "__main__":
    asyncio.run(subir_todos_los_videos_optimizados())
