#!/usr/bin/env python3
"""
🥷 UPLOADER TIKTOK STEALTH - ANTI-DETECCIÓN
Versión sigilosa para evitar detección de bot
"""

import asyncio
import json
import os
import random
from playwright.async_api import async_playwright
from dotenv import load_dotenv

async def cargar_cookies(context, cookies_path):
    """Cargar cookies de sesión"""
    try:
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
        
        for cookie in cookies:
            if 'sameSite' in cookie:
                val = cookie['sameSite']
                if val not in ["Strict", "Lax", "None"]:
                    cookie["sameSite"] = "None"
        
        await context.add_cookies(cookies)
        print(f"✅ Cookies cargadas desde {cookies_path}")
        return True
    except Exception as e:
        print(f"❌ Error cargando cookies: {e}")
        return False

async def esperar_humanizado(min_sec=2.0, max_sec=5.0):
    """Espera humanizada con variación aleatoria"""
    wait_time = random.uniform(min_sec, max_sec)
    await asyncio.sleep(wait_time)

async def subir_video_stealth(video_path, descripcion):
    """Subir video en modo stealth anti-detección"""
    print("🥷 UPLOADER TIKTOK STEALTH MODE")
    print("=" * 50)
    print(f"📹 Video: {os.path.basename(video_path)}")
    print(f"📏 Tamaño: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    
    async with async_playwright() as p:
        # Configuración stealth anti-detección
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--exclude-switches=enable-automation',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-default-apps',
                '--disable-popup-blocking',
                '--disable-extensions-file-access-check',
                '--disable-extensions-http-throttling',
                '--disable-ipc-flooding-protection'
            ]
        )
        
        # Contexto con características de navegador real
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            locale='es-ES',
            timezone_id='America/Mexico_City',
            permissions=['camera', 'microphone'],
            extra_http_headers={
                'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document'
            }
        )
        
        page = await context.new_page()
        
        # Inyectar scripts anti-detección
        await page.add_init_script("""
            // Eliminar webdriver flag
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Falsificar plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Falsificar languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['es-ES', 'es', 'en'],
            });
            
            // Falsificar chrome object
            window.chrome = {
                runtime: {},
            };
            
            // Eliminar automation flag
            delete window.navigator.__webdriver_script_fn;
        """)
        
        try:
            # Cargar cookies
            if not await cargar_cookies(context, "config/upload_cookies_playwright.json"):
                return False
            
            # Navegar de forma humanizada
            print("\n🌐 Navegando a TikTok...")
            await page.goto("https://www.tiktok.com", timeout=30000)
            await esperar_humanizado(2, 4)
            
            # Simular actividad humana
            print("🎭 Simulando actividad humana...")
            await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
            await esperar_humanizado(1, 2)
            
            # Ir a creator center
            print("\n📤 Navegando a Creator Center...")
            await page.goto("https://www.tiktok.com/creator-center/upload", timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            await esperar_humanizado(3, 5)
            
            # Cerrar banner de navegador no soportado si aparece
            try:
                close_banner = await page.wait_for_selector('button[aria-label="Close"]', timeout=3000)
                if close_banner:
                    await close_banner.click()
                    print("✅ Banner cerrado")
                    await esperar_humanizado(1, 2)
            except:
                pass
            
            # Verificar página
            if "upload" not in page.url:
                print(f"❌ URL incorrecta: {page.url}")
                return False
            
            print("✅ Página de upload cargada")
            
            # Buscar y usar input file directamente
            print("\n📁 Localizando input de archivo...")
            
            # Múltiples selectores para el input
            input_selectors = [
                'input[type="file"]',
                'input[accept*="video"]',
                '[data-e2e="upload-input"]'
            ]
            
            upload_success = False
            for selector in input_selectors:
                try:
                    print(f"🔍 Probando selector: {selector}")
                    input_elem = await page.wait_for_selector(selector, timeout=10000)
                    if input_elem:
                        # Verificar que el input está habilitado
                        is_enabled = await input_elem.is_enabled()
                        if is_enabled:
                            print(f"✅ Input encontrado y habilitado: {selector}")
                            await input_elem.set_input_files(video_path)
                            print("🎉 ARCHIVO CARGADO EXITOSAMENTE")
                            upload_success = True
                            break
                        else:
                            print(f"⚠️ Input deshabilitado: {selector}")
                except Exception as e:
                    print(f"❌ Error con selector {selector}: {e}")
                    continue
            
            if not upload_success:
                print("❌ No se pudo cargar el archivo")
                return False
            
            # Esperar procesamiento más tiempo
            print("\n⏳ Esperando procesamiento del video (45 segundos)...")
            await asyncio.sleep(45)
            
            # Verificar que el video se procesó correctamente
            print("\n🔍 Verificando procesamiento...")
            try:
                # Buscar indicadores de video procesado
                video_processed = False
                
                # Verificar preview del video
                video_preview = await page.query_selector('video')
                if video_preview:
                    print("✅ Preview de video detectado")
                    video_processed = True
                
                # Verificar thumbnail
                thumbnail = await page.query_selector('canvas, img[src*="thumb"]')
                if thumbnail:
                    print("✅ Thumbnail detectado")
                    video_processed = True
                
                if not video_processed:
                    print("⚠️ Video aún procesando - esperando más tiempo...")
                    await asyncio.sleep(30)
                
            except Exception as e:
                print(f"⚠️ Error verificando procesamiento: {e}")
            
            # Buscar "Show More" con movimiento humanizado
            print("\n🔍 Buscando opciones avanzadas...")
            await page.mouse.move(random.randint(300, 800), random.randint(400, 600))
            await esperar_humanizado(1, 2)
            
            show_more_selectors = [
                'text="Show more"',
                'text="Mostrar más"',
                'button:has-text("Show")',
                'button:has-text("more")',
                '[class*="show-more"]'
            ]
            
            for selector in show_more_selectors:
                try:
                    btn = await page.wait_for_selector(selector, timeout=5000)
                    if btn:
                        await btn.scroll_into_view_if_needed()
                        await esperar_humanizado(0.5, 1)
                        await btn.click()
                        print(f"✅ Click en Show More: {selector}")
                        await esperar_humanizado(2, 3)
                        break
                except:
                    continue
            
            # Habilitar AI Content con movimiento humanizado
            print("\n🤖 Configurando AI Content...")
            await page.mouse.move(random.randint(200, 700), random.randint(500, 700))
            await esperar_humanizado(1, 2)
            
            ai_selectors = [
                'text="AI-generated content"',
                'text="AI content"',
                'input[type="checkbox"]:near(text="AI")',
                'label:has-text("AI")'
            ]
            
            for selector in ai_selectors:
                try:
                    ai_elem = await page.wait_for_selector(selector, timeout=5000)
                    if ai_elem:
                        await ai_elem.scroll_into_view_if_needed()
                        await esperar_humanizado(0.5, 1)
                        await ai_elem.click()
                        print(f"✅ AI Content habilitado: {selector}")
                        await esperar_humanizado(2, 3)
                        
                        # Manejar modal si aparece
                        try:
                            modal = await page.wait_for_selector('[role="dialog"]', timeout=3000)
                            if modal:
                                accept_btn = await modal.wait_for_selector('text="Accept"', timeout=3000)
                                if accept_btn:
                                    await accept_btn.click()
                                    print("✅ Modal AI Content aceptado")
                                    await esperar_humanizado(1, 2)
                        except:
                            pass
                        break
                except:
                    continue
            
            # Agregar descripción con escritura humanizada
            print("\n📝 Agregando descripción...")
            desc_selectors = [
                '[data-e2e="video-caption"]',
                'textarea[placeholder*="description"]',
                'div[contenteditable="true"]'
            ]
            
            for selector in desc_selectors:
                try:
                    desc_input = await page.wait_for_selector(selector, timeout=5000)
                    if desc_input:
                        await desc_input.scroll_into_view_if_needed()
                        await desc_input.click()
                        await esperar_humanizado(0.5, 1)
                        
                        # Escribir descripción de forma humanizada
                        await desc_input.fill("")  # Limpiar primero
                        await esperar_humanizado(0.5, 1)
                        
                        # Escribir carácter por carácter con variación
                        for char in descripcion:
                            await desc_input.type(char)
                            if random.random() < 0.1:  # 10% chance de pausa
                                await asyncio.sleep(random.uniform(0.05, 0.15))
                        
                        print(f"✅ Descripción agregada: {selector}")
                        await esperar_humanizado(2, 3)
                        break
                except:
                    continue
            
            # Tomar screenshot antes de publicar
            screenshot_path = f"pre_publish_{random.randint(1000,9999)}.png"
            await page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot pre-publicación: {screenshot_path}")
            
            # Esperar antes de publicar
            print("\n⏳ Esperando antes de publicar (30 segundos)...")
            await asyncio.sleep(30)
            
            # Verificar una vez más el preview
            print("\n📺 Verificación final del preview...")
            try:
                video_final = await page.query_selector('video')
                if video_final:
                    print("✅ Preview final confirmado")
                else:
                    print("⚠️ Preview no disponible - continuando...")
            except:
                print("⚠️ No se pudo verificar preview final")
            
            # Publicar con movimiento humanizado
            print("\n🚀 Publicando video...")
            await page.mouse.move(random.randint(800, 1200), random.randint(600, 800))
            await esperar_humanizado(1, 2)
            
            publish_selectors = [
                '[data-e2e="post-btn"]',
                'text="Post"',
                'button[type="submit"]',
                'button:has-text("Post")'
            ]
            
            published = False
            for selector in publish_selectors:
                try:
                    post_btn = await page.wait_for_selector(selector, timeout=10000)
                    if post_btn and not await post_btn.is_disabled():
                        await post_btn.scroll_into_view_if_needed()
                        await esperar_humanizado(1, 2)
                        await post_btn.click()
                        print(f"✅ Video publicado: {selector}")
                        
                        # Manejar modal post-publicación
                        try:
                            await asyncio.sleep(5)
                            modal = await page.wait_for_selector('[role="dialog"]', timeout=10000)
                            if modal:
                                accept_btn = await modal.wait_for_selector('text="Accept"', timeout=5000)
                                if accept_btn:
                                    await accept_btn.click()
                                    print("✅ Modal post-publicación aceptado")
                        except:
                            pass
                        
                        published = True
                        break
                except:
                    continue
            
            if published:
                print("\n🎉 ¡VIDEO SUBIDO EXITOSAMENTE!")
                
                # Tomar screenshot final
                screenshot_path = f"upload_success_stealth_{random.randint(1000,9999)}.png"
                await page.screenshot(path=screenshot_path)
                print(f"📸 Screenshot final: {screenshot_path}")
                
                await asyncio.sleep(15)
                return True
            else:
                print("❌ No se pudo publicar el video")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la subida: {e}")
            return False
        finally:
            print("\n🔍 Manteniendo browser abierto 30s para inspección...")
            await asyncio.sleep(30)
            await browser.close()

async def main():
    """Función principal"""
    load_dotenv()
    
    # Video a subir
    video_path = os.path.join("data", "videos", "final", "videos_unidos_FUNDIDO_TIKTOK.mp4")
    
    if not os.path.exists(video_path):
        print(f"❌ Video no encontrado: {video_path}")
        return
    
    descripcion = "🎭 Video ASMR viral generado con IA | Contenido hipnótico y relajante para máximo engagement #ASMR #IA #Viral #Satisfying #TikTok"
    
    success = await subir_video_stealth(video_path, descripcion)
    
    if success:
        print("\n🎉 ¡MISIÓN CUMPLIDA! Video subido en modo stealth")
    else:
        print("\n❌ Subida no completada - revisar manualmente")

if __name__ == "__main__":
    asyncio.run(main())
