import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import time
import json

# Cargar credenciales de cuenta
with open('config/youtube_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)
account_email = creds['channel_verified']['email']
account_password = creds.get('channel_password', None)  # Debes agregar este campo manualmente si no existe

# Configuración Selenium


import tempfile
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option('prefs', {
    'profile.default_content_setting_values.notifications': 2
})
# Usar perfil temporal para evitar conflictos
temp_profile = tempfile.mkdtemp()
chrome_options.add_argument(f'--user-data-dir={temp_profile}')


# Inicializar driver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)



# Abrir YouTube Studio para cargar cookies
driver.get('https://studio.youtube.com/channel/UCeL3EES7F5v_kDyiZz_F-6A')
time.sleep(3)

# Cargar cookies SOLO, nunca intentar login manual
cookies_path = 'config/youtube_cookies.json'
cookies_loaded = False
if os.path.exists(cookies_path):
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    print("--- Cookies cargadas ---")
    for cookie in cookies:
        print(f"{cookie['name']} | domain: {cookie.get('domain', '')}")
        # Selenium requiere que el dominio coincida
        if 'domain' in cookie and 'studio.youtube.com' not in cookie['domain']:
            cookie['domain'] = 'studio.youtube.com'
        try:
            driver.add_cookie(cookie)
            cookies_loaded = True
        except Exception as e:
            print(f"[Cookie] Error: {e} -> {cookie}")
    print("--- Fin cookies ---")
    driver.refresh()
    time.sleep(3)
    # Verificar si la sesión está activa (por ejemplo, buscar el botón de subir video)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//ytcp-button[@id='create-icon']")))
        print('✅ Cookies de YouTube Studio válidas, sesión activa.')
    except Exception:
        print('❌ Las cookies no iniciaron sesión. Exporta cookies válidas desde studio.youtube.com con sesión activa.')
        driver.quit()
        exit(1)
else:
    print('❌ No se encontró config/youtube_cookies.json. Exporta cookies válidas desde studio.youtube.com.')
    driver.quit()
    exit(1)

# Ir a subir video
wait.until(EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='create-icon']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-item[@test-id='upload-video']"))).click()

# Seleccionar archivo
video_folder = Path('data/videos/final')
videos = list(video_folder.glob('*FUNDIDO*.mp4'))
if not videos:
    print('No se encontró ningún video FUNDIDO para subir.')
    driver.quit()
    exit(1)
video_path = str(videos[0].resolve())

upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
upload_input.send_keys(video_path)

# Esperar a que cargue el formulario
wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='title-textarea']")))

# Rellenar título y descripción
video_title = "ASMR Viral | Efectos Épicos #Shorts #Viral"
video_desc = "🔥 ¡Este contenido está EXPLOTANDO en todas las redes sociales! #Shorts #Viral #Trending"
driver.find_element(By.XPATH, "//textarea[@id='title-textarea']").clear()
driver.find_element(By.XPATH, "//textarea[@id='title-textarea']").send_keys(video_title)
driver.find_element(By.XPATH, "//textarea[@id='description-textarea']").clear()
driver.find_element(By.XPATH, "//textarea[@id='description-textarea']").send_keys(video_desc)

# Marcar "No es para niños"
wait.until(EC.element_to_be_clickable((By.NAME, 'VIDEO_MADE_FOR_KIDS_NOT_MADE_FOR_KIDS'))).click()

# Siguiente, siguiente, publicar
for _ in range(3):
    wait.until(EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='next-button']"))).click()
    time.sleep(1)

# Seleccionar "Público" y publicar
wait.until(EC.element_to_be_clickable((By.NAME, 'PUBLIC'))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='done-button']"))).click()

print('✅ Video subido a YouTube Shorts (Selenium)')
time.sleep(5)
driver.quit()
