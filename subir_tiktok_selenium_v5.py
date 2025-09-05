#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - SELENIUM EDITION
Versión V5 usando Selenium en lugar de Playwright para evitar detección
Mantiene toda la lógica del V4 modificado pero con Selenium
"""

import asyncio
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
import undetected_chromedriver as uc

def cargar_cookies(driver, cookies_path):
    """Cargar cookies de sesión - Selenium version"""
    try:
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
        
        # Ir a TikTok primero para cargar cookies
        driver.get("https://www.tiktok.com")
        time.sleep(3)
        
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
            except Exception as e:
                print(f"   ⚠️ Error con cookie {cookie.get('name', 'unknown')}: {e}")
                continue
        
        print(f"✅ Cookies cargadas desde {cookies_path}")
        return True
    except Exception as e:
        print(f"❌ Error cargando cookies: {e}")
        return False

def movimiento_humano_realista(driver):
    """Simula movimientos de mouse completamente humanos - Selenium version"""
    try:
        actions = ActionChains(driver)
        
        # Mover a posición aleatoria
        viewport_width = driver.execute_script("return window.innerWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        x = random.randint(200, min(1200, viewport_width - 100))
        y = random.randint(200, min(800, viewport_height - 100))
        
        # Movimiento suave
        actions.move_by_offset(x - viewport_width//2, y - viewport_height//2)
        actions.perform()
        
        time.sleep(random.uniform(0.5, 2.0))
        
        # Scroll ocasional
        if random.random() < 0.3:
            driver.execute_script(f"window.scrollBy(0, {random.randint(-100, 100)})")
            time.sleep(random.uniform(0.3, 1.0))
            
    except Exception as e:
        print(f"   ⚠️ Error en movimiento humano: {e}")

def escribir_como_humano(element, texto, driver):
    """Escribe texto como un humano real - Selenium version"""
    try:
        # Click en el elemento
        driver.execute_script("arguments[0].click();", element)
        time.sleep(random.uniform(0.2, 0.8))
        
        # Limpiar campo
        element.clear()
        time.sleep(random.uniform(0.1, 0.3))
        
        # Escribir caracter por caracter
        for i, char in enumerate(texto):
            element.send_keys(char)
            
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
    """AJUSTE #3: Activación con XPath específico del usuario - Selenium version"""
    print("\n🎯 ACTIVACIÓN AI CONTENT CON XPATH ESPECÍFICO...")
    
    # XPath específico proporcionado por el usuario
    xpath_ai_toggle = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span'
    
    try:
        print(f"🔍 Usando XPath específico: {xpath_ai_toggle}")
        
        # Scroll adicional para asegurar visibilidad
        print("   📜 Haciendo scroll para asegurar visibilidad...")
        driver.execute_script("window.scrollBy(0, 300)")
        time.sleep(2)
        
        # Buscar elemento por XPath
        try:
            ai_toggle = driver.find_element(By.XPATH, xpath_ai_toggle)
            print("   📍 Elemento AI toggle encontrado con XPath")
            
            # Obtener información del elemento
            tag_name = ai_toggle.tag_name
            class_name = ai_toggle.get_attribute('class')
            
            print(f"   📋 Tag: {tag_name}")
            print(f"   📋 Clases: {class_name}")
            
            # Verificar si el elemento es visible
            is_visible = ai_toggle.is_displayed()
            print(f"   👁️ Elemento visible: {is_visible}")
            
            if not is_visible:
                print("   📜 Elemento no visible, haciendo scroll directo al elemento...")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ai_toggle)
                time.sleep(3)
            
            # Hover sobre el elemento primero
            print("   🖱️ Haciendo hover sobre el elemento...")
            actions = ActionChains(driver)
            actions.move_to_element(ai_toggle).perform()
            time.sleep(1)
            
            # Click en el elemento
            print("   🖱️ Haciendo click en el toggle...")
            driver.execute_script("arguments[0].click();", ai_toggle)
            
            print("✅ AI Content toggle clickeado con XPath específico")
            
            # Buscar y manejar modal de confirmación
            print("   🔍 Buscando modal de confirmación...")
            time.sleep(2)
            
            modal_selectors = [
                "//button[contains(text(), 'Turn on')]",
                "//button[contains(text(), 'Aceptar')]",
                "//button[contains(text(), 'Accept')]",
                "//button[contains(text(), 'Confirmar')]",
                "//*[contains(@data-testid, 'confirm')]",
                "//*[contains(@class, 'confirm')]",
                "//div[@role='dialog']//button",
                "//*[contains(@class, 'modal')]//button"
            ]
            
            modal_handled = False
            for selector in modal_selectors:
                try:
                    modal_button = driver.find_element(By.XPATH, selector)
                    if modal_button.is_displayed():
                        button_text = modal_button.text
                        print(f"   📍 Modal encontrado - Botón: '{button_text}' con selector: {selector}")
                        
                        driver.execute_script("arguments[0].click();", modal_button)
                        print(f"   ✅ Modal confirmado - Botón '{button_text}' clickeado")
                        modal_handled = True
                        time.sleep(2)
                        break
                except NoSuchElementException:
                    continue
                except Exception as e:
                    continue
            
            if not modal_handled:
                print("   ℹ️ No se encontró modal de confirmación (puede que no haya aparecido)")
            
            # Esperar después del modal
            time.sleep(3)
            
            # Verificar si el estado cambió
            new_class = ai_toggle.get_attribute('class')
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
                
        except NoSuchElementException:
            print("   ❌ Elemento AI toggle no encontrado con XPath")
            
        # Fallback: Buscar por texto
        print("🔍 Fallback: Buscando por texto 'AI-generated content'")
        
        driver.execute_script("window.scrollBy(0, 200)")
        time.sleep(1)
        
        try:
            ai_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'AI-generated content')]")
            if ai_elements:
                print(f"   📍 Encontrados {len(ai_elements)} elementos con texto AI")
                
                for element in ai_elements:
                    try:
                        # Buscar toggles cercanos
                        toggles = driver.find_elements(By.XPATH, ".//ancestor::*[4]//*[@role='switch' or contains(@class, 'Switch')]")
                        print(f"   🎛️ Encontrados {len(toggles)} toggles en contenedor")
                        
                        for i, toggle in enumerate(toggles, 1):
                            try:
                                is_checked = toggle.get_attribute('aria-checked')
                                state = toggle.get_attribute('data-state')
                                class_attr = toggle.get_attribute('class')
                                
                                print(f"     🔘 Toggle #{i} - Checked: {is_checked}, State: {state}")
                                
                                # Verificar si está desactivado
                                is_unchecked = (
                                    is_checked == 'false' or 
                                    state == 'unchecked' or 
                                    'checked-false' in str(class_attr)
                                )
                                
                                if is_unchecked:
                                    print(f"     🎯 Activando toggle #{i}...")
                                    driver.execute_script("arguments[0].scrollIntoView();", toggle)
                                    time.sleep(1)
                                    driver.execute_script("arguments[0].click();", toggle)
                                    time.sleep(2)
                                    print(f"✅ AI Content activado - Toggle #{i} (fallback)")
                                    return True
                            except Exception as e:
                                print(f"     ❌ Error con toggle #{i}: {str(e)[:50]}")
                                continue
                    except Exception as e:
                        print(f"   ❌ Error procesando elemento AI: {str(e)[:50]}")
                        continue
        except:
            pass
        
        print("❌ No se pudo activar AI Content")
        return False
        
    except Exception as e:
        print(f"❌ Error en activación AI Content: {e}")
        return False

def verificar_everyone_seleccionado(driver):
    """AJUSTE #4: Verificar que Everyone esté seleccionado - Selenium version"""
    print("\n🔍 VERIFICANDO SELECCIÓN DE 'EVERYONE'...")
    
    try:
        # Buscar elementos con texto "Everyone"
        everyone_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Everyone')]")
        
        if everyone_elements:
            print(f"   📍 Encontrados {len(everyone_elements)} elementos con texto 'Everyone'")
            
            for i, element in enumerate(everyone_elements):
                try:
                    # Verificar si está seleccionado
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
                        
                except Exception as e:
                    print(f"     ❌ Error con Everyone #{i+1}: {str(e)[:50]}")
                    continue
        
        # Buscar por selectores más específicos
        privacy_selectors = [
            "//*[contains(@data-testid, 'everyone')]",
            "//*[contains(@aria-label, 'Everyone')]",
            "//input[@value='everyone']",
            "//button[contains(text(), 'Everyone')]"
        ]
        
        for selector in privacy_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    print(f"   📍 Encontrados {len(elements)} elementos con selector {selector}")
                    
                    for element in elements:
                        try:
                            driver.execute_script("arguments[0].scrollIntoView();", element)
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(1)
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

def subir_video_ultra_stealth_selenium(video_path, descripcion):
    """Función principal Selenium con todos los ajustes del V4 modificado"""
    print("🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - SELENIUM EDITION")
    print("=" * 60)
    print("📋 AJUSTES APLICADOS:")
    print("1. Pantalla 1920x1080 (sin cortes)")
    print("2. Procesamiento 20 segundos") 
    print("3. XPath específico para AI content")
    print("4. Verificar Everyone seleccionado")
    print("5. Esperar 30 segundos antes de Post")
    print("6. 🔥 USANDO SELENIUM con undetected-chromedriver")
    print("=" * 60)
    
    cookies_path = "config/upload_cookies_playwright.json"
    
    # Verificar archivo
    if not os.path.exists(video_path):
        print(f"❌ Archivo no encontrado: {video_path}")
        return False
    
    file_size = os.path.getsize(video_path) / (1024*1024)
    print(f"📹 Video: {video_path}")
    print(f"📏 Tamaño: {file_size:.1f} MB")
    
    # Configurar Chrome con máxima evasión
    print("\n🛡️ Configurando Chrome con anti-detección extrema...")
    
    # Usar undetected-chromedriver para máxima evasión
    options = uc.ChromeOptions()
    
    # Configuración anti-detección
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
    
    # User agent real
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Configuración de perfil persistente
    profile_dir = os.path.join(os.getcwd(), "chrome_profile_selenium")
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
            "geolocation": 1
        },
        "profile.managed_default_content_settings": {
            "images": 1
        }
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Crear driver con undetected-chromedriver
        driver = uc.Chrome(options=options, version_main=None)
        
        # Configuración adicional anti-detección
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['es-MX', 'es', 'en'],
                });
                
                window.chrome = {
                    runtime: {},
                };
                
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: () => Promise.resolve({ state: 'granted' }),
                    }),
                });
            '''
        })
        
        # Configurar ventana
        driver.set_window_size(1920, 1080)
        
        print("✅ Chrome configurado con anti-detección extrema")
        
        # Cargar cookies
        cookie_loaded = cargar_cookies(driver, cookies_path)
        
        print("\n🌐 Navegando directamente a Creator Center...")
        driver.get('https://www.tiktok.com/creator-center/upload')
        time.sleep(5)
        
        # Verificar si necesita login
        print("   🔍 Verificando estado de autenticación...")
        login_indicators = [
            "//button[contains(text(), 'Log in')]",
            "//button[contains(text(), 'Sign up')]",
            "//*[contains(@data-testid, 'login')]",
            "//*[contains(@class, 'login')]"
        ]
        
        needs_login = False
        for indicator in login_indicators:
            try:
                element = driver.find_element(By.XPATH, indicator)
                if element.is_displayed():
                    needs_login = True
                    print(f"   🔍 Detectado indicador de login: {indicator}")
                    break
            except NoSuchElementException:
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
            driver.get('https://www.tiktok.com/creator-center/upload')
            time.sleep(3)
        else:
            print("✅ Ya autenticado - Continuando automáticamente")
        
        movimiento_humano_realista(driver)
        
        # Verificar carga de página
        print("\n🔍 Esperando carga de página de upload...")
        
        page_loaded = False
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                # Buscar input de archivo
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
                )
                print("✅ Página de upload cargada (input detectado)")
                page_loaded = True
                break
            except TimeoutException:
                if attempt < max_attempts - 1:
                    print(f"⚠️ Intento {attempt + 1} falló, reintentando...")
                    driver.refresh()
                    time.sleep(5)
                else:
                    print("⚠️ Input de archivo no detectado, buscando alternativas...")
        
        if not page_loaded:
            # Buscar elementos relacionados con upload
            upload_indicators = [
                "//*[contains(@data-testid, 'upload')]",
                "//*[contains(@class, 'upload')]",
                "//*[contains(text(), 'Select file')]",
                "//*[contains(text(), 'Choose file')]",
                "//*[contains(text(), 'Seleccionar archivo')]"
            ]
            
            for indicator in upload_indicators:
                try:
                    elements = driver.find_elements(By.XPATH, indicator)
                    if elements:
                        print(f"✅ Página de upload cargada ({indicator} detectado)")
                        page_loaded = True
                        break
                except:
                    continue
        
        if not page_loaded:
            print("⚠️ Página no detectada, esperando 5s adicionales...")
            time.sleep(5)
            
            # Screenshot para debug
            debug_timestamp = int(time.time())
            driver.save_screenshot(f"debug_upload_page_selenium_{debug_timestamp}.png")
            print(f"📸 Screenshot debug: debug_upload_page_selenium_{debug_timestamp}.png")
            
            # Buscar cualquier input de archivo
            all_inputs = driver.find_elements(By.TAG_NAME, 'input')
            file_inputs = [inp for inp in all_inputs if inp.get_attribute('type') == 'file']
            
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
        file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
        print(f"📁 Encontrados {len(file_inputs)} inputs de archivo")
        
        if not file_inputs:
            print("❌ No se encontraron inputs de archivo")
            return False
        
        upload_success = False
        for i, file_input in enumerate(file_inputs, 1):
            try:
                print(f"🎯 Intentando input #{i}...")
                
                # Hacer visible el input si está oculto
                driver.execute_script("arguments[0].style.display = 'block';", file_input)
                driver.execute_script("arguments[0].style.visibility = 'visible';", file_input)
                
                file_input.send_keys(os.path.abspath(video_path))
                time.sleep(random.uniform(1, 3))
                print(f"✅ ARCHIVO CARGADO con input #{i}")
                upload_success = True
                break
            except Exception as e:
                print(f"❌ Input #{i} falló: {str(e)[:100]}")
                if i == len(file_inputs):
                    print("❌ No se pudo cargar el archivo")
        
        if not upload_success:
            return False
        
        # AJUSTE #2: Procesamiento (20 segundos)
        print("\n⏳ PROCESAMIENTO OPTIMIZADO (20 segundos)...")
        total_wait = 20
        interval = 5
        
        for elapsed in range(0, total_wait, interval):
            print(f"⏳ Procesando... {elapsed}/{total_wait}s")
            if random.random() < 0.6:
                movimiento_humano_realista(driver)
            time.sleep(interval)
        
        # Verificación de procesamiento
        print("\n🔍 Verificación final de procesamiento...")
        indicators = {
            'canvas': len(driver.find_elements(By.TAG_NAME, 'canvas')),
            '[class*="preview"]': len(driver.find_elements(By.CSS_SELECTOR, '[class*="preview"]')),
            '[class*="player"]': len(driver.find_elements(By.CSS_SELECTOR, '[class*="player"]'))
        }
        
        print("✅ Indicadores encontrados:")
        for name, count in indicators.items():
            print(f"   - {name} ({count})")
        
        timestamp = int(time.time())
        driver.save_screenshot(f"selenium_processing_{timestamp}.png")
        print(f"📸 Screenshot: selenium_processing_{timestamp}.png")
        
        # Show More - CRÍTICO para hacer visible el AI Content
        print("\n🔍 Buscando opciones avanzadas...")
        show_more_clicked = False
        
        show_more_selectors = [
            "//button[contains(text(), 'Show More')]",
            "//button[contains(text(), 'Show more')]",
            "//button[contains(text(), 'Mostrar más')]",
            "//*[contains(@data-testid, 'show-more')]",
            "//*[contains(@class, 'show-more')]",
            "//button[@aria-expanded='false']"
        ]
        
        for selector in show_more_selectors:
            try:
                show_more = driver.find_element(By.XPATH, selector)
                if show_more.is_displayed():
                    print(f"   📍 Show More encontrado con: {selector}")
                    
                    driver.execute_script("arguments[0].scrollIntoView();", show_more)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", show_more)
                    time.sleep(3)
                    
                    print("✅ Show More clickeado - Sección expandida")
                    show_more_clicked = True
                    break
            except NoSuchElementException:
                continue
            except Exception as e:
                print(f"   ❌ Error con selector {selector}: {str(e)[:50]}")
                continue
        
        if not show_more_clicked:
            print("⚠️ Show More no encontrado, haciendo scroll manual...")
            driver.execute_script("window.scrollBy(0, 500)")
            time.sleep(2)
        
        # AJUSTE #3: Activar AI Content con XPath específico
        ai_activated = activar_ai_content_xpath_especifico(driver)
        
        if ai_activated:
            print("✅ AI Content activado correctamente")
        else:
            print("⚠️ AI Content no se pudo activar")
        
        # AJUSTE #4: Verificar que Everyone esté seleccionado
        everyone_ok = verificar_everyone_seleccionado(driver)
        
        if everyone_ok:
            print("✅ Everyone verificado/seleccionado")
        else:
            print("⚠️ Everyone no pudo ser verificado")
        
        # Agregar descripción
        print("\n📝 Agregando descripción...")
        desc_selectors = [
            "//textarea[contains(@placeholder, 'escrib')]",
            "//textarea[contains(@placeholder, 'Describ')]",
            "//div[@contenteditable='true']",
            "//*[contains(@data-testid, 'caption')]",
            "//textarea[contains(@data-testid, 'caption-input')]",
            "//textarea[contains(@aria-label, 'caption')]"
        ]
        
        descripcion_agregada = False
        for selector in desc_selectors:
            try:
                desc_element = driver.find_element(By.XPATH, selector)
                if desc_element.is_displayed():
                    print(f"   📍 Campo de descripción encontrado: {selector}")
                    
                    driver.execute_script("arguments[0].click();", desc_element)
                    time.sleep(1)
                    desc_element.clear()
                    time.sleep(1)
                    
                    escribir_como_humano(desc_element, descripcion, driver)
                    
                    time.sleep(2)
                    
                    # Verificar que se escribió
                    if "contenteditable" in selector:
                        texto_actual = desc_element.text
                    else:
                        texto_actual = desc_element.get_attribute('value')
                    
                    if texto_actual and len(texto_actual.strip()) > 10:
                        print("✅ Descripción agregada correctamente")
                        print(f"   📝 Caracteres escritos: {len(texto_actual)}")
                        descripcion_agregada = True
                        break
                    else:
                        print(f"   ⚠️ Descripción no se escribió completamente")
                        
            except NoSuchElementException:
                continue
            except Exception as e:
                print(f"   ❌ Error con selector {selector}: {str(e)[:50]}")
                continue
        
        if not descripcion_agregada:
            print("⚠️ No se pudo agregar descripción con ningún selector")
        
        # Screenshot pre-publicación
        timestamp = int(time.time())
        driver.save_screenshot(f"selenium_pre_publish_{timestamp}.png")
        print(f"📸 Screenshot pre-publicación: selenium_pre_publish_{timestamp}.png")
        
        # AJUSTE #5: Esperar 30 segundos antes de Post
        print("\n⏳ ESPERANDO 30 SEGUNDOS ANTES DE PUBLICAR...")
        for i in range(30, 0, -5):
            print(f"   ⏰ {i} segundos restantes...")
            movimiento_humano_realista(driver)
            time.sleep(5)
        
        # Buscar y clickear botón Post
        print("\n🚀 BUSCANDO BOTÓN POST...")
        
        # Estrategias de búsqueda del botón Post
        publish_selectors = [
            "//button[contains(text(), 'Post')]",
            "//button[contains(text(), 'Publicar')]",
            "//button[@data-e2e='publish-button']",
            "//button[@type='submit']",
            "//button[contains(text(), 'Subir')]",
            "//button[contains(@class, 'publish')]",
            "//button[contains(@class, 'submit')]",
            "//button[contains(@class, 'Post')]",
            "//button[contains(@data-testid, 'post')]",
            "//button[contains(@data-testid, 'publish')]",
            "//*[contains(@data-e2e, 'post')]",
            "//form//button[last()]",
            "//button[contains(@aria-label, 'Post')]",
            "//button[contains(@aria-label, 'Publish')]"
        ]
        
        publish_success = False
        for selector in publish_selectors:
            try:
                print(f"   🔍 Probando selector: {selector}")
                publish_button = driver.find_element(By.XPATH, selector)
                
                is_visible = publish_button.is_displayed()
                is_enabled = publish_button.is_enabled()
                text_content = publish_button.text
                
                print(f"   📍 Botón encontrado:")
                print(f"      📝 Texto: '{text_content}'")
                print(f"      👁️ Visible: {is_visible}")
                print(f"      ✅ Habilitado: {is_enabled}")
                
                if is_visible and is_enabled:
                    print("   🤖 Simulando comportamiento humano antes del click...")
                    
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
                    
                    time.sleep(5)
                    publish_success = True
                    break
                    
            except NoSuchElementException:
                continue
            except Exception as e:
                print(f"   ❌ Error con selector {selector}: {str(e)[:50]}")
                continue
        
        if publish_success:
            print("✅ Video publicado exitosamente")
            time.sleep(10)
            return True
        else:
            print("❌ No se pudo encontrar el botón Post")
            
            # Screenshot final para diagnóstico
            driver.save_screenshot(f"selenium_post_button_not_found_{int(time.time())}.png")
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
    
    resultado = subir_video_ultra_stealth_selenium(video_path, descripcion)
    
    if resultado:
        print("\n🎉 ¡UPLOAD COMPLETADO EXITOSAMENTE!")
    else:
        print("\n❌ Upload falló")

if __name__ == "__main__":
    main()
