#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - ANTI-DETECCIÓN EXTREMA
Versión V5 con técnicas anti-detección más avanzadas para evadir bloqueos progresivos
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

async def setup_stealth_extreme(page):
    """Configuración anti-detección extrema"""
    print("🕵️ CONFIGURANDO ANTI-DETECCIÓN EXTREMA...")
    
    # Eliminar todas las propiedades de automation
    await page.add_init_script("""
        // Eliminar webdriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Eliminar automation
        delete window.chrome.runtime.onConnect;
        
        // Redefinir plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Redefinir languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['es-MX', 'es', 'en'],
        });
        
        // Eliminar propiedades de Playwright
        delete window.playwright;
        delete window.__playwright;
        delete window._playwright;
        
        // Redefinir permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // Ocultar automation flags
        Object.defineProperty(window, 'outerHeight', {
            get: () => 1040,
        });
        Object.defineProperty(window, 'outerWidth', {
            get: () => 1920,
        });
        
        // Simular comportamiento humano en eventos
        const originalAddEventListener = EventTarget.prototype.addEventListener;
        EventTarget.prototype.addEventListener = function(type, listener, options) {
            // Agregar delay humano a eventos críticos
            if (type === 'click' || type === 'input' || type === 'change') {
                const humanListener = function(event) {
                    setTimeout(() => listener.call(this, event), Math.random() * 10);
                };
                return originalAddEventListener.call(this, type, humanListener, options);
            }
            return originalAddEventListener.call(this, type, listener, options);
        };
        
        // Redefinir canvas fingerprinting
        const getContext = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function(type, attributes) {
            if (type === '2d') {
                const context = getContext.call(this, type, attributes);
                const originalFillText = context.fillText;
                context.fillText = function(text, x, y, maxWidth) {
                    // Agregar ruido al canvas
                    const noise = Math.random() * 0.0001;
                    return originalFillText.call(this, text, x + noise, y + noise, maxWidth);
                };
                return context;
            }
            return getContext.call(this, type, attributes);
        };
        
        // Simular timing humano
        const originalSetTimeout = window.setTimeout;
        window.setTimeout = function(callback, delay) {
            const humanDelay = delay + (Math.random() * 50 - 25); // ±25ms de variación
            return originalSetTimeout.call(this, callback, Math.max(0, humanDelay));
        };
        
        console.log('🛡️ Anti-detección extrema activada');
    """)

async def movimiento_humano_avanzado(page):
    """Movimientos de mouse ultra realistas"""
    # Patrones de movimiento humano reales
    patterns = [
        # Patrón de lectura
        [(300, 200), (800, 250), (400, 350), (900, 400)],
        # Patrón de navegación
        [(500, 300), (600, 400), (700, 350), (550, 500)],
        # Patrón de revisión
        [(200, 400), (1000, 450), (300, 600), (800, 550)]
    ]
    
    pattern = random.choice(patterns)
    
    for i, (x, y) in enumerate(pattern):
        # Agregar variación natural
        x_var = x + random.randint(-20, 20)
        y_var = y + random.randint(-20, 20)
        
        # Movimiento con curvas naturales
        await page.mouse.move(x_var, y_var, steps=random.randint(15, 25))
        await asyncio.sleep(random.uniform(0.3, 1.2))
        
        # Pausa ocasional como humano
        if random.random() < 0.3:
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
        # Scroll ocasional
        if random.random() < 0.4:
            await page.mouse.wheel(0, random.randint(-50, 50))
            await asyncio.sleep(random.uniform(0.2, 0.8))

async def escribir_ultra_humano(element, texto):
    """Escritura ultra humana con errores y correcciones"""
    await element.click()
    await asyncio.sleep(random.uniform(0.5, 1.5))
    
    # Limpiar campo
    await element.fill("")
    await asyncio.sleep(random.uniform(0.2, 0.6))
    
    # Escribir con patrones humanos reales
    i = 0
    while i < len(texto):
        char = texto[i]
        
        # Simular errores de tipeo ocasionales
        if random.random() < 0.03 and i > 0:  # 3% de errores
            # Escribir carácter incorrecto
            wrong_chars = 'abcdefghijklmnopqrstuvwxyz'
            wrong_char = random.choice(wrong_chars)
            await element.type(wrong_char)
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Detectar error y corregir
            await asyncio.sleep(random.uniform(0.2, 0.8))
            await element.press('Backspace')
            await asyncio.sleep(random.uniform(0.1, 0.4))
        
        # Escribir carácter correcto
        await element.type(char)
        
        # Timing natural según el tipo de carácter
        if char == ' ':
            await asyncio.sleep(random.uniform(0.1, 0.4))
        elif char in '.,!?':
            await asyncio.sleep(random.uniform(0.3, 0.8))
        elif char in '\n':
            await asyncio.sleep(random.uniform(0.2, 0.6))
        elif i > 0 and i % random.randint(5, 12) == 0:
            # Pausa de pensamiento
            await asyncio.sleep(random.uniform(0.2, 1.0))
        else:
            await asyncio.sleep(random.uniform(0.05, 0.2))
        
        i += 1

async def buscar_boton_post_extremo(page):
    """Búsqueda exhaustiva del botón Post con múltiples estrategias"""
    print("\n🔍 BÚSQUEDA EXTREMA DEL BOTÓN POST...")
    
    # Estrategia 1: Forzar carga completa de la página
    print("1️⃣ Forzando carga completa...")
    await page.evaluate("""
        // Forzar carga de todos los lazy elements
        window.dispatchEvent(new Event('load'));
        window.dispatchEvent(new Event('DOMContentLoaded'));
        
        // Trigger scroll events para lazy loading
        window.scrollTo(0, document.body.scrollHeight);
        window.scrollTo(0, 0);
        
        // Forzar render de elementos ocultos
        const hiddenElements = document.querySelectorAll('[style*="display: none"], [style*="visibility: hidden"]');
        hiddenElements.forEach(el => {
            el.style.display = 'block';
            el.style.visibility = 'visible';
        });
    """)
    await asyncio.sleep(3)
    
    # Estrategia 2: Buscar por múltiples métodos
    search_strategies = [
        # Texto directo
        'button:has-text("Post")',
        'button:has-text("Publicar")',
        'button:has-text("Share")',
        'button:has-text("Upload")',
        
        # Atributos específicos
        'button[data-e2e*="post"]',
        'button[data-e2e*="publish"]',
        'button[data-e2e*="share"]',
        'button[type="submit"]',
        
        # Clases comunes
        'button[class*="post"]',
        'button[class*="publish"]',
        'button[class*="submit"]',
        'button[class*="share"]',
        'button[class*="upload"]',
        
        # Aria labels
        'button[aria-label*="Post"]',
        'button[aria-label*="Publish"]',
        'button[aria-label*="Share"]',
        
        # Selectores específicos de TikTok
        '[data-testid*="post"]',
        '[data-testid*="publish"]',
        'div[role="button"]:has-text("Post")',
        
        # Formularios
        'form button:last-child',
        'form [type="submit"]',
        
        # Posición típica
        'div:last-child button',
        '.upload-container button:last-child'
    ]
    
    for i, strategy in enumerate(search_strategies, 1):
        try:
            print(f"2️⃣ Estrategia {i}: {strategy}")
            elements = await page.query_selector_all(strategy)
            
            for j, element in enumerate(elements):
                try:
                    text = await element.text_content() or ""
                    is_visible = await element.is_visible()
                    is_enabled = await element.is_enabled()
                    
                    if text.strip():
                        print(f"   📍 Elemento {j+1}: '{text[:30]}...' - Visible: {is_visible}, Enabled: {is_enabled}")
                    
                    # Si parece ser un botón de publicación
                    if (any(keyword in text.lower() for keyword in ['post', 'publish', 'publicar', 'share', 'upload']) or
                        any(keyword in strategy.lower() for keyword in ['post', 'publish', 'submit'])):
                        
                        if is_visible and is_enabled:
                            print(f"   🎯 ¡BOTÓN POST CANDIDATO ENCONTRADO!")
                            return element
                        elif not is_visible:
                            # Intentar hacer visible
                            print(f"   🔧 Intentando hacer visible...")
                            await element.evaluate("""
                                el => {
                                    el.style.display = 'block !important';
                                    el.style.visibility = 'visible !important';
                                    el.style.opacity = '1 !important';
                                    el.style.position = 'relative !important';
                                    el.style.zIndex = '9999 !important';
                                    
                                    // Hacer visible contenedores padre
                                    let parent = el.parentElement;
                                    while (parent && parent !== document.body) {
                                        parent.style.display = 'block !important';
                                        parent.style.visibility = 'visible !important';
                                        parent.style.opacity = '1 !important';
                                        parent = parent.parentElement;
                                    }
                                    
                                    // Remover atributos que oculten
                                    el.removeAttribute('hidden');
                                    el.removeAttribute('disabled');
                                    
                                    // Scroll al elemento
                                    el.scrollIntoView({behavior: 'smooth', block: 'center'});
                                }
                            """)
                            await asyncio.sleep(2)
                            
                            if await element.is_visible() and await element.is_enabled():
                                print(f"   ✅ ¡Elemento hecho visible y habilitado!")
                                return element
                
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"   ❌ Error con estrategia {i}: {str(e)[:50]}")
            continue
    
    # Estrategia 3: Búsqueda por coordenadas inteligente
    print("3️⃣ Búsqueda por coordenadas inteligente...")
    
    # Analizar la página para encontrar patrones de botones
    button_positions = await page.evaluate("""
        () => {
            const buttons = Array.from(document.querySelectorAll('button'));
            return buttons.map(btn => {
                const rect = btn.getBoundingClientRect();
                const text = btn.textContent || btn.innerText || '';
                const classes = btn.className;
                
                return {
                    x: rect.x + rect.width / 2,
                    y: rect.y + rect.height / 2,
                    width: rect.width,
                    height: rect.height,
                    text: text.trim(),
                    classes: classes,
                    visible: rect.width > 0 && rect.height > 0
                };
            }).filter(btn => btn.visible && btn.width > 50 && btn.height > 20);
        }
    """)
    
    # Buscar botones en posiciones típicas de "Post"
    post_positions = []
    for btn in button_positions:
        # Botones en la parte inferior derecha son candidatos
        if (btn['x'] > 1200 and btn['y'] > 600) or 'post' in btn['text'].lower():
            post_positions.append(btn)
            print(f"   🎯 Candidato por posición: '{btn['text'][:20]}...' en ({btn['x']:.0f}, {btn['y']:.0f})")
    
    # Probar click en el candidato más probable
    if post_positions:
        best_candidate = max(post_positions, key=lambda x: (
            'post' in x['text'].lower() * 100 +
            'publish' in x['text'].lower() * 100 +
            x['x'] * 0.1 +  # Preferir derecha
            x['y'] * 0.1    # Preferir abajo
        ))
        
        print(f"   🎯 Mejor candidato: '{best_candidate['text']}' en ({best_candidate['x']:.0f}, {best_candidate['y']:.0f})")
        
        try:
            await page.mouse.click(best_candidate['x'], best_candidate['y'])
            await asyncio.sleep(2)
            print("   ✅ Click por coordenadas ejecutado")
            return True
        except Exception as e:
            print(f"   ❌ Error en click por coordenadas: {e}")
    
    print("❌ No se pudo encontrar botón Post con ninguna estrategia")
    return None

async def subir_video_ultra_stealth_v5(video_path, descripcion):
    """Función principal V5 con anti-detección extrema"""
    print("🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - ANTI-DETECCIÓN EXTREMA")
    print("=" * 70)
    
    cookies_path = "config/upload_cookies_playwright.json"
    
    # Verificar archivo
    if not os.path.exists(video_path):
        print(f"❌ Archivo no encontrado: {video_path}")
        return False
    
    file_size = os.path.getsize(video_path) / (1024*1024)
    print(f"📹 Video: {video_path}")
    print(f"📏 Tamaño: {file_size:.1f} MB")
    
    async with async_playwright() as p:
        # Configuración anti-detección extrema
        user_data_dir = os.path.join(os.getcwd(), "browser_profile")
        
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)
            print(f"📁 Creado directorio de perfil: {user_data_dir}")
        
        # Contexto con máxima evasión
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            channel="chrome",
            viewport={'width': 1920, 'height': 1080},
            # User agent más reciente y común
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='es-MX',
            timezone_id='America/Mexico_City',
            geolocation={'latitude': 19.4326, 'longitude': -99.1332},
            permissions=['geolocation', 'microphone', 'camera', 'notifications'],
            color_scheme='light',
            reduced_motion='no-preference',
            # Args anti-detección máxima
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor,TranslateUI',
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--disable-infobars',
                '--disable-extensions',
                '--disable-default-apps',
                '--start-maximized',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-field-trial-config',
                '--disable-component-extensions-with-background-pages',
                '--disable-features=TranslateUI,BlinkGenPropertyTrees',
                '--enable-features=NetworkService,NetworkServiceLogging',
                '--force-device-scale-factor=1',
                '--aggressive-cache-discard',
                '--memory-pressure-off'
            ],
            ignore_default_args=['--enable-automation', '--enable-blink-features=IdleDetection'],
            extra_http_headers={
                'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8,en-US;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"'
            }
        )
        
        await cargar_cookies(context, cookies_path)
        page = await context.new_page()
        
        # Configurar anti-detección extrema
        await setup_stealth_extreme(page)
        
        try:
            print("\n🌐 Navegando con comportamiento humano extremo...")
            
            # Navegar de forma humana
            await page.goto('https://www.tiktok.com/', wait_until='networkidle')
            await asyncio.sleep(random.uniform(3, 6))
            await movimiento_humano_avanzado(page)
            
            # Navegar al creator center como humano
            print("🎯 Navegando a Creator Center...")
            await page.goto('https://www.tiktok.com/creator-center/upload', wait_until='networkidle')
            await asyncio.sleep(random.uniform(4, 8))
            await movimiento_humano_avanzado(page)
            
            # Verificar autenticación
            print("🔍 Verificando autenticación...")
            if await page.query_selector('text="Log in"'):
                print("❌ Requiere login manual")
                input("Presiona Enter después de loguearte...")
                await page.goto('https://www.tiktok.com/creator-center/upload', wait_until='networkidle')
                await asyncio.sleep(3)
            else:
                print("✅ Autenticado correctamente")
            
            # Esperar carga completa con comportamiento humano
            print("⏳ Esperando carga completa...")
            await asyncio.sleep(random.uniform(5, 10))
            await movimiento_humano_avanzado(page)
            
            # Buscar inputs de archivo con persistencia
            print("📁 Buscando inputs de archivo...")
            file_input = None
            attempts = 0
            max_attempts = 10
            
            while not file_input and attempts < max_attempts:
                file_inputs = await page.query_selector_all('input[type="file"]')
                if file_inputs:
                    file_input = file_inputs[0]
                    print(f"✅ Input de archivo encontrado (intento {attempts + 1})")
                    break
                
                attempts += 1
                print(f"⏳ Intento {attempts}/{max_attempts} - Esperando inputs...")
                await asyncio.sleep(2)
                await movimiento_humano_avanzado(page)
            
            if not file_input:
                print("❌ No se encontraron inputs de archivo")
                return False
            
            # Cargar archivo con comportamiento humano
            print("📤 Cargando archivo...")
            await movimiento_humano_avanzado(page)
            await file_input.set_input_files(video_path)
            await asyncio.sleep(random.uniform(2, 4))
            print("✅ Archivo cargado")
            
            # Esperar procesamiento con actividad humana
            print("⏳ Esperando procesamiento (con actividad humana)...")
            processing_time = 30
            for i in range(0, processing_time, 5):
                print(f"   Procesando... {i}/{processing_time}s")
                await movimiento_humano_avanzado(page)
                await asyncio.sleep(5)
            
            # Verificar que cargó correctamente
            preview_elements = await page.query_selector_all('canvas, video, [class*="preview"]')
            print(f"🎬 Elementos de preview: {len(preview_elements)}")
            
            if len(preview_elements) == 0:
                print("⚠️ No se detectaron elementos de preview")
                # Continuar anyway
            
            # Agregar descripción con escritura humana
            print("📝 Agregando descripción...")
            desc_selectors = [
                'div[contenteditable="true"]',
                'textarea[placeholder*="escrib"]',
                'textarea[data-testid*="caption"]'
            ]
            
            desc_added = False
            for selector in desc_selectors:
                try:
                    desc_element = await page.query_selector(selector)
                    if desc_element and await desc_element.is_visible():
                        print(f"   📍 Campo encontrado: {selector}")
                        await movimiento_humano_avanzado(page)
                        await escribir_ultra_humano(desc_element, descripcion)
                        desc_added = True
                        break
                except Exception as e:
                    continue
            
            if desc_added:
                print("✅ Descripción agregada")
            else:
                print("⚠️ No se pudo agregar descripción")
            
            # Simular revisión humana del formulario
            print("👀 Simulando revisión humana del formulario...")
            await movimiento_humano_avanzado(page)
            await asyncio.sleep(random.uniform(10, 20))
            
            # Buscar y clickear botón Post con estrategias extremas
            post_button = await buscar_boton_post_extremo(page)
            
            if post_button:
                print("🚀 Publicando video...")
                
                # Comportamiento humano antes del click final
                await movimiento_humano_avanzado(page)
                await asyncio.sleep(random.uniform(3, 8))
                
                # Click con comportamiento humano
                await post_button.hover()
                await asyncio.sleep(random.uniform(1, 3))
                await post_button.click()
                
                print("✅ Video publicado exitosamente")
                await asyncio.sleep(10)
                return True
            else:
                print("❌ No se pudo encontrar el botón Post")
                return False
            
        except Exception as e:
            print(f"❌ Error en proceso: {e}")
            return False
        
        finally:
            await asyncio.sleep(5)
            await context.close()

async def main():
    """Función principal"""
    video_path = "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4"
    descripcion = """🔥 ¡Contenido ÉPICO que te va a SORPRENDER! ✨ 

No puedes perderte esta increíble experiencia viral que está rompiendo TikTok 🚀
¡Dale LIKE si te gustó y COMPARTE con tus amigos! 💖

Prepárate para algo que jamás has visto antes... ¿Estás listo? 👀

#fyp #viral #trending #amazing #foryou"""
    
    resultado = await subir_video_ultra_stealth_v5(video_path, descripcion)
    
    if resultado:
        print("\n🎉 ¡UPLOAD COMPLETADO EXITOSAMENTE!")
    else:
        print("\n❌ Upload falló")

if __name__ == "__main__":
    asyncio.run(main())
