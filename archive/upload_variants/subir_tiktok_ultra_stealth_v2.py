#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V2 - OPTIMIZADO
Versión mejorada con ajustes basados en feedback
"""

import asyncio
import json
import os
import random
import time
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

async def movimiento_humano_realista(page):
    """Simula movimientos de mouse completamente humanos"""
    await page.mouse.move(
        random.randint(200, 1200), 
        random.randint(200, 800),
        steps=random.randint(10, 30)
    )
    await asyncio.sleep(random.uniform(0.5, 2.0))
    
    if random.random() < 0.3:
        await page.mouse.wheel(0, random.randint(-100, 100))
        await asyncio.sleep(random.uniform(0.3, 1.0))

async def escribir_como_humano(element, texto):
    """Escribe texto como un humano real"""
    await element.click()
    await asyncio.sleep(random.uniform(0.2, 0.8))
    
    await element.fill("")
    await asyncio.sleep(random.uniform(0.1, 0.3))
    
    for i, char in enumerate(texto):
        await element.type(char)
        
        if char == ' ':
            await asyncio.sleep(random.uniform(0.1, 0.3))
        elif char in '.,!?':
            await asyncio.sleep(random.uniform(0.2, 0.5))
        elif i > 0 and i % random.randint(8, 15) == 0:
            await asyncio.sleep(random.uniform(0.1, 0.4))
        else:
            await asyncio.sleep(random.uniform(0.05, 0.15))

async def subir_video_ultra_stealth_v2(video_path, descripcion):
    """Upload ultra sigiloso optimizado v2"""
    print("🎯 UPLOADER TIKTOK ULTRA STEALTH V2")
    print("=" * 60)
    print(f"📹 Video: {os.path.basename(video_path)}")
    print(f"📏 Tamaño: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=[
                '--start-maximized',
                '--disable-blink-features=AutomationControlled',
                '--exclude-switches=enable-automation',
                '--no-first-run',
                '--disable-default-apps',
                '--disable-popup-blocking',
                '--allow-running-insecure-content',
                '--disable-web-security',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-field-trial-config'
            ],
            ignore_default_args=['--enable-automation']
        )
        
        # Viewport más grande para evitar cortes
        context = await browser.new_context(
            viewport={'width': 1440, 'height': 900},  # Tamaño optimizado
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            locale='es-MX',
            timezone_id='America/Mexico_City',
            geolocation={'latitude': 19.4326, 'longitude': -99.1332},
            permissions=['geolocation', 'microphone', 'camera', 'notifications'],
            color_scheme='dark',
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Cache-Control': 'max-age=0'
            }
        )
        
        page = await context.new_page()
        
        # Scripts ultra avanzados anti-detección
        await page.add_init_script("""
            // Eliminar TODOS los rastros de automation
            delete Object.getPrototypeOf(navigator).webdriver;
            delete navigator.__webdriver_script_fn;
            delete navigator.__webdriver_evaluate;
            delete navigator.__selenium_unwrapped;
            delete navigator.__webdriver_unwrapped;
            delete navigator.__driver_evaluate;
            delete navigator.__webdriver_script_func;
            delete navigator.__fxdriver_evaluate;
            delete navigator.__driver_unwrapped;
            delete navigator.__fxdriver_unwrapped;
            
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
                configurable: true
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => ({
                    length: 3,
                    0: { name: 'Chrome PDF Plugin' },
                    1: { name: 'Chrome PDF Viewer' },
                    2: { name: 'Native Client' }
                })
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['es-MX', 'es', 'en-US', 'en']
            });
            
            window.chrome = {
                runtime: {
                    onConnect: undefined,
                    onMessage: undefined
                },
                loadTimes: function() {
                    return {
                        commitLoadTime: Date.now() / 1000 - Math.random(),
                        finishDocumentLoadTime: Date.now() / 1000 - Math.random(),
                        finishLoadTime: Date.now() / 1000 - Math.random(),
                        firstPaintAfterLoadTime: 0,
                        firstPaintTime: Date.now() / 1000 - Math.random(),
                        navigationType: 'Other',
                        npnNegotiatedProtocol: 'h2',
                        requestTime: Date.now() / 1000 - Math.random(),
                        startLoadTime: Date.now() / 1000 - Math.random(),
                        wasAlternateProtocolAvailable: false,
                        wasFetchedViaSpdy: true,
                        wasNpnNegotiated: true
                    };
                }
            };
            
            Object.defineProperty(screen, 'availHeight', { get: () => 1040 });
            Object.defineProperty(screen, 'availWidth', { get: () => 1920 });
            Object.defineProperty(screen, 'height', { get: () => 1080 });
            Object.defineProperty(screen, 'width', { get: () => 1920 });
            
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            if ('getBattery' in navigator) {
                const originalGetBattery = navigator.getBattery;
                navigator.getBattery = () => Promise.resolve({
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity,
                    level: Math.random() * 0.3 + 0.7
                });
            }
            
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Google Inc. (Intel)';
                }
                if (parameter === 37446) {
                    return 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8681)';
                }
                return getParameter(parameter);
            };
            
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function(...args) {
                const context = this.getContext('2d');
                if (context) {
                    const imageData = context.getImageData(0, 0, this.width, this.height);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        imageData.data[i] += Math.floor(Math.random() * 3) - 1;
                        imageData.data[i + 1] += Math.floor(Math.random() * 3) - 1;
                        imageData.data[i + 2] += Math.floor(Math.random() * 3) - 1;
                    }
                    context.putImageData(imageData, 0, 0);
                }
                return originalToDataURL.apply(this, args);
            };
            
            ['webdriver-evaluate', 'webdriver-evaluate-response'].forEach(
                eventType => document.addEventListener(eventType, e => e.stopImmediatePropagation(), true)
            );
            
            console.log('🎯 Ultra stealth V2 activated');
        """)
        
        try:
            if not await cargar_cookies(context, "config/upload_cookies_playwright.json"):
                return False
            
            # Navegación humana gradual
            print("\n🌐 Navegando como humano a TikTok...")
            await page.goto("https://www.tiktok.com", timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            
            await movimiento_humano_realista(page)
            await asyncio.sleep(random.uniform(3, 5))
            
            # Actividad humana reducida
            print("📱 Simulando actividad humana...")
            for _ in range(random.randint(1, 2)):  # Menos scrolls
                await page.mouse.wheel(0, random.randint(300, 600))
                await asyncio.sleep(random.uniform(1, 2))
                await movimiento_humano_realista(page)
            
            # Ir a upload
            print("\n📤 Navegando a Creator Center...")
            await page.goto("https://www.tiktok.com/creator-center/upload", timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(random.uniform(3, 5))
            
            # Cerrar popups/banners
            try:
                close_btns = await page.query_selector_all('button[aria-label*="lose"], button[aria-label*="ose"], [data-e2e="close"]')
                for btn in close_btns:
                    try:
                        await btn.click()
                        await asyncio.sleep(random.uniform(0.5, 1.0))
                    except:
                        pass
            except:
                pass
            
            await movimiento_humano_realista(page)
            print("✅ Página de upload cargada")
            
            # Cargar archivo
            print("\n📁 Cargando archivo como humano...")
            all_inputs = await page.query_selector_all('input[type="file"]')
            print(f"📁 Encontrados {len(all_inputs)} inputs de archivo")
            
            upload_success = False
            for i, input_elem in enumerate(all_inputs):
                try:
                    print(f"\n🎯 Intentando input #{i+1}...")
                    accept_attr = await input_elem.get_attribute('accept')
                    print(f"   Accept: {accept_attr}")
                    
                    await asyncio.sleep(random.uniform(0.5, 1.0))
                    await input_elem.set_input_files(video_path)
                    print(f"✅ ARCHIVO CARGADO con input #{i+1}")
                    upload_success = True
                    break
                    
                except Exception as e:
                    print(f"❌ Error con input #{i+1}: {e}")
                    continue
            
            if not upload_success:
                print("❌ No se pudo cargar el archivo")
                return False
            
            # Procesamiento optimizado: 30 segundos
            print("\n⏳ Procesamiento optimizado (30 segundos)...")
            total_wait = 30  # Reducido de 90 a 30
            interval = 5     # Revisar cada 5 segundos
            
            for elapsed in range(0, total_wait, interval):
                print(f"⏳ Procesando... {elapsed}/{total_wait}s")
                
                if random.random() < 0.6:
                    await movimiento_humano_realista(page)
                
                try:
                    progress_indicators = await page.query_selector_all('[class*="progress"], [class*="loading"], [class*="upload"]')
                    if progress_indicators:
                        print(f"   📊 {len(progress_indicators)} indicadores de progreso")
                except:
                    pass
                
                await asyncio.sleep(interval)
            
            # Verificación final
            print("\n🔍 Verificación final de procesamiento...")
            try:
                indicators = [
                    'video',
                    'canvas', 
                    'img[src*="thumb"]',
                    '[class*="preview"]',
                    '[class*="thumbnail"]',
                    '[class*="player"]'
                ]
                
                found_indicators = []
                for indicator in indicators:
                    elements = await page.query_selector_all(indicator)
                    if elements:
                        found_indicators.append(f"{indicator} ({len(elements)})")
                
                if found_indicators:
                    print("✅ Indicadores encontrados:")
                    for ind in found_indicators:
                        print(f"   - {ind}")
                else:
                    print("⚠️ No se detectaron indicadores de procesamiento")
                
            except Exception as e:
                print(f"⚠️ Error verificando procesamiento: {e}")
            
            # Screenshot después de procesamiento
            screenshot_path = f"ultra_stealth_v2_processing_{random.randint(1000,9999)}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot post-procesamiento: {screenshot_path}")
            
            # Configuración con comportamiento humano
            await asyncio.sleep(random.uniform(2, 3))
            await movimiento_humano_realista(page)
            
            # Show More
            print("\n🔍 Buscando opciones avanzadas...")
            try:
                show_more = await page.wait_for_selector('text="Show more"', timeout=10000)
                if show_more:
                    await show_more.hover()
                    await asyncio.sleep(random.uniform(0.5, 1.0))
                    await show_more.click()
                    print("✅ Show More clickeado")
                    await asyncio.sleep(random.uniform(2, 3))
            except:
                print("⚠️ Show More no encontrado")
            
            # AI Content - MEJORADO con múltiples intentos
            print("\n🤖 Configurando AI Content (mejorado)...")
            ai_content_success = False
            
            # Múltiples selectores para AI Content
            ai_selectors = [
                'text="AI-generated content"',
                'text="AI content"',
                'input[type="checkbox"]:near(text="AI")',
                'label:has-text("AI")',
                '[data-e2e="ai-content"]',
                'input[name*="ai"]',
                'input[id*="ai"]',
                'span:has-text("AI-generated")',
                'div:has-text("AI-generated content")'
            ]
            
            for selector in ai_selectors:
                try:
                    print(f"🔍 Buscando AI Content: {selector}")
                    ai_elem = await page.wait_for_selector(selector, timeout=5000)
                    if ai_elem:
                        await ai_elem.scroll_into_view_if_needed()
                        await ai_elem.hover()
                        await asyncio.sleep(random.uniform(0.3, 0.8))
                        await ai_elem.click()
                        print(f"✅ AI Content activado: {selector}")
                        ai_content_success = True
                        await asyncio.sleep(random.uniform(1, 2))
                        
                        # Manejar modal si aparece
                        try:
                            modal = await page.wait_for_selector('[role="dialog"]', timeout=3000)
                            if modal:
                                await asyncio.sleep(random.uniform(1, 2))
                                accept_btn = await modal.wait_for_selector('text="Accept"', timeout=3000)
                                if accept_btn:
                                    await accept_btn.hover()
                                    await asyncio.sleep(random.uniform(0.2, 0.5))
                                    await accept_btn.click()
                                    print("✅ Modal AI aceptado")
                        except:
                            pass
                        break
                except:
                    continue
            
            if not ai_content_success:
                print("⚠️ AI Content no encontrado con ningún selector")
                # Tomar screenshot para debug
                debug_screenshot = f"ai_content_debug_{random.randint(1000,9999)}.png"
                await page.screenshot(path=debug_screenshot, full_page=True)
                print(f"📸 Screenshot debug AI Content: {debug_screenshot}")
            
            # Privacy settings - MEJORADO
            print("\n🔒 Configurando Privacy (Everyone)...")
            try:
                # Buscar configuración de privacidad
                privacy_selectors = [
                    'text="Who can view this video"',
                    'text="Privacy"',
                    '[data-e2e="privacy"]',
                    'select[name*="privacy"]',
                    'button:has-text("Only me")',
                    'button:has-text("Friends")',
                    'button:has-text("Everyone")'
                ]
                
                for selector in privacy_selectors:
                    try:
                        privacy_elem = await page.wait_for_selector(selector, timeout=3000)
                        if privacy_elem:
                            await privacy_elem.scroll_into_view_if_needed()
                            await privacy_elem.hover()
                            await asyncio.sleep(random.uniform(0.5, 1.0))
                            print(f"🔍 Elemento privacy encontrado: {selector}")
                            
                            # Si es un botón de "Only me", hacer click para cambiar
                            text_content = await privacy_elem.inner_text()
                            if "Only me" in text_content:
                                await privacy_elem.click()
                                await asyncio.sleep(random.uniform(1, 2))
                                
                                # Buscar opción "Everyone"
                                everyone_option = await page.wait_for_selector('text="Everyone"', timeout=5000)
                                if everyone_option:
                                    await everyone_option.click()
                                    print("✅ Privacy cambiado a Everyone")
                                    break
                            break
                    except:
                        continue
                        
            except:
                print("⚠️ No se pudo cambiar privacy settings")
            
            # Descripción
            print("\n📝 Agregando descripción...")
            desc_selectors = [
                '[data-e2e="video-caption"]',
                'div[contenteditable="true"]',
                'textarea[placeholder*="description"]'
            ]
            
            for selector in desc_selectors:
                try:
                    desc_input = await page.wait_for_selector(selector, timeout=5000)
                    if desc_input:
                        await desc_input.hover()
                        await asyncio.sleep(random.uniform(0.5, 1.0))
                        await escribir_como_humano(desc_input, descripcion)
                        print(f"✅ Descripción agregada con escritura humana")
                        await asyncio.sleep(random.uniform(2, 3))
                        break
                except:
                    continue
            
            # Screenshot pre-publicación
            screenshot_path = f"ultra_stealth_v2_pre_publish_{random.randint(1000,9999)}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot pre-publicación: {screenshot_path}")
            
            # Espera reducida antes de publicar
            print("\n⏳ Espera antes de publicar (reducida)...")
            await asyncio.sleep(random.uniform(5, 10))  # Reducido de 10-20 a 5-10
            await movimiento_humano_realista(page)
            
            # Publicar
            print("\n🚀 Publicando video...")
            publish_selectors = [
                '[data-e2e="post-btn"]',
                'text="Post"',
                'button[type="submit"]'
            ]
            
            for selector in publish_selectors:
                try:
                    post_btn = await page.wait_for_selector(selector, timeout=10000)
                    if post_btn and not await post_btn.is_disabled():
                        await post_btn.hover()
                        await asyncio.sleep(random.uniform(1, 2))
                        await post_btn.click()
                        print(f"✅ Video publicado con comportamiento humano")
                        
                        # Manejar modal post-publicación
                        try:
                            await asyncio.sleep(random.uniform(3, 5))
                            modal = await page.wait_for_selector('[role="dialog"]', timeout=10000)
                            if modal:
                                await asyncio.sleep(random.uniform(1, 2))
                                accept_btn = await modal.wait_for_selector('text="Accept"', timeout=5000)
                                if accept_btn:
                                    await accept_btn.hover()
                                    await asyncio.sleep(random.uniform(0.5, 1.0))
                                    await accept_btn.click()
                                    print("✅ Modal post-publicación manejado")
                        except:
                            pass
                        
                        # Screenshot final
                        screenshot_path = f"ultra_stealth_v2_success_{random.randint(1000,9999)}.png"
                        await page.screenshot(path=screenshot_path, full_page=True)
                        print(f"📸 Screenshot final: {screenshot_path}")
                        
                        print("\n🎉 ¡VIDEO SUBIDO CON ULTRA STEALTH V2!")
                        await asyncio.sleep(random.uniform(10, 20))  # Reducido de 15-30
                        return True
                except:
                    continue
            
            print("❌ No se pudo publicar")
            return False
                
        except Exception as e:
            print(f"❌ Error durante ultra stealth V2 upload: {e}")
            return False
        finally:
            print("\n🔍 Manteniendo browser abierto para inspección...")
            await asyncio.sleep(30)  # Reducido de 60 a 30
            await browser.close()

async def main():
    """Función principal"""
    load_dotenv()
    
    video_path = os.path.join("data", "videos", "final", "videos_unidos_FUNDIDO_TIKTOK.mp4")
    
    if not os.path.exists(video_path):
        print(f"❌ Video no encontrado: {video_path}")
        return
    
    descripcion = "🎭 Video ASMR viral generado con IA | Contenido hipnótico y relajante para máximo engagement #ASMR #IA #Viral #Satisfying #TikTok"
    
    success = await subir_video_ultra_stealth_v2(video_path, descripcion)
    
    if success:
        print("\n🎉 ¡ULTRA STEALTH V2 MISSION ACCOMPLISHED!")
    else:
        print("\n❌ Ultra stealth V2 fallido - necesita revisión manual")

if __name__ == "__main__":
    asyncio.run(main())
