import asyncio
import os
from playwright.async_api import async_playwright
import json
import base64

async def subir_tiktok_definitivo():
    """Pipeline completo de subida TikTok sin depender del preview visual"""
    
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
            return False
        
        try:
            # Paso 1: Ir a upload
            print("🚀 Navegando a TikTok upload...")
            await page.goto("https://www.tiktok.com/upload")
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(3000)
            
            # Paso 2: Subir video usando drag & drop
            print("📁 Subiendo video con drag & drop...")
            
            # Buscar dropzone
            dropzone = await page.query_selector('div:has-text("Select video")')
            if not dropzone:
                print("❌ Dropzone no encontrado")
                return False
            
            # Cargar video
            video_path = "data/videos/veo_video_tiktok_optimized.mp4"
            if not os.path.exists(video_path):
                print(f"❌ Video no encontrado: {video_path}")
                return False
            
            with open(video_path, 'rb') as f:
                video_data = f.read()
            
            video_base64 = base64.b64encode(video_data).decode()
            print(f"📁 Video cargado: {len(video_data)} bytes")
            
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
                    
                    // Crear archivo
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
                    
                    // Disparar eventos de drag & drop
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
                    
                    // Backup con input
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
                'fileName': 'veo_video_tiktok_optimized.mp4'
            })
            
            # Verificar que el video se cargó (botón Select desaparece)
            print("⏳ Verificando carga del video...")
            video_loaded = False
            for i in range(10):
                await page.wait_for_timeout(2000)
                select_btn = await page.query_selector('[data-e2e="select_video_button"]')
                if not (select_btn and await select_btn.is_visible()):
                    print("✅ Video cargado exitosamente")
                    video_loaded = True
                    break
                print(f"⏳ Esperando carga... {i+1}/10")
            
            if not video_loaded:
                print("❌ Video no se cargó correctamente")
                return False
            
            # Paso 3: Rellenar descripción
            print("✏️ Escribiendo descripción...")
            
            # Esperar el editor
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
                        print(f"✅ Editor encontrado: {selector}")
                        break
                except:
                    continue
            
            if not editor:
                print("❌ Editor no encontrado")
                return False
            
            # Limpiar y escribir descripción
            await editor.click()
            await page.keyboard.press('Control+a')
            await page.keyboard.press('Delete')
            
            descripcion = """✨ ¿Sabías que puedes crear videos increíbles con IA? 
            
🎬 Este contenido te enseña trucos fascinantes que cambiarán tu perspectiva
💡 #IA #VideoMarketing #Contenido #Tips #Viral"""
            
            await editor.type(descripcion, delay=50)
            print("✅ Descripción escrita")
            
            # Paso 4: Manejar modal de IA si aparece
            await page.wait_for_timeout(2000)
            try:
                ai_modal = await page.query_selector('[data-e2e="ai-modal-close"]')
                if ai_modal and await ai_modal.is_visible():
                    await ai_modal.click()
                    print("✅ Modal IA cerrado")
                    await page.wait_for_timeout(1000)
            except:
                pass
            
            # Paso 5: Configurar privacidad
            print("🔒 Configurando privacidad...")
            try:
                # Buscar botón de configuración de privacidad
                privacy_selectors = [
                    '[data-e2e="public-post"]',
                    'button:has-text("Who can view this video")',
                    '[data-e2e="privacy-selector"]'
                ]
                
                for selector in privacy_selectors:
                    try:
                        privacy_btn = await page.query_selector(selector)
                        if privacy_btn and await privacy_btn.is_visible():
                            await privacy_btn.click()
                            print("✅ Menú privacidad abierto")
                            await page.wait_for_timeout(1000)
                            
                            # Seleccionar "Público"
                            public_option = await page.query_selector('text="Public"')
                            if public_option:
                                await public_option.click()
                                print("✅ Configurado como público")
                            break
                    except:
                        continue
            except Exception as e:
                print(f"⚠️ No se pudo configurar privacidad: {e}")
            
            # Paso 6: Publicar
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
                        print(f"✅ Botón publicar encontrado: {selector}")
                        break
                except:
                    continue
            
            if not publish_btn:
                print("❌ Botón de publicar no encontrado")
                await page.screenshot(path="error_no_publish_btn.png")
                return False
            
            await publish_btn.click()
            print("✅ Video enviado para publicación")
            
            # Verificar éxito
            print("⏳ Verificando publicación...")
            success = False
            
            for i in range(15):
                await page.wait_for_timeout(2000)
                
                # Buscar indicadores de éxito
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
                            print(f"✅ ¡ÉXITO! Video en proceso: {indicator}")
                            success = True
                            break
                    except:
                        continue
                
                if success:
                    break
                
                # También verificar si regresamos al inicio (otro indicador de éxito)
                if "upload" not in page.url:
                    print("✅ ¡ÉXITO! Redirigido fuera de upload")
                    success = True
                    break
                
                print(f"⏳ Verificando éxito... {i+1}/15")
            
            # Screenshot final
            await page.screenshot(path="resultado_final.png")
            
            if success:
                print("🎉 ¡VIDEO SUBIDO EXITOSAMENTE!")
                print("📱 El video aparecerá en tu perfil en unos minutos")
            else:
                print("⚠️ No se pudo confirmar el éxito, pero el video puede haberse subido")
                print("📱 Revisa tu perfil en unos minutos")
            
            # Mantener abierto para verificación manual
            print("⏳ Manteniendo navegador abierto 30 segundos...")
            await page.wait_for_timeout(30000)
            
            return success
            
        except Exception as e:
            print(f"❌ Error durante la subida: {e}")
            await page.screenshot(path="error_subida.png")
            return False
        
        finally:
            await browser.close()

if __name__ == "__main__":
    resultado = asyncio.run(subir_tiktok_definitivo())
    if resultado:
        print("🎉 ¡MISIÓN CUMPLIDA!")
    else:
        print("❌ Hubo problemas, revisa los screenshots")
