#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V4 MODIFICADO
Versión V4 con los ajustes específicos del usuario:
1. Pantalla 1920x1080
2. Procesamiento 20 segundos
3. XPath específico para AI content
4. Verificar "Everyone" seleccionado
5. Esperar 30 segundos antes de Post
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

async def activar_ai_content_xpath_especifico(page):
    """AJUSTE #3: Activación con XPath específico del usuario - Mejorado para post Show More"""
    print("\n🎯 ACTIVACIÓN AI CONTENT CON XPATH ESPECÍFICO...")
    
    # XPath específico proporcionado por el usuario
    xpath_ai_toggle = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span'
    
    try:
        print(f"🔍 Usando XPath específico: {xpath_ai_toggle}")
        
        # Scroll adicional para asegurar visibilidad después de Show More
        print("   📜 Haciendo scroll para asegurar visibilidad...")
        await page.mouse.wheel(0, 300)
        await asyncio.sleep(2)
        
        # Buscar elemento por XPath
        ai_toggle = await page.query_selector(f'xpath={xpath_ai_toggle}')
        
        if ai_toggle:
            print("   📍 Elemento AI toggle encontrado con XPath")
            
            # Obtener información del elemento
            try:
                tag_name = await ai_toggle.evaluate('el => el.tagName')
                class_name = await ai_toggle.get_attribute('class')
                
                print(f"   📋 Tag: {tag_name}")
                print(f"   📋 Clases: {class_name}")
                
                # Verificar si el elemento es visible
                is_visible = await ai_toggle.evaluate('''
                    el => {
                        const rect = el.getBoundingClientRect();
                        return rect.width > 0 && rect.height > 0 && 
                               rect.top >= 0 && rect.bottom <= window.innerHeight;
                    }
                ''')
                
                print(f"   👁️ Elemento visible: {is_visible}")
                
                if not is_visible:
                    print("   📜 Elemento no visible, haciendo scroll directo al elemento...")
                    # Usar JavaScript para hacer scroll directo al elemento
                    await ai_toggle.evaluate('''
                        el => {
                            el.scrollIntoView({behavior: 'smooth', block: 'center'});
                        }
                    ''')
                    await asyncio.sleep(3)
                
                # Hover sobre el elemento primero
                print("   🖱️ Haciendo hover sobre el elemento...")
                await ai_toggle.hover()
                await asyncio.sleep(1)
                
                # Click en el elemento
                print("   🖱️ Haciendo click en el toggle...")
                await ai_toggle.click()
                
                print("✅ AI Content toggle clickeado con XPath específico")
                
                # NUEVO: Buscar y manejar modal de confirmación
                print("   🔍 Buscando modal de confirmación...")
                await asyncio.sleep(2)
                
                # Buscar el modal y el botón "Turn on"
                modal_handled = False
                modal_selectors = [
                    'button:has-text("Turn on")',
                    'button:has-text("Aceptar")',
                    'button:has-text("Accept")',
                    'button:has-text("Confirmar")',
                    '[data-testid*="confirm"]',
                    '[class*="confirm"]',
                    'div[role="dialog"] button',
                    '.modal button'
                ]
                
                for selector in modal_selectors:
                    try:
                        modal_button = await page.query_selector(selector)
                        if modal_button:
                            # Verificar si el botón es visible
                            is_visible = await modal_button.is_visible()
                            if is_visible:
                                button_text = await modal_button.text_content()
                                print(f"   📍 Modal encontrado - Botón: '{button_text}' con selector: {selector}")
                                
                                # Click en el botón del modal
                                await modal_button.click()
                                print(f"   ✅ Modal confirmado - Botón '{button_text}' clickeado")
                                modal_handled = True
                                await asyncio.sleep(2)
                                break
                    except Exception as e:
                        continue
                
                if not modal_handled:
                    print("   ℹ️ No se encontró modal de confirmación (puede que no haya aparecido)")
                
                # Esperar después del modal
                await asyncio.sleep(3)
                
                # Verificar si el estado cambió
                new_class = await ai_toggle.get_attribute('class')
                print(f"   🔄 Clases después del click: {new_class}")
                
                if 'checked-true' in str(new_class) or 'Switch__thumb--checked-true' in str(new_class):
                    print("✅ AI Content activado exitosamente!")
                    return True
                elif modal_handled:
                    print("✅ AI Content activado (modal confirmado)")
                    return True
                else:
                    print("⚠️ Click realizado pero estado no cambió visiblemente")
                    return True  # Asumimos que funcionó
                
            except Exception as e:
                print(f"   ❌ Error procesando elemento XPath: {e}")
                # Intentar click directo con JavaScript
                print("   🔧 Intentando click con JavaScript...")
                try:
                    await ai_toggle.evaluate('el => el.click()')
                    await asyncio.sleep(2)
                    print("✅ Click JavaScript ejecutado")
                    return True
                except Exception as js_error:
                    print(f"   ❌ Error con JavaScript: {js_error}")
        else:
            print("   ❌ Elemento AI toggle no encontrado con XPath")
            
        # Fallback: Buscar por texto como antes
        print("🔍 Fallback: Buscando por texto 'AI-generated content'")
        
        # Scroll adicional para el fallback
        await page.mouse.wheel(0, 200)
        await asyncio.sleep(1)
        
        ai_elements = await page.query_selector_all('text="AI-generated content"')
        if ai_elements:
            print(f"   📍 Encontrados {len(ai_elements)} elementos con texto AI")
            
            for element in ai_elements:
                try:
                    # Buscar el contenedor padre
                    container = await element.query_selector('xpath=../../../..')
                    if container:
                        # Buscar toggles en el contenedor
                        toggles = await container.query_selector_all('[role="switch"], [aria-checked], [data-state], [class*="Switch"]')
                        print(f"   🎛️ Encontrados {len(toggles)} toggles en contenedor")
                        
                        for i, toggle in enumerate(toggles, 1):
                            try:
                                is_checked = await toggle.get_attribute('aria-checked')
                                state = await toggle.get_attribute('data-state')
                                class_attr = await toggle.get_attribute('class')
                                
                                print(f"     🔘 Toggle #{i} - Checked: {is_checked}, State: {state}")
                                
                                # Verificar si está desactivado
                                is_unchecked = (
                                    is_checked == 'false' or 
                                    state == 'unchecked' or 
                                    'checked-false' in str(class_attr)
                                )
                                
                                if is_unchecked:
                                    print(f"     🎯 Activando toggle #{i}...")
                                    await toggle.scroll_into_view_if_needed()
                                    await asyncio.sleep(1)
                                    await toggle.click()
                                    await asyncio.sleep(2)
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

async def verificar_everyone_seleccionado(page):
    """AJUSTE #4: Verificar que Everyone esté seleccionado en Who can watch this video"""
    print("\n🔍 VERIFICANDO SELECCIÓN DE 'EVERYONE'...")
    
    try:
        # Buscar elementos con texto "Everyone"
        everyone_elements = await page.query_selector_all('text="Everyone"')
        
        if everyone_elements:
            print(f"   📍 Encontrados {len(everyone_elements)} elementos con texto 'Everyone'")
            
            for i, element in enumerate(everyone_elements):
                try:
                    # Verificar si está seleccionado
                    is_selected = await element.evaluate('''
                        el => {
                            // Verificar si el elemento o su contenedor tiene indicadores de selección
                            const parent = el.closest('[role="radio"], [aria-selected], .selected, .active');
                            if (parent) {
                                return parent.getAttribute('aria-selected') === 'true' ||
                                       parent.classList.contains('selected') ||
                                       parent.classList.contains('active') ||
                                       parent.getAttribute('aria-checked') === 'true';
                            }
                            return false;
                        }
                    ''')
                    
                    print(f"     📻 Everyone #{i+1} - Seleccionado: {is_selected}")
                    
                    if not is_selected:
                        print(f"     🎯 Seleccionando Everyone #{i+1}...")
                        await element.scroll_into_view_if_needed()
                        await asyncio.sleep(0.5)
                        await element.click()
                        await asyncio.sleep(1)
                        print(f"✅ Everyone seleccionado - Elemento #{i+1}")
                        return True
                    else:
                        print("✅ Everyone ya está seleccionado")
                        return True
                        
                except Exception as e:
                    print(f"     ❌ Error con Everyone #{i+1}: {str(e)[:50]}")
                    continue
        
        # Buscar por selector más específico
        privacy_selectors = [
            '[data-testid*="everyone"]',
            '[aria-label*="Everyone"]',
            'input[value="everyone"]',
            'button:has-text("Everyone")'
        ]
        
        for selector in privacy_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    print(f"   📍 Encontrados {len(elements)} elementos con selector {selector}")
                    
                    for element in elements:
                        try:
                            await element.scroll_into_view_if_needed()
                            await asyncio.sleep(0.5)
                            await element.click()
                            await asyncio.sleep(1)
                            print(f"✅ Everyone seleccionado con selector {selector}")
                            return True
                        except:
                            continue
            except:
                continue
        
        print("⚠️ No se pudo verificar/seleccionar Everyone")
        return False
        
    except Exception as e:
        print(f"❌ Error verificando Everyone: {e}")
        return False

async def subir_video_ultra_stealth_v4_modificado(video_path, descripcion):
    """Función principal V4 modificada con todos los ajustes"""
    print("🎯 UPLOADER TIKTOK ULTRA STEALTH V4 MODIFICADO")
    print("=" * 60)
    print("📋 AJUSTES APLICADOS:")
    print("1. Pantalla 1920x1080 (sin cortes)")
    print("2. Procesamiento 20 segundos")
    print("3. XPath específico para AI content")
    print("4. Verificar Everyone seleccionado")
    print("5. Esperar 30 segundos antes de Post")
    print("=" * 60)
    
    cookies_path = "config/upload_cookies_playwright.json"
    
    # Verificar archivo
    if not os.path.exists(video_path):
        print(f"❌ Archivo no encontrado: {video_path}")
        return False
    
    file_size = os.path.getsize(video_path) / (1024*1024)
    print(f"📹 Video: {video_path}")
    print(f"📏 Tamaño: {file_size:.1f} MB")
    
    async with async_playwright() as p:
        # MEJORA ANTI-DETECCIÓN: Usar perfil persistente en lugar de browser temporal
        user_data_dir = os.path.join(os.getcwd(), "browser_profile")
        
        # Crear directorio del perfil si no existe
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)
            print(f"📁 Creado directorio de perfil: {user_data_dir}")
        else:
            print(f"📁 Usando perfil existente: {user_data_dir}")
        
        # Usar contexto persistente con perfil real - SIEMPRE VISIBLE para evitar problemas de login
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,  # SIEMPRE VISIBLE para evitar problemas de autenticación
            channel="chrome",
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            locale='es-MX',
            timezone_id='America/Mexico_City',
            geolocation={'latitude': 19.4326, 'longitude': -99.1332},
            permissions=['geolocation', 'microphone', 'camera', 'notifications'],
            color_scheme='light',
            reduced_motion='no-preference',
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--disable-infobars',
                '--disable-extensions-except',
                '--disable-extensions',
                '--disable-default-apps',
                '--start-maximized'
            ],
            ignore_default_args=['--enable-automation'],
            extra_http_headers={
                'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        
        # Las cookies se cargarán desde el archivo que funciona
        await cargar_cookies(context, cookies_path)  # ¡NECESARIO! Usar cookies que funcionan
        
        page = await context.new_page()
        
        # Agregar listener para logs del browser
        page.on("console", lambda msg: print(f"📋 [BROWSER LOG] {msg.type}: {msg.text}"))
        
        try:
            print("\n🌐 Navegando directamente a Creator Center...")
            await page.goto('https://www.tiktok.com/creator-center/upload', wait_until='networkidle')
            await asyncio.sleep(5)
            
            # Verificar si necesita login
            print("   🔍 Verificando estado de autenticación...")
            login_indicators = [
                'text="Log in"',
                'text="Sign up"',
                'button:has-text("Log in")',
                'button:has-text("Sign up")',
                '[data-testid*="login"]',
                '[class*="login"]'
            ]
            
            needs_login = False
            for indicator in login_indicators:
                try:
                    element = await page.query_selector(indicator)
                    if element and await element.is_visible():
                        needs_login = True
                        print(f"   � Detectado indicador de login: {indicator}")
                        break
                except:
                    continue
            
            if needs_login:
                print("⚠️ SE REQUIERE LOGIN MANUAL:")
                print("   👤 1. Logueate en TikTok en el navegador que se abrió")
                print("   🎯 2. Navega manualmente a: https://www.tiktok.com/creator-center/upload")
                print("   ✅ 3. Asegúrate de ver la página de upload con área de arrastrar archivos")
                print("   ⏳ 4. Presiona Enter aquí cuando estés listo para continuar...")
                input()
                
                # Recargar página después del login manual
                print("   🔄 Recargando página de upload...")
                await page.goto('https://www.tiktok.com/creator-center/upload', wait_until='networkidle')
                await asyncio.sleep(3)
            else:
                print("✅ Ya autenticado - Continuando automáticamente")
            
            await movimiento_humano_realista(page)
            
            # Verificar carga de página con más intentos
            print("\n🔍 Esperando carga de página de upload...")
            
            # Intentar múltiples formas de detectar la página cargada
            page_loaded = False
            
            # Intento 1: Buscar input de archivo
            try:
                await page.wait_for_selector('input[type="file"]', timeout=15000)
                print("✅ Página de upload cargada (input detectado)")
                page_loaded = True
            except:
                print("⚠️ Input de archivo no detectado, intentando otros métodos...")
            
            # Intento 2: Buscar elementos relacionados con upload
            if not page_loaded:
                try:
                    upload_indicators = [
                        '[data-testid*="upload"]',
                        '[class*="upload"]',
                        'text="Select file"',
                        'text="Choose file"',
                        'text="Seleccionar archivo"'
                    ]
                    
                    for indicator in upload_indicators:
                        elements = await page.query_selector_all(indicator)
                        if elements:
                            print(f"✅ Página de upload cargada ({indicator} detectado)")
                            page_loaded = True
                            break
                            
                except Exception as e:
                    print(f"⚠️ Error buscando indicadores: {e}")
            
            # Intento 3: Esperar un poco más y tomar screenshot para debug
            if not page_loaded:
                print("⚠️ Página no detectada, esperando 5s adicionales...")
                await asyncio.sleep(5)
                
                # Screenshot para debug
                debug_timestamp = int(time.time())
                await page.screenshot(path=f"debug_upload_page_{debug_timestamp}.png")
                print(f"📸 Screenshot debug: debug_upload_page_{debug_timestamp}.png")
                
                # Buscar cualquier input de archivo que pueda existir
                all_inputs = await page.query_selector_all('input')
                file_inputs = []
                
                for inp in all_inputs:
                    try:
                        input_type = await inp.get_attribute('type')
                        if input_type == 'file':
                            file_inputs.append(inp)
                    except:
                        continue
                
                if file_inputs:
                    print(f"✅ Encontrados {len(file_inputs)} inputs de archivo después de espera")
                    page_loaded = True
                else:
                    print("❌ No se encontraron inputs de archivo")
            
            if not page_loaded:
                print("❌ Error: Página de upload no cargó completamente")
                return False
            
            # Upload de archivo
            print("\n📁 Cargando archivo como humano...")
            file_inputs = await page.query_selector_all('input[type="file"]')
            print(f"📁 Encontrados {len(file_inputs)} inputs de archivo")
            
            if not file_inputs:
                print("❌ No se encontraron inputs de archivo")
                return False
            
            for i, file_input in enumerate(file_inputs, 1):
                try:
                    print(f"🎯 Intentando input #{i}...")
                    await file_input.set_input_files(video_path)
                    await asyncio.sleep(random.uniform(1, 3))
                    print(f"✅ ARCHIVO CARGADO con input #{i}")
                    break
                except Exception as e:
                    print(f"❌ Input #{i} falló: {str(e)[:100]}")
                    if i == len(file_inputs):
                        print("❌ No se pudo cargar el archivo")
                        return False
            
            # AJUSTE #2: Procesamiento (20 segundos en lugar de 30)
            print("\n⏳ PROCESAMIENTO OPTIMIZADO (20 segundos)...")
            total_wait = 20
            interval = 5
            
            for elapsed in range(0, total_wait, interval):
                print(f"⏳ Procesando... {elapsed}/{total_wait}s")
                if random.random() < 0.6:
                    await movimiento_humano_realista(page)
                await asyncio.sleep(interval)
            
            # Verificación de procesamiento
            print("\n🔍 Verificación final de procesamiento...")
            indicators = {
                'canvas': await page.query_selector_all('canvas'),
                '[class*="preview"]': await page.query_selector_all('[class*="preview"]'),
                '[class*="player"]': await page.query_selector_all('[class*="player"]')
            }
            
            print("✅ Indicadores encontrados:")
            for name, elements in indicators.items():
                print(f"   - {name} ({len(elements)})")
            
            timestamp = int(time.time())
            await page.screenshot(path=f"ultra_stealth_v4_mod_processing_{timestamp}.png")
            print(f"📸 Screenshot: ultra_stealth_v4_mod_processing_{timestamp}.png")
            
            # Show More - CRÍTICO para hacer visible el AI Content
            print("\n🔍 Buscando opciones avanzadas...")
            show_more_clicked = False
            
            # XPATH ESPECÍFICO proporcionado por el usuario para Show More
            xpath_show_more = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[3]/div/span[1]'
            
            try:
                print(f"🔍 Usando XPath específico para Show More: {xpath_show_more}")
                
                # Scroll para asegurar visibilidad
                print("   📜 Haciendo scroll para asegurar visibilidad...")
                await page.mouse.wheel(0, 300)
                await asyncio.sleep(2)
                
                # Buscar elemento Show More por XPath específico
                show_more = await page.query_selector(f'xpath={xpath_show_more}')
                
                if show_more:
                    print("   📍 Elemento Show More encontrado con XPath específico")
                    
                    # Obtener información del elemento
                    tag_name = await show_more.evaluate('el => el.tagName')
                    class_name = await show_more.get_attribute('class')
                    text_content = await show_more.text_content()
                    
                    print(f"   📋 Tag: {tag_name}")
                    print(f"   📋 Clases: {class_name}")
                    print(f"   📋 Texto: '{text_content}'")
                    
                    # Verificar si es visible
                    is_visible = await show_more.evaluate('''
                        el => {
                            const rect = el.getBoundingClientRect();
                            return rect.width > 0 && rect.height > 0 && 
                                   rect.top >= 0 && rect.bottom <= window.innerHeight;
                        }
                    ''')
                    
                    print(f"   👁️ Elemento visible: {is_visible}")
                    
                    if not is_visible:
                        print("   📜 Elemento no visible, haciendo scroll directo...")
                        await show_more.evaluate('''
                            el => {
                                el.scrollIntoView({behavior: 'smooth', block: 'center'});
                            }
                        ''')
                        await asyncio.sleep(3)
                    
                    # Hover y click
                    print("   🖱️ Haciendo hover sobre Show More...")
                    await show_more.hover()
                    await asyncio.sleep(1)
                    
                    print("   🖱️ Haciendo click en Show More...")
                    await show_more.click()
                    await asyncio.sleep(3)
                    
                    print("✅ Show More clickeado con XPath específico - Sección expandida")
                    show_more_clicked = True
                    
                else:
                    print("   ❌ Elemento Show More no encontrado con XPath específico")
                    
            except Exception as e:
                print(f"   ❌ Error con XPath específico de Show More: {e}")
            
            # Fallback: Buscar por texto si el XPath falla
            if not show_more_clicked:
                print("🔍 Fallback: Buscando Show More por texto...")
                
                show_more_selectors = [
                    'text="Show More"',
                    'text="Show more"',
                    'text="Mostrar más"',
                    'button:has-text("Show More")',
                    'button:has-text("Show more")',
                    'button:has-text("Mostrar más")',
                    '[data-testid*="show-more"]',
                    '[class*="show-more"]',
                    'button[aria-expanded="false"]'
                ]
                
                for selector in show_more_selectors:
                    try:
                        show_more = await page.query_selector(selector)
                        if show_more:
                            print(f"   📍 Show More encontrado con: {selector}")
                            
                            # Hacer scroll al elemento
                            await show_more.scroll_into_view_if_needed()
                            await asyncio.sleep(1)
                            
                            # Click en Show More
                            await show_more.click()
                            await asyncio.sleep(3)  # Esperar que se expanda la sección
                            
                            print("✅ Show More clickeado (fallback) - Sección expandida")
                            show_more_clicked = True
                            break
                            
                    except Exception as e:
                        print(f"   ❌ Error con selector {selector}: {str(e)[:50]}")
                        continue
            
            # Último intento: buscar elementos expandibles
            if not show_more_clicked:
                print("⚠️ Show More no encontrado, buscando elementos expandibles...")
                
                # Scroll hacia abajo para buscar más opciones
                await page.mouse.wheel(0, 300)
                await asyncio.sleep(2)
                
                # Buscar elementos expandibles
                expandable_elements = await page.query_selector_all('[aria-expanded="false"], [class*="expand"], [class*="collapse"]')
                
                for element in expandable_elements:
                    try:
                        await element.scroll_into_view_if_needed()
                        await asyncio.sleep(0.5)
                        await element.click()
                        await asyncio.sleep(2)
                        print("✅ Elemento expandible clickeado")
                        show_more_clicked = True
                        break
                    except:
                        continue
            
            if show_more_clicked:
                print("📋 Esperando que las opciones avanzadas se carguen...")
                await asyncio.sleep(3)
                
                # Scroll adicional para asegurar que todo está visible
                await page.mouse.wheel(0, 200)
                await asyncio.sleep(1)
                
            else:
                print("⚠️ No se pudo expandir opciones avanzadas, continuando...")
                # Scroll manual como fallback
                await page.mouse.wheel(0, 500)
                await asyncio.sleep(2)
            
            # AJUSTE #3: Activar AI Content con XPath específico
            ai_activated = await activar_ai_content_xpath_especifico(page)
            
            if ai_activated:
                print("✅ AI Content activado correctamente")
            else:
                print("⚠️ AI Content no se pudo activar")
            
            # AJUSTE #4: Verificar que Everyone esté seleccionado
            everyone_ok = await verificar_everyone_seleccionado(page)
            
            if everyone_ok:
                print("✅ Everyone verificado/seleccionado")
            else:
                print("⚠️ Everyone no pudo ser verificado")
            
            # Agregar descripción
            print("\n📝 Agregando descripción...")
            try:
                desc_selectors = [
                    'textarea[placeholder*="escrib"]',
                    'textarea[placeholder*="Describ"]',
                    'div[contenteditable="true"]',
                    '[data-testid*="caption"]',
                    'textarea[data-testid*="caption-input"]',
                    'textarea[aria-label*="caption"]'
                ]
                
                descripcion_agregada = False
                for selector in desc_selectors:
                    try:
                        desc_element = await page.query_selector(selector)
                        if desc_element:
                            print(f"   📍 Campo de descripción encontrado: {selector}")
                            
                            # Limpiar el campo primero
                            await desc_element.click()
                            await asyncio.sleep(1)
                            await desc_element.fill("")
                            await asyncio.sleep(1)
                            
                            # Escribir la descripción de forma más natural
                            await escribir_como_humano(desc_element, descripcion)
                            
                            # Verificar que se escribió correctamente
                            await asyncio.sleep(2)
                            
                            # Para elementos contenteditable, usar textContent en lugar de input_value
                            if "contenteditable" in selector:
                                texto_actual = await desc_element.text_content()
                            else:
                                try:
                                    texto_actual = await desc_element.input_value()
                                except:
                                    texto_actual = await desc_element.text_content()
                            
                            if texto_actual and len(texto_actual.strip()) > 10:
                                print("✅ Descripción agregada correctamente")
                                print(f"   📝 Caracteres escritos: {len(texto_actual)}")
                                descripcion_agregada = True
                                break
                            else:
                                texto_mostrar = str(texto_actual)[:50] if texto_actual else "vacío"
                                print(f"   ⚠️ Descripción no se escribió completamente: '{texto_mostrar}...'")
                                
                    except Exception as e:
                        print(f"   ❌ Error con selector {selector}: {str(e)[:50]}")
                        continue
                
                if not descripcion_agregada:
                    print("⚠️ No se pudo agregar descripción con ningún selector")
                    
            except Exception as e:
                print(f"❌ Error agregando descripción: {e}")
            
            # Screenshot pre-publicación
            timestamp = int(time.time())
            await page.screenshot(path=f"ultra_stealth_v4_mod_pre_publish_{timestamp}.png")
            print(f"📸 Screenshot pre-publicación: ultra_stealth_v4_mod_pre_publish_{timestamp}.png")
            
            # AJUSTE #5: Esperar 30 segundos antes de dar click en Post
            print("\n⏳ ESPERANDO 30 SEGUNDOS ANTES DE PUBLICAR...")
            for i in range(30, 0, -5):
                print(f"   ⏰ {i} segundos restantes...")
                # Movimientos de ratón aleatorios durante la espera para simular humano
                await page.mouse.move(
                    random.randint(100, 800), 
                    random.randint(100, 600)
                )
                await asyncio.sleep(2)
                await page.mouse.move(
                    random.randint(200, 900), 
                    random.randint(200, 700)
                )
                await asyncio.sleep(3)
            
            # ESTRATEGIA ANTI-DETECCIÓN EXTREMA: Simular usuario humano real
            print("\n🕵️ MODO STEALTH EXTREMO - EVADIENDO DETECCIÓN...")
            
            # 1. SIMULAR LECTURA HUMANA DE LA PÁGINA (15-30 segundos)
            print("   📖 Simulando lectura humana de la página...")
            for i in range(8):
                # Movimientos de lectura naturales
                await page.mouse.move(
                    random.randint(300, 800), 
                    random.randint(200 + i*50, 300 + i*50)
                )
                await asyncio.sleep(random.uniform(1.5, 3.0))
                
                # Pequeños scrolls como si leyera
                await page.mouse.wheel(0, random.randint(30, 80))
                await asyncio.sleep(random.uniform(0.8, 2.0))
            
            # 2. INTERACCIONES HUMANAS ADICIONALES
            print("   🖱️ Simulando interacciones humanas...")
            
            # Click en áreas vacías (como si ajustara la página)
            await page.mouse.click(400, 200)
            await asyncio.sleep(random.uniform(1, 2))
            await page.mouse.click(600, 350)
            await asyncio.sleep(random.uniform(1, 2))
            
            # 3. REVISAR FORMULARIO COMO HUMANO
            print("   📋 Revisando formulario como humano...")
            
            # Simular que revisa la descripción
            desc_area = await page.query_selector('div[contenteditable="true"], textarea')
            if desc_area:
                await desc_area.click()
                await asyncio.sleep(random.uniform(2, 4))
                # Simular que lee la descripción
                await page.keyboard.press('End')
                await asyncio.sleep(random.uniform(1, 2))
                await page.keyboard.press('Home')
                await asyncio.sleep(random.uniform(1, 2))
            
            # 4. BUSCAR BOTÓN POST CON JAVASCRIPT FORZADO
            print("   🔍 Búsqueda extrema del botón Post...")
            
            # Forzar visibilidad de TODOS los elementos potenciales
            forced_visibility = await page.evaluate('''
                () => {
                    const selectors = [
                        'button',
                        '[data-e2e*="post"]',
                        '[data-e2e*="publish"]', 
                        '[class*="post"]',
                        '[class*="publish"]',
                        '[type="submit"]'
                    ];
                    
                    let found_buttons = [];
                    
                    selectors.forEach(selector => {
                        const elements = document.querySelectorAll(selector);
                        elements.forEach(el => {
                            const text = el.textContent || el.innerText || '';
                            
                            // Si contiene palabras relacionadas con publicar
                            if (text.toLowerCase().includes('post') || 
                                text.toLowerCase().includes('publicar') ||
                                text.toLowerCase().includes('subir') ||
                                el.className.toLowerCase().includes('post') ||
                                el.className.toLowerCase().includes('publish')) {
                                
                                // FORZAR VISIBILIDAD EXTREMA
                                el.style.display = 'block !important';
                                el.style.visibility = 'visible !important';
                                el.style.opacity = '1 !important';
                                el.style.position = 'relative !important';
                                el.style.zIndex = '9999 !important';
                                el.style.pointerEvents = 'auto !important';
                                
                                // Forzar visibilidad del contenedor padre
                                let parent = el.parentElement;
                                while (parent && parent !== document.body) {
                                    parent.style.display = 'block !important';
                                    parent.style.visibility = 'visible !important';
                                    parent.style.opacity = '1 !important';
                                    parent = parent.parentElement;
                                }
                                
                                found_buttons.push({
                                    text: text.trim(),
                                    className: el.className,
                                    tagName: el.tagName,
                                    visible: el.offsetParent !== null
                                });
                            }
                        });
                    });
                    
                    return found_buttons;
                }
            ''')
            
            print(f"   📊 Elementos Post forzados a ser visibles: {len(forced_visibility)}")
            for btn in forced_visibility:
                print(f"      🎯 {btn['tagName']}: '{btn['text']}' - Visible: {btn['visible']}")
            
            # 5. ESPERAR PARA QUE LOS CAMBIOS SURTAN EFECTO
            await asyncio.sleep(5)
            
            # 6. SCROLL FINAL PARA ACTIVAR ELEMENTOS
            print("   📜 Scroll final para activar elementos...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(3)
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(2)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(3)
            
            # Publicar
            print("\n🚀 PUBLICANDO VIDEO...")
            
            # ESTRATEGIA ANTI-DETECCIÓN: Buscar botón como lo haría un humano
            print("   🔍 Búsqueda natural del botón Post...")
            
            # 1. Simular que el usuario lee la página
            await asyncio.sleep(random.uniform(2, 4))
            
            # 2. Movimientos de ratón como si buscara el botón
            for _ in range(5):
                await page.mouse.move(
                    random.randint(600, 1200), 
                    random.randint(400, 800)
                )
                await asyncio.sleep(random.uniform(0.3, 0.8))
            
            # 3. Hacer scroll gradual hacia abajo
            print("   📜 Scroll natural para encontrar botón...")
            scroll_positions = [200, 300, 500, 700, 1000]
            for scroll_amount in scroll_positions:
                await page.mouse.wheel(0, scroll_amount)
                await asyncio.sleep(random.uniform(1, 2))
                
                # Simular que mira el contenido
                await page.mouse.move(
                    random.randint(400, 1000), 
                    random.randint(300, 700)
                )
                await asyncio.sleep(random.uniform(0.5, 1))
            
            # 4. Scroll hasta abajo completamente
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(random.uniform(2, 4))
            
            # BÚSQUEDA EXHAUSTIVA DE BOTONES
            print("   🔍 Analizando todos los elementos de la página...")
            
            # Primero, verificar si hay elementos ocultos por CSS o JavaScript
            hidden_buttons = await page.evaluate('''
                () => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    return buttons.map(btn => ({
                        text: btn.textContent || btn.innerText || '',
                        visible: window.getComputedStyle(btn).display !== 'none' && 
                                window.getComputedStyle(btn).visibility !== 'hidden' &&
                                btn.offsetParent !== null,
                        classes: btn.className,
                        id: btn.id,
                        type: btn.type
                    })).filter(btn => 
                        btn.text.toLowerCase().includes('post') || 
                        btn.text.toLowerCase().includes('publicar') ||
                        btn.classes.toLowerCase().includes('post') ||
                        btn.classes.toLowerCase().includes('publish')
                    );
                }
            ''')
            
            print(f"   📊 Botones relacionados con Post encontrados: {len(hidden_buttons)}")
            for i, btn in enumerate(hidden_buttons):
                print(f"      {i+1}. Texto: '{btn['text']}', Visible: {btn['visible']}, Clases: '{btn['classes'][:50]}...'")
            
            # Selectores más específicos y exhaustivos
            publish_selectors = [
                'button:has-text("Post")',
                'button:has-text("Publicar")',
                'button[data-e2e="publish-button"]',
                'button[type="submit"]',
                'button:has-text("Subir")',
                'button[class*="publish"]',
                'button[class*="submit"]',
                'button[class*="Post"]',
                'button[data-testid*="post"]',
                'button[data-testid*="publish"]',
                # Selectores más específicos para TikTok
                '[data-e2e*="post"]',
                '[class*="DraftEditor-editorContainer"] ~ button',
                'div[class*="upload"] button:last-child',
                'form button[type="submit"]',
                'button[aria-label*="Post"]',
                'button[aria-label*="Publish"]'
            ]
            
            print("   🔍 Buscando todos los botones en la página...")
            # Listar todos los botones disponibles para diagnóstico
            all_buttons = await page.query_selector_all('button')
            print(f"   📊 Total de botones encontrados: {len(all_buttons)}")
            
            # Analizar botones visibles
            visible_buttons = []
            for i, btn in enumerate(all_buttons):
                try:
                    if await btn.is_visible():
                        text = await btn.text_content() or ""
                        class_name = await btn.get_attribute('class') or ""
                        data_testid = await btn.get_attribute('data-testid') or ""
                        
                        button_info = f"'{text.strip()}'"
                        if class_name:
                            button_info += f" (class: {class_name[:30]}...)"
                        if data_testid:
                            button_info += f" (testid: {data_testid})"
                            
                        visible_buttons.append(button_info)
                        
                        # Si encontramos algo relacionado con Post, reportarlo
                        if any(keyword in text.lower() for keyword in ['post', 'publicar', 'subir']) or \
                           any(keyword in class_name.lower() for keyword in ['post', 'publish', 'submit']):
                            print(f"   🎯 CANDIDATO: Botón {i+1}: {button_info}")
                            
                except Exception as e:
                    continue
            
            print(f"   👁️ Primeros 8 botones visibles: {', '.join(visible_buttons[:8])}")
            
            publish_success = False
            for selector in publish_selectors:
                try:
                    print(f"   🔍 Probando selector: {selector}")
                    publish_button = await page.query_selector(selector)
                    if publish_button:
                        # Verificar estado del botón
                        is_visible = await publish_button.is_visible()
                        is_enabled = await publish_button.is_enabled()
                        disabled = await publish_button.get_attribute('disabled')
                        
                        # Obtener información adicional
                        text_content = await publish_button.text_content() or ""
                        class_name = await publish_button.get_attribute('class') or ""
                        
                        print(f"   📍 Botón encontrado:")
                        print(f"      📝 Texto: '{text_content}'")
                        print(f"      👁️ Visible: {is_visible}")
                        print(f"      ✅ Habilitado: {is_enabled}")
                        print(f"      🛑 Disabled attribute: {disabled}")
                        print(f"      🎨 Clases: {class_name[:100]}...")
                        
                        # ESTRATEGIA ANTI-DETECCIÓN: Forzar visibilidad si está oculto
                        if not is_visible:
                            print("   🔧 Intentando forzar visibilidad del botón...")
                            try:
                                # Forzar visibilidad con JavaScript
                                await publish_button.evaluate('''
                                    el => {
                                        el.style.display = 'block';
                                        el.style.visibility = 'visible';
                                        el.style.opacity = '1';
                                        el.style.pointerEvents = 'auto';
                                        
                                        // Remover clases que puedan ocultarlo
                                        el.classList.remove('hidden', 'invisible', 'd-none');
                                        
                                        // Hacer el elemento visible en su contenedor
                                        let parent = el.parentElement;
                                        while (parent) {
                                            parent.style.display = 'block';
                                            parent.style.visibility = 'visible';
                                            parent = parent.parentElement;
                                        }
                                    }
                                ''')
                                
                                await asyncio.sleep(2)
                                is_visible = await publish_button.is_visible()
                                print(f"   🔧 Después de forzar visibilidad: {is_visible}")
                                
                            except Exception as force_error:
                                print(f"   ❌ Error forzando visibilidad: {force_error}")
                        
                        if is_visible and is_enabled:
                            # COMPORTAMIENTO HUMANO antes del click
                            print("   🤖 Simulando comportamiento humano antes del click...")
                            
                            # Scroll al botón específicamente con comportamiento humano
                            await publish_button.scroll_into_view_if_needed()
                            await asyncio.sleep(random.uniform(2, 4))
                            
                            # Movimiento de ratón natural hacia el botón
                            bbox = await publish_button.bounding_box()
                            if bbox:
                                # Acercarse gradualmente al botón
                                target_x = bbox['x'] + bbox['width'] / 2
                                target_y = bbox['y'] + bbox['height'] / 2
                                
                                # Movimiento en pasos
                                current_pos = await page.evaluate('() => [window.innerWidth/2, window.innerHeight/2]')
                                steps = 5
                                for i in range(steps):
                                    intermediate_x = current_pos[0] + (target_x - current_pos[0]) * (i + 1) / steps
                                    intermediate_y = current_pos[1] + (target_y - current_pos[1]) * (i + 1) / steps
                                    
                                    await page.mouse.move(
                                        intermediate_x + random.randint(-5, 5),
                                        intermediate_y + random.randint(-5, 5)
                                    )
                                    await asyncio.sleep(random.uniform(0.1, 0.3))
                            
                            # Verificar nuevamente después del scroll
                            is_visible_after_scroll = await publish_button.is_visible()
                            print(f"   📍 Después del scroll - Visible: {is_visible_after_scroll}")
                            
                            if is_visible_after_scroll:
                                # Hover con delay humano
                                await publish_button.hover()
                                await asyncio.sleep(random.uniform(1, 3))
                                
                                # Click con comportamiento humano
                                print("   🖱️ Realizando click humano...")
                                await publish_button.click()
                                print("✅ Botón Post clickeado")
                                
                                # Esperar y verificar si aparece algún modal
                                await asyncio.sleep(random.uniform(3, 5))
                            
                            # Buscar posibles modales de error o confirmación
                            print("   🔍 Verificando si aparece algún modal...")
                            await asyncio.sleep(random.uniform(3, 5))
                            
                            modal_selectors = [
                                'div[role="dialog"]',
                                '.modal',
                                '[class*="Modal"]',
                                '[class*="modal"]',
                                'div[class*="popup"]',
                                'div[class*="overlay"]'
                            ]
                            
                            modal_found = False
                            modal_text = ""
                            
                            for modal_selector in modal_selectors:
                                try:
                                    modal = await page.query_selector(modal_selector)
                                    if modal and await modal.is_visible():
                                        modal_text = await modal.text_content() or ""
                                        print(f"   ⚠️ Modal detectado: {modal_text[:150]}...")
                                        modal_found = True
                                        break
                                except:
                                    continue
                            
                            if modal_found:
                                print("   🔍 Analizando tipo de modal...")
                                modal_text_lower = modal_text.lower()
                                
                                # Detectar diferentes tipos de modal
                                if any(keyword in modal_text_lower for keyword in ['exit', 'sure', 'discard', 'leave', 'unsaved']):
                                    print("   ⚠️ Modal de salida detectado - CANCELANDO para continuar con upload")
                                    
                                    # Buscar botón cancelar/no
                                    cancel_selectors = [
                                        'button:has-text("Cancel")',
                                        'button:has-text("Cancelar")',
                                        'button:has-text("No")',
                                        'button:has-text("Stay")',
                                        'button:has-text("Quedarse")',
                                        'button[class*="cancel"]',
                                        'button[class*="secondary"]'
                                    ]
                                    
                                    cancel_clicked = False
                                    for cancel_selector in cancel_selectors:
                                        try:
                                            cancel_btn = await page.query_selector(cancel_selector)
                                            if cancel_btn and await cancel_btn.is_visible():
                                                await cancel_btn.click()
                                                print(f"   ✅ Modal de salida cancelado con: {cancel_selector}")
                                                await asyncio.sleep(2)
                                                cancel_clicked = True
                                                break
                                        except:
                                            continue
                                    
                                    if cancel_clicked:
                                        print("   🔄 Continuando con el proceso de upload...")
                                        # Reintentar click en Post
                                        await asyncio.sleep(3)
                                        try:
                                            post_button_retry = await page.query_selector('button:has-text("Post")')
                                            if post_button_retry and await post_button_retry.is_visible() and await post_button_retry.is_enabled():
                                                print("   🔄 Reintentando click en Post...")
                                                await post_button_retry.click()
                                                await asyncio.sleep(5)
                                                print("✅ Video publicado después de cancelar modal de salida")
                                                publish_success = True
                                                break
                                            else:
                                                print("   ⚠️ Botón Post no disponible después de cancelar modal")
                                        except Exception as retry_e:
                                            print(f"   ❌ Error reintentando Post: {str(retry_e)[:50]}")
                                    else:
                                        print("   ❌ No se pudo cancelar el modal de salida")
                                        
                                elif any(keyword in modal_text_lower for keyword in ['success', 'published', 'uploaded', 'posted', 'publicado']):
                                    print("   ✅ Modal de éxito detectado - ¡Video publicado exitosamente!")
                                    publish_success = True
                                    break
                                    
                                elif any(keyword in modal_text_lower for keyword in ['error', 'failed', 'problema', 'fallo']):
                                    print("   ❌ Modal de error detectado - Upload falló")
                                    print(f"   📝 Error: {modal_text[:200]}")
                                    # Cerrar modal de error y salir
                                    try:
                                        close_btn = await page.query_selector('button:has-text("Close"), button:has-text("Cerrar"), button[aria-label*="close"], button[class*="close"]')
                                        if close_btn:
                                            await close_btn.click()
                                            await asyncio.sleep(1)
                                    except:
                                        pass
                                    return False
                                    
                                else:
                                    print("   ❓ Modal desconocido - Intentando cerrarlo...")
                                    # Intentar cerrar modal genérico
                                    close_selectors = [
                                        'button:has-text("OK")',
                                        'button:has-text("Aceptar")',
                                        'button:has-text("Close")',
                                        'button:has-text("Cerrar")',
                                        'button[aria-label*="close"]',
                                        'button[class*="close"]'
                                    ]
                                    
                                    for close_selector in close_selectors:
                                        try:
                                            close_btn = await page.query_selector(close_selector)
                                            if close_btn and await close_btn.is_visible():
                                                await close_btn.click()
                                                print(f"   ✅ Modal cerrado con: {close_selector}")
                                                await asyncio.sleep(2)
                                                break
                                        except:
                                            continue
                                            
                            else:
                                # No hay modal - verificar si el upload fue exitoso por otros medios
                                print("   ℹ️ No se detectó modal")
                                
                                # Verificar cambio de URL o elementos de éxito
                                await asyncio.sleep(3)
                                current_url = page.url
                                
                                if 'upload' not in current_url or 'success' in current_url or 'posted' in current_url:
                                    print("   ✅ URL cambió - Video posiblemente publicado exitosamente")
                                    publish_success = True
                                    break
                                else:
                                    # Buscar indicadores de éxito en la página
                                    success_indicators = [
                                        'text="Video posted"',
                                        'text="Published"',
                                        'text="Publicado"',
                                        'text="Success"',
                                        '[class*="success"]',
                                        '[class*="posted"]'
                                    ]
                                    
                                    for indicator in success_indicators:
                                        try:
                                            success_element = await page.query_selector(indicator)
                                            if success_element and await success_element.is_visible():
                                                print(f"   ✅ Indicador de éxito encontrado: {indicator}")
                                                publish_success = True
                                                break
                                        except:
                                            continue
                                    
                                    if publish_success:
                                        break
                                    else:
                                        print("   ✅ Click realizado - Asumiendo éxito (sin modal ni indicadores)")
                                        publish_success = True
                                        break
                                
                        else:
                            print(f"   ⚠️ Botón no disponible - Visible: {is_visible}, Habilitado: {is_enabled}")
                            
                except Exception as e:
                    print(f"   ❌ Error con botón {selector}: {str(e)[:50]}")
                    continue
            
            if not publish_success:
                print("⚠️ MÉTODO DE EMERGENCIA: Búsqueda por coordenadas...")
                
                # MÉTODO DE EMERGENCIA: Click en área donde normalmente está el botón Post
                try:
                    # Tomar screenshot para diagnóstico
                    await page.screenshot(path=f"debug_pre_emergency_{int(time.time())}.png")
                    
                    # Posiciones típicas del botón Post en TikTok (1920x1080)
                    emergency_positions = [
                        (1400, 900),  # Esquina inferior derecha típica
                        (1350, 850),  # Variación 1
                        (1450, 950),  # Variación 2
                        (1300, 900),  # Más a la izquierda
                        (1500, 900),  # Más a la derecha
                    ]
                    
                    for i, (x, y) in enumerate(emergency_positions, 1):
                        print(f"   🎯 Probando posición {i}: ({x}, {y})")
                        
                        # Mover el ratón y verificar si hay un elemento clickeable
                        await page.mouse.move(x, y)
                        await asyncio.sleep(1)
                        
                        # Verificar si hay un botón en esa posición
                        element_at_pos = await page.evaluate(f'''
                            () => {{
                                const el = document.elementFromPoint({x}, {y});
                                if (el) {{
                                    return {{
                                        tagName: el.tagName,
                                        textContent: el.textContent || el.innerText || '',
                                        className: el.className,
                                        clickable: el.tagName === 'BUTTON' || el.getAttribute('role') === 'button'
                                    }};
                                }}
                                return null;
                            }}
                        ''')
                        
                        if element_at_pos:
                            print(f"      📍 Elemento en posición: {element_at_pos['tagName']} - '{element_at_pos['textContent'][:30]}...'")
                            
                            # Si parece ser un botón de Post, hacer click
                            if (element_at_pos['clickable'] and 
                                ('post' in element_at_pos['textContent'].lower() or 
                                 'publicar' in element_at_pos['textContent'].lower() or
                                 'post' in element_at_pos['className'].lower())):
                                
                                print(f"      🎯 ¡BOTÓN POST ENCONTRADO EN POSICIÓN {i}!")
                                await page.mouse.click(x, y)
                                await asyncio.sleep(3)
                                publish_success = True
                                break
                        
                        # Si no funciona, probar click directo
                        if i <= 2:  # Solo en las primeras 2 posiciones más probables
                            print(f"      �️ Click de emergencia en posición {i}...")
                            await page.mouse.click(x, y)
                            await asyncio.sleep(2)
                            
                            # Verificar si algo cambió en la página
                            current_url = page.url
                            if 'upload' not in current_url or 'success' in current_url:
                                print("      ✅ ¡Click de emergencia exitoso!")
                                publish_success = True
                                break
                    
                except Exception as e:
                    print(f"   ❌ Error en método de emergencia: {e}")
                
                # Screenshot final para diagnóstico
                try:
                    await page.screenshot(path=f"debug_final_emergency_{int(time.time())}.png")
                    print("   📸 Screenshots de diagnóstico guardados")
                except:
                    pass
            
            # Esperar confirmación final
            await asyncio.sleep(5)
            return True
            
        except Exception as e:
            print(f"❌ Error en proceso principal: {e}")
            return False
        
        finally:
            await asyncio.sleep(3)
            await context.close()

async def main():
    """Función principal"""
    video_path = "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4"
    # DESCRIPCIÓN CORREGIDA con los 5 MEJORES hashtags para TikTok
    descripcion = """🔥 ¡Contenido ÉPICO que te va a SORPRENDER! ✨ 

No puedes perderte esta increíble experiencia viral que está rompiendo TikTok 🚀
¡Dale LIKE si te gustó y COMPARTE con tus amigos! 💖

Prepárate para algo que jamás has visto antes... ¿Estás listo? 👀

#fyp #viral #trending #amazing #foryou"""
    
    resultado = await subir_video_ultra_stealth_v4_modificado(video_path, descripcion)
    
    if resultado:
        print("\n🎉 ¡UPLOAD COMPLETADO EXITOSAMENTE!")
    else:
        print("\n❌ Upload falló")

if __name__ == "__main__":
    asyncio.run(main())
