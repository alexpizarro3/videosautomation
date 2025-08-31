from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
def login_and_save_cookies(driver, email, password, cookies_path):
    """
    Inicia sesión manualmente en TikTok y guarda las cookies actualizadas en el archivo.
    """
    driver.get("https://www.tiktok.com/login")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    email_input = driver.find_element(By.NAME, "username")
    email_input.clear()
    email_input.send_keys(email)
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(password)
    submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_btn.click()
    # Esperar a que la sesión esté activa
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-e2e='profile-icon'] | //span[contains(@class, 'avatar')] | //a[contains(@href, '/@')]") )
    )
    print("✅ Login exitoso, guardando cookies...")
    cookies = driver.get_cookies()
    import json
    with open(cookies_path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"✅ Cookies guardadas en {cookies_path}")
import os
import json
import random
import time
import shutil
import subprocess
import cv2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException


def ensure_9_16(video_path: str) -> str:
    """Asegura que el video tenga relación 9:16. Si no, intenta convertirlo con ffmpeg.

    Devuelve la ruta al archivo final (puede ser la original si no se pudo convertir).
    """
    abs_video_path = os.path.abspath(video_path)
    print(f"Ruta absoluta del video: {abs_video_path}")
    if not os.path.exists(abs_video_path):
        print(f"❌ El archivo de video no existe: {abs_video_path}")
        return abs_video_path

    try:
        cap = cv2.VideoCapture(abs_video_path)
        if not cap.isOpened():
            print(f"⚠️  No se pudo abrir el video: {abs_video_path}")
            return abs_video_path
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        # Si ya es vertical con ratio cercano a 9:16 (>=1.7) no convertimos
        if height > width and (height / width) >= 1.7:
            print(f"✅ Video ya está en formato vertical: {abs_video_path}")
            return abs_video_path
    except Exception as e:
        print(f"⚠️  Error leyendo dimensiones del video: {e}")

    ffmpeg_bin = shutil.which('ffmpeg')
    if not ffmpeg_bin:
        ffmpeg_bin = r'C:\Users\Alexis Pizarro\Downloads\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\ffmpeg-2025-08-25-git-1b62f9d3ae-essentials_build\bin\ffmpeg.exe'

    temp_path = abs_video_path + '.tmp.mp4'
    vf = "crop='min(iw,1080)':'min(ih,1920)':(iw-1080)/2:(ih-1920)/2,scale=1080:1920"
    cmd = [ffmpeg_bin, '-y', '-i', abs_video_path, '-vf', vf, '-c:a', 'copy', temp_path]
    try:
        subprocess.run(cmd, check=True)
        os.replace(temp_path, abs_video_path)
        print(f"✅ Video convertido y reemplazado: {abs_video_path}")
        return abs_video_path
    except Exception as e:
        print(f"❌ Error al convertir video: {e}")
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass
        return abs_video_path


def setup_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-extensions')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_experimental_option('excludeSwitches', ['enable-automation'])
    try:
        driver = webdriver.Chrome(options=opts)
        driver.maximize_window()
        return driver
    except Exception as e:
        print(f"❌ Error iniciando WebDriver: {e}")
        raise


def restart_driver(old_driver):
    try:
        old_driver.quit()
    except Exception:
        pass
    new_driver = setup_driver()
    try:
        load_cookies(new_driver)
    except Exception:
        pass
    return new_driver


def save_debug_state(driver, label: str):
    try:
        os.makedirs('debug', exist_ok=True)
        ts = int(time.time())
        png_path = os.path.join('debug', f'{ts}_{label}.png')
        html_path = os.path.join('debug', f'{ts}_{label}.html')
        driver.save_screenshot(png_path)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"ℹ️  Estado guardado: {png_path}, {html_path}")
    except Exception as e:
        print(f"⚠️  No se pudo guardar estado de depuración: {e}")


def load_cookies(driver) -> bool:
    # Preferir el archivo exacto solicitado por el usuario
    possible_paths = [
        'upload_cookes.json.example',
        os.path.join('config', 'upload_cookies.json.example'),
        os.path.join('config', 'upload_cookies.json'),
        'upload_cookies.json'
    ]
    cookies_path = None
    for p in possible_paths:
        if os.path.exists(p):
            cookies_path = p
            break
    if not cookies_path:
        print("⚠️  No se encontró archivo de cookies en los paths esperados.")
        return False

    print(f"📝 Usando archivo de cookies: {cookies_path}")
    try:
        with open(cookies_path, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        print(f"📝 Contenido de cookies: {json.dumps(cookies, indent=2)[:1000]}...")

        driver.get('https://www.tiktok.com')
        time.sleep(1)

        if isinstance(cookies, list):
            for cookie_dict in cookies:
                try:
                    driver.add_cookie(cookie_dict)
                except Exception:
                    pass
            print(f"✅ Cookies cargadas: {len(cookies)} cookies (formato lista)")
        elif isinstance(cookies, dict):
            for name, value in cookies.items():
                try:
                    driver.add_cookie({'name': name, 'value': value, 'domain': '.tiktok.com'})
                except Exception:
                    pass
            print(f"✅ Cookies cargadas: {len(cookies)} cookies (formato dict)")
        else:
            print("❌ Formato de cookies no soportado")
            return False

        # Guardar screenshot y HTML tras cargar cookies
        save_debug_state(driver, 'post_cookies')

        return True
    except Exception as e:
        print(f"❌ Error cargando cookies: {e}")
        return False


def generar_descripcion_y_hashtags(prompt: str):
    hashtags_base = [
        '#Viral', '#ASMR', '#Capybara', '#Relax', '#FYP', '#HamsterCore', '#FantasyArt', '#ViralVideo',
        '#TikTokViral', '#ArteDigital', '#Neon', '#Gelatina', '#Acuario', '#Explosión', '#Sonido',
        '#Adictivo', '#Estilo', '#Tendencia', '#Viral2025', '#ViralTikTok'
    ]
    palabras = [w for w in prompt.split() if len(w) > 4]
    hashtags_prompt = [f'#{w.capitalize()}' for w in palabras if w.isalpha()][:5]
    try:
        hashtags = list(dict.fromkeys(hashtags_prompt + random.sample(hashtags_base, 5)))[:5]
    except Exception:
        hashtags = (hashtags_prompt + hashtags_base)[:5]
    descripcion = f"{prompt}\n\nDisfruta este video viral con sonido envolvente y efectos ASMR. ¡No olvides seguirme para más contenido único!"
    return descripcion, hashtags


def subir_videos():
    print("🕷️  SUBIDA AUTOMÁTICA DE VIDEOS TIKTOK")
    print("=" * 50)
    try:
        with open("video_prompt_map.json", "r", encoding="utf-8") as f:
            video_prompt_map = json.load(f)
    except Exception as e:
        print(f"❌ No se pudo leer 'video_prompt_map.json': {e}")
        return

    from dotenv import load_dotenv
    load_dotenv()
    email = os.getenv("TIKTOK_EMAIL")
    password = os.getenv("TIKTOK_PASSWORD")
    cookies_path = "config/upload_cookies.json.example"
    driver = setup_driver()
    cookies_ok = load_cookies(driver)
    try:
        driver.refresh()
    except NoSuchWindowException:
        print("⚠️  Ventana del navegador cerrada, reiniciando WebDriver y recargando cookies.")
        try:
            driver.quit()
        except Exception:
            pass
        driver = setup_driver()
        cookies_ok = load_cookies(driver)
    print("⏳ Espera 10 segundos para resolver el puzzle/captcha manualmente si aparece...")
    time.sleep(10)

    username = os.getenv('TIKTOK_USERNAME', 'chakakitafreakyvideos')
    profile_url = f"https://www.tiktok.com/@{username}"
    driver.get(profile_url)
    print("⏳ Espera 10 segundos para resolver el puzzle/captcha en el perfil si aparece...")
    time.sleep(10)
    logged_in_indicators = driver.find_elements(By.XPATH, "//div[@data-e2e='profile-icon'] | //span[contains(@class, 'avatar')] | //a[contains(@href, '/@')]")
    if not logged_in_indicators:
        print("⚠️  No se detectó sesión activa con cookies, iniciando login manual...")
        login_and_save_cookies(driver, email, password, cookies_path)
        driver.get(profile_url)
        time.sleep(10)
        logged_in_indicators = driver.find_elements(By.XPATH, "//div[@data-e2e='profile-icon'] | //span[contains(@class, 'avatar')] | //a[contains(@href, '/@')]")
        if not logged_in_indicators:
            print("❌ Login manual falló, no se puede subir el video")
            driver.quit()
            return
    print("✅ Sesión activa detectada para subida")
    for item in video_prompt_map:
        video_path = ensure_9_16(item.get("video", ""))
        prompt = item.get("prompt", "")
        if not os.path.exists(video_path):
            print(f"❌ Archivo no encontrado, saltando: {video_path}")
            continue

        descripcion, hashtags = generar_descripcion_y_hashtags(prompt)

        attempts = 0
        while attempts < 2:
            try:
                driver.get('https://www.tiktok.com/upload')
                try:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
                    )
                    upload_input = driver.find_element(By.XPATH, '//input[@type="file"]')
                except TimeoutException:
                    print("❌ Timeout esperando el input de subida. Guardando estado de depuración y continuando.")
                    save_debug_state(driver, 'upload_input_timeout')
                    break
                upload_input.send_keys(os.path.abspath(video_path))
                WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.caption-editor [contenteditable="true"]'))
                )
                try:
                    show_more_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.more-btn'))
                    )
                    show_more_btn.click()
                    print("✅ Botón 'Show more' clickeado")
                except Exception as e:
                    print(f"⚠️  No se pudo clicar 'Show more': {e}")
                try:
                    switch_thumb = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.Switch__thumb'))
                    )
                    driver.execute_script("arguments[0].click();", switch_thumb)
                    print("✅ Switch activado")
                except Exception as e:
                    print(f"⚠️  No se pudo activar el switch: {e}")
                editable_box = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.caption-editor [contenteditable="true"]'))
                )
                from selenium.webdriver.common.keys import Keys
                editable_box.click()
                editable_box.send_keys(Keys.CONTROL, 'a')
                editable_box.send_keys(Keys.DELETE)
                texto = f"{descripcion}\n{' '.join(hashtags)}"
                editable_box.send_keys(texto)
                try:
                    ai_modal = WebDriverWait(driver, 3).until(
                        lambda d: d.find_element(By.XPATH, "//div[contains(., 'Labeling AI-generated content')]")
                    )
                    not_now_btn = ai_modal.find_element(By.XPATH, ".//button[contains(., 'Not now')]")
                    driver.execute_script("arguments[0].click();", not_now_btn)
                    print("✅ Modal 'Labeling AI-generated content' cerrado")
                except Exception:
                    pass
                try:
                    disclose_switch_content = driver.find_element(By.CSS_SELECTOR, 'div[data-e2e="disclose_content_container"] .Switch__content')
                    disclose_state = disclose_switch_content.get_attribute('aria-checked')
                    print(f"Estado actual de 'Disclose post content': {disclose_state}")
                    if disclose_state == 'true':
                        disclose_thumb = disclose_switch_content.find_element(By.CSS_SELECTOR, '.Switch__thumb')
                        driver.execute_script("arguments[0].click();", disclose_thumb)
                        print("✅ Switch 'Disclose post content' desactivado")
                except Exception as e:
                    print(f"⚠️  No se pudo desactivar 'Disclose post content': {e}")
                try:
                    ai_switch_content = driver.find_element(By.CSS_SELECTOR, 'div[data-e2e="aigc_container"] .Switch__content')
                    ai_state = ai_switch_content.get_attribute('aria-checked')
                    print(f"Estado actual de 'AI-generated content': {ai_state}")
                    if ai_state == 'false':
                        ai_thumb = ai_switch_content.find_element(By.CSS_SELECTOR, '.Switch__thumb')
                        driver.execute_script("arguments[0].click();", ai_thumb)
                        print("✅ Switch 'AI-generated content' activado")
                except Exception as e:
                    print(f"⚠️  No se pudo activar 'AI-generated content': {e}")
                try:
                    last_exception = None
                    for _ in range(3):
                        try:
                            post_btn = WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-e2e="post_video_button"]'))
                            )
                            # Esperar a que desaparezca el overlay/modal de verificación
                            try:
                                WebDriverWait(driver, 30).until_not(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.TUXModal-overlay[data-transition-status="open"]'))
                                )
                            except Exception:
                                print("Overlay/modal sigue presente, intentando cierre automático...")
                                # Intentar clicar botón de cierre/aceptar si existe
                                try:
                                    close_btn = driver.find_element(By.XPATH, "//button[contains(.,'Entiendo') or contains(.,'Aceptar') or contains(.,'Cerrar')]")
                                    close_btn.click()
                                    print("Botón de cierre/aceptar clickeado.")
                                    WebDriverWait(driver, 10).until_not(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.TUXModal-overlay[data-transition-status="open"]'))
                                    )
                                except Exception:
                                    print("No se pudo cerrar el modal automáticamente. Pausando 10s para cierre manual...")
                                    time.sleep(10)
                            post_btn.click()
                            print("✅ Botón Post clickeado")
                            break
                        except Exception as e:
                            last_exception = e
                            print(f"⚠️ Intento de click fallido, reintentando: {e}")
                            time.sleep(2)
                    else:
                        print(f"❌ Error al clicar el botón Post tras reintentos: {last_exception}")
                except Exception as e:
                    print(f"❌ Error al clicar el botón Post: {e}")
                try:
                    post_btn = WebDriverWait(driver, 60).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-e2e="post_video_button"]'))
                    )
                    post_btn.click()
                    print(f"✅ Video subido automáticamente a TikTok: {video_path}")
                    time.sleep(15)
                except Exception as e:
                    print(f"❌ Error al clicar el botón Post: {e}")
                break
            except NoSuchWindowException:
                print("⚠️  Se detectó que la ventana del navegador se cerró durante la subida; reiniciando WebDriver y reintentando.")
                driver = restart_driver(driver)
                attempts += 1
                continue
            except Exception as e:
                print(f"❌ Error en la subida: {e}")
                try:
                    save_debug_state(driver, 'error_en_subida')
                except Exception:
                    pass
                break

    driver.quit()


def human_delay(min_s=0.7, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))

def human_scroll(driver, px=200):
    driver.execute_script(f"window.scrollBy(0, {px})")
    human_delay()

def human_hover(driver, element):
    from selenium.webdriver.common.action_chains import ActionChains
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    human_delay()

if __name__ == "__main__":
    subir_videos()
