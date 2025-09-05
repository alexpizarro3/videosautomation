#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V5 - SELENIUM XPATHS DEFINITIVOS
Versión con todos los XPaths específicos proporcionados por el usuario:
- Show More: //*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[3]/div/span[1]
- AI Content: //*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span
- Descripción: //*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]
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
        actions = ActionChains(driver)
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        actions.move_by_offset(x, y).perform()
        time.sleep(random.uniform(0.5, 1.5))
    except:
        pass

def cargar_cookies(driver, cookies_path):
    """Cargar cookies de sesión"""
    try:
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
        
        driver.get("https://www.tiktok.com")
        time.sleep(3)
        
        cookies_loaded = 0
        for cookie in cookies:
            try:
                selenium_cookie = {
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie.get('domain', '.tiktok.com'),
                    'path': cookie.get('path', '/'),
                }
                
                if 'secure' in cookie:
                    selenium_cookie['secure'] = cookie['secure']
                if 'httpOnly' in cookie:
                    selenium_cookie['httpOnly'] = cookie['httpOnly']
                
                driver.add_cookie(selenium_cookie)
                cookies_loaded += 1
            except Exception as e:
                print(f"   ⚠️ Error con cookie {cookie.get('name', 'unknown')}: {e}")
                continue
        
        print(f"✅ Cookies cargadas: {cookies_loaded}/{len(cookies)}")
        return True
    except Exception as e:
        print(f"❌ Error cargando cookies: {e}")
        return False

def setup_stealth_chrome():
    """Configurar Chrome con anti-detección"""
    print("🛡️ Configurando Chrome con anti-detección...")
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-first-run')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-infobars')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    profile_dir = os.path.join(os.getcwd(), "chrome_profile_selenium_final")
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    options.add_argument(f'--user-data-dir={profile_dir}')
    
    prefs = {
        "profile.default_content_setting_values": {"notifications": 2},
        "profile.managed_default_content_settings": {"images": 1}
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options

def subir_video_selenium_xpaths_definitivos(video_path, descripcion):
    """Función principal con XPaths definitivos"""
    print("🎯 UPLOADER TIKTOK - SELENIUM XPATHS DEFINITIVOS")
    print("=" * 60)
    print("📋 XPATHS ESPECÍFICOS:")
    print("1. Show More: //*[@id=\"root\"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[3]/div/span[1]")
    print("2. AI Content: //*[@id=\"root\"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span")
    print("3. Descripción: //*[@id=\"root\"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]")
    print("4. Post Button: //*[@id=\"root\"]/div/div/div[2]/div[2]/div/div/div/div[5]/div/button[1]/div[2]")
    print("=" * 60)
    
    cookies_path = "config/upload_cookies_playwright.json"
    
    if not os.path.exists(video_path):
        print(f"❌ Archivo no encontrado: {video_path}")
        return False
    
    file_size = os.path.getsize(video_path) / (1024*1024)
    print(f"📹 Video: {video_path}")
    print(f"📏 Tamaño: {file_size:.1f} MB")
    
    # Limpiar descripción
    descripcion_limpia = descripcion.encode('ascii', 'ignore').decode('ascii')
    if len(descripcion_limpia) < 20:
        descripcion_limpia = "Contenido EPICO! No te pierdas esta experiencia viral #fyp #viral #trending"
    
    options = setup_stealth_chrome()
    
    try:
        print("🚀 Iniciando ChromeDriver...")
        driver = webdriver.Chrome(options=options)
        
        # Anti-detección
        driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            window.chrome = {runtime: {}};
        """)
        
        driver.set_window_size(1920, 1080)
        driver.maximize_window()
        print("✅ Chrome configurado")
        
        # Cargar cookies y navegar
        cargar_cookies(driver, cookies_path)
        
        print("\n🌐 Navegando a Creator Center...")
        driver.get('https://www.tiktok.com/creator-center/upload')
        time.sleep(5)
        
        # Verificar login
        try:
            login_elements = driver.find_elements(By.XPATH, "//button[contains(text(), 'Log in')]")
            if any(el.is_displayed() for el in login_elements):
                print("⚠️ SE REQUIERE LOGIN MANUAL - Presiona Enter cuando estés listo...")
                input()
                driver.get('https://www.tiktok.com/creator-center/upload')
                time.sleep(3)
        except:
            pass
        
        # Esperar página de upload
        print("\n🔍 Esperando página de upload...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        print("✅ Página cargada")
        
        # Upload archivo
        print("\n📁 Cargando archivo...")
        file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
        
        for i, file_input in enumerate(file_inputs, 1):
            try:
                driver.execute_script("""
                    arguments[0].style.display = 'block';
                    arguments[0].style.visibility = 'visible';
                """, file_input)
                
                file_input.send_keys(os.path.abspath(video_path))
                time.sleep(2)
                print(f"✅ Archivo cargado con input #{i}")
                break
            except:
                continue
        
        # Procesamiento
        print("\n⏳ Procesamiento (20 segundos)...")
        for i in range(4):
            print(f"⏳ {i*5}/20s")
            time.sleep(5)
        
        # Show More con XPath específico
        print("\n🔍 Expandiendo opciones (Show More)...")
        xpath_show_more = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[3]/div/span[1]'
        
        try:
            driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(2)
            
            show_more = driver.find_element(By.XPATH, xpath_show_more)
            if show_more.is_displayed():
                driver.execute_script("arguments[0].click();", show_more)
                print("✅ Show More clickeado")
                time.sleep(3)
        except:
            print("❌ Show More no encontrado")
        
        # AI Content con XPath específico
        print("\n🎯 Activando AI Content...")
        xpath_ai = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div/div/span'
        
        try:
            ai_toggle = driver.find_element(By.XPATH, xpath_ai)
            if ai_toggle.is_displayed():
                driver.execute_script("arguments[0].click();", ai_toggle)
                print("✅ AI Content activado")
                time.sleep(3)
                
                # MANEJO MEJORADO DEL MODAL DE AI CONTENT
                print("   🔍 Buscando modal de confirmación AI Content...")
                time.sleep(2)
                
                modal_found = False
                
                # Buscar el modal primero
                modal_selectors = [
                    "//div[@role='dialog']",
                    "//*[contains(@class, 'modal')]",
                    "//*[contains(@class, 'Modal')]",
                    "//*[contains(@class, 'popup')]",
                    "//div[contains(@class, 'overlay')]"
                ]
                
                for modal_selector in modal_selectors:
                    try:
                        modal = driver.find_element(By.XPATH, modal_selector)
                        if modal.is_displayed():
                            modal_text = modal.text
                            print(f"   📍 Modal detectado: {modal_text[:100]}...")
                            modal_found = True
                            break
                    except:
                        continue
                
                if modal_found:
                    print("   🔄 Buscando botones de confirmación en el modal...")
                    
                    # Lista específica SOLO para confirmar AI Content (NO botones de publicación)
                    confirm_selectors = [
                        "//button[contains(text(), 'Aceptar')]",
                        "//button[contains(text(), 'Accept')]",
                        "//button[contains(text(), 'Continuar')]", 
                        "//button[contains(text(), 'Continue')]",
                        "//button[contains(text(), 'OK')]",
                        "//button[contains(text(), 'Confirm')]",
                        "//button[contains(text(), 'Got it')]",
                        "//button[contains(text(), 'Turn on')]",
                        "//button[contains(text(), 'Enable')]",
                        "//button[contains(text(), 'Activar')]",
                        "//button[contains(text(), 'Close')]",
                        "//button[contains(text(), 'Cerrar')]",
                        "//button[contains(@aria-label, 'Close')]",
                        "//button[contains(@class, 'close')]",
                        "//*[text()='×']",  # X para cerrar
                        "//div[@role='dialog']//button[contains(@class, 'primary') and not(contains(text(), 'Post')) and not(contains(text(), 'Upload'))]"
                    ]
                    
                    button_clicked = False
                    for selector in confirm_selectors:
                        try:
                            buttons = driver.find_elements(By.XPATH, selector)
                            for button in buttons:
                                if button.is_displayed() and button.is_enabled():
                                    button_text = button.text.strip()
                                    
                                    # FILTRAR BOTONES QUE NO QUEREMOS TOCAR
                                    if any(word in button_text.lower() for word in ['post', 'upload', 'publish', 'publicar']):
                                        print(f"   ⚠️ Saltando botón de publicación: '{button_text}'")
                                        continue
                                    
                                    print(f"   🎯 Intentando botón de confirmación: '{button_text}'")
                                    
                                    # Hacer click
                                    driver.execute_script("arguments[0].click();", button)
                                    time.sleep(2)
                                    
                                    # Verificar si el modal desapareció
                                    try:
                                        modal_check = driver.find_element(By.XPATH, modal_selector)
                                        if not modal_check.is_displayed():
                                            print(f"   ✅ Modal AI Content cerrado con: '{button_text}'")
                                            button_clicked = True
                                            break
                                    except:
                                        print(f"   ✅ Modal AI Content cerrado con: '{button_text}'")
                                        button_clicked = True
                                        break
                            
                            if button_clicked:
                                break
                        except:
                            continue
                    
                    if not button_clicked:
                        print("   ⚠️ Intentando cerrar modal con ESC...")
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                        time.sleep(2)
                        print("   ✅ Modal cerrado con ESC")
                    
                    time.sleep(2)
                else:
                    print("   ℹ️ No se detectó modal - AI Content puede estar ya activado")
                
        except Exception as e:
            print(f"❌ AI Content error: {e}")
            print("   🔄 Continuando sin AI Content...")
        
        # Descripción con XPath específico editable
        print("\n📝 Agregando descripción...")
        xpath_desc = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]'
        
        try:
            print(f"🎯 Usando XPath editable para descripción:")
            print(f"   {xpath_desc}")
            
            desc_element = driver.find_element(By.XPATH, xpath_desc)
            if desc_element.is_displayed():
                print("   📍 Campo editable encontrado")
                
                # Scroll al elemento para asegurar visibilidad
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", desc_element)
                time.sleep(2)
                
                # Hacer click para activar el campo
                print("   🖱️ Haciendo click para activar campo...")
                driver.execute_script("arguments[0].click();", desc_element)
                time.sleep(1)
                
                # Focus
                driver.execute_script("arguments[0].focus();", desc_element)
                time.sleep(1)
                
                print("   🧹 Limpiando campo editable...")
                
                # Seleccionar todo y borrar
                desc_element.send_keys(Keys.CONTROL + "a")
                time.sleep(0.5)
                desc_element.send_keys(Keys.DELETE)
                time.sleep(0.5)
                
                # Limpiar con backspace adicional
                for _ in range(50):
                    desc_element.send_keys(Keys.BACKSPACE)
                    time.sleep(0.01)
                
                # Verificar limpieza
                current_text = driver.execute_script("""
                    var el = arguments[0];
                    return el.textContent || el.innerText || el.value || '';
                """, desc_element)
                print(f"   🔍 Texto después de limpiar: '{current_text}'")
                
                print("   ⌨️ Insertando nueva descripción...")
                
                # Método 1: Insertar con JavaScript
                driver.execute_script("""
                    var el = arguments[0];
                    var text = arguments[1];
                    
                    // Limpiar completamente
                    el.textContent = '';
                    el.innerText = '';
                    
                    // Insertar nuevo texto
                    el.textContent = text;
                    el.innerText = text;
                    
                    // Disparar eventos
                    el.dispatchEvent(new Event('input', {bubbles: true, cancelable: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true, cancelable: true}));
                    el.dispatchEvent(new Event('keyup', {bubbles: true, cancelable: true}));
                """, desc_element, descripcion_limpia)
                
                time.sleep(2)
                
                # Verificar inserción con JavaScript
                texto_final = driver.execute_script("""
                    var el = arguments[0];
                    return el.textContent || el.innerText || el.value || '';
                """, desc_element)
                
                if texto_final and len(texto_final.strip()) > 10:
                    print(f"✅ Descripción agregada con JavaScript: {len(texto_final)} caracteres")
                    print(f"   📄 Contenido: {texto_final[:50]}...")
                else:
                    print("   ⚠️ Fallback: Usando send_keys...")
                    # Fallback: send_keys character by character
                    desc_element.click()
                    time.sleep(1)
                    
                    # Limpiar una vez más
                    desc_element.send_keys(Keys.CONTROL + "a")
                    desc_element.send_keys(Keys.DELETE)
                    time.sleep(1)
                    
                    # Enviar texto caracter por caracter
                    for char in descripcion_limpia:
                        desc_element.send_keys(char)
                        time.sleep(0.02)
                    
                    time.sleep(2)
                    
                    # Verificar con send_keys
                    texto_final = driver.execute_script("return arguments[0].textContent || arguments[0].innerText;", desc_element)
                    if texto_final and len(texto_final.strip()) > 10:
                        print(f"✅ Descripción agregada con send_keys: {len(texto_final)} caracteres")
                    else:
                        print("❌ No se pudo agregar descripción")
            else:
                print("   ❌ Campo no visible")
                
        except Exception as e:
            print(f"❌ Error con descripción: {e}")
            print("   🔄 Intentando con selectores alternativos...")
            
            # Fallback con selectores alternativos
            fallback_selectors = [
                "//div[@contenteditable='true']",
                "//textarea[contains(@placeholder, 'escrib')]",
                "//*[contains(@class, 'caption')]//div",
                "//*[contains(@class, 'description')]//div"
            ]
            
            for selector in fallback_selectors:
                try:
                    fallback_element = driver.find_element(By.XPATH, selector)
                    if fallback_element.is_displayed():
                        print(f"   📍 Elemento alternativo encontrado")
                        fallback_element.click()
                        time.sleep(1)
                        fallback_element.send_keys(Keys.CONTROL + "a")
                        fallback_element.send_keys(descripcion_limpia)
                        print("   ✅ Descripción agregada con selector alternativo")
                        break
                except:
                    continue
        
        # Screenshot
        driver.save_screenshot(f"pre_publish_{int(time.time())}.png")
        
        # Esperar antes de publicar
        print("\n⏳ Esperando 30 segundos...")
        for i in range(6):
            print(f"   {30-i*5}s restantes...")
            time.sleep(5)
        
        # Post con XPath específico
        print("\n🚀 Publicando video...")
        xpath_post = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[5]/div/button[1]/div[2]'
        
        try:
            post_button = driver.find_element(By.XPATH, xpath_post)
            if post_button.is_displayed() and post_button.is_enabled():
                print("   📍 Botón Post encontrado con XPath específico")
                driver.execute_script("arguments[0].click();", post_button)
                print("✅ Video publicado!")
                time.sleep(10)
                return True
            else:
                print("❌ Botón Post no disponible")
        except:
            print("❌ Botón Post no encontrado con XPath")
            
            # Fallback genérico
            try:
                post_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
                if post_btn.is_displayed():
                    driver.execute_script("arguments[0].click();", post_btn)
                    print("✅ Video publicado con selector genérico!")
                    time.sleep(10)
                    return True
            except:
                pass
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
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
    
    resultado = subir_video_selenium_xpaths_definitivos(video_path, descripcion)
    
    if resultado:
        print("\n🎉 ¡UPLOAD COMPLETADO EXITOSAMENTE!")
    else:
        print("\n❌ Upload falló")

if __name__ == "__main__":
    main()
