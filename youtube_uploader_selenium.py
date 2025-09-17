from dotenv import load_dotenv
load_dotenv()

import os
import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_stealth_chrome_youtube():
    """Configurar Chrome con anti-detección para YouTube."""
    print("Configurando Chrome con anti-detección para YouTube...")
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    profile_dir = os.path.join(os.getcwd(), "chrome_profile_selenium_youtube")
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    options.add_argument(f'--user-data-dir={profile_dir}')
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options

def load_youtube_cookies(driver):
    """Cargar cookies de sesión para YouTube."""
    cookies_path = "config/youtube_cookies.json"
    if not os.path.exists(cookies_path):
        print(f"Archivo de cookies no encontrado en {cookies_path}. Se requerirá login manual.")
        return False
        
    try:
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
        
        driver.get("https://www.youtube.com")
        time.sleep(2)
        
        for cookie in cookies:
            driver.add_cookie(cookie)
        
        print("Cookies de YouTube cargadas.")
        return True
    except Exception as e:
        print(f"Error cargando cookies de YouTube: {e}")
        return False

def login_to_google(driver):
    """Realiza el login en Google si es necesario."""
    email = os.getenv("YOUTUBE_EMAIL")
    password = os.getenv("YOUTUBE_PASSWORD")

    if not email or not password:
        print("Variables de entorno YOUTUBE_EMAIL y YOUTUBE_PASSWORD no configuradas.")
        return False

    try:
        print("Verificando si se necesita login...")
        if "accounts.google.com" in driver.current_url:
            print("Realizando login en Google...")
            
            # Ingresar email
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
            email_input.send_keys(email)
            driver.find_element(By.XPATH, "//button[.//span[text()='Next']]").click()
            time.sleep(random.uniform(2, 4))

            # Ingresar contraseña
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_input.send_keys(password)
            driver.find_element(By.XPATH, "//button[.//span[text()='Next']]").click()
            time.sleep(random.uniform(3, 5))
            
            print("Login exitoso.")
            driver.get("https://studio.youtube.com/channel/UCeL3EES7F5v_kDyiZz_F-6A") # Redirigir a Studio
            time.sleep(5)
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error durante el login: {e}")
        driver.save_screenshot("debug_login_error.png")
        return False

def subir_video_youtube_selenium(video_path, metadata):
    """Sube un video a YouTube usando Selenium."""
    print("Iniciando subida a YouTube con Selenium...")
    
    options = setup_stealth_chrome_youtube()
    driver = webdriver.Chrome(options=options)
    
    try:
        # No cargamos cookies, vamos directo al login si es necesario
        # load_youtube_cookies(driver) 
        
        print("Navegando a YouTube Studio...")
        driver.get("https://studio.youtube.com/channel/UCeL3EES7F5v_kDyiZz_F-6A")
        time.sleep(5)

        # Realizar login si es necesario
        if not login_to_google(driver):
            print("No se pudo completar el login. Abortando subida.")
            return False

        # Esperar a que la página principal de Studio cargue
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "create-icon"))
            )
            print("Página principal de YouTube Studio cargada.")
        except (TimeoutException, NoSuchElementException):
            print("No se pudo cargar la página principal de YouTube Studio.")
            driver.save_screenshot(f"debug_youtube_studio_load_error_{int(time.time())}.png")
            return False

        # Ya no es necesario cambiar de cuenta, el link directo selecciona el canal correcto



        # Buscar y hacer clic en el botón directo de subir videos en el panel de control
        print("Buscando botón directo de subir videos en el panel de control...")
        try:
            # Esperar y cerrar overlays/modals si aparecen
            time.sleep(2)
            for _ in range(3):
                try:
                    overlay = driver.find_element(By.CSS_SELECTOR, "tp-yt-iron-overlay-backdrop")
                    driver.execute_script("arguments[0].click();", overlay)
                    print("Overlay cerrado.")
                    time.sleep(1)
                except Exception:
                    break

            # Buscar el botón por id 'upload-icon' y hacer clic
            upload_icon_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "upload-icon"))
            )
            driver.execute_script("arguments[0].click();", upload_icon_button)
            print("Botón directo de subir videos clickeado (id='upload-icon').")
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error al buscar el botón directo de subida: {e}")
            driver.save_screenshot(f"debug_youtube_upload_direct_button_error_{int(time.time())}.png")
            return False
        time.sleep(2)

        # Subir archivo
        print("Seleccionando archivo de video...")
        file_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        file_input.send_keys(os.path.abspath(video_path))
        print("Esperando que el video se procese...")
        

        # Esperar a que aparezca el editor de detalles
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "//ytcp-video-metadata-editor"))
        )
        print("Video procesado. Rellenando detalles...")


        # Título (máx 99 caracteres, incluye hashtags)
        print("Buscando y llenando el título...")
        try:
            title_box = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='textbox' and @aria-label[contains(.,'título')]]"))
            )
            title_box.click()
            driver.execute_script("arguments[0].innerText = arguments[1];", title_box, metadata['title'][:95] + " #Shorts #Viral" if len(metadata['title']) < 90 else metadata['title'][:99])
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", title_box)
            print(f"✔ Título agregado: {metadata['title'][:95] + ' #Shorts #Viral' if len(metadata['title']) < 90 else metadata['title'][:99]}")
        except Exception as e:
            print(f"Error llenando título: {e}")
        time.sleep(1)

        # Descripción (máx 300 caracteres)
        print("Buscando y llenando la descripción...")
        try:
            description_box = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='textbox' and @aria-label[contains(.,'Cuenta a los usuarios')]]"))
            )
            description_box.click()
            description_box.send_keys(Keys.CONTROL + "a")
            description_box.send_keys(Keys.DELETE)
            descripcion_final = metadata['description'][:300]
            driver.execute_script("arguments[0].innerText = arguments[1];", description_box, descripcion_final)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", description_box)
            print(f"✔ Descripción agregada: {descripcion_final}")
        except Exception as e:
            print(f"Error llenando descripción: {e}")
        time.sleep(1)
        # Hacer clic en 'Siguiente' tres veces para avanzar a visibilidad
        print("Avanzando con tres clics en 'Siguiente'...")
        for i in range(3):
            try:
                next_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Siguiente')]] | //button[contains(text(),'Siguiente')]"))
                )
                driver.execute_script("arguments[0].click();", next_button)
                print(f"✔ Botón 'Siguiente' clickeado ({i+1}/3)")
                time.sleep(5)
            except Exception as e:
                print(f"Error al buscar/clickear el botón 'Siguiente' en paso {i+1}: {e}")

        # Marcar 'No, no está creado para niños'
        print("Buscando y marcando 'No, no está creado para niños'...")
        try:
            not_for_kids_radio = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-radio-button[@name='VIDEO_MADE_FOR_KIDS_NOT_MFK'] | //span[contains(text(),'No, no está creado para niños')]/ancestor::tp-yt-paper-radio-button"))
            )
            driver.execute_script("arguments[0].click();", not_for_kids_radio)
            print("✔ 'No está creado para niños' seleccionado.")
        except Exception as e:
            print(f"Error marcando 'No está creado para niños': {e}")
        time.sleep(1)



        # Configuración de audiencia: No es para niños
        print("Configurando audiencia: No es para niños...")
        try:
            not_for_kids_radio = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'No, no está creado para niños')]/ancestor::tp-yt-paper-radio-button | //tp-yt-paper-radio-button[@name='VIDEO_MADE_FOR_KIDS_NOT_MFK']"))
            )
            driver.execute_script("arguments[0].click();", not_for_kids_radio)
            print("✔ 'No está creado para niños' seleccionado.")
        except Exception as e:
            print(f"Error seleccionando audiencia: {e}")
        time.sleep(1)


        # Hacer clic en el botón 'Siguiente' con espera extra
        print("Esperando antes de buscar el botón 'Siguiente'...")
        time.sleep(2)
        print("Buscando y clickeando el botón 'Siguiente'...")
        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Siguiente')]] | //button[contains(text(),'Siguiente')]"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            print("✔ Botón 'Siguiente' clickeado.")
        except Exception as e:
            print(f"Error al buscar/clickear el botón 'Siguiente': {e}")
        time.sleep(2)


        # Clic adicional en 'Siguiente' antes de seleccionar 'Público'
        print("Clic adicional en 'Siguiente' antes de visibilidad...")
        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Siguiente')]] | //button[contains(text(),'Siguiente')]"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            print("✔ Botón 'Siguiente' clickeado (antes de visibilidad)")
            time.sleep(5)
        except Exception as e:
            print(f"Error al buscar/clickear el botón 'Siguiente' antes de visibilidad: {e}")


        # Seleccionar 'Público' y publicar
        print("Configurando visibilidad a 'Público'...")
        try:
            public_radio = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Público')]/ancestor::tp-yt-paper-radio-button | //tp-yt-paper-radio-button[@name='PUBLIC']"))
            )
            driver.execute_script("arguments[0].click();", public_radio)
            print("✔ Visibilidad 'Público' seleccionada.")
        except Exception as e:
            print(f"Error seleccionando visibilidad 'Público': {e}")
        time.sleep(2)

        # Hacer clic en 'Publicar'
        print("Buscando y clickeando el botón 'Publicar'...")
        try:
            publish_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Publicar')]] | //button[contains(text(),'Publicar')]"))
            )
            driver.execute_script("arguments[0].click();", publish_button)
            print("✔ Botón 'Publicar' clickeado.")
        except Exception as e:
            print(f"Error al buscar/clickear el botón 'Publicar': {e}")
        time.sleep(2)

        # Esperar confirmación
        try:
            WebDriverWait(driver, 180).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Video publicado')]"))
            )
            print("¡Video publicado en YouTube exitosamente!")
            return True
        except Exception as e:
            print(f"Error esperando confirmación de publicación: {e}")
            return False

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error de Selenium: No se pudo encontrar un elemento: {e}")
        driver.save_screenshot(f"debug_youtube_error_{int(time.time())}.png")
        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la subida a YouTube: {e}")
        driver.save_screenshot(f"debug_youtube_error_{int(time.time())}.png")
        return False
    finally:
        print("Cerrando navegador de YouTube.")
        driver.quit()


if __name__ == '__main__':
    print("Modo de prueba del subidor de YouTube con Selenium.")
    video_path = "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4"
    from upload_shorts_now import generar_metadata_youtube
    if os.path.exists(video_path):
        metadata = generar_metadata_youtube(video_path)
        subir_video_youtube_selenium(video_path, metadata)
    else:
        print(f"Video no encontrado: {video_path}")
