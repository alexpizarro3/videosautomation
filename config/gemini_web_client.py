import asyncio
import json
import os
import random
from pathlib import Path
from playwright.async_api import async_playwright, Page, BrowserContext

class GeminiWebClient:
    """
    Un cliente para interactuar con la interfaz web de Gemini (gemini.google.com/app)
    usando Playwright, como reemplazo de las llamadas a la API.
    """
    def __init__(self, cookies_path: str = "config/gemini_cookies.json"):
        self.cookies_path = cookies_path
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def _launch_browser(self):
        """Inicia Playwright y el navegador si aún no están activos."""
        if self.page and not self.page.is_closed():
            return

        print("[GeminiWebClient] Iniciando navegador con Playwright...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False) # False para depurar

        # Cargar cookies para autenticación
        if not os.path.exists(self.cookies_path):
            raise FileNotFoundError(f"Archivo de cookies no encontrado en {self.cookies_path}. Por favor, créalo.")

        with open(self.cookies_path, 'r') as f:
            cookies = json.load(f)

        self.context = await self.browser.new_context()
        await self.context.add_cookies(cookies)
        self.page = await self.context.new_page()

        print("[GeminiWebClient] Navegando a Gemini...")
        await self.page.goto("https://gemini.google.com/app", timeout=60000)
        await self.page.wait_for_load_state('networkidle')
        print("[GeminiWebClient] Navegador y sesión listos.")

    async def close(self):
        """Cierra el navegador y Playwright."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("[GeminiWebClient] Navegador cerrado.")

    async def _human_delay(self, min_seconds=0.5, max_seconds=1.5):
        """Introduce un retraso aleatorio para simular comportamiento humano."""
        await asyncio.sleep(random.uniform(min_seconds, max_seconds))

    async def generate_text(self, prompt: str) -> str:
        """
        Genera una respuesta de texto a partir de un prompt.
        """
        await self._launch_browser()
        print(f"[GeminiWebClient] Generando texto para prompt: '{prompt[:50]}...'")

        # Localizar el cuadro de texto principal
        prompt_box_selector = 'div[contenteditable="true"][role="textbox"]'
        await self.page.wait_for_selector(prompt_box_selector, state="visible")
        
        # Escribir el prompt y enviar
        await self.page.fill(prompt_box_selector, prompt)
        await self._human_delay()
        await self.page.keyboard.press("Enter")

        # Esperar la respuesta (identificar el último bloque de respuesta)
        # Este selector puede necesitar ajuste. Busca el contenedor de la respuesta.
        response_selector = ".response-content-container .markdown"
        await self.page.wait_for_selector(f"{response_selector}:not(:empty)", timeout=120000)
        
        # Esperar a que el indicador de "generando" desaparezca
        # await self.page.wait_for_selector(".generating-indicator", state="hidden")

        # Extraer el texto de la última respuesta
        all_responses = await self.page.query_selector_all(response_selector)
        last_response_element = all_responses[-1]
        response_text = await last_response_element.inner_text()

        print("[GeminiWebClient] Respuesta de texto generada.")
        return response_text.strip()

    async def generate_image(self, prompt: str, output_dir: str = "data/images") -> str:
        """
        Genera una imagen a partir de un prompt.
        """
        await self._launch_browser()
        print(f"[GeminiWebClient] Generando imagen para prompt: '{prompt[:50]}...'")

        # 1. Hacer clic en el botón "Imagen" (necesitaremos el XPath/selector)
        image_button_xpath = "XPATH_DEL_BOTON_IMAGEN" # <- REEMPLAZAR
        print(f"[GeminiWebClient] Haciendo clic en el botón de imagen: {image_button_xpath}")
        # await self.page.click(f"xpath={image_button_xpath}")
        # await self._human_delay()

        # 2. Escribir el prompt en el nuevo campo y generar
        # El selector del prompt de imagen puede ser diferente
        image_prompt_selector = 'div[contenteditable="true"][role="textbox"]' # <- AJUSTAR SI ES NECESARIO
        await self.page.fill(image_prompt_selector, prompt)
        await self.page.keyboard.press("Enter")

        # 3. Esperar a que la imagen se genere
        # Este selector es un ejemplo, hay que inspeccionar el real
        generated_image_selector = "img.generated-image" # <- REEMPLAZAR
        await self.page.wait_for_selector(generated_image_selector, timeout=180000)

        # 4. Descargar la imagen
        image_element = await self.page.query_selector(generated_image_selector)
        image_buffer = await image_element.screenshot()

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = Path(output_dir) / f"gemini_web_{timestamp}.png"
        
        with open(image_path, "wb") as f:
            f.write(image_buffer)

        print(f"[GeminiWebClient] Imagen guardada en: {image_path}")
        return str(image_path)

    async def generate_video(self, prompt: str, base_image_path: str, output_dir: str = "data/videos/original") -> str:
        """
        Genera un video a partir de una imagen base y un prompt.
        """
        await self._launch_browser()
        print(f"[GeminiWebClient] Generando video para: '{prompt[:50]}...'")

        # 1. Hacer clic en el botón "Video" (necesitaremos el XPath/selector)
        video_button_xpath = "XPATH_DEL_BOTON_VIDEO" # <- REEMPLAZAR
        print(f"[GeminiWebClient] Haciendo clic en el botón de video: {video_button_xpath}")
        # await self.page.click(f"xpath={video_button_xpath}")
        # await self.page.wait_for_load_state('networkidle') # Esperar a que cargue el nuevo chat

        # 2. Subir la imagen base
        # El selector para subir archivos puede ser un input[type="file"]
        upload_input_selector = 'input[type="file"]' # <- AJUSTAR SI ES NECESARIO
        async with self.page.expect_file_chooser() as fc_info:
            # await self.page.click("SELECTOR_DEL_BOTON_DE_SUBIR_IMAGEN") # Clic en el ícono de clip/imagen
            pass
        file_chooser = await fc_info.value
        await file_chooser.set_files(base_image_path)
        print(f"[GeminiWebClient] Imagen base '{base_image_path}' subida.")

        # 3. Escribir el prompt y generar
        video_prompt_selector = 'div[contenteditable="true"][role="textbox"]' # <- AJUSTAR SI ES NECESARIO
        await self.page.fill(video_prompt_selector, prompt)
        await self.page.keyboard.press("Enter")

        # 4. Esperar a que el video se genere y aparezca el botón de descarga
        # Este selector es un ejemplo, hay que inspeccionar el real
        download_button_selector = "button.download-video-button" # <- REEMPLAZAR
        await self.page.wait_for_selector(download_button_selector, timeout=600000) # Timeout largo para video

        # 5. Descargar el video
        async with self.page.expect_download() as download_info:
            await self.page.click(download_button_selector)
        
        download = await download_info.value
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = Path(output_dir) / f"gemini_web_video_{timestamp}.mp4"
        await download.save_as(video_path)

        print(f"[GeminiWebClient] Video guardado en: {video_path}")
        return str(video_path)

async def example_usage():
    """Función de ejemplo para probar el cliente."""
    client = GeminiWebClient()
    try:
        # Ejemplo de texto
        response = await client.generate_text("Hola, ¿cómo estás?")
        print("Respuesta de texto:", response)
    finally:
        await client.close()

if __name__ == "__main__":
    # Para ejecutar este ejemplo, necesitarás crear 'config/gemini_cookies.json'
    # y descomentar las líneas de acción en los métodos.
    # asyncio.run(example_usage())
    print("Este script es un módulo. Importa GeminiWebClient en tus scripts del pipeline.")