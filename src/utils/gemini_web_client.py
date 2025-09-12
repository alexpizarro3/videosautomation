import json
import os
import random
import re
import time
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

class GeminiWebClient:
    """
    Un cliente para interactuar con la interfaz web de Gemini (gemini.google.com/app)
    usando Selenium, como reemplazo de las llamadas a la API.
    """
    def __init__(self, profile_path: str = "config/chrome_profile", download_dir: str = "data/downloads"):
        self.profile_path = os.path.abspath(profile_path)
        self.driver = None
        self.download_dir = os.path.abspath(download_dir)
        os.makedirs(self.profile_path, exist_ok=True)
        os.makedirs(self.download_dir, exist_ok=True)

    def _launch_browser(self):
        """Inicia Selenium y el navegador si aún no están activos."""
        if self.driver:
            return

        print("[GeminiWebClient] Iniciando navegador con Selenium...")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
        
        prefs = {"download.default_directory": self.download_dir}
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print("[GeminiWebClient] Navegando a Gemini...")
        self.driver.get("https://gemini.google.com/app")
        self._human_delay(2, 3)

        print("[GeminiWebClient] Verificando estado de la sesión...")
        try:
            session_selectors = [
                'a[aria-label*="Cuenta de Google"]',
                'a[aria-label*="Google Account"]',
            ]
            
            session_confirmed = any(
                self.driver.find_elements(By.CSS_SELECTOR, selector) for selector in session_selectors
            )
            
            if not session_confirmed:
                 raise ConnectionError("No se pudo confirmar la sesión con ningún selector conocido.")

            print("[GeminiWebClient] ✅ Sesión de usuario activa confirmada.")

        except (ConnectionError, TimeoutException):
            print("\n" + "="*60)
            print("[GeminiWebClient] ❌ ¡ACCIÓN REQUERIDA! No se detectó una sesión activa.")
            print("   Por favor, inicia sesión manualmente en la ventana de Chrome que se ha abierto.")
            print("   La sesión se guardará para futuras ejecuciones.")
            print("="*60 + "\n")
            input(">> Presiona Enter aquí después de haber iniciado sesión para continuar...")
            raise ConnectionError("Se requiere inicio de sesión manual. Por favor, vuelve a ejecutar el script.")

        print("[GeminiWebClient] Verificando que el chat esté habilitado...")
        try:
            prompt_box_selector = 'div[contenteditable="true"][role="textbox"]'
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, prompt_box_selector)))
            print("[GeminiWebClient] ✅ ¡Chat listo para usarse!")
        except TimeoutException:
            print("[GeminiWebClient] ❌ ¡ERROR! El chat no se habilitó.")
            raise ConnectionError("La UI de Gemini no se inicializó correctamente.")

    def close(self):
        """Cierra el navegador."""
        if self.driver:
            self.driver.quit()
            self.driver = None
        print("[GeminiWebClient] Navegador cerrado.")

    def _human_delay(self, min_seconds=0.5, max_seconds=1.5):
        """Introduce un retraso aleatorio."""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def _type_like_human(self, element, text: str):
        """
        Usa JavaScript para pegar el texto directamente en el elemento,
        lo que es más rápido y fiable para prompts largos.
        """
        self.driver.execute_script("arguments[0].textContent = arguments[1];", element, text)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
        self._human_delay(0.5, 1)

    def generate_text(self, prompt: str) -> str:
        """Genera una respuesta de texto a partir de un prompt."""
        self._launch_browser()
        print(f"[GeminiWebClient] Generando texto para prompt: '{prompt[:50]}...'")

        send_button_selector = '//button[.//mat-icon[@fonticon="send"]]'
        stop_button_selector = '//button[.//mat-icon[@fonticon="stop"]]'
        prompt_box_selector = 'div[contenteditable="true"][role="textbox"]'

        # 1. Localizar y escribir en el cuadro de texto
        wait = WebDriverWait(self.driver, 10)
        prompt_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, prompt_box_selector)))
        self._type_like_human(prompt_box, prompt)
        self._human_delay()

        # 2. Localizar el botón de enviar y hacer clic
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_selector)))
        send_button.click()

        # 3. Esperar el ciclo de 3 pasos: Stop aparece -> Stop desaparece -> Send reaparece
        print("[GeminiWebClient] Esperando el ciclo de generación completo...")
        try:
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, stop_button_selector)))
            print("[GeminiWebClient] -> Paso 1/3: Generación iniciada.")
            WebDriverWait(self.driver, 120).until(EC.invisibility_of_element_located((By.XPATH, stop_button_selector)))
            print("[GeminiWebClient] -> Paso 2/3: Generación finalizada.")
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, send_button_selector)))
            print("[GeminiWebClient] -> Paso 3/3: UI restaurada.")
        except TimeoutException:
            print("[GeminiWebClient] ⚠️ No se completó el ciclo de generación de 3 pasos.")
            return ""

        # --- Extracción de texto ---
        print("[GeminiWebClient] Extrayendo texto...")
        raw_response_text = ""
        try:
            # Plan A: Usar el botón Copiar y la API del portapapeles
            print("[GeminiWebClient] -> Intentando Plan A: Extracción por Portapapeles...")
            copy_button_selector = '//button[.//mat-icon[@fonticon="content_copy"]]' # Selector corregido
            
            all_copy_buttons = self.driver.find_elements(By.XPATH, copy_button_selector)
            if not all_copy_buttons:
                raise Exception("No se encontró el botón de copiar.")
            
            last_copy_button = all_copy_buttons[-1]

            print("[GeminiWebClient] -> Esperando 5s antes de hacer clic en Copiar...")
            time.sleep(5)

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(last_copy_button))
            last_copy_button.click()
            
            print("[GeminiWebClient] -> Botón Copiar presionado. Esperando 5s después...")
            time.sleep(5)
            
            raw_response_text = self.driver.execute_script("return navigator.clipboard.readText();")
            if not raw_response_text:
                 raise Exception("La API del portapapeles no devolvió texto.")
            print("[GeminiWebClient] -> Éxito del Plan A: Texto extraído del portapapeles.")

        except Exception as e:
            print(f"[GeminiWebClient] ⚠️ Plan A fallido: {e}")
            print("[GeminiWebClient] -> Intentando Plan B: Lectura directa del contenedor.")
            try:
                time.sleep(2)
                response_selector = "div.markdown"
                all_responses = self.driver.find_elements(By.CSS_SELECTOR, response_selector)
                if not all_responses:
                     raise Exception("No se encontró el contenedor de la respuesta.")
                last_response_element = all_responses[-1]
                raw_response_text = last_response_element.get_attribute('textContent')
                print("[GeminiWebClient] -> Éxito del Plan B: Texto extraído del div.")
            except Exception as e2:
                print(f"[GeminiWebClient] ❌ Plan B fallido: {e2}")
                return ""

        if not raw_response_text or not raw_response_text.strip():
            print("[GeminiWebClient] ⚠️ Advertencia: El texto final extraído está vacío.")
            return ""

        # Limpieza final del texto por si acaso incluye los marcadores de JSON
        if '```json' in raw_response_text:
            raw_response_text = raw_response_text.split('```json')[1].split('```')[0]
        elif '```' in raw_response_text:
            raw_response_text = raw_response_text.split('```')[1]

        print("[GeminiWebClient] Respuesta de texto final procesada.")
        return raw_response_text.strip()

    def generate_image(self, prompt: str, output_dir: str = "data/images") -> str:
        """Genera una imagen a partir de un prompt."""
        self._launch_browser()
        print(f"[GeminiWebClient] Generando imagen para prompt: '{prompt[:50]}...'")

        try:
            image_button_selector = 'button[aria-label*="imagen"]'
            self.driver.find_element(By.CSS_SELECTOR, image_button_selector).click()
            self._human_delay()

            prompt_box_selector = 'div[contenteditable="true"][role="textbox"]'
            prompt_box = self.driver.find_element(By.CSS_SELECTOR, prompt_box_selector)
            self._type_like_human(prompt_box, prompt)
            prompt_box.send_keys(webdriver.common.keys.Keys.ENTER)

            generated_image_selector = "img.generated-image"
            WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.CSS_SELECTOR, generated_image_selector)))

            download_button_selector = 'button[aria-label*="Descargar"]'
            all_download_buttons = self.driver.find_elements(By.CSS_SELECTOR, download_button_selector)
            all_download_buttons[-1].click()
            
            downloaded_file = self._wait_for_download(self.download_dir)
            if not downloaded_file:
                raise Exception("La descarga de la imagen falló.")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_image_path = Path(output_dir) / f"gemini_web_{timestamp}.png"
            os.rename(downloaded_file, final_image_path)

            print(f"[GeminiWebClient] Imagen guardada en: {final_image_path}")
            return str(final_image_path)

        except Exception as e:
            print(f"[GeminiWebClient] ❌ Error generando imagen: {e}")
            raise

    def _wait_for_download(self, download_path, timeout=60):
        """Espera a que un archivo termine de descargarse."""
        seconds = 0
        while seconds < timeout:
            for fname in os.listdir(download_path):
                if fname.endswith('.crdownload'):
                    time.sleep(1)
                    seconds += 1
                    break
            else:
                time.sleep(1)
                files = sorted(Path(download_path).iterdir(), key=os.path.getmtime)
                if files:
                    return str(files[-1])
        return None
