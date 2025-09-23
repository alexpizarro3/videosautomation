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

    def click_next_button(timeout=10):
        """Función auxiliar para hacer clic en el botón 'Siguiente'."""
        try:
            next_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.ID, "next-button"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            print("✔ Botón 'Siguiente' clickeado.")
            time.sleep(1) # Pequeña pausa para que la UI reaccione
            return True
        except Exception as e:
            print(f"Error al buscar/clickear el botón 'Siguiente': {e}")
            return False

    try:
        print("Navegando a YouTube Studio...")
        driver.get("https://studio.youtube.com/channel/UCeL3EES7F5v_kDyiZz_F-6A")
        time.sleep(2)

        if not login_to_google(driver):
            print("No se pudo completar el login. Abortando subida.")
            return False

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "create-icon")))
        print("Página principal de YouTube Studio cargada.")

        print("Buscando botón directo de subir videos...")
        upload_icon_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "upload-icon")))
        driver.execute_script("arguments[0].click();", upload_icon_button)
        print("Botón directo de subir videos clickeado.")
        
        file_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(os.path.abspath(video_path))
        print("Esperando que el video se procese...")

        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//ytcp-video-metadata-editor")))
        print("Video procesado. Rellenando detalles...")

        print("Buscando y llenando el título...")
        title_box = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='textbox' and @aria-label[contains(.,'título')]]")))
        title_box.click()
        driver.execute_script("arguments[0].innerText = arguments[1];", title_box, metadata['title'][:99])
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", title_box)
        print(f"✔ Título agregado: {metadata['title'][:99]}")

        print("Buscando y llenando la descripción...")
        description_box = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='textbox' and @aria-label[contains(.,'Cuenta a los usuarios')]]")))
        description_box.click()
        description_box.send_keys(Keys.CONTROL + "a")
        description_box.send_keys(Keys.DELETE)
        driver.execute_script("arguments[0].innerText = arguments[1];", description_box, metadata['description'][:4999])
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", description_box)
        print("✔ Descripción agregada.")

        print("Configurando audiencia: 'No, no está creado para niños'...")
        not_for_kids_radio = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME, "VIDEO_MADE_FOR_KIDS_NOT_MFK")))
        driver.execute_script("arguments[0].click();", not_for_kids_radio)
        print("✔ 'No está creado para niños' seleccionado.")

        # Avanzar por las siguientes 3 pantallas
        for i in range(3):
            print(f"Avanzando a la pantalla {i+2}/4...")
            if not click_next_button():
                # Si falla un clic, intentar de nuevo una vez más por si acaso
                time.sleep(3)
                click_next_button()

        print("Configurando visibilidad a 'Público'...")
        public_radio = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME, "PUBLIC")))
        driver.execute_script("arguments[0].click();", public_radio)
        print("✔ Visibilidad 'Público' seleccionada.")

        print("Buscando y clickeando el botón 'Publicar'...")
        publish_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "done-button")))
        driver.execute_script("arguments[0].click();", publish_button)
        print("✔ Botón 'Publicar' clickeado.")

        WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Video publicado')]")))
        print("¡Video publicado en YouTube exitosamente!")
        return True

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
