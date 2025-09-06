import asyncio
import os
from playwright.async_api import async_playwright
import json
import base64

async def subir_tiktok_con_preview_mejorado():
    """
    🎬 SUBIDA TIKTOK CON VERIFICACIÓN COMPLETA DE PREVIEW
    Se enfoca en asegurar que el video se cargue correctamente en portada y preview
    """
    
    # Configurar video a subir
    video_path = "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Video no encontrado: {video_path}")
        return False
    
    print(f"🎬 SUBIENDO VIDEO VIRAL A TIKTOK")
    print("=" * 60)
    print(f"📁 Archivo: {video_path}")
    print(f"📦 Tamaño: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        page = await context.new_page()
        
        # Scripts anti-detección mejorados
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            window.chrome = { runtime: {} };
        """)
        
        try:
            # Cargar cookies si existen
            print("🍪 Cargando cookies...")
            try:
                with open('tiktok_cookies.json', 'r') as f:
                    cookies = json.load(f)
                await context.add_cookies(cookies)
                print("✅ Cookies cargadas")
            except:
                print("⚠️ No se pudieron cargar cookies, continuando...")
            
            # Ir a TikTok
            print("🌐 Navegando a TikTok...")
            await page.goto('https://www.tiktok.com/upload', wait_until='networkidle')
            await page.wait_for_timeout(3000)
            
            # Verificar login
            current_url = page.url
            if '/login' in current_url or '/signup' in current_url:
                print("❌ Necesitas hacer login manualmente")
                print("🔄 Por favor, haz login y presiona Enter para continuar...")
                input()
                await page.goto('https://www.tiktok.com/upload', wait_until='networkidle')
            
            print("✅ En página de upload")
            
            # PASO 1: SUBIR VIDEO CON VERIFICACIÓN MEJORADA
            print("\n📤 PASO 1: SUBIENDO VIDEO...")
            print("-" * 40)
            
            # Preparar video en base64
            with open(video_path, 'rb') as f:
                video_data = f.read()
            video_base64 = base64.b64encode(video_data).decode()
            
            # Buscar área de upload
            upload_selectors = [
                '[data-e2e="select_video_button"]',
                'input[type="file"]',
                '[data-e2e="upload-btn"]'
            ]
            
            upload_area = None
            for selector in upload_selectors:
                try:
                    upload_area = await page.query_selector(selector)
                    if upload_area:
                        print(f"✅ Área de upload encontrada: {selector}")
                        break
                except:
                    continue
            
            if not upload_area:
                print("❌ No se encontró área de upload")
                return False
            
            # Obtener posición para drop
            box = await upload_area.bounding_box()
            if box:
                center_x = box['x'] + box['width'] / 2
                center_y = box['y'] + box['height'] / 2
                print(f"📍 Posición de drop: {center_x}, {center_y}")
            else:
                print("⚠️ No se pudo obtener posición, usando coordenadas por defecto")
                center_x = 960  # Centro de pantalla
                center_y = 540
            
            # Simular drag & drop mejorado
            await page.evaluate("""
                async (params) => {
                    const { centerX, centerY, videoBase64, fileName } = params;
                    
                    // Convertir base64 a blob
                    const response = await fetch(`data:video/mp4;base64,${videoBase64}`);
                    const blob = await response.blob();
                    const file = new File([blob], fileName, { type: 'video/mp4' });
                    
                    // Crear eventos de drag and drop
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    
                    const dropEvent = new DragEvent('drop', {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    });
                    
                    const dragOverEvent = new DragEvent('dragover', {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    });
                    
                    // Buscar el elemento target correcto
                    const targets = [
                        document.querySelector('[data-e2e="select_video_button"]'),
                        document.querySelector('input[type="file"]'),
                        document.querySelector('[data-e2e="upload-btn"]'),
                        document.elementFromPoint(centerX, centerY)
                    ].filter(el => el);
                    
                    for (const target of targets) {
                        if (target) {
                            target.dispatchEvent(dragOverEvent);
                            target.dispatchEvent(dropEvent);
                            
                            // También intentar con input file directo
                            if (target.tagName === 'INPUT') {
                                Object.defineProperty(target, 'files', {
                                    value: dataTransfer.files,
                                    writable: false,
                                });
                                target.dispatchEvent(new Event('change', { bubbles: true }));
                            }
                            break;
                        }
                    }
                    
                    return true;
                }
            """, {
                'centerX': center_x,
                'centerY': center_y,
                'videoBase64': video_base64,
                'fileName': 'videos_unidos_FUNDIDO_TIKTOK.mp4'
            })
            
            # PASO 2: VERIFICACIÓN COMPLETA DE CARGA Y PREVIEW
            print("\n🔍 PASO 2: VERIFICANDO CARGA Y PREVIEW...")
            print("-" * 40)
            
            # Verificaciones múltiples
            video_cargado = False
            preview_visible = False
            
            for intento in range(15):  # 30 segundos total
                await page.wait_for_timeout(2000)
                print(f"⏳ Verificación {intento + 1}/15...")
                
                # 1. Verificar que desaparece el botón de selección
                select_btn = await page.query_selector('[data-e2e="select_video_button"]')
                select_visible = select_btn and await select_btn.is_visible() if select_btn else False
                
                # 2. Verificar que aparece preview del video
                preview_selectors = [
                    'video',
                    '[data-e2e="video-preview"]',
                    '.video-player',
                    'canvas',
                    '[class*="preview"]'
                ]
                
                for selector in preview_selectors:
                    try:
                        preview_el = await page.query_selector(selector)
                        if preview_el and await preview_el.is_visible():
                            preview_visible = True
                            print(f"✅ Preview encontrado: {selector}")
                            break
                    except:
                        continue
                
                # 3. Verificar elementos de la interfaz de edición
                editor_selectors = [
                    '[contenteditable="true"]',
                    '[data-e2e="editor-caption"]',
                    'textarea'
                ]
                
                editor_visible = False
                for selector in editor_selectors:
                    try:
                        editor = await page.query_selector(selector)
                        if editor and await editor.is_visible():
                            editor_visible = True
                            break
                    except:
                        continue
                
                # Evaluar estado
                if not select_visible and (preview_visible or editor_visible):
                    video_cargado = True
                    print("✅ Video cargado correctamente!")
                    print(f"   📱 Preview visible: {preview_visible}")
                    print(f"   ✏️ Editor visible: {editor_visible}")
                    break
                
                print(f"   📱 Preview: {preview_visible}, ✏️ Editor: {editor_visible}, 🔘 Select oculto: {not select_visible}")
            
            if not video_cargado:
                print("❌ El video no se cargó correctamente después de 30 segundos")
                print("🔍 Diagnóstico:")
                
                # Diagnóstico detallado
                all_videos = await page.query_selector_all('video')
                print(f"   Videos encontrados: {len(all_videos)}")
                
                all_canvas = await page.query_selector_all('canvas')
                print(f"   Canvas encontrados: {len(all_canvas)}")
                
                # Tomar screenshot para debug
                await page.screenshot(path='debug_upload_failed.png')
                print("📸 Screenshot guardado: debug_upload_failed.png")
                
                return False
            
            # PASO 3: ESCRIBIR DESCRIPCIÓN
            print("\n✏️ PASO 3: ESCRIBIENDO DESCRIPCIÓN...")
            print("-" * 40)
            
            descripcion = """🔥 MOMENTO ASMR ULTRA SATISFYING 🔥
            
¿Puedes ver esto sin quedarte hipnotizado? 😵‍💫

#ASMR #Satisfying #Viral #Tingles #Relaxing #Aesthetic #Dreamy #Therapeutic #Mindful #Peaceful"""
            
            # Buscar editor con múltiples selectores
            editor_selectors = [
                '[contenteditable="true"]',
                '[data-e2e="editor-caption"]',
                'textarea[placeholder*="escribe"]',
                'textarea[placeholder*="caption"]',
                '[data-e2e="caption-input"]'
            ]
            
            editor = None
            for selector in editor_selectors:
                try:
                    editor = await page.query_selector(selector)
                    if editor and await editor.is_visible():
                        print(f"✅ Editor encontrado: {selector}")
                        break
                except:
                    continue
            
            if editor:
                await editor.click()
                await page.wait_for_timeout(500)
                # Limpiar contenido existente
                await page.keyboard.press('Control+a')
                await page.keyboard.press('Delete')
                await editor.type(descripcion, delay=30)
                print("✅ Descripción escrita")
            else:
                print("⚠️ No se encontró editor de texto")
            
            # PASO 4: VERIFICAR CONFIGURACIÓN Y PUBLICAR
            print("\n🚀 PASO 4: CONFIGURACIÓN Y PUBLICACIÓN...")
            print("-" * 40)
            
            # Cerrar modal de IA si aparece
            try:
                ai_modal = await page.query_selector('[data-e2e="ai-modal-close"]')
                if ai_modal and await ai_modal.is_visible():
                    await ai_modal.click()
                    print("✅ Modal IA cerrado")
            except:
                pass
            
            # Buscar botón de publicar
            publish_selectors = [
                '[data-e2e="post-button"]',
                'button:has-text("Post")',
                'button:has-text("Publicar")',
                '[data-e2e="submit-post"]',
                'button[type="submit"]'
            ]
            
            publish_btn = None
            for selector in publish_selectors:
                try:
                    publish_btn = await page.query_selector(selector)
                    if publish_btn and await publish_btn.is_visible():
                        print(f"✅ Botón publicar encontrado: {selector}")
                        break
                except:
                    continue
            
            if publish_btn:
                # Verificar que el botón esté habilitado
                is_enabled = await publish_btn.is_enabled()
                print(f"🔘 Botón habilitado: {is_enabled}")
                
                if is_enabled:
                    print("🚀 Publicando...")
                    await publish_btn.click()
                    
                    # Verificar publicación exitosa
                    await page.wait_for_timeout(3000)
                    
                    success_indicators = [
                        'text="Your video is being uploaded"',
                        'text="Successfully uploaded"',
                        'text="Video uploaded"',
                        '[data-e2e="upload-success"]'
                    ]
                    
                    success = False
                    for indicator in success_indicators:
                        try:
                            element = await page.query_selector(indicator)
                            if element:
                                success = True
                                print("✅ Video publicado exitosamente!")
                                break
                        except:
                            continue
                    
                    if not success:
                        print("⚠️ No se pudo confirmar la publicación")
                    
                    return success
                else:
                    print("❌ Botón de publicar no está habilitado")
                    return False
            else:
                print("❌ No se encontró botón de publicar")
                return False
            
        except Exception as e:
            print(f"❌ Error durante la subida: {e}")
            await page.screenshot(path='debug_error.png')
            return False
        
        finally:
            print("\n📋 Manteniendo navegador abierto para revisión...")
            print("🔍 Revisa el resultado y presiona Enter para cerrar...")
            input()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(subir_tiktok_con_preview_mejorado())
