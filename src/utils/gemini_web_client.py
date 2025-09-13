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

            print("[GeminiWebClient] [OK] Sesión de usuario activa confirmada.")

        except (ConnectionError, TimeoutException):
            print("\n" + "="*60)
            print("[GeminiWebClient] [ERROR] ¡ACCIÓN REQUERIDA! No se detectó una sesión activa.")
            print("   Por favor, inicia sesión manualmente en la ventana de Chrome que se ha abierto.")
            print("   La sesión se guardará para futuras ejecuciones.")
            print("="*60 + "\n")
            input(">> Presiona Enter aquí después de haber iniciado sesión para continuar...")
            raise ConnectionError("Se requiere inicio de sesión manual. Por favor, vuelve a ejecutar el script.")

        print("[GeminiWebClient] Verificando que el chat esté habilitado...")
        try:
            prompt_box_selector = 'div[contenteditable="true"][role="textbox"]'
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, prompt_box_selector)))
            print("[GeminiWebClient] [OK] ¡Chat listo para usarse!")
        except TimeoutException:
            print("[GeminiWebClient] [ERROR] ¡ERROR! El chat no se habilitó.")
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

    def _clear_download_directory(self):
        """Limpia el directorio de descargas para evitar conflictos."""
        print(f"[GeminiWebClient] -> Limpiando directorio de descargas: {self.download_dir}")
        for f in Path(self.download_dir).glob('*'):
            try:
                f.unlink()
            except OSError as e:
                print(f"[GeminiWebClient] [WARN] No se pudo eliminar el archivo {f}: {e}")

    def _send_prompt(self, prompt: str):
        """Método robusto para encontrar, limpiar, y enviar un prompt inyectando el texto con JS."""
        prompt_box_selector = 'div[contenteditable="true"][role="textbox"]'
        wait = WebDriverWait(self.driver, 10)
        
        print("[GeminiWebClient] -> Localizando el cuadro de prompt...")
        prompt_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, prompt_box_selector)))
        
        print("[GeminiWebClient] -> Haciendo clic y limpiando el cuadro...")
        self.driver.execute_script("arguments[0].click();", prompt_box)
        self._human_delay(0.2, 0.5)
        
        print("[GeminiWebClient] -> Inyectando el prompt completo con JavaScript...")
        # Usar JS para establecer el contenido es más rápido y fiable que send_keys o el portapapeles
        self.driver.execute_script("arguments[0].textContent = arguments[1];", prompt_box, prompt)
        self._human_delay(0.5, 1)

        # Pausa de 2 segundos solicitada por el usuario
        print("[GeminiWebClient] -> Esperando 2 segundos antes de enviar...")
        time.sleep(2)
        
        print("[GeminiWebClient] -> Enviando prompt con la tecla ENTER...")
        # Es necesario hacer clic de nuevo o enfocar el elemento antes de enviar Enter
        prompt_box.click()
        prompt_box.send_keys(Keys.ENTER)

    def _clean_json_response(self, text: str) -> str:
        """Intenta extraer un objeto JSON de una cadena de texto."""
        print(f"[GeminiWebClient] -> Limpiando texto para JSON: '{text[:100]}...'")
        try:
            start = text.index('{')
            end = text.rindex('}') + 1
            json_str = text[start:end]
            json.loads(json_str) # Validar
            print("[GeminiWebClient] -> JSON extraído por llaves {}.")
            return json_str
        except (ValueError, json.JSONDecodeError):
            try:
                if '```json' in text:
                    json_str = text.split('```json')[1].split('```')[0].strip()
                    json.loads(json_str) # Validar
                    print("[GeminiWebClient] -> JSON extraído por marcadores ```json.")
                    return json_str
                elif '```' in text:
                    json_str = text.split('```')[1].strip()
                    json.loads(json_str) # Validar
                    print("[GeminiWebClient] -> JSON extraído por marcadores ```.")
                    return json_str
            except (IndexError, json.JSONDecodeError):
                print("[GeminiWebClient] [WARN] No se pudo extraer JSON válido.")
                return text # Devolver texto original si todo falla
        return text

    def generate_text(self, prompt: str) -> str:
        """Genera una respuesta de texto a partir de un prompt."""
        self._launch_browser()
        print(f"[GeminiWebClient] Generando texto para prompt: '{prompt[:50]}...'")

        self._send_prompt(prompt)

        stop_button_selector = '//button[.//mat-icon[@fonticon="stop"]]'
        print("[GeminiWebClient] Esperando el ciclo de generación completo...")
        try:
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, stop_button_selector)))
            print("[GeminiWebClient] -> Paso 1/2: Generación iniciada.")
            WebDriverWait(self.driver, 120).until(EC.invisibility_of_element_located((By.XPATH, stop_button_selector)))
            print("[GeminiWebClient] -> Paso 2/2: Generación finalizada.")
        except TimeoutException:
            print("[GeminiWebClient] [WARN] No se completó el ciclo de generación.")
            return ""

        print("[GeminiWebClient] Extrayendo texto...")
        raw_response_text = ""
        try:
            print("[GeminiWebClient] -> Intentando Plan A: Extracción por Portapapeles...")
            copy_button_selector = '//button[.//mat-icon[@fonticon="content_copy"]]'
            last_copy_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, copy_button_selector))
            )[-1]
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(last_copy_button)).click()
            self._human_delay()
            raw_response_text = self.driver.execute_script("return navigator.clipboard.readText();")
            if not raw_response_text:
                 raise Exception("La API del portapapeles no devolvió texto.")
            print("[GeminiWebClient] -> Éxito del Plan A: Texto extraído del portapapeles.")
        except Exception as e:
            print(f"[GeminiWebClient] [WARN] Plan A fallido: {e}")
            print("[GeminiWebClient] -> Intentando Plan B: Lectura directa del contenedor.")
            try:
                time.sleep(2)
                response_selector = "div.markdown"
                last_response_element = self.driver.find_elements(By.CSS_SELECTOR, response_selector)[-1]
                raw_response_text = last_response_element.get_attribute('textContent')
                print("[GeminiWebClient] -> Éxito del Plan B: Texto extraído del div.")
            except Exception as e2:
                print(f"[GeminiWebClient] [ERROR] Plan B fallido: {e2}")
                return ""

        if not raw_response_text or not raw_response_text.strip():
            print("[GeminiWebClient] [WARN] Advertencia: El texto final extraído está vacío.")
            return ""

        return self._clean_json_response(raw_response_text)

    def generate_image(self, prompt: str, output_dir: str = "data/images") -> str:
        """
        Genera una imagen, espera a que termine, y la descarga haciendo clic
        en el botón de descarga correcto.
        """
        self._launch_browser()
        print(f"[GeminiWebClient] Generando imagen para prompt: '{prompt[:50]}...'")

        try:
            self._send_prompt(prompt)

            stop_button_selector = '//button[.//mat-icon[@fonticon="stop"]]'
            print("[GeminiWebClient] -> Esperando el ciclo de generación de imagen...")
            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, stop_button_selector)))
                print("[GeminiWebClient] -> Paso 1/2: Generación de imagen iniciada.")
                WebDriverWait(self.driver, 120).until(EC.invisibility_of_element_located((By.XPATH, stop_button_selector)))
                print("[GeminiWebClient] -> Paso 2/2: Generación de imagen finalizada.")
            except TimeoutException:
                raise Exception("El ciclo de generación de imagen no se completó en el tiempo esperado.")

            self._human_delay(2, 3) # Pausa para que la UI se estabilice

            # Limpiar directorio de descargas ANTES de hacer clic
            self._clear_download_directory()

            # Hacer clic en el botón de descargar
            print("[GeminiWebClient] -> Buscando y haciendo clic en el botón de descargar imagen...")
            try:
                # Selector robusto basado en el tag custom y el click con JS
                download_button_selector = "download-generated-image-button button"
                
                all_download_buttons = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, download_button_selector))
                )
                last_download_button = all_download_buttons[-1]
                
                self.driver.execute_script("arguments[0].click();", last_download_button)
                print("[GeminiWebClient] -> Botón de descargar presionado.")
            except Exception as e:
                raise Exception(f"No se pudo encontrar o hacer clic en el botón de descargar: {e}")

            # Esperar a que el archivo se descargue con el nuevo timeout
            downloaded_file_path = self._wait_for_download(timeout=15)

            return downloaded_file_path

        except Exception as e:
            print(f"[GeminiWebClient] [ERROR] Error generando imagen: {e}")
            try:
                screenshot_path = os.path.abspath(f"debug_gemini_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                self.driver.save_screenshot(screenshot_path)
                print(f"[GeminiWebClient] -> Captura de pantalla de depuración guardada en: {screenshot_path}")
            except Exception as screenshot_error:
                print(f"[GeminiWebClient] [ERROR] No se pudo tomar la captura de pantalla: {screenshot_error}")
            raise

    def _wait_for_download(self, timeout=15):
        """Espera a que un archivo termine de descargarse en un directorio limpio."""
        print(f"[GeminiWebClient] -> Esperando descarga en: {self.download_dir} (timeout: {timeout}s)")
        seconds = 0
        while seconds < timeout:
            # Omitir archivos temporales de Chrome
            files = [f for f in Path(self.download_dir).glob('*') if not str(f).endswith('.crdownload')]
            if files:
                downloaded_file = files[0]
                print(f"[GeminiWebClient] -> Descarga completada: {downloaded_file.name}")
                return str(downloaded_file)
            
            time.sleep(1)
            seconds += 1
            if seconds % 2 == 0:
                print(f"[GeminiWebClient] -> ...esperando descarga ({seconds}s)")
        
        raise Exception("Tiempo de espera de descarga agotado. El archivo no apareció.")
