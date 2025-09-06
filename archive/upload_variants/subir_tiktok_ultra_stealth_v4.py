#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V4 - AI CONTENT ULTRA ESPECÍFICO
Versión mejorada con selectores ultra-específicos para el AI Content toggle
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

async def activar_ai_content_ultra_especifico(page):
    """AJUSTE #3: Activación con XPath específico del usuario"""
    print("\n🎯 ACTIVACIÓN AI CONTENT CON XPATH ESPECÍFICO...")
    
    # XPath específico proporcionado por el usuario
    xpath_ai_toggle = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span'
    
    try:
        print(f"🔍 Usando XPath específico: {xpath_ai_toggle}")
        
        # Buscar elemento por XPath
        ai_toggle = await page.query_selector(f'xpath={xpath_ai_toggle}')
        
        if ai_toggle:
            print("   📍 Elemento AI toggle encontrado con XPath")
            
            # Obtener información del elemento
            tag_name = await ai_toggle.evaluate('el => el.tagName')
            class_name = await ai_toggle.get_attribute('class')
            
            print(f"   � Tag: {tag_name}")
            print(f"   📋 Clases: {class_name}")
            
            # Hacer scroll al elemento y click
            await ai_toggle.scroll_into_view_if_needed()
            await asyncio.sleep(random.uniform(0.5, 1.0))
            await ai_toggle.hover()
            await asyncio.sleep(random.uniform(0.3, 0.8))
            await ai_toggle.click()
            
            print("✅ AI Content toggle clickeado con XPath específico")
            
            # Esperar un momento para que se aplique el cambio
            await asyncio.sleep(2)
            
            return True
        else:
            print("   ❌ Elemento AI toggle no encontrado con XPath")
            
        # Fallback: Buscar por texto como antes
        print("🔍 Fallback: Buscando por texto 'AI-generated content'")
        
        ai_elements = await page.query_selector_all('text="AI-generated content"')
        if ai_elements:
            print(f"   📍 Encontrados {len(ai_elements)} elementos con texto AI")
            
            for element in ai_elements:
                try:
                    # Buscar el contenedor padre
                    container = await element.query_selector('xpath=../../../..')
                    if container:
                        # Buscar toggles en el contenedor
                        toggles = await container.query_selector_all('[role="switch"], [aria-checked], [data-state]')
                        print(f"   🎛️ Encontrados {len(toggles)} toggles en contenedor")
                        
                        for i, toggle in enumerate(toggles, 1):
                            try:
                                is_checked = await toggle.get_attribute('aria-checked')
                                state = await toggle.get_attribute('data-state')
                                print(f"     🔘 Toggle #{i} - Checked: {is_checked}, State: {state}")
                                
                                if is_checked == 'false' or state == 'unchecked':
                                    await toggle.click()
                                    await asyncio.sleep(1)
                                    print(f"✅ AI Content activado - Toggle #{i} (fallback)")
                                    return True
                            except Exception as e:
                                print(f"     ❌ Error con toggle #{i}: {str(e)[:50]}")
                                continue
                except Exception as e:
                    print(f"   ❌ Error procesando elemento AI: {str(e)[:50]}")
                    continue
        
        print("❌ No se pudo activar AI Content")
        return False
        
    except Exception as e:
        print(f"❌ Error en activación AI Content: {e}")
        return False
                        const switches = container.querySelectorAll(
                            '[role="switch"], input[type="checkbox"], .toggle, [class*="switch"], [class*="toggle"]'
                        );
                        
                        for (let sw of switches) {
                            const isChecked = sw.checked || 
                                            sw.getAttribute('aria-checked') === 'true' ||
                                            sw.getAttribute('data-state') === 'checked' ||
                                            sw.classList.contains('checked');
                                            
                            console.log('Switch encontrado, checked:', isChecked);
                            
                            if (!isChecked) {
                                // Intentar activar
                                sw.click();
                                
                                // Disparar eventos adicionales
                                sw.dispatchEvent(new Event('change', { bubbles: true }));
                                sw.dispatchEvent(new Event('input', { bubbles: true }));
                                
                                console.log('AI Content activado via JavaScript V4');
                                return true;
                            }
                        }
                        
                        container = container.parentElement;
                    }
                }
                
                return false;
            }
        ''')
        
        if result:
            print("✅ AI Content activado via JavaScript V4")
            return True
            
    except Exception as e:
        print(f"❌ Error en estrategia V4 #2: {e}")
    
    # Estrategia 3: Buscar por estructura específica de la imagen
    try:
        print("🔍 Estrategia V4 #3: Estructura específica de TikTok")
        
        # Buscar divs que contengan tanto el texto como el toggle
        containers = await page.query_selector_all('div')
        
        for container in containers:
            try:
                text_content = await container.inner_text()
                if "AI-generated content" in text_content:
                    print(f"   📦 Container encontrado con AI content")
                    
                    # Buscar input checkbox específicamente
                    checkboxes = await container.query_selector_all('input[type="checkbox"]')
                    print(f"   📱 Checkboxes en container: {len(checkboxes)}")
                    
                    for checkbox in checkboxes:
                        is_checked = await checkbox.is_checked()
                        print(f"     ☑️ Checkbox checked: {is_checked}")
                        
                        if not is_checked:
                            await checkbox.scroll_into_view_if_needed()
                            await asyncio.sleep(random.uniform(0.5, 1.0))
                            
                            # Intentar click en el checkbox
                            await checkbox.click()
                            print("✅ AI Content activado via checkbox V4")
                            return True
                            
                    # Buscar también por role="switch"
                    switches = await container.query_selector_all('[role="switch"]')
                    print(f"   🎛️ Switches en container: {len(switches)}")
                    
                    for switch in switches:
                        aria_checked = await switch.get_attribute('aria-checked')
                        print(f"     🔄 Switch aria-checked: {aria_checked}")
                        
                        if aria_checked == 'false':
                            await switch.scroll_into_view_if_needed()
                            await asyncio.sleep(random.uniform(0.5, 1.0))
                            await switch.click()
                            print("✅ AI Content activado via switch V4")
                            return True
                            
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"❌ Error en estrategia V4 #3: {e}")
    
    # Estrategia 4: Click por coordenadas relativas
    try:
        print("🔍 Estrategia V4 #4: Click por coordenadas")
        
        # Buscar el texto "AI-generated content" y hacer click al lado
        ai_element = await page.locator('text=AI-generated content').first
        if ai_element:
            # Obtener las coordenadas del texto
            box = await ai_element.bounding_box()
            if box:
                # Click a la derecha del texto (donde debería estar el toggle)
                click_x = box['x'] + box['width'] + 20  # 20px a la derecha
                click_y = box['y'] + box['height'] / 2  # Centro vertical
                
                print(f"   🎯 Haciendo click en coordenadas: ({click_x}, {click_y})")
                await page.mouse.click(click_x, click_y)
                print("✅ AI Content activado via coordenadas V4")
                return True
                
    except Exception as e:
        print(f"❌ Error en estrategia V4 #4: {e}")
    
    # Tomar screenshot de debug ultra-detallado
    debug_screenshot = f"ai_content_debug_v4_{random.randint(1000,9999)}.png"
    await page.screenshot(path=debug_screenshot, full_page=True)
    print(f"📸 Screenshot debug AI Content V4: {debug_screenshot}")
    
    # Imprimir información de debug
    try:
        debug_info = await page.evaluate('''
            () => {
                const elements = document.querySelectorAll('*');
                let aiElements = [];
                
                for (let el of elements) {
                    if (el.textContent && el.textContent.includes('AI-generated content')) {
                        aiElements.push({
                            tagName: el.tagName,
                            className: el.className,
                            id: el.id,
                            textContent: el.textContent.substring(0, 100)
                        });
                    }
                }
                
                return aiElements;
            }
        ''')
        
        print("🔍 Elementos con 'AI-generated content' encontrados:")
        for i, elem in enumerate(debug_info):
            print(f"   {i+1}. {elem['tagName']} - Class: {elem['className']} - Text: {elem['textContent']}")
            
    except:
        pass
    
    print("⚠️ AI Content no pudo ser activado con ninguna estrategia V4")
    return False

async def verificar_ai_content_activado(page):
    """Verificar si el AI Content está realmente activado con máxima precisión"""
    try:
        # Verificación múltiple ultra-específica
        verifications = [
            # Verificación 1: Por aria-checked
            '''document.querySelector('[role="switch"][aria-checked="true"]') !== null''',
            
            # Verificación 2: Por checkbox checked
            '''Array.from(document.querySelectorAll('input[type="checkbox"]')).some(cb => cb.checked)''',
            
            # Verificación 3: Por clases específicas
            '''document.querySelector('.checked, .active, .on, [data-state="checked"]') !== null''',
            
            # Verificación 4: Verificación contextual
            '''
            (() => {
                const aiElements = Array.from(document.querySelectorAll('*')).filter(el => 
                    el.textContent && el.textContent.includes('AI-generated content')
                );
                
                for (let elem of aiElements) {
                    const container = elem.closest('div');
                    if (container) {
                        const switches = container.querySelectorAll('[role="switch"], input[type="checkbox"]');
                        for (let sw of switches) {
                            if (sw.checked || sw.getAttribute('aria-checked') === 'true') {
                                return true;
                            }
                        }
                    }
                }
                return false;
            })()
            '''
        ]
        
        for i, verification in enumerate(verifications):
            try:
                result = await page.evaluate(verification)
                print(f"   ✅ Verificación #{i+1}: {result}")
                if result:
                    return True
            except:
                print(f"   ❌ Verificación #{i+1}: Error")
                
        return False
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

async def subir_video_ultra_stealth_v4(video_path, descripcion):
    """Upload ultra sigiloso v4 con AI Content ultra-específico"""
    print("🎯 UPLOADER TIKTOK ULTRA STEALTH V4")
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
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},  # AJUSTE #1: Pantalla más grande para evitar cortes
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
        
        # Scripts anti-detección (mismo que versiones anteriores)
        await page.add_init_script("""
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
            
            console.log('🎯 Ultra stealth V4 activated - AI Content Ultra Específico');
        """)
        
        try:
            if not await cargar_cookies(context, "config/upload_cookies_playwright.json"):
                return False
            
            # Navegación (mismo flujo optimizado)
            print("\n🌐 Navegando como humano a TikTok...")
            await page.goto("https://www.tiktok.com", timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            await movimiento_humano_realista(page)
            await asyncio.sleep(random.uniform(3, 5))
            
            print("📱 Simulando actividad humana...")
            for _ in range(random.randint(1, 2)):
                await page.mouse.wheel(0, random.randint(300, 600))
                await asyncio.sleep(random.uniform(1, 2))
                await movimiento_humano_realista(page)
            
            print("\n📤 Navegando a Creator Center...")
            await page.goto("https://www.tiktok.com/creator-center/upload", timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(random.uniform(3, 5))
            
            # Cerrar popups
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
            
            # AJUSTE #2: Procesamiento (20 segundos en lugar de 30)
            print("\n⏳ Procesamiento optimizado (20 segundos)...")
            total_wait = 20
            interval = 5
            
            for elapsed in range(0, total_wait, interval):
                print(f"⏳ Procesando... {elapsed}/{total_wait}s")
                if random.random() < 0.6:
                    await movimiento_humano_realista(page)
                await asyncio.sleep(interval)
            
            # Verificación de procesamiento
            print("\n🔍 Verificación final de procesamiento...")
            try:
                indicators = ['video', 'canvas', 'img[src*="thumb"]', '[class*="preview"]', '[class*="thumbnail"]', '[class*="player"]']
                found_indicators = []
                for indicator in indicators:
                    elements = await page.query_selector_all(indicator)
                    if elements:
                        found_indicators.append(f"{indicator} ({len(elements)})")
                
                if found_indicators:
                    print("✅ Indicadores encontrados:")
                    for ind in found_indicators:
                        print(f"   - {ind}")
            except Exception as e:
                print(f"⚠️ Error verificando procesamiento: {e}")
            
            # Screenshot post-procesamiento
            screenshot_path = f"ultra_stealth_v4_processing_{random.randint(1000,9999)}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot post-procesamiento: {screenshot_path}")
            
            # Configuración
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
                    await asyncio.sleep(random.uniform(5, 8))  # Más tiempo para cargar todas las opciones
            except:
                print("⚠️ Show More no encontrado")
            
            # AI Content V4 - ULTRA ESPECÍFICO
            ai_success = await activar_ai_content_ultra_especifico(page)
            
            # Verificar activación con máxima precisión
            if ai_success:
                await asyncio.sleep(random.uniform(2, 3))
                is_really_active = await verificar_ai_content_activado(page)
                if is_really_active:
                    print("✅ AI Content CONFIRMADO como activado V4")
                else:
                    print("⚠️ AI Content click realizado pero verificación falló V4")
            
            # Privacy settings (optimizado)
            print("\n🔒 Configurando Privacy (Everyone)...")
            try:
                privacy_selectors = [
                    'text="Who can view this video"',
                    'text="Everyone"',
                    'button:has-text("Everyone")',
                    'select option[value="everyone"]'
                ]
                
                for selector in privacy_selectors:
                    try:
                        privacy_elem = await page.wait_for_selector(selector, timeout=3000)
                        if privacy_elem:
                            await privacy_elem.scroll_into_view_if_needed()
                            await privacy_elem.hover()
                            await asyncio.sleep(random.uniform(0.5, 1.0))
                            await privacy_elem.click()
                            print(f"✅ Privacy configurado: {selector}")
                            break
                    except:
                        continue
            except:
                print("⚠️ No se pudo cambiar privacy settings")
            
            # Descripción
            print("\n📝 Agregando descripción...")
            desc_selectors = ['[data-e2e="video-caption"]', 'div[contenteditable="true"]', 'textarea[placeholder*="description"]']
            
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
            screenshot_path = f"ultra_stealth_v4_pre_publish_{random.randint(1000,9999)}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot pre-publicación: {screenshot_path}")
            
            # Espera antes de publicar
            print("\n⏳ Espera antes de publicar...")
            await asyncio.sleep(random.uniform(5, 10))
            await movimiento_humano_realista(page)
            
            # Publicar
            print("\n🚀 Publicando video...")
            publish_selectors = ['[data-e2e="post-btn"]', 'text="Post"', 'button[type="submit"]']
            
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
                        screenshot_path = f"ultra_stealth_v4_success_{random.randint(1000,9999)}.png"
                        await page.screenshot(path=screenshot_path, full_page=True)
                        print(f"📸 Screenshot final: {screenshot_path}")
                        
                        print("\n🎉 ¡VIDEO SUBIDO CON ULTRA STEALTH V4!")
                        await asyncio.sleep(30)
                        return True
                except:
                    continue
            
            print("❌ No se pudo publicar")
            return False
                
        except Exception as e:
            print(f"❌ Error durante ultra stealth V4 upload: {e}")
            return False
        finally:
            print("\n🔍 Manteniendo browser abierto para inspección...")
            await asyncio.sleep(30)
            await browser.close()

async def main():
    """Función principal"""
    load_dotenv()
    
    video_path = os.path.join("data", "videos", "final", "videos_unidos_FUNDIDO_TIKTOK.mp4")
    
    if not os.path.exists(video_path):
        print(f"❌ Video no encontrado: {video_path}")
        return
    
    descripcion = "🎭 Video ASMR viral generado con IA | Contenido hipnótico y relajante para máximo engagement #ASMR #IA #Viral #Satisfying #TikTok"
    
    success = await subir_video_ultra_stealth_v4(video_path, descripcion)
    
    if success:
        print("\n🎉 ¡ULTRA STEALTH V4 MISSION ACCOMPLISHED!")
    else:
        print("\n❌ Ultra stealth V4 fallido - necesita revisión manual")

if __name__ == "__main__":
    asyncio.run(main())
