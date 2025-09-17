
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_stealth_chrome_drive():
    """Configurar Chrome con anti-detección para Google Drive."""
    print("🛡️ Configurando Chrome con anti-detección para Google Drive...")
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    profile_dir = os.path.join(os.getcwd(), "chrome_profile_selenium_drive")
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    options.add_argument(f'--user-data-dir={profile_dir}')
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options

def upload_file_to_drive(driver, file_path, folder_id):
    """Sube un único archivo a una carpeta específica de Google Drive."""
    try:
        print(f"\n🚀 Subiendo {os.path.basename(file_path)} a la carpeta {folder_id}...")
        folder_url = f"https://drive.google.com/drive/u/0/folders/{folder_id}"
        driver.get(folder_url)
        time.sleep(5)

        # Hacer clic en el botón 'Nuevo'
        new_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Nuevo')]" ))
        )
        new_button.click()
        time.sleep(2)

        # Seleccionar 'Subir archivo'
        upload_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Subir archivo']"))
        )
        upload_option.click()
        time.sleep(3)

        # Aquí es donde se complica, porque se abre un diálogo del sistema operativo.
        # La solución estándar es usar una librería como pyautogui o autoit, 
        # pero una alternativa es encontrar un input de archivo oculto si existe.
        # Por ahora, asumimos que el diálogo del SO no se puede automatizar directamente
        # y buscamos un input de archivo.
        
        # Este es un enfoque alternativo que a veces funciona:
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        file_input.send_keys(os.path.abspath(file_path))

        # Esperar a que la subida se complete
        print("⏳ Esperando a que la subida se complete...")
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'subida completa')]" ))
        )
        print(f"✅ Archivo {os.path.basename(file_path)} subido exitosamente.")
        time.sleep(5) # Dar tiempo para que se cierre la notificación
        return True

    except TimeoutException as e:
        print(f"❌ Error de tiempo de espera subiendo {os.path.basename(file_path)}: {e}")
        driver.save_screenshot(f"debug_drive_upload_error_{int(time.time())}.png")
        return False
    except Exception as e:
        print(f"❌ Error inesperado subiendo {os.path.basename(file_path)}: {e}")
        driver.save_screenshot(f"debug_drive_upload_error_{int(time.time())}.png")
        return False
