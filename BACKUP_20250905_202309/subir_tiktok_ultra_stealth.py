#!/usr/bin/env python3
"""
🕵️ UPLOADER TIKTOK ULTRA STEALTH - INDISTINGUIBLE DE HUMANO
Versión que engaña completamente a TikTok para evitar detección
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
    # Movimientos aleatorios pero realistas
    await page.mouse.move(
        random.randint(100, 800), 
        random.randint(100, 600),
        steps=random.randint(10, 30)
    )
    await asyncio.sleep(random.uniform(0.5, 2.0))
    
    # Scroll ocasional
    if random.random() < 0.3:
        await page.mouse.wheel(0, random.randint(-100, 100))
        await asyncio.sleep(random.uniform(0.3, 1.0))

async def escribir_como_humano(element, texto):
    """Escribe texto como un humano real"""
    await element.click()
    await asyncio.sleep(random.uniform(0.2, 0.8))
    
    # Limpiar campo
    await element.fill("")
    await asyncio.sleep(random.uniform(0.1, 0.3))
    
    # Escribir con velocidad humana variable
    for i, char in enumerate(texto):
        await element.type(char)
        
        # Pausas realistas
        if char == ' ':
            await asyncio.sleep(random.uniform(0.1, 0.3))
        elif char in '.,!?':
            await asyncio.sleep(random.uniform(0.2, 0.5))
        elif i > 0 and i % random.randint(8, 15) == 0:
            await asyncio.sleep(random.uniform(0.1, 0.4))
        else:
            await asyncio.sleep(random.uniform(0.05, 0.15))

async def subir_video_ultra_stealth(video_path, descripcion):
    """Upload ultra sigiloso que engaña completamente a TikTok"""
    print("🕵️ UPLOADER TIKTOK ULTRA STEALTH")
    print("=" * 60)
    print(f"📹 Video: {os.path.basename(video_path)}")
    print(f"📏 Tamaño: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    
    async with async_playwright() as p:
        # Lanzar con Chrome real - NO Chromium
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",  # USA CHROME REAL, NO CHROMIUM
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
        
        # Contexto ultra realista
        context = await browser.new_context(
            viewport=None,  # Usar tamaño real de ventana
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            locale='es-MX',
            timezone_id='America/Mexico_City',
            geolocation={'latitude': 19.4326, 'longitude': -99.1332},  # Ciudad de México
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
        
        # Inyectar scripts ultra avanzados anti-detección
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
            
            // Falsificar webdriver como undefined
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
                configurable: true
            });
            
            // Plugins realistas
            Object.defineProperty(navigator, 'plugins', {
                get: () => ({
                    length: 3,
                    0: { name: 'Chrome PDF Plugin' },
                    1: { name: 'Chrome PDF Viewer' },
                    2: { name: 'Native Client' }
                })
            });
            
            // Languages realistas
            Object.defineProperty(navigator, 'languages', {
                get: () => ['es-MX', 'es', 'en-US', 'en']
            });
            
            // Chrome object realista
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
            
            // Screen realista
            Object.defineProperty(screen, 'availHeight', { get: () => 1040 });
            Object.defineProperty(screen, 'availWidth', { get: () => 1920 });
            Object.defineProperty(screen, 'height', { get: () => 1080 });
            Object.defineProperty(screen, 'width', { get: () => 1920 });
            
            // Permission API
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Battery API (si existe)
            if ('getBattery' in navigator) {
                const originalGetBattery = navigator.getBattery;
                navigator.getBattery = () => Promise.resolve({
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity,
                    level: Math.random() * 0.3 + 0.7
                });
            }
            
            // WebGL fingerprint
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
            
            // Canvas fingerprint randomization
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
            
            // Eliminar automation events
            ['webdriver-evaluate', 'webdriver-evaluate-response'].forEach(
                eventType => document.addEventListener(eventType, e => e.stopImmediatePropagation(), true)
            );
            
            console.log('🕵️ Ultra stealth mode activated');
        """)
        
        try:
            # Cargar cookies
            if not await cargar_cookies(context, "config/upload_cookies_playwright.json"):
                return False
            
            # Comportamiento humano: Ir a TikTok principal primero
            print("\n🌐 Navegando como humano a TikTok...")
            await page.goto("https://www.tiktok.com", timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            
            # Simular navegación humana
            await movimiento_humano_realista(page)
            await asyncio.sleep(random.uniform(3, 7))
            
            # Scroll para simular lectura
            print("📱 Simulando actividad humana...")
            for _ in range(random.randint(2, 4)):
                await page.mouse.wheel(0, random.randint(300, 800))
                await asyncio.sleep(random.uniform(1, 3))
                await movimiento_humano_realista(page)
            
            # Ir a perfil (comportamiento típico antes de upload)
            try:
                profile_link = await page.wait_for_selector('[data-e2e="nav-profile"]', timeout=5000)
                if profile_link:
                    await profile_link.hover()
                    await asyncio.sleep(random.uniform(1, 2))
            except:
                pass
            
            # Ahora ir a upload - como lo haría un humano
            print("\n📤 Navegando a Creator Center...")
            await page.goto("https://www.tiktok.com/creator-center/upload", timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(random.uniform(4, 8))
            
            # Movimiento humano en página upload
            await movimiento_humano_realista(page)
            
            # Cerrar cualquier popup/banner
            try:
                close_btns = await page.query_selector_all('button[aria-label*="lose"], button[aria-label*="ose"], [data-e2e="close"]')
                for btn in close_btns:
                    try:
                        await btn.click()
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                    except:
                        pass
            except:
                pass
            
            print("✅ Página de upload cargada")
            
            # Simular que el usuario está mirando la página
            await movimiento_humano_realista(page)
            await asyncio.sleep(random.uniform(2, 4))
            
            # Encontrar y usar input file de forma humana
            print("\n📁 Cargando archivo como humano...")
            
            # Buscar todos los inputs file
            all_inputs = await page.query_selector_all('input[type="file"]')
            print(f"📁 Encontrados {len(all_inputs)} inputs de archivo")
            
            upload_success = False
            for i, input_elem in enumerate(all_inputs):
                try:
                    print(f"\n🎯 Intentando input #{i+1}...")
                    
                    # Verificar atributos
                    accept_attr = await input_elem.get_attribute('accept')
                    print(f"   Accept: {accept_attr}")
                    
                    # Intentar cargar con pausa humana
                    await asyncio.sleep(random.uniform(0.5, 1.5))
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
            
            # CRUCIAL: Esperar mucho más tiempo y simular actividad humana
            print("\n⏳ Simulando espera humana durante procesamiento...")
            total_wait = 90  # 90 segundos total
            interval = 10    # Revisar cada 10 segundos
            
            for elapsed in range(0, total_wait, interval):
                print(f"⏳ Procesando... {elapsed}/{total_wait}s")
                
                # Movimiento humano ocasional
                if random.random() < 0.7:
                    await movimiento_humano_realista(page)
                
                # Verificar si hay elementos de progreso
                try:
                    progress_indicators = await page.query_selector_all('[class*="progress"], [class*="loading"], [class*="upload"]')
                    if progress_indicators:
                        print(f"   📊 {len(progress_indicators)} indicadores de progreso")
                except:
                    pass
                
                await asyncio.sleep(interval)
            
            # Verificar procesamiento final
            print("\n🔍 Verificación final de procesamiento...")
            try:
                # Buscar múltiples indicadores
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
            screenshot_path = f"ultra_stealth_processing_{random.randint(1000,9999)}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot post-procesamiento: {screenshot_path}")
            
            # Configuración con comportamiento humano
            await asyncio.sleep(random.uniform(2, 4))
            await movimiento_humano_realista(page)
            
            # Show More con comportamiento humano
            print("\n🔍 Buscando opciones avanzadas...")
            try:
                show_more = await page.wait_for_selector('text="Show more"', timeout=10000)
                if show_more:
                    await show_more.hover()
                    await asyncio.sleep(random.uniform(0.5, 1.0))
                    await show_more.click()
                    print("✅ Show More clickeado")
                    await asyncio.sleep(random.uniform(2, 4))
            except:
                print("⚠️ Show More no encontrado")
            
            # AI Content con comportamiento humano
            print("\n🤖 Configurando AI Content...")
            try:
                ai_checkbox = await page.wait_for_selector('text="AI-generated content"', timeout=10000)
                if ai_checkbox:
                    await ai_checkbox.hover()
                    await asyncio.sleep(random.uniform(0.3, 0.8))
                    await ai_checkbox.click()
                    print("✅ AI Content habilitado")
                    await asyncio.sleep(random.uniform(1, 3))
                    
                    # Manejar modal con comportamiento humano
                    try:
                        modal = await page.wait_for_selector('[role="dialog"]', timeout=5000)
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
            except:
                print("⚠️ AI Content no encontrado")
            
            # Descripción con escritura humana
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
                        await asyncio.sleep(random.uniform(2, 4))
                        break
                except:
                    continue
            
            # Screenshot pre-publicación
            screenshot_path = f"ultra_stealth_pre_publish_{random.randint(1000,9999)}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot pre-publicación: {screenshot_path}")
            
            # Espera humana antes de publicar
            print("\n⏳ Espera humana antes de publicar...")
            await asyncio.sleep(random.uniform(10, 20))
            await movimiento_humano_realista(page)
            
            # Publicar con comportamiento humano
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
                            await asyncio.sleep(random.uniform(3, 7))
                            modal = await page.wait_for_selector('[role="dialog"]', timeout=10000)
                            if modal:
                                await asyncio.sleep(random.uniform(1, 3))
                                accept_btn = await modal.wait_for_selector('text="Accept"', timeout=5000)
                                if accept_btn:
                                    await accept_btn.hover()
                                    await asyncio.sleep(random.uniform(0.5, 1.0))
                                    await accept_btn.click()
                                    print("✅ Modal post-publicación manejado")
                        except:
                            pass
                        
                        # Screenshot final
                        screenshot_path = f"ultra_stealth_success_{random.randint(1000,9999)}.png"
                        await page.screenshot(path=screenshot_path, full_page=True)
                        print(f"📸 Screenshot final: {screenshot_path}")
                        
                        print("\n🎉 ¡VIDEO SUBIDO CON ULTRA STEALTH!")
                        await asyncio.sleep(random.uniform(15, 30))
                        return True
                except:
                    continue
            
            print("❌ No se pudo publicar")
            return False
                
        except Exception as e:
            print(f"❌ Error durante ultra stealth upload: {e}")
            return False
        finally:
            print("\n🔍 Manteniendo browser abierto para inspección manual...")
            await asyncio.sleep(60)  # Más tiempo para inspección
            await browser.close()

async def main():
    """Función principal"""
    load_dotenv()
    
    video_path = os.path.join("data", "videos", "final", "videos_unidos_FUNDIDO_TIKTOK.mp4")
    
    if not os.path.exists(video_path):
        print(f"❌ Video no encontrado: {video_path}")
        return
    
    descripcion = "🎭 Video ASMR viral generado con IA | Contenido hipnótico y relajante para máximo engagement #ASMR #IA #Viral #Satisfying #TikTok"
    
    success = await subir_video_ultra_stealth(video_path, descripcion)
    
    if success:
        print("\n🎉 ¡ULTRA STEALTH MISSION ACCOMPLISHED!")
    else:
        print("\n❌ Ultra stealth fallido - necesita revisión manual")

if __name__ == "__main__":
    asyncio.run(main())
