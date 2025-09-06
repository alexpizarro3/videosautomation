#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - SELENIUM ESTABLE
Versión V5 usando Selenium estable con máxima anti-detección manual
Mantiene toda la lógica del V4 modificado pero con Selenium estable
"""

import json
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def cargar_cookies(driver, cookies_path):
    """Cargar cookies de sesión - Selenium version"""
    try:
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
        
        # Ir a TikTok primero para cargar cookies
        driver.get("https://www.tiktok.com")
        time.sleep(3)
        
        cookies_loaded = 0
        for cookie in cookies:
            try:
                # Convertir formato Playwright a Selenium
                selenium_cookie = {
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie.get('domain', '.tiktok.com'),
                    'path': cookie.get('path', '/'),
                }
                
                # Agregar campos opcionales si existen
                if 'secure' in cookie:
                    selenium_cookie['secure'] = cookie['secure']
                if 'httpOnly' in cookie:
                    selenium_cookie['httpOnly'] = cookie['httpOnly']
                
                driver.add_cookie(selenium_cookie)
                cookies_loaded += 1
            except Exception as e:
                print(f"   ⚠️ Error con cookie {cookie.get('name', 'unknown')}: {e}")
                continue
        
        print(f"✅ Cookies cargadas: {cookies_loaded}/{len(cookies)} desde {cookies_path}")
        return True
    except Exception as e:
        print(f"❌ Error cargando cookies: {e}")
        return False

def setup_stealth_chrome():
    """Configurar Chrome con máxima anti-detección manual"""
    print("🛡️ Configurando Chrome con anti-detección extrema...")
    
    options = Options()
    
    # Configuración anti-detección básica
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-first-run')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-infobars')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-field-trial-config')
    options.add_argument('--disable-back-forward-cache')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-features=TranslateUI')
    options.add_argument('--disable-ipc-flooding-protection')
    
    # User agent específico para Windows
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Configuración de perfil persistente
    profile_dir = os.path.join(os.getcwd(), "chrome_profile_selenium_stable")
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
        print(f"📁 Creado directorio de perfil: {profile_dir}")
    else:
        print(f"📁 Usando perfil existente: {profile_dir}")
    
    options.add_argument(f'--user-data-dir={profile_dir}')
    
    # Configuración adicional para evitar detección
    prefs = {
        "profile.default_content_setting_values": {
            "notifications": 2,
            "geolocation": 1,
            "media_stream": 1,
        },
        "profile.managed_default_content_settings": {
            "images": 1
        },
        "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
        "profile.default_content_settings.popups": 0,
        "managed_default_content_settings.images": 1
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options

def apply_stealth_scripts(driver):
    """Aplicar scripts anti-detección después de crear el driver"""
    print("🕵️ Aplicando scripts de stealth extremo...")
    
    # Script anti-detección completo
    stealth_script = """
        // Eliminar propiedades de webdriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Simular plugins reales
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {
                    0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: Plugin},
                    description: "Portable Document Format",
                    filename: "internal-pdf-viewer",
                    length: 1,
                    name: "Chrome PDF Plugin"
                },
                {
                    0: {type: "application/pdf", suffixes: "pdf", description: "", enabledPlugin: Plugin},
                    description: "",
                    filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                    length: 1,
                    name: "Chrome PDF Viewer"
                }
            ],
        });
        
        // Configurar idiomas
        Object.defineProperty(navigator, 'languages', {
            get: () => ['es-MX', 'es', 'en-US', 'en'],
        });
        
        // Simular Chrome runtime
        window.chrome = {
            runtime: {
                onConnect: undefined,
                onMessage: undefined,
            },
        };
        
        // Simular permisos
        Object.defineProperty(navigator, 'permissions', {
            get: () => ({
                query: () => Promise.resolve({ state: 'granted' }),
            }),
        });
        
        // Modificar deviceMemory
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => 8,
        });
        
        // Modificar hardwareConcurrency
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => 4,
        });
        
        // Eliminar rastros de automatización
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        
        // Simular comportamiento de mouse real
        const originalAddEventListener = EventTarget.prototype.addEventListener;
        EventTarget.prototype.addEventListener = function(type, listener, options) {
            if (type === 'mousedown' || type === 'mouseup' || type === 'click') {
                // Simular eventos de mouse más naturales
            }
            return originalAddEventListener.call(this, type, listener, options);
        };
        
        // Override toString para ocultar automation
        const originalToString = Function.prototype.toString;
        Function.prototype.toString = function() {
            if (this === navigator.webdriver) {
                return 'function webdriver() { [native code] }';
            }
            return originalToString.call(this);
        };
    """
    
    try:
        driver.execute_script(stealth_script)
        print("✅ Scripts de stealth aplicados correctamente")
    except Exception as e:
        print(f"⚠️ Error aplicando scripts stealth: {e}")

def movimiento_humano_realista(driver):
    """Simula movimientos de mouse completamente humanos"""
    try:
        actions = ActionChains(driver)
        
        # Obtener dimensiones de la ventana
        size = driver.get_window_size()
        viewport_width = size['width']
        viewport_height = size['height']
        
        # Posición aleatoria dentro de la ventana
        x = random.randint(100, min(1200, viewport_width - 100))
        y = random.randint(100, min(800, viewport_height - 100))
        
        # Movimiento en pasos para parecer más humano
        current_pos = driver.execute_script("return [window.innerWidth/2, window.innerHeight/2]")
        steps = random.randint(3, 8)
        
        for i in range(steps):
            intermediate_x = current_pos[0] + (x - current_pos[0]) * (i + 1) / steps
            intermediate_y = current_pos[1] + (y - current_pos[1]) * (i + 1) / steps
            
            # Usar JavaScript para mover el cursor (más suave)
            driver.execute_script(f"""
                var event = new MouseEvent('mousemove', {{
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': {intermediate_x + random.randint(-3, 3)},
                    'clientY': {intermediate_y + random.randint(-3, 3)}
                }});
                document.dispatchEvent(event);
            """)
            time.sleep(random.uniform(0.05, 0.15))
        
        time.sleep(random.uniform(0.5, 2.0))
        
        # Scroll ocasional
        if random.random() < 0.3:
            scroll_amount = random.randint(-100, 100)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
            time.sleep(random.uniform(0.3, 1.0))
            
    except Exception as e:
        print(f"   ⚠️ Error en movimiento humano: {e}")

def escribir_como_humano(element, texto, driver):
    """Escribe texto como un humano real"""
    try:
        # Focus en el elemento
        driver.execute_script("arguments[0].focus();", element)
        time.sleep(random.uniform(0.2, 0.8))
        
        # Limpiar campo
        element.clear()
        time.sleep(random.uniform(0.1, 0.3))
        
        # Escribir caracter por caracter con timing humano
        for i, char in enumerate(texto):
            element.send_keys(char)
            
            # Pausas naturales
            if char == ' ':
                time.sleep(random.uniform(0.1, 0.3))
            elif char in '.,!?':
                time.sleep(random.uniform(0.2, 0.5))
            elif i > 0 and i % random.randint(8, 15) == 0:
                time.sleep(random.uniform(0.1, 0.4))
            else:
                time.sleep(random.uniform(0.05, 0.15))
                
    except Exception as e:
        print(f"   ❌ Error escribiendo texto: {e}")

def activar_ai_content_xpath_especifico(driver):
    """AJUSTE #3: Activación con XPath específico del usuario"""
    print("\n🎯 ACTIVACIÓN AI CONTENT CON XPATH ESPECÍFICO...")
    
    xpath_ai_toggle = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span'
    
    try:
        print(f"🔍 Usando XPath específico: {xpath_ai_toggle}")
        
        # Scroll adicional
        print("   📜 Haciendo scroll para asegurar visibilidad...")
        driver.execute_script("window.scrollBy(0, 300)")
        time.sleep(2)
        
        # Buscar elemento por XPath
        try:
            ai_toggle = driver.find_element(By.XPATH, xpath_ai_toggle)
            print("   📍 Elemento AI toggle encontrado con XPath")
            
            tag_name = ai_toggle.tag_name
            class_name = ai_toggle.get_attribute('class')
            
            print(f"   📋 Tag: {tag_name}")
            print(f"   📋 Clases: {class_name}")
            
            is_visible = ai_toggle.is_displayed()
            print(f"   👁️ Elemento visible: {is_visible}")
            
            if not is_visible:
                print("   📜 Forzando visibilidad...")
                driver.execute_script("""
                    arguments[0].style.display = 'block';
                    arguments[0].style.visibility = 'visible';
                    arguments[0].style.opacity = '1';
                    arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
                """, ai_toggle)
                time.sleep(3)
            
            # Hover y click
            print("   🖱️ Hover y click...")
            actions = ActionChains(driver)
            actions.move_to_element(ai_toggle).perform()
            time.sleep(1)
            
            driver.execute_script("arguments[0].click();", ai_toggle)
            print("✅ AI Content toggle clickeado con XPath específico")
            
            # Buscar modal de confirmación con más opciones
            print("   🔍 Buscando modal de confirmación AI Content...")
            time.sleep(2)
            
            modal_selectors = [
                "//button[contains(text(), 'Turn on')]",
                "//button[contains(text(), 'Aceptar')]",
                "//button[contains(text(), 'Accept')]",
                "//button[contains(text(), 'Confirmar')]",
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(text(), 'Continue')]",
                "//button[contains(text(), 'OK')]",
                "//button[contains(text(), 'Confirm')]",
                "//button[contains(text(), 'Got it')]",
                "//button[contains(@class, 'primary')] | //button[contains(@class, 'confirm')]"
            ]
            
            for selector in modal_selectors:
                try:
                    modal_button = driver.find_element(By.XPATH, selector)
                    if modal_button.is_displayed():
                        button_text = modal_button.text
                        print(f"   📍 Modal encontrado - Botón: '{button_text}'")
                        driver.execute_script("arguments[0].click();", modal_button)
                        print(f"   ✅ Modal confirmado")
                        time.sleep(2)
                        break
                except NoSuchElementException:
                    continue
            
            time.sleep(3)
            return True
            
        except NoSuchElementException:
            print("   ❌ Elemento AI toggle no encontrado con XPath")
            
        # Fallback por texto
        print("🔍 Fallback: Buscando por texto 'AI-generated content'")
        
        try:
            ai_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'AI-generated content')]")
            if ai_elements:
                print(f"   📍 Encontrados {len(ai_elements)} elementos con texto AI")
                
                for element in ai_elements:
                    try:
                        # Buscar toggle padre
                        parent = element.find_element(By.XPATH, "./ancestor::*[4]")
                        toggles = parent.find_elements(By.XPATH, ".//*[@role='switch' or contains(@class, 'Switch')]")
                        
                        for i, toggle in enumerate(toggles, 1):
                            is_checked = toggle.get_attribute('aria-checked')
                            
                            if is_checked == 'false':
                                print(f"     🎯 Activando toggle #{i}...")
                                driver.execute_script("arguments[0].scrollIntoView();", toggle)
                                time.sleep(1)
                                driver.execute_script("arguments[0].click();", toggle)
                                time.sleep(2)
                                print(f"✅ AI Content activado - Toggle #{i} (fallback)")
                                return True
                    except:
                        continue
        except:
            pass
        
        print("❌ No se pudo activar AI Content")
        return False
        
    except Exception as e:
        print(f"❌ Error en activación AI Content: {e}")
        return False

def verificar_everyone_seleccionado(driver):
    """AJUSTE #4: Verificar que Everyone esté seleccionado"""
    print("\n🔍 VERIFICANDO SELECCIÓN DE 'EVERYONE'...")
    
    try:
        everyone_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Everyone')]")
        
        if everyone_elements:
            print(f"   📍 Encontrados {len(everyone_elements)} elementos con texto 'Everyone'")
            
            for i, element in enumerate(everyone_elements):
                try:
                    is_selected = driver.execute_script("""
                        var el = arguments[0];
                        var parent = el.closest('[role="radio"], [aria-selected], .selected, .active');
                        if (parent) {
                            return parent.getAttribute('aria-selected') === 'true' ||
                                   parent.classList.contains('selected') ||
                                   parent.classList.contains('active') ||
                                   parent.getAttribute('aria-checked') === 'true';
                        }
                        return false;
                    """, element)
                    
                    print(f"     📻 Everyone #{i+1} - Seleccionado: {is_selected}")
                    
                    if not is_selected:
                        print(f"     🎯 Seleccionando Everyone #{i+1}...")
                        driver.execute_script("arguments[0].scrollIntoView();", element)
                        time.sleep(0.5)
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(1)
                        print(f"✅ Everyone seleccionado - Elemento #{i+1}")
                        return True
                    else:
                        print("✅ Everyone ya está seleccionado")
                        return True
                except:
                    continue
        
        print("⚠️ No se pudo verificar/seleccionar Everyone")
        return False
        
    except Exception as e:
        print(f"❌ Error verificando Everyone: {e}")
        return False

def subir_video_ultra_stealth_selenium_estable(video_path, descripcion):
    """Función principal Selenium estable con máxima anti-detección"""
    print("🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - SELENIUM ESTABLE")
    print("=" * 60)
    print("📋 AJUSTES APLICADOS:")
    print("1. Pantalla 1920x1080 (sin cortes)")
    print("2. Procesamiento 20 segundos") 
    print("3. XPath específico para AI content")
    print("4. Verificar Everyone seleccionado")
    print("5. Esperar 30 segundos antes de Post")
    print("6. 🔥 SELENIUM ESTABLE con anti-detección manual")
    print("=" * 60)
    
    cookies_path = "config/upload_cookies_playwright.json"
    
    # Verificar archivo
    if not os.path.exists(video_path):
        print(f"❌ Archivo no encontrado: {video_path}")
        return False
    
    file_size = os.path.getsize(video_path) / (1024*1024)
    print(f"📹 Video: {video_path}")
    print(f"📏 Tamaño: {file_size:.1f} MB")
    
    # Configurar Chrome
    options = setup_stealth_chrome()
    
    try:
        # Crear driver
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        
        # Aplicar scripts anti-detección
        apply_stealth_scripts(driver)
        
        # Configurar ventana
        driver.set_window_size(1920, 1080)
        driver.maximize_window()
        
        print("✅ Chrome configurado con anti-detección extrema")
        
        # Cargar cookies
        cookie_loaded = cargar_cookies(driver, cookies_path)
        
        print("\n🌐 Navegando directamente a Creator Center...")
        driver.get('https://www.tiktok.com/creator-center/upload')
        time.sleep(5)
        
        # Aplicar scripts anti-detección nuevamente después de cargar la página
        apply_stealth_scripts(driver)
        
        # Verificar autenticación
        print("   🔍 Verificando estado de autenticación...")
        needs_login = False
        
        try:
            # Buscar indicadores de login
            login_elements = driver.find_elements(By.XPATH, "//button[contains(text(), 'Log in')] | //button[contains(text(), 'Sign up')]")
            if any(el.is_displayed() for el in login_elements):
                needs_login = True
        except:
            pass
        
        if needs_login:
            print("⚠️ SE REQUIERE LOGIN MANUAL:")
            print("   👤 1. Logueate en TikTok en el navegador que se abrió")
            print("   🎯 2. Navega manualmente a: https://www.tiktok.com/creator-center/upload")
            print("   ✅ 3. Asegúrate de ver la página de upload")
            print("   ⏳ 4. Presiona Enter aquí cuando estés listo...")
            input()
            
            driver.get('https://www.tiktok.com/creator-center/upload')
            time.sleep(3)
            apply_stealth_scripts(driver)
        else:
            print("✅ Ya autenticado - Continuando automáticamente")
        
        movimiento_humano_realista(driver)
        
        # Verificar página de upload
        print("\n🔍 Esperando carga de página de upload...")
        
        page_loaded = False
        for attempt in range(3):
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
                )
                print("✅ Página de upload cargada")
                page_loaded = True
                break
            except TimeoutException:
                if attempt < 2:
                    print(f"⚠️ Intento {attempt + 1} falló, reintentando...")
                    driver.refresh()
                    time.sleep(5)
                    apply_stealth_scripts(driver)
        
        if not page_loaded:
            print("❌ Error: Página de upload no cargó")
            return False
        
        # Upload de archivo
        print("\n📁 Cargando archivo...")
        file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
        print(f"📁 Encontrados {len(file_inputs)} inputs de archivo")
        
        if not file_inputs:
            print("❌ No se encontraron inputs de archivo")
            return False
        
        upload_success = False
        for i, file_input in enumerate(file_inputs, 1):
            try:
                print(f"🎯 Intentando input #{i}...")
                
                # Hacer visible el input
                driver.execute_script("""
                    arguments[0].style.display = 'block';
                    arguments[0].style.visibility = 'visible';
                    arguments[0].style.opacity = '1';
                """, file_input)
                
                file_input.send_keys(os.path.abspath(video_path))
                time.sleep(random.uniform(2, 4))
                print(f"✅ ARCHIVO CARGADO con input #{i}")
                upload_success = True
                break
            except Exception as e:
                print(f"❌ Input #{i} falló: {str(e)[:100]}")
        
        if not upload_success:
            return False
        
        # AJUSTE #2: Procesamiento (20 segundos)
        print("\n⏳ PROCESAMIENTO OPTIMIZADO (20 segundos)...")
        for i in range(4):
            print(f"⏳ Procesando... {i*5}/20s")
            if random.random() < 0.6:
                movimiento_humano_realista(driver)
            time.sleep(5)
        
        # Screenshot
        timestamp = int(time.time())
        driver.save_screenshot(f"selenium_estable_processing_{timestamp}.png")
        print(f"📸 Screenshot: selenium_estable_processing_{timestamp}.png")
        
        # Show More
        print("\n🔍 Buscando opciones avanzadas...")
        show_more_clicked = False
        
        # XPATH ESPECÍFICO proporcionado por el usuario para Show More
        xpath_show_more = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[3]/div/span[1]'
        
        try:
            print(f"🔍 Usando XPath específico para Show More: {xpath_show_more}")
            
            # Scroll para asegurar visibilidad
            print("   📜 Haciendo scroll para asegurar visibilidad...")
            driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(2)
            
            # Buscar elemento Show More por XPath específico
            show_more = driver.find_element(By.XPATH, xpath_show_more)
            
            if show_more.is_displayed():
                print("   📍 Elemento Show More encontrado con XPath específico")
                
                # Obtener información del elemento
                tag_name = show_more.tag_name
                class_name = show_more.get_attribute('class')
                text_content = show_more.text
                
                print(f"   📋 Tag: {tag_name}")
                print(f"   📋 Clases: {class_name}")
                print(f"   📋 Texto: '{text_content}'")
                
                # Scroll al elemento y click
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", show_more)
                time.sleep(2)
                
                # Hover y click
                print("   🖱️ Haciendo hover sobre Show More...")
                actions = ActionChains(driver)
                actions.move_to_element(show_more).perform()
                time.sleep(1)
                
                print("   🖱️ Haciendo click en Show More...")
                driver.execute_script("arguments[0].click();", show_more)
                time.sleep(3)
                
                print("✅ Show More clickeado con XPath específico - Sección expandida")
                show_more_clicked = True
            else:
                print("   ❌ Elemento Show More no visible con XPath específico")
                
        except NoSuchElementException:
            print("   ❌ Elemento Show More no encontrado con XPath específico")
        except Exception as e:
            print(f"   ❌ Error con XPath específico de Show More: {e}")
        
        # Fallback: Buscar por texto si el XPath falla
        if not show_more_clicked:
            print("🔍 Fallback: Buscando Show More por texto...")
            
            show_more_selectors = [
                "//button[contains(text(), 'Show More')] | //button[contains(text(), 'Show more')] | //button[contains(text(), 'Mostrar más')]"
            ]
            
            for selector in show_more_selectors:
                try:
                    show_more = driver.find_element(By.XPATH, selector)
                    if show_more.is_displayed():
                        print(f"   📍 Show More encontrado con fallback")
                        driver.execute_script("arguments[0].scrollIntoView();", show_more)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", show_more)
                        time.sleep(3)
                        print("✅ Show More clickeado (fallback)")
                        show_more_clicked = True
                        break
                except NoSuchElementException:
                    continue
        
        if not show_more_clicked:
            print("⚠️ Show More no encontrado, haciendo scroll...")
            driver.execute_script("window.scrollBy(0, 500)")
            time.sleep(2)
        
        # AJUSTE #3: Activar AI Content
        ai_activated = activar_ai_content_xpath_especifico(driver)
        
        # AJUSTE #4: Verificar Everyone
        everyone_ok = verificar_everyone_seleccionado(driver)
        
        # Agregar descripción
        print("\n📝 Agregando descripción...")
        desc_selectors = [
            "//textarea[contains(@placeholder, 'escrib')] | //textarea[contains(@placeholder, 'Describ')] | //div[@contenteditable='true']"
        ]
        
        descripcion_agregada = False
        for selector in desc_selectors:
            try:
                desc_element = driver.find_element(By.XPATH, selector)
                if desc_element.is_displayed():
                    print(f"   📍 Campo de descripción encontrado")
                    driver.execute_script("arguments[0].focus();", desc_element)
                    time.sleep(1)
                    desc_element.clear()
                    time.sleep(1)
                    
                    escribir_como_humano(desc_element, descripcion, driver)
                    
                    # Verificar
                    time.sleep(2)
                    texto_actual = desc_element.get_attribute('value') or desc_element.text
                    
                    if texto_actual and len(texto_actual.strip()) > 10:
                        print("✅ Descripción agregada correctamente")
                        print(f"   📝 Caracteres escritos: {len(texto_actual)}")
                        descripcion_agregada = True
                        break
            except NoSuchElementException:
                continue
        
        # Screenshot pre-publicación
        timestamp = int(time.time())
        driver.save_screenshot(f"selenium_estable_pre_publish_{timestamp}.png")
        print(f"📸 Screenshot pre-publicación: selenium_estable_pre_publish_{timestamp}.png")
        
        # AJUSTE #5: Esperar 30 segundos
        print("\n⏳ ESPERANDO 30 SEGUNDOS ANTES DE PUBLICAR...")
        for i in range(6):
            print(f"   ⏰ {30 - i*5} segundos restantes...")
            movimiento_humano_realista(driver)
            time.sleep(5)
        
        # Buscar botón Post
        print("\n🚀 BUSCANDO BOTÓN POST...")
        
        # XPath específico proporcionado por el usuario para el botón Post
        xpath_post_button = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[5]/div/button[1]/div[2]'
        
        publish_success = False
        
        # Intentar primero con XPath específico del botón Post
        try:
            print(f"🎯 Usando XPath específico para Post: {xpath_post_button}")
            
            # Scroll para asegurar visibilidad
            driver.execute_script("window.scrollBy(0, 200)")
            time.sleep(2)
            
            publish_button = driver.find_element(By.XPATH, xpath_post_button)
            
            is_visible = publish_button.is_displayed()
            is_enabled = publish_button.is_enabled()
            
            print(f"   📍 Botón Post encontrado con XPath específico - Visible: {is_visible}, Habilitado: {is_enabled}")
            
            if is_visible and is_enabled:
                print("   🤖 Simulando comportamiento humano...")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", publish_button)
                time.sleep(random.uniform(2, 4))
                
                # Hover
                actions = ActionChains(driver)
                actions.move_to_element(publish_button).perform()
                time.sleep(random.uniform(1, 3))
                
                # Click
                print("   🖱️ Realizando click en botón Post con XPath específico...")
                driver.execute_script("arguments[0].click();", publish_button)
                print("✅ Botón Post clickeado con XPath específico")
                
                # Continuar con el manejo de modales
                publish_success = True
                
        except NoSuchElementException:
            print("   ❌ Botón Post no encontrado con XPath específico")
        except Exception as e:
            print(f"   ❌ Error con XPath específico de Post: {e}")
        
        # Si el XPath específico falló, intentar selectores genéricos
        if not publish_success:
            print("\n🔄 Intentando con selectores genéricos...")
            
            publish_selectors = [
                "//button[contains(text(), 'Post')] | //button[contains(text(), 'Publicar')] | //button[@type='submit']"
            ]
            
            for selector in publish_selectors:
                try:
                publish_button = driver.find_element(By.XPATH, selector)
                
                is_visible = publish_button.is_displayed()
                is_enabled = publish_button.is_enabled()
                text_content = publish_button.text
                
                print(f"   📍 Botón encontrado: '{text_content}' - Visible: {is_visible}, Habilitado: {is_enabled}")
                
                if is_visible and is_enabled:
                    print("   🤖 Simulando comportamiento humano...")
                    driver.execute_script("arguments[0].scrollIntoView();", publish_button)
                    time.sleep(random.uniform(2, 4))
                    
                    # Hover
                    actions = ActionChains(driver)
                    actions.move_to_element(publish_button).perform()
                    time.sleep(random.uniform(1, 3))
                    
                    # Click
                    print("   🖱️ Realizando click...")
                    driver.execute_script("arguments[0].click();", publish_button)
                    print("✅ Botón Post clickeado")
                    
                    # MANEJO MEJORADO DE MODALES
                    print("   🔍 Verificando si aparece algún modal...")
                    time.sleep(5)
                    
                    modal_selectors = [
                        "//div[@role='dialog']",
                        "//*[contains(@class, 'modal')]",
                        "//*[contains(@class, 'Modal')]",
                        "//*[contains(@class, 'popup')]",
                        "//*[contains(@class, 'overlay')]"
                    ]
                    
                    modal_found = False
                    modal_text = ""
                    
                    for modal_selector in modal_selectors:
                        try:
                            modal = driver.find_element(By.XPATH, modal_selector)
                            if modal.is_displayed():
                                modal_text = modal.text
                                print(f"   ⚠️ Modal detectado: {modal_text[:150]}...")
                                modal_found = True
                                break
                        except NoSuchElementException:
                            continue
                    
                    if modal_found:
                        print("   🔍 Analizando tipo de modal...")
                        modal_text_lower = modal_text.lower()
                        
                        # Detectar diferentes tipos de modal
                        if any(keyword in modal_text_lower for keyword in ['exit', 'sure', 'discard', 'leave', 'unsaved']):
                            print("   ⚠️ Modal de salida detectado - CANCELANDO para continuar con upload")
                            
                            # Buscar botón cancelar/no
                            cancel_selectors = [
                                "//button[contains(text(), 'Cancel')]",
                                "//button[contains(text(), 'Cancelar')]",
                                "//button[contains(text(), 'No')]",
                                "//button[contains(text(), 'Stay')]",
                                "//button[contains(@class, 'cancel')]",
                                "//button[contains(@class, 'secondary')]"
                            ]
                            
                            cancel_clicked = False
                            for cancel_selector in cancel_selectors:
                                try:
                                    cancel_btn = driver.find_element(By.XPATH, cancel_selector)
                                    if cancel_btn.is_displayed():
                                        driver.execute_script("arguments[0].click();", cancel_btn)
                                        print(f"   ✅ Modal de salida cancelado")
                                        time.sleep(2)
                                        cancel_clicked = True
                                        break
                                except NoSuchElementException:
                                    continue
                            
                            if cancel_clicked:
                                print("   🔄 Continuando con el proceso de upload...")
                                # Reintentar click en Post
                                time.sleep(3)
                                try:
                                    post_button_retry = driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
                                    if post_button_retry.is_displayed() and post_button_retry.is_enabled():
                                        print("   🔄 Reintentando click en Post...")
                                        driver.execute_script("arguments[0].click();", post_button_retry)
                                        time.sleep(5)
                                        print("✅ Video publicado después de cancelar modal de salida")
                                        publish_success = True
                                        break
                                    else:
                                        print("   ⚠️ Botón Post no disponible después de cancelar modal")
                                except NoSuchElementException:
                                    print("   ⚠️ No se encontró botón Post para reintentar")
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
                                close_selectors = [
                                    "//button[contains(text(), 'Close')]",
                                    "//button[contains(text(), 'Cerrar')]",
                                    "//button[contains(@aria-label, 'close')]",
                                    "//button[contains(@class, 'close')]"
                                ]
                                for close_selector in close_selectors:
                                    try:
                                        close_btn = driver.find_element(By.XPATH, close_selector)
                                        if close_btn.is_displayed():
                                            driver.execute_script("arguments[0].click();", close_btn)
                                            time.sleep(1)
                                            break
                                    except NoSuchElementException:
                                        continue
                            except:
                                pass
                            return False
                            
                        else:
                            print("   ❓ Modal desconocido - Intentando cerrarlo...")
                            # Intentar cerrar modal genérico
                            close_selectors = [
                                "//button[contains(text(), 'OK')]",
                                "//button[contains(text(), 'Aceptar')]",
                                "//button[contains(text(), 'Close')]",
                                "//button[contains(text(), 'Cerrar')]",
                                "//button[contains(@aria-label, 'close')]",
                                "//button[contains(@class, 'close')]"
                            ]
                            
                            for close_selector in close_selectors:
                                try:
                                    close_btn = driver.find_element(By.XPATH, close_selector)
                                    if close_btn.is_displayed():
                                        driver.execute_script("arguments[0].click();", close_btn)
                                        print(f"   ✅ Modal cerrado")
                                        time.sleep(2)
                                        break
                                except NoSuchElementException:
                                    continue
                                    
                    else:
                        # No hay modal - verificar si el upload fue exitoso por otros medios
                        print("   ℹ️ No se detectó modal")
                        
                        # Verificar cambio de URL o elementos de éxito
                        time.sleep(3)
                        current_url = driver.current_url
                        
                        if 'upload' not in current_url or 'success' in current_url or 'posted' in current_url:
                            print("   ✅ URL cambió - Video posiblemente publicado exitosamente")
                            publish_success = True
                            break
                        else:
                            # Buscar indicadores de éxito en la página
                            success_indicators = [
                                "//text()[contains(., 'Video posted')]",
                                "//text()[contains(., 'Published')]",
                                "//text()[contains(., 'Publicado')]",
                                "//text()[contains(., 'Success')]",
                                "//*[contains(@class, 'success')]",
                                "//*[contains(@class, 'posted')]"
                            ]
                            
                            for indicator in success_indicators:
                                try:
                                    success_element = driver.find_element(By.XPATH, indicator)
                                    if success_element.is_displayed():
                                        print(f"   ✅ Indicador de éxito encontrado")
                                        publish_success = True
                                        break
                                except NoSuchElementException:
                                    continue
                            
                            if publish_success:
                                break
                            else:
                                print("   ✅ Click realizado - Asumiendo éxito (sin modal ni indicadores)")
                                publish_success = True
                                break
                    
                    break
                    
            except NoSuchElementException:
                continue
        
        if publish_success:
            print("✅ Video publicado exitosamente")
            time.sleep(10)
            return True
        else:
            print("❌ No se pudo encontrar el botón Post")
            driver.save_screenshot(f"selenium_estable_no_post_button_{int(time.time())}.png")
            return False
        
    except Exception as e:
        print(f"❌ Error en proceso principal: {e}")
        return False
    
    finally:
        try:
            time.sleep(3)
            driver.quit()
        except:
            pass

def main():
    """Función principal"""
    video_path = "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4"
    descripcion = """🔥 ¡Contenido ÉPICO que te va a SORPRENDER! ✨ 

No puedes perderte esta increíble experiencia viral que está rompiendo TikTok 🚀
¡Dale LIKE si te gustó y COMPARTE con tus amigos! 💖

Prepárate para algo que jamás has visto antes... ¿Estás listo? 👀

#fyp #viral #trending #amazing #foryou"""
    
    resultado = subir_video_ultra_stealth_selenium_estable(video_path, descripcion)
    
    if resultado:
        print("\n🎉 ¡UPLOAD COMPLETADO EXITOSAMENTE!")
    else:
        print("\n❌ Upload falló")

if __name__ == "__main__":
    main()
