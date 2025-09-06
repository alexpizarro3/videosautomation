import asyncio
import os
from playwright.async_api import async_playwright
import json
import base64

async def test_drag_drop_simulation():
    """Simular drag & drop como lo haría un usuario real"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
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
        
        # Cargar cookies
        try:
            with open("config/upload_cookies_playwright.json", 'r') as f:
                cookies = json.load(f)
            
            for cookie in cookies:
                if 'sameSite' in cookie:
                    val = cookie['sameSite']
                    if val not in ["Strict", "Lax", "None"]:
                        cookie["sameSite"] = "None"
            
            await context.add_cookies(cookies)
            print("✅ Cookies cargadas")
        except Exception as e:
            print(f"❌ Error cargando cookies: {e}")
            return
        
        # Ir a upload
        await page.goto("https://www.tiktok.com/upload")
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)
        
        print("🎯 Buscando dropzone...")
        
        # Buscar el área de drop
        dropzone_selectors = [
            '[data-e2e="upload-container"]',
            '.upload-container',
            '.upload-area',
            '.drop-zone',
            'div:has-text("Select video")',
            '[class*="upload"]'
        ]
        
        dropzone = None
        for selector in dropzone_selectors:
            try:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    dropzone = element
                    print(f"✅ Dropzone encontrado: {selector}")
                    break
            except:
                continue
        
        if not dropzone:
            # Buscar cualquier elemento clickeable grande en el centro
            dropzone = await page.query_selector('body')
            print("🎯 Usando body como dropzone")
        
        # Leer archivo de video
        video_path = "data/videos/veo_video_tiktok_optimized.mp4"
        if not os.path.exists(video_path):
            print(f"❌ Video no encontrado: {video_path}")
            return
        
        # Convertir archivo a base64 para el drag & drop
        with open(video_path, 'rb') as f:
            video_data = f.read()
        
        video_base64 = base64.b64encode(video_data).decode()
        file_size = len(video_data)
        
        print(f"📁 Video cargado: {file_size} bytes")
        
        # Obtener coordenadas del dropzone
        dropzone_box = await dropzone.bounding_box()
        if dropzone_box:
            center_x = dropzone_box['x'] + dropzone_box['width'] / 2
            center_y = dropzone_box['y'] + dropzone_box['height'] / 2
        else:
            # Usar centro de pantalla como fallback
            center_x = 960
            center_y = 540
        
        print(f"🎯 Centro del dropzone: ({center_x}, {center_y})")
        
        # Simular drag & drop usando JavaScript
        await page.evaluate(f"""
            async (data) => {{
                const {{ centerX, centerY, videoBase64, fileName }} = data;
                
                // Convertir base64 a File object
                const byteCharacters = atob(videoBase64);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {{
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }}
                const byteArray = new Uint8Array(byteNumbers);
                const blob = new Blob([byteArray], {{ type: 'video/mp4' }});
                const file = new File([blob], fileName, {{ type: 'video/mp4' }});
                
                // Crear DataTransfer object
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                
                // Encontrar el dropzone
                const dropzone = document.elementFromPoint(centerX, centerY) || document.body;
                
                console.log('Dropzone encontrado:', dropzone);
                console.log('File creado:', file.name, file.size, file.type);
                
                // Simular eventos de drag & drop
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
                
                // Disparar eventos
                dropzone.dispatchEvent(dragEnterEvent);
                await new Promise(resolve => setTimeout(resolve, 100));
                
                dropzone.dispatchEvent(dragOverEvent);
                await new Promise(resolve => setTimeout(resolve, 100));
                
                dropzone.dispatchEvent(dropEvent);
                
                console.log('Eventos de drag & drop disparados');
                
                // También intentar con input de archivo como backup
                const fileInput = document.querySelector('input[type="file"]');
                if (fileInput) {{
                    const changeEvent = new Event('change', {{ bubbles: true }});
                    Object.defineProperty(fileInput, 'files', {{
                        value: dataTransfer.files,
                        configurable: true
                    }});
                    fileInput.dispatchEvent(changeEvent);
                    console.log('Evento change disparado en input');
                }}
                
                return true;
            }}
        """, {
            'centerX': center_x,
            'centerY': center_y,
            'videoBase64': video_base64,
            'fileName': 'veo_video_tiktok_optimized.mp4'
        })
        
        print("🚀 Drag & drop simulado")
        
        # Esperar y monitorear cambios
        print("⏳ Esperando respuesta del drag & drop...")
        
        for i in range(30):
            await page.wait_for_timeout(2000)
            
            # Verificar si desapareció el botón select
            select_btn = await page.query_selector('[data-e2e="select_video_button"]')
            if not (select_btn and await select_btn.is_visible()):
                print("✅ Botón 'Select video' desapareció")
            
            # Verificar editor
            editor = await page.query_selector('[contenteditable="true"]')
            if editor and await editor.is_visible():
                print("✅ Editor disponible")
            
            # Verificar preview
            video_preview = await page.query_selector('video')
            if video_preview and await video_preview.is_visible():
                print("🎉 ¡PREVIEW DE VIDEO VISIBLE!")
                break
            
            # Screenshot de progreso
            await page.screenshot(path=f"dragdrop_progress_{i:02d}.png")
            print(f"📸 Screenshot {i:02d}/30")
            
            if i % 5 == 0:
                print(f"⏳ Progreso: {i}/30 - esperando preview...")
        
        # Screenshot final
        await page.screenshot(path="dragdrop_final.png")
        
        print("⏳ Manteniendo abierto 30 segundos para inspección...")
        await page.wait_for_timeout(30000)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_drag_drop_simulation())
