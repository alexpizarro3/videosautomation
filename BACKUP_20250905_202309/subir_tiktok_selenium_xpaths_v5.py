#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - SELENIUM CON XPATHS ESPECÍFICOS
Versión V5 con XPaths específicos del usuario:
- Show More: //*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[3]/div/span[1]
- AI Content: //*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span
- Post Button: //*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[5]/div/button[1]/div[2]
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

def movimiento_humano_realista(driver):
    """Simular movimientos humanos"""
    try:
        # Mover mouse a posición aleatoria
        actions = ActionChains(driver)
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        actions.move_by_offset(x, y).perform()
        time.sleep(random.uniform(0.5, 1.5))
    except:
        pass

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
    """Configurar Chrome con máxima anti-detección"""
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
    options.add_argument('--disable-features=TranslateUI')
    options.add_argument('--disable-ipc-flooding-protection')
    
    # User agent específico para Windows
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Configuración de perfil persistente
    profile_dir = os.path.join(os.getcwd(), "chrome_profile_selenium_xpaths")
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
    driver.execute_script("""
        // Eliminar propiedades de webdriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Simular plugins reales
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Configurar idiomas
        Object.defineProperty(navigator, 'languages', {
            get: () => ['es-MX', 'es', 'en-US', 'en'],
        });
        
        // Simular Chrome runtime
        window.chrome = {
            runtime: {},
        };
        
        // Simular permisos
        Object.defineProperty(navigator, 'permissions', {
            get: () => ({
                query: () => Promise.resolve({ state: 'granted' }),
            }),
        });
    """)

def subir_video_ultra_stealth_selenium_xpaths(video_path, descripcion):
    """Función principal Selenium con XPaths específicos"""
    print("🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - SELENIUM XPATHS ESPECÍFICOS")
    print("=" * 70)
    print("📋 XPATH ESPECÍFICOS CONFIGURADOS:")
    print("1. Show More: //*[@id=\"root\"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[3]/div/span[1]")
    print("2. AI Content: //*[@id=\"root\"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span")
    print("3. Post Button: //*[@id=\"root\"]/div/div/div[2]/div[2]/div/div/div/div[5]/div/button[1]/div[2]")
    print("=" * 70)
    
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
        print("🚀 Iniciando ChromeDriver...")
        driver = webdriver.Chrome(options=options)
        
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
        else:
            print("✅ Ya autenticado - Continuando automáticamente")
        
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
        
        # Procesamiento (20 segundos)
        print("\n⏳ PROCESAMIENTO OPTIMIZADO (20 segundos)...")
        for i in range(4):
            print(f"⏳ Procesando... {i*5}/20s")
            movimiento_humano_realista(driver)
            time.sleep(5)
        
        # Screenshot
        timestamp = int(time.time())
        driver.save_screenshot(f"selenium_xpaths_processing_{timestamp}.png")
        print(f"📸 Screenshot: selenium_xpaths_processing_{timestamp}.png")
        
        # Show More con XPath específico del usuario
        print("\n🔍 Expandiendo opciones avanzadas con XPath específico...")
        
        xpath_show_more = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[3]/div/span[1]'
        show_more_clicked = False
        
        try:
            print(f"🎯 Usando XPath específico para Show More:")
            print(f"   {xpath_show_more}")
            
            # Scroll para asegurar visibilidad
            driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(2)
            
            show_more = driver.find_element(By.XPATH, xpath_show_more)
            
            if show_more.is_displayed():
                print("   📍 Elemento Show More encontrado con XPath específico")
                
                # Scroll al elemento y click
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", show_more)
                time.sleep(2)
                
                print("   🖱️ Haciendo click en Show More...")
                driver.execute_script("arguments[0].click();", show_more)
                time.sleep(3)
                
                print("✅ Show More clickeado con XPath específico - Opciones expandidas")
                show_more_clicked = True
            else:
                print("   ❌ Elemento Show More no visible con XPath específico")
                
        except NoSuchElementException:
            print("   ❌ Elemento Show More no encontrado con XPath específico")
        except Exception as e:
            print(f"   ❌ Error con XPath específico de Show More: {e}")
        
        # Activar AI Content con XPath específico del usuario
        print("\n🎯 ACTIVACIÓN AI CONTENT CON XPATH ESPECÍFICO...")
        
        xpath_ai_toggle = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span'
        
        try:
            print(f"🎯 Usando XPath específico para AI Content:")
            print(f"   {xpath_ai_toggle}")
            
            # Scroll adicional
            driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(2)
            
            ai_toggle = driver.find_element(By.XPATH, xpath_ai_toggle)
            
            if ai_toggle.is_displayed():
                print("   📍 Elemento AI toggle encontrado con XPath específico")
                
                # Scroll al elemento y click
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ai_toggle)
                time.sleep(2)
                
                print("   🖱️ Haciendo click en AI Content toggle...")
                driver.execute_script("arguments[0].click();", ai_toggle)
                
                print("✅ AI Content toggle clickeado con XPath específico")
                time.sleep(3)
                
                # MANEJO DEL MODAL DE AI CONTENT
                print("   🔍 Verificando si aparece modal de AI Content...")
                time.sleep(2)
                
                modal_handled = False
                
                # Buscar botones de confirmación del modal AI Content
                modal_confirm_selectors = [
                    "//button[contains(text(), 'Aceptar')]",
                    "//button[contains(text(), 'Accept')]", 
                    "//button[contains(text(), 'Continuar')]",
                    "//button[contains(text(), 'Continue')]",
                    "//button[contains(text(), 'OK')]",
                    "//button[contains(text(), 'Confirm')]",
                    "//button[contains(text(), 'Got it')]",
                    "//button[contains(@class, 'primary')] | //button[contains(@class, 'confirm')]"
                ]
                
                for selector in modal_confirm_selectors:
                    try:
                        modal_button = driver.find_element(By.XPATH, selector)
                        if modal_button.is_displayed():
                            button_text = modal_button.text
                            print(f"   📍 Modal AI Content detectado - Botón: '{button_text}'")
                            
                            # Hacer click en el botón de confirmación
                            driver.execute_script("arguments[0].click();", modal_button)
                            print(f"   ✅ Modal confirmado - Click en '{button_text}'")
                            
                            time.sleep(2)
                            modal_handled = True
                            break
                    except NoSuchElementException:
                        continue
                
                if modal_handled:
                    print("✅ Modal de AI Content manejado exitosamente")
                else:
                    print("   ℹ️ No se detectó modal de AI Content (puede que no aparezca)")
            else:
                print("   ❌ Elemento AI toggle no visible")
                
        except NoSuchElementException:
            print("   ❌ Elemento AI toggle no encontrado con XPath específico")
        except Exception as e:
            print(f"   ❌ Error con XPath específico AI Content: {e}")
        
        # Agregar descripción con XPath específico
        print("\n📝 Agregando descripción con XPath específico...")
        
        # Limpiar descripción de caracteres problemáticos
        descripcion_limpia = descripcion
        try:
            # Convertir emojis y caracteres especiales a texto ASCII seguro
            descripcion_limpia = descripcion.encode('ascii', 'ignore').decode('ascii')
            if len(descripcion_limpia) < 20:  # Si se perdió mucho contenido, usar versión simple
                descripcion_limpia = "Contenido EPICO que te va a SORPRENDER! No puedes perderte esta increible experiencia viral que esta rompiendo TikTok. Dale LIKE si te gusto y COMPARTE con tus amigos! Preparate para algo que jamas has visto antes... Estas listo? #fyp #viral #trending #amazing #foryou"
        except:
            descripcion_limpia = "Contenido EPICO que te va a SORPRENDER! No puedes perderte esta increible experiencia viral que esta rompiendo TikTok. Dale LIKE si te gusto y COMPARTE con tus amigos! Preparate para algo que jamas has visto antes... Estas listo? #fyp #viral #trending #amazing #foryou"
        
        print(f"   📝 Descripción limpia preparada: {len(descripcion_limpia)} caracteres")
        
        # XPath específico del campo de descripción proporcionado por el usuario
        xpath_descripcion = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]'
        
        descripcion_agregada = False
        
        # Intentar primero con XPath específico
        try:
            print(f"🎯 Usando XPath específico para descripción:")
            print(f"   {xpath_descripcion}")
            
            desc_element = driver.find_element(By.XPATH, xpath_descripcion)
            
            if desc_element.is_displayed():
                print(f"   📍 Campo de descripción encontrado con XPath específico")
                
                # Hacer focus y limpiar completamente
                driver.execute_script("arguments[0].focus();", desc_element)
                time.sleep(1)
                
                print("   🧹 Limpiando campo con XPath específico...")
                
                # Limpiar completamente con múltiples métodos
                driver.execute_script("""
                    var element = arguments[0];
                    element.focus();
                    element.select();
                    element.value = '';
                    element.textContent = '';
                    element.innerHTML = '';
                    element.innerText = '';
                """, desc_element)
                time.sleep(1)
                
                # Seleccionar todo y borrar
                desc_element.send_keys(Keys.CONTROL + "a")
                time.sleep(0.5)
                desc_element.send_keys(Keys.DELETE)
                time.sleep(0.5)
                desc_element.send_keys(Keys.BACKSPACE)
                time.sleep(1)
                
                # Verificar que está limpio
                texto_actual = driver.execute_script("return arguments[0].value || arguments[0].textContent || arguments[0].innerText;", desc_element)
                print(f"   🔍 Texto restante: '{texto_actual}'")
                
                # Si aún hay texto, limpiar más agresivamente
                if texto_actual and len(texto_actual.strip()) > 0:
                    print("   🧹 Limpieza adicional...")
                    for _ in range(50):  # Borrar hasta 50 caracteres
                        desc_element.send_keys(Keys.BACKSPACE)
                        time.sleep(0.01)
                
                # Insertar nuestra descripción
                print("   ⌨️ Insertando nueva descripción con XPath específico...")
                driver.execute_script("""
                    var element = arguments[0];
                    var text = arguments[1];
                    element.value = text;
                    element.textContent = text;
                    element.innerText = text;
                    
                    // Disparar eventos
                    element.dispatchEvent(new Event('input', {bubbles: true}));
                    element.dispatchEvent(new Event('change', {bubbles: true}));
                    element.dispatchEvent(new Event('keyup', {bubbles: true}));
                    element.dispatchEvent(new Event('focus', {bubbles: true}));
                """, desc_element, descripcion_limpia)
                
                time.sleep(2)
                
                # Verificar inserción
                texto_final = driver.execute_script("return arguments[0].value || arguments[0].textContent || arguments[0].innerText;", desc_element)
                
                if texto_final and len(texto_final.strip()) > 10:
                    print("✅ Descripción agregada correctamente con XPath específico")
                    print(f"   📝 Caracteres insertados: {len(texto_final)}")
                    print(f"   📄 Contenido: {texto_final[:100]}...")
                    descripcion_agregada = True
                else:
                    print("   ⚠️ Fallback: Intentando con send_keys...")
                    # Fallback con send_keys
                    desc_element.click()
                    time.sleep(1)
                    desc_element.send_keys(descripcion_limpia)
                    time.sleep(2)
                    
                    texto_final = driver.execute_script("return arguments[0].value || arguments[0].textContent;", desc_element)
                    if texto_final and len(texto_final.strip()) > 10:
                        print("✅ Descripción agregada con send_keys")
                        descripcion_agregada = True
            else:
                print("   ❌ Campo de descripción no visible con XPath específico")
                
        except NoSuchElementException:
            print("   ❌ Campo de descripción no encontrado con XPath específico")
        except Exception as e:
            print(f"   ❌ Error con XPath específico de descripción: {e}")
        
        # Si el XPath específico falló, usar selectores genéricos
        if not descripcion_agregada:
            print("\n🔄 Intentando con selectores genéricos...")
            desc_selectors = [
                "//textarea[contains(@placeholder, 'escrib')] | //textarea[contains(@placeholder, 'Describ')]",
                "//div[@contenteditable='true']",
                "//textarea[@data-test='description-input']",
                "//div[contains(@class, 'description')]//textarea",
                "//div[contains(@class, 'caption')]//textarea",
                "//textarea",
                "//div[@contenteditable]"
            ]
        
            for selector in desc_selectors:
                try:
                desc_element = driver.find_element(By.XPATH, selector)
                if desc_element.is_displayed():
                    print(f"   📍 Campo de descripción encontrado")
                    
                    # Hacer focus y seleccionar todo
                    driver.execute_script("arguments[0].focus();", desc_element)
                    time.sleep(1)
                    
                    # Limpiar completamente el campo de múltiples maneras
                    print("   🧹 Limpiando campo de descripción...")
                    
                    # Método 1: Seleccionar todo y borrar con JavaScript
                    driver.execute_script("""
                        arguments[0].focus();
                        arguments[0].select();
                        arguments[0].value = '';
                        arguments[0].textContent = '';
                        arguments[0].innerHTML = '';
                    """, desc_element)
                    time.sleep(1)
                    
                    # Método 2: Usar Ctrl+A y Delete
                    desc_element.send_keys(Keys.CONTROL + "a")
                    time.sleep(0.5)
                    desc_element.send_keys(Keys.DELETE)
                    time.sleep(0.5)
                    desc_element.send_keys(Keys.BACKSPACE)
                    time.sleep(1)
                    
                    # Método 3: Clear tradicional
                    try:
                        desc_element.clear()
                    except:
                        pass
                    time.sleep(1)
                    
                    # Verificar que está limpio
                    texto_actual = driver.execute_script("return arguments[0].value || arguments[0].textContent || arguments[0].innerHTML;", desc_element)
                    print(f"   🔍 Texto restante después de limpiar: '{texto_actual[:50]}...'")
                    
                    # Si aún hay texto, limpiar caracter por caracter
                    if texto_actual and len(texto_actual.strip()) > 0:
                        print("   🧹 Limpieza adicional caracter por caracter...")
                        for _ in range(len(texto_actual) + 10):
                            desc_element.send_keys(Keys.BACKSPACE)
                            time.sleep(0.01)
                    
                    # Insertar nuestra descripción con JavaScript
                    print("   ⌨️ Insertando nueva descripción...")
                    driver.execute_script("""
                        arguments[0].value = arguments[1];
                        arguments[0].textContent = arguments[1];
                        arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                        arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                        arguments[0].dispatchEvent(new Event('keyup', {bubbles: true}));
                    """, desc_element, descripcion_limpia)
                    
                    time.sleep(2)
                    
                    # Verificar que se insertó correctamente
                    texto_final = driver.execute_script("return arguments[0].value || arguments[0].textContent;", desc_element)
                    
                    if texto_final and len(texto_final.strip()) > 10:
                        print("✅ Descripción agregada correctamente con JavaScript")
                        print(f"   📝 Caracteres insertados: {len(texto_final)}")
                        print(f"   📄 Contenido: {texto_final[:100]}...")
                        descripcion_agregada = True
                        break
                    else:
                        print("   ⚠️ Reintentando con send_keys...")
                        # Fallback: enviar con send_keys
                        desc_element.click()
                        time.sleep(1)
                        desc_element.send_keys(descripcion_limpia)
                        time.sleep(2)
                        
                        texto_final = desc_element.get_attribute('value') or desc_element.text
                        if texto_final and len(texto_final.strip()) > 10:
                            print("✅ Descripción agregada con send_keys")
                            descripcion_agregada = True
                            break
                            
            except NoSuchElementException:
                continue
            except Exception as e:
                print(f"   ⚠️ Error con descripción: {str(e)[:100]}")
                continue
        
        # Screenshot pre-publicación
        timestamp = int(time.time())
        driver.save_screenshot(f"selenium_xpaths_pre_publish_{timestamp}.png")
        print(f"📸 Screenshot pre-publicación: selenium_xpaths_pre_publish_{timestamp}.png")
        
        # Esperar 30 segundos
        print("\n⏳ ESPERANDO 30 SEGUNDOS ANTES DE PUBLICAR...")
        for i in range(6):
            print(f"   ⏰ {30 - i*5} segundos restantes...")
            movimiento_humano_realista(driver)
            time.sleep(5)
        
        # Buscar botón Post con XPath específico del usuario
        print("\n🚀 BUSCANDO BOTÓN POST CON XPATH ESPECÍFICO...")
        
        xpath_post_button = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[5]/div/button[1]/div[2]'
        publish_success = False
        
        try:
            print(f"🎯 Usando XPath específico para Post Button:")
            print(f"   {xpath_post_button}")
            
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
                
                # Manejo de modales
                print("   🔍 Verificando resultado después del click...")
                time.sleep(5)
                
                # Detectar diferentes tipos de modal/respuesta
                modal_detected = False
                
                # 1. Buscar modal de éxito
                try:
                    success_modals = driver.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'posted') or contains(text(), 'published') or contains(text(), 'Your video') or contains(text(), 'Video uploaded')]")
                    if any(modal.is_displayed() for modal in success_modals):
                        print("✅ Modal de éxito detectado - Video publicado!")
                        modal_detected = True
                        publish_success = True
                except:
                    pass
                
                # 2. Buscar modal de error
                try:
                    error_modals = driver.find_elements(By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'failed') or contains(text(), 'try again') or contains(text(), 'something went wrong')]")
                    if any(modal.is_displayed() for modal in error_modals):
                        print("❌ Modal de error detectado")
                        modal_detected = True
                except:
                    pass
                
                # 3. Si no hay modal, verificar cambio de URL
                if not modal_detected:
                    time.sleep(3)
                    current_url = driver.current_url
                    if 'upload' not in current_url or 'success' in current_url or 'creator' in current_url:
                        print("✅ URL cambió - Video posiblemente publicado")
                        publish_success = True
                    else:
                        print("✅ Click realizado - Esperando confirmación...")
                        time.sleep(5)
                        # Verificar una vez más
                        current_url = driver.current_url
                        if 'upload' not in current_url:
                            print("✅ Navegación completada - Video publicado")
                            publish_success = True
                
        except NoSuchElementException:
            print("   ❌ Botón Post no encontrado con XPath específico")
        except Exception as e:
            print(f"   ❌ Error con XPath específico de Post: {e}")
        
        # Si el XPath específico falló, intentar selectores genéricos
        if not publish_success:
            print("\n🔄 Intentando con selectores genéricos como respaldo...")
            
            publish_selectors = [
                "//button[contains(text(), 'Post')]",
                "//button[contains(text(), 'Publicar')]",
                "//button[@type='submit']"
            ]
            
            for selector in publish_selectors:
                try:
                    publish_button = driver.find_element(By.XPATH, selector)
                    
                    is_visible = publish_button.is_displayed()
                    is_enabled = publish_button.is_enabled()
                    text_content = publish_button.text
                    
                    print(f"   📍 Botón genérico encontrado: '{text_content}' - Visible: {is_visible}, Habilitado: {is_enabled}")
                    
                    if is_visible and is_enabled:
                        print("   🖱️ Realizando click con selector genérico...")
                        driver.execute_script("arguments[0].click();", publish_button)
                        print("✅ Botón Post clickeado (genérico)")
                        publish_success = True
                        time.sleep(5)
                        break
                        
                except NoSuchElementException:
                    continue
        
        if publish_success:
            print("✅ Video publicado exitosamente")
            time.sleep(10)
            return True
        else:
            print("❌ No se pudo encontrar el botón Post")
            driver.save_screenshot(f"selenium_xpaths_no_post_button_{int(time.time())}.png")
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
    descripcion = """Contenido EPICO que te va a SORPRENDER! 

No puedes perderte esta increible experiencia viral que esta rompiendo TikTok
Dale LIKE si te gusto y COMPARTE con tus amigos!

Preparate para algo que jamas has visto antes... Estas listo?

#fyp #viral #trending #amazing #foryou"""
    
    resultado = subir_video_ultra_stealth_selenium_xpaths(video_path, descripcion)
    
    if resultado:
        print("\n🎉 ¡UPLOAD COMPLETADO EXITOSAMENTE!")
    else:
        print("\n❌ Upload falló")

if __name__ == "__main__":
    main()
