import asyncio
import random
import time
from playwright.async_api import async_playwright
import os
import json
from dotenv import load_dotenv
from convertir_video_tiktok import convertir_a_9_16_zoom

def human_delay(min_s=0.7, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))


async def human_mouse_move(page):
    """Mueve el mouse a posiciones aleatorias de forma humana."""
    for _ in range(random.randint(2, 5)):
        x = random.randint(50, 1600)
        y = random.randint(50, 900)
        try:
            await page.mouse.move(x, y, steps=random.randint(8, 20))
        except Exception:
            pass
        human_delay(0.05, 0.25)


async def human_scroll(page):
    """Scrolls suaves arriba/abajo para simular lectura."""
    for _ in range(random.randint(1, 3)):
        px = random.randint(100, 600)
        try:
            await page.evaluate(f'window.scrollBy(0, {px})')
        except Exception:
            pass
        human_delay(0.2, 0.6)
    for _ in range(random.randint(0, 2)):
        px = random.randint(50, 200)
        try:
            await page.evaluate(f'window.scrollBy(0, {-px})')
        except Exception:
            pass
        human_delay(0.1, 0.4)


async def click_maybe_disabled(page, selector):
    """Intentar clickear un elemento; si parece deshabilitado, quitar atributos/classes comunes y reintentar."""
    try:
        el = await page.query_selector(selector)
        if not el:
            return False
        try:
            await el.click()
            return True
        except Exception:
            # Intentar hacer visible / habilitar vía JS
            try:
                await page.evaluate(f"(function() {{const e=document.querySelector('{selector.replace("'","\\'")}'); if(!e) return; e.removeAttribute('disabled'); e.removeAttribute('aria-disabled'); e.classList.remove('disabled'); e.style.pointerEvents='auto';}})()")
            except Exception:
                pass
            human_delay(0.2, 0.6)
            try:
                await el.click()
                return True
            except Exception:
                return False
    except Exception:
        return False

async def cargar_cookies(context, cookies_path):
    with open(cookies_path, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    # Playwright espera cookies en formato dict, sin campos extra
    for cookie in cookies:
        # Elimina campos no soportados
        for k in ["hostOnly", "storeId"]:
            cookie.pop(k, None)
        # Playwright espera expires, no expirationDate
        if "expirationDate" in cookie:
            cookie["expires"] = int(cookie["expirationDate"])
            del cookie["expirationDate"]
        # Corregir el campo sameSite
        if "sameSite" in cookie:
            val = cookie["sameSite"]
            if val in [None, "null", "no_restriction"]:
                cookie["sameSite"] = "None"
            elif val in ["Strict", "Lax", "None"]:
                pass
            else:
                cookie["sameSite"] = "None"
    await context.add_cookies(cookies)
    print(f"✅ Cookies cargadas desde {cookies_path}")
    human_delay(2, 4)

async def subir_video_tiktok(page, video_path, descripcion, hashtags):
    await page.goto("https://www.tiktok.com/upload", timeout=60000)
    # Esperar que el input exista en el DOM (puede estar oculto); luego usar set_input_files aunque esté hidden
    try:
        await page.wait_for_selector('input[type="file"]', timeout=15000, state='attached')
    except Exception:
        pass
    # Simula hover y scroll antes de interactuar
    try:
        await page.evaluate('window.scrollBy(0, 100)')
    except Exception:
        pass
    human_delay()
    input_el = await page.query_selector('input[type="file"]')
    if input_el:
        try:
            await input_el.set_input_files(video_path)
        except Exception as e:
            print(f"❌ Error al set_input_files: {e}")
            await page.screenshot(path="debug_set_input_error.png", full_page=True)
            return
    else:
        print("❌ No se encontró input[type=file] en la página de upload. Guardando debug y saltando video.")
        await page.screenshot(path="debug_no_input.png", full_page=True)
        return
    print(f"✅ Video seleccionado: {video_path}")
    # Espera a que aparezca el editor de descripción
    await page.wait_for_selector('.caption-editor [contenteditable="true"]', timeout=120000)
    await page.hover('.caption-editor [contenteditable="true"]')
    await page.click('.caption-editor [contenteditable="true"]')
    human_delay()
    texto = f"{descripcion}\n{' '.join(hashtags)}"
    await page.fill('.caption-editor [contenteditable="true"]', texto)
    print("✅ Descripción y hashtags ingresados")
    # Esperar 30 segundos para que TikTok procese o complete verificaciones/activación de contenido IA
    human_delay(30, 30)
    # Scroll y hover al botón Post
    await page.evaluate('window.scrollBy(0, 200)')
    await page.hover('button[data-e2e="post_video_button"]')
    human_delay(1, 3)
    await page.click('button[data-e2e="post_video_button"]')
    print("✅ Botón Post clickeado")
    # Manejar modal tipo "Continue to post" / "Post now" si aparece
    try:
        modal_selectors = [
            'text=Post now',
            'text=Post Now',
            "button:has-text('Post now')",
            "button:has-text('Post Now')",
            'text=Continue to post',
            "button:has-text('Continue to post')",
        ]
        clicked = False
        for sel in modal_selectors:
            try:
                btn = await page.wait_for_selector(sel, timeout=5000)
                await btn.click()
                print(f"✅ Modal confirmado con selector: {sel}")
                clicked = True
                break
            except Exception:
                pass
        if not clicked:
            # intentar localizar botones dentro de dialog
            try:
                dialog_btn = page.locator('[role="dialog"] button:has-text("Post now")')
                if await dialog_btn.count() > 0:
                    await dialog_btn.first.click()
                    print("✅ Modal 'Post now' clickeado (role dialog).")
            except Exception:
                pass
    except Exception as e:
        print(f"⚠️ Error manejando modal de confirmación: {e}")

    human_delay(3, 6)

async def main():
    load_dotenv()
    cookies_path = "config/upload_cookies_playwright.json"
    with open("video_prompt_map.json", "r", encoding="utf-8") as f:
        video_prompt_map = json.load(f)
    async with async_playwright() as p:
        # Ruta de Brave en Windows
        brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        # Forzar ventana más grande y posición para evitar contenido cortado
        launch_args = ["--start-maximized", "--window-size=1920,1080", "--window-position=0,0"]
        if not os.path.exists(brave_path):
            print(f"❌ No se encontró Brave en {brave_path}. Usando Chromium por defecto.")
            browser = await p.chromium.launch(headless=False, slow_mo=150, args=launch_args)
        else:
            browser = await p.chromium.launch(headless=False, slow_mo=150, executable_path=brave_path, args=launch_args)
        # No fijar viewport: usar el tamaño real de la ventana para que todo el contenido sea visible
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport=None
        )
        await cargar_cookies(context, cookies_path)
        page = await context.new_page()
        # Forzar tamaño/posición en la ventana del navegador (fallback JS)
        try:
            await page.evaluate('window.moveTo(0,0); window.resizeTo(1920,1080);')
        except Exception:
            pass
        # Ir primero a la página principal y simular comportamiento humano
        await page.goto("https://www.tiktok.com/", timeout=60000)
        await human_mouse_move(page)
        await human_scroll(page)
        human_delay(2, 4)
        # Intentar encontrar y clicar el enlace "Upload" antes de ir por URL directa
        try:
            # Intentar clickear el boton upload (puede estar deshabilitado)
            clicked = await click_maybe_disabled(page, 'a:has-text("Upload"), button:has-text("Upload"), a[href*="/tiktokstudio/upload"]')
            if clicked:
                human_delay(1, 2)
        except Exception:
            pass
        # Finalmente navegar a /upload si no redirigió
        try:
            await page.goto("https://www.tiktok.com/tiktokstudio/upload", timeout=120000, wait_until='domcontentloaded')
        except Exception:
            pass
        # Verifica si la sesión está activa (si no, no cerrar inmediatamente; haremos checks adicionales)
        session_ok = False
        try:
            await page.wait_for_selector('[data-e2e="profile-icon"], .avatar, a[href*="/@"]', timeout=10000)
            session_ok = True
            print("✅ Sesión activa detectada con cookies")
        except Exception:
            # Fallback: comprobar si hay cookies de sesión cargadas
            cookies_list = await context.cookies()
            session_keys = {"sessionid", "sid_tt", "ttwid", "msToken", "sid_guard"}
            for c in cookies_list:
                if c.get("name") in session_keys and c.get("value"):
                    session_ok = True
                    print(f"✅ Cookie de sesión detectada: {c.get('name')}")
                    break
            if not session_ok:
                print("⚠️ No se detectó sesión activa por selector ni por cookies. Mantendré el navegador abierto para depuración.")
                try:
                    await page.screenshot(path="debug_no_session.png", full_page=True)
                    html = await page.content()
                    with open('debug_no_session.html', 'w', encoding='utf-8') as fh:
                        fh.write(html)
                    print("Captura y HTML guardados: debug_no_session.png / debug_no_session.html")
                except Exception:
                    pass
        # Intentar navegar explícitamente a la página de upload para validar que el viewport y cookies permiten el acceso
        try:
            await page.goto("https://www.tiktok.com/tiktokstudio/upload", timeout=120000, wait_until='domcontentloaded')
            # esperar input aunque esté oculto
            try:
                await page.wait_for_selector('input[type="file"]', timeout=60000, state='attached')
                print("✅ Página de upload accesible")
            except Exception:
                print("⚠️ No se detectó el input de upload tras navegar; la página podría estar limitada o el contenido se muestra cortado.")
                try:
                    await page.screenshot(path="debug_upload_access.png", full_page=True, timeout=60000)
                except Exception:
                    print("⚠️ Screenshot también falló por timeout")
                html = await page.content()
                with open('debug_upload_access.html', 'w', encoding='utf-8') as fh:
                    fh.write(html)
                print("Captura y HTML guardados: debug_upload_access.png / debug_upload_access.html")
        except Exception as e:
            print(f"❌ Error navegando a upload: {e}")
            try:
                await page.screenshot(path="debug_upload_nav_error.png", full_page=True, timeout=60000)
                print("Screenshot guardado: debug_upload_nav_error.png")
            except Exception:
                print("⚠️ No se pudo tomar captura del error (timeout)")

        for item in video_prompt_map:
            video_path = item.get("video", "")
            prompt = item.get("prompt", "")
            if not os.path.exists(video_path):
                print(f"❌ Archivo no encontrado, saltando: {video_path}")
                continue
            # Preparar archivo convertido a formato TikTok (9:16) usando zoom logic
            base, ext = os.path.splitext(video_path)
            converted_path = f"{base}_tiktok{ext}"
            if not os.path.exists(converted_path):
                print(f"🔁 Convirtiendo {video_path} -> {converted_path} (9:16 zoom)")
                try:
                    # convertir_a_9_16_zoom usa subprocess/cv2 y es bloqueante -> ejecutarlo en thread
                    await asyncio.to_thread(convertir_a_9_16_zoom, video_path, converted_path)
                    print(f"✅ Conversión completada: {converted_path}")
                except Exception as e:
                    print(f"❌ Error convirtiendo video {video_path}: {e}. Usando archivo original.")
                    converted_path = video_path
            else:
                print(f"ℹ️ Video ya convertido encontrado: {converted_path}")
            # Usar el path convertido para subir
            upload_path = converted_path
            descripcion = f"{prompt}\n\nDisfruta este video viral con sonido envolvente y efectos ASMR. ¡No olvides seguirme para más contenido único!"
            hashtags = [f"#{w.capitalize()}" for w in prompt.split() if w.isalpha()][:5]
            hashtags += ['#Viral', '#ASMR', '#FYP', '#TikTokViral']
            hashtags = list(dict.fromkeys(hashtags))[:5]
            await subir_video_tiktok(page, upload_path, descripcion, hashtags)
            human_delay(5, 10)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
