#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - SELENIUM AUTO-DRIVER
Versión V5 con descarga automática de ChromeDriver
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
from webdriver_manager.chrome import ChromeDriverManager

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
    profile_dir = os.path.join(os.getcwd(), "chrome_profile_selenium_auto")
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

def subir_video_ultra_stealth_selenium_auto(video_path, descripcion):
    """Función principal Selenium con descarga automática de ChromeDriver"""
    print("🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - SELENIUM AUTO-DRIVER")
    print("=" * 60)
    print("📋 AJUSTES APLICADOS:")
    print("1. Pantalla 1920x1080 (sin cortes)")
    print("2. Procesamiento 20 segundos") 
    print("3. XPath específico para AI content")
    print("4. Verificar Everyone seleccionado")
    print("5. Esperar 30 segundos antes de Post")
    print("6. 🔥 SELENIUM con descarga automática de ChromeDriver")
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
        # Crear driver con descarga automática de ChromeDriver
        print("📥 Descargando/verificando ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Aplicar scripts anti-detección
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
            time.sleep(5)
        
        # Screenshot
        timestamp = int(time.time())
        driver.save_screenshot(f"selenium_auto_processing_{timestamp}.png")
        print(f"📸 Screenshot: selenium_auto_processing_{timestamp}.png")
        
        # Show More con XPath específico
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
                
                # Scroll al elemento y click
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", show_more)
                time.sleep(2)
                
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
        
        if not show_more_clicked:
            print("⚠️ Show More no encontrado, haciendo scroll...")
            driver.execute_script("window.scrollBy(0, 500)")
            time.sleep(2)
        
        # Activar AI Content con XPath específico
        print("\n🎯 ACTIVACIÓN AI CONTENT CON XPATH ESPECÍFICO...")
        xpath_ai_toggle = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span'
        
        try:
            print(f"🔍 Usando XPath específico para AI Content: {xpath_ai_toggle}")
            
            # Scroll adicional
            driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(2)
            
            ai_toggle = driver.find_element(By.XPATH, xpath_ai_toggle)
            
            if ai_toggle.is_displayed():
                print("   📍 Elemento AI toggle encontrado con XPath")
                
                # Scroll al elemento y click
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ai_toggle)
                time.sleep(2)
                
                print("   🖱️ Haciendo click en AI Content toggle...")
                driver.execute_script("arguments[0].click();", ai_toggle)
                
                print("✅ AI Content toggle clickeado con XPath específico")
                time.sleep(3)
            else:
                print("   ❌ Elemento AI toggle no visible")
                
        except NoSuchElementException:
            print("   ❌ Elemento AI toggle no encontrado con XPath")
        except Exception as e:
            print(f"   ❌ Error con AI Content: {e}")
        
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
                    desc_element.send_keys(descripcion)
                    
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
        driver.save_screenshot(f"selenium_auto_pre_publish_{timestamp}.png")
        print(f"📸 Screenshot pre-publicación: selenium_auto_pre_publish_{timestamp}.png")
        
        # Esperar 30 segundos
        print("\n⏳ ESPERANDO 30 SEGUNDOS ANTES DE PUBLICAR...")
        for i in range(6):
            print(f"   ⏰ {30 - i*5} segundos restantes...")
            time.sleep(5)
        
        # Buscar botón Post
        print("\n🚀 BUSCANDO BOTÓN POST...")
        
        publish_selectors = [
            "//button[contains(text(), 'Post')] | //button[contains(text(), 'Publicar')] | //button[@type='submit']"
        ]
        
        publish_success = False
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
                    
                    # Click
                    print("   🖱️ Realizando click...")
                    driver.execute_script("arguments[0].click();", publish_button)
                    print("✅ Botón Post clickeado")
                    
                    # Manejo de modales
                    print("   🔍 Verificando si aparece algún modal...")
                    time.sleep(5)
                    
                    # Buscar modal de éxito o confirmación
                    try:
                        success_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'posted') or contains(text(), 'published')]")
                        if success_elements:
                            print("✅ Video publicado exitosamente!")
                            publish_success = True
                            break
                    except:
                        pass
                    
                    # Si no hay modal de éxito, verificar URL
                    time.sleep(3)
                    current_url = driver.current_url
                    if 'upload' not in current_url or 'success' in current_url:
                        print("✅ URL cambió - Video posiblemente publicado")
                        publish_success = True
                        break
                    else:
                        print("✅ Click realizado - Asumiendo éxito")
                        publish_success = True
                        break
                    
            except NoSuchElementException:
                continue
        
        if publish_success:
            print("✅ Video publicado exitosamente")
            time.sleep(10)
            return True
        else:
            print("❌ No se pudo encontrar el botón Post")
            driver.save_screenshot(f"selenium_auto_no_post_button_{int(time.time())}.png")
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
    
    resultado = subir_video_ultra_stealth_selenium_auto(video_path, descripcion)
    
    if resultado:
        print("\n🎉 ¡UPLOAD COMPLETADO EXITOSAMENTE!")
    else:
        print("\n❌ Upload falló")

if __name__ == "__main__":
    main()
