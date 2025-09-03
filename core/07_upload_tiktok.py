import asyncio
import random
import time
import subprocess
from datetime import datetime
from playwright.async_api import async_playwright
import os
import json
from dotenv import load_dotenv
from convertir_video_tiktok import convertir_a_9_16_zoom

def human_delay(min_s=0.7, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))

def clean_video_metadata(input_path, output_path):
    """Limpiar metadatos de IA del video para evitar detección automática"""
    try:
        cmd = [
            'ffmpeg', '-i', input_path, 
            '-map_metadata', '-1',  # Remover todos los metadatos
            '-c', 'copy',  # No recodificar
            '-y', output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"⚠️ No se pudieron limpiar metadatos: {e}")
        return False


async def human_mouse_move(page):
    """Mueve el mouse a posiciones aleatorias de forma humana."""
    for _ in range(random.randint(3, 8)):  # Más movimientos naturales
        x = random.randint(100, 1400)
        y = random.randint(100, 800)
        try:
            await page.mouse.move(x, y, steps=random.randint(15, 35))
        except Exception:
            pass
        human_delay(0.3, 0.8)  # Pausas más naturales

async def human_scroll(page):
    """Scrolls suaves arriba/abajo para simular lectura."""
    for _ in range(random.randint(2, 5)):
        px = random.randint(150, 800)
        try:
            await page.evaluate(f'window.scrollBy(0, {px})')
        except Exception:
            pass
        human_delay(0.5, 1.2)
    for _ in range(random.randint(1, 3)):
        px = random.randint(100, 400)
        try:
            await page.evaluate(f'window.scrollBy(0, {-px})')
        except Exception:
            pass
        human_delay(0.3, 0.8)

def generate_varied_hashtags(prompt):
    """Genera hashtags trending y robustos para videos ASMR virales"""
    
    # Hashtags ASMR trending actuales
    asmr_tags = ['#ASMR', '#ASMRVideo', '#ASMRCommunity', '#ASMRTriggers', '#ASMRRelax', '#SleepASMR', '#TinglASMR']
    
    # Hashtags de viralidad y engagement
    viral_tags = ['#FYP', '#ForYou', '#Viral', '#Trending', '#Satisfying', '#OddlySatisfying', '#Relaxing', '#Chill']
    
    # Hashtags de contenido específico basado en palabras clave del prompt
    content_specific = []
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['capibara', 'capy']):
        content_specific.extend(['#Capybara', '#CapybaraASMR', '#Animals', '#Cute'])
    
    if any(word in prompt_lower for word in ['agua', 'acuario', 'nadan']):
        content_specific.extend(['#Water', '#Aquarium', '#Swimming', '#Underwater'])
        
    if any(word in prompt_lower for word in ['gelatina', 'gomitas', 'jelly']):
        content_specific.extend(['#Jelly', '#Slime', '#Squishy', '#SlimeASMR'])
        
    if any(word in prompt_lower for word in ['lava', 'maquillaje', 'brillant']):
        content_specific.extend(['#Makeup', '#Lava', '#Glossy', '#Beauty'])
        
    if any(word in prompt_lower for word in ['neon', 'vibrant', 'color']):
        content_specific.extend(['#Neon', '#Colors', '#Aesthetic', '#Glow'])
    
    # Hashtags de temporada y tendencias actuales 2025
    seasonal_tags = ['#September2025', '#BackToSchool', '#AutumnVibes', '#Cozy', '#StudyASMR', '#MoodBooster']
    
    # Combinar todos los pools
    all_pools = [asmr_tags, viral_tags, content_specific, seasonal_tags]
    
    # Seleccionar hashtags de forma inteligente
    selected_tags = []
    
    # Siempre incluir al menos 1 tag ASMR
    selected_tags.append(random.choice(asmr_tags))
    
    # Siempre incluir FYP o ForYou
    selected_tags.append(random.choice(['#FYP', '#ForYou', '#ForYouPage']))
    
    # Añadir tags específicos de contenido
    if content_specific:
        selected_tags.extend(random.sample(content_specific, min(3, len(content_specific))))
    
    # Completar con tags virales y de temporada
    remaining_pools = viral_tags + seasonal_tags
    while len(selected_tags) < 8 and remaining_pools:
        tag = random.choice(remaining_pools)
        if tag not in selected_tags:
            selected_tags.append(tag)
            remaining_pools.remove(tag)
    
    return selected_tags[:8]  # Máximo 8 hashtags

def generate_varied_description(prompt):
    """Genera descripciones atractivas estilo creador de contenido TikTok"""
    
    # Extraer elementos clave del prompt para hacer descripción relevante
    prompt_lower = prompt.lower()
    
    # Hooks llamativos
    hooks = [
        "POV: Encontré el video más relajante de TikTok 😴",
        "Esto va a ponerte a dormir en 30 segundos 💤",
        "El ASMR que necesitabas después de un día pesado ✨",
        "Dime que esto no te da tingles 🤤",
        "Cuando necesitas 5 minutos de paz mental 🧘‍♀️",
        "Plot twist: Esto es mejor que cualquier medicina para dormir 😍",
        "Me tomó 5 horas hacer este video pero valió la pena 🥺"
    ]
    
    # Descripciones del contenido basadas en elementos del prompt
    content_descriptions = []
    
    if 'capibara' in prompt_lower:
        content_descriptions.extend([
            "Capybara ASMR porque todos necesitamos un poco de calma 🐾",
            "Los capibaras saben cómo vivir sin estrés y este video lo prueba 🌿",
            "Capybara aesthetic porque son los animales más zen del mundo �"
        ])
    
    if any(word in prompt_lower for word in ['acuario', 'agua', 'nadan']):
        content_descriptions.extend([
            "Sonidos de agua que te van a hipnotizar 🌊",
            "Underwater ASMR hits different ✨",
            "El sonido del agua es mi terapia favorita �"
        ])
    
    if any(word in prompt_lower for word in ['gelatina', 'gomitas']):
        content_descriptions.extend([
            "Jelly ASMR porque los sonidos squishy son VIDA 🍬",
            "Los sonidos de gelatina me tienen obsesionada 🤤",
            "Squishy sounds que necesitabas escuchar hoy ✨"
        ])
    
    if any(word in prompt_lower for word in ['lava', 'maquillaje']):
        content_descriptions.extend([
            "Lava makeup aesthetic porque ¿por qué no? 🔥",
            "Glossy vibes que te van a encantar ✨",
            "Beauty ASMR pero make it surreal 💄"
        ])
    
    # CTAs (Call to Action) variados
    ctas = [
        "¿Te relajó tanto como a mí? 💭",
        "Cuéntame en comentarios si te dio tingles 👇",
        "¿Más videos así? ¡Dame señales! 🙋‍♀️",
        "Si esto te gustó, hay más en mi perfil 👀",
        "¿Qué otros ASMR quieren ver? Ideas en comentarios 💡",
        "Double tap si necesitabas este momento de calma 💖",
        "Sígueme para más contenido que cure tu ansiedad ✨"
    ]
    
    # Emojis trending
    emoji_combinations = [
        "✨💤🌙", "🧘‍♀️💚🌿", "💙🌊✨", "🤤💭💤", 
        "🥺💖✨", "😴🌙💙", "🔥✨💄", "🐾💚🌿"
    ]
    
    # Construir descripción
    hook = random.choice(hooks)
    
    if content_descriptions:
        content = random.choice(content_descriptions)
    else:
        content = "ASMR content que necesitabas en tu FYP ✨"
    
    cta = random.choice(ctas)
    emojis = random.choice(emoji_combinations)
    
    # Formatos de descripción variados
    formats = [
        f"{hook}\n\n{content}\n\n{cta} {emojis}",
        f"{content}\n\n{hook}\n\n{cta} {emojis}",
        f"{hook}\n\n{cta}\n\n{content} {emojis}",
        f"{content} {emojis}\n\n{cta}",
        f"{hook}\n\n{content} • {cta} {emojis}"
    ]
    
    return random.choice(formats)
    return random.choice(descriptions)


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
    
    # Comportamiento humano inicial
    await human_mouse_move(page)
    human_delay(1, 2)  # Reducido de 2-5 a 1-2
    
    # PASO 1: Buscar directamente el input de archivo (puede estar oculto)
    print(f"📤 Buscando input de archivo para subir: {video_path}")
    
    # Usar ruta absoluta desde el inicio
    import os
    absolute_path = os.path.abspath(video_path)
    print(f"📁 Usando ruta absoluta: {absolute_path}")
    
    # Buscar el input de archivo sin hacer click en el botón
    file_input_selectors = [
        'input[type="file"]',
        'input[accept*="video"]',
        '.jsx-2995057667 input[type="file"]',
        'input[type="file"][accept="video/*"]'
    ]
    
    file_input_found = False
    for selector in file_input_selectors:
        try:
            print(f"🔍 Buscando input de archivo: {selector}")
            
            # Esperar a que aparezca el input
            await page.wait_for_selector(selector, timeout=15000, state='attached')
            element = await page.query_selector(selector)
            
            if element:
                print(f"✅ Input de archivo encontrado: {selector}")
                
                # Subir archivo directamente sin hacer click en botones
                try:
                    await element.set_input_files(absolute_path)
                    print(f"✅ Video subido exitosamente: {absolute_path}")
                    file_input_found = True
                    break
                except Exception as e:
                    print(f"⚠️ Error subiendo archivo con {selector}: {e}")
                    continue
            else:
                print(f"⚠️ Input no encontrado: {selector}")
        except Exception as e:
            print(f"⚠️ Error buscando input {selector}: {e}")
            continue
    
    if not file_input_found:
        print("❌ No se pudo encontrar o usar el input de archivo")
        return False
    
    # PASO CRÍTICO: Monitorear cambios en la página después de subir
    print("⏳ Monitoreando cambios en la página después de subir el video...")
    
    # Tomar screenshot inicial
    await page.screenshot(path="debug_after_upload.png", full_page=True)
    print("📸 Screenshot tomado: debug_after_upload.png")
    
    # Esperar y monitorear cambios
    max_attempts = 6
    for attempt in range(max_attempts):
        print(f"🔍 Intento {attempt + 1}/{max_attempts} - Esperando cambios...")
        human_delay(15, 20)  # Esperar tiempo considerable
        
        # Tomar screenshot para comparar
        await page.screenshot(path=f"debug_attempt_{attempt + 1}.png", full_page=True)
        
        # Verificar si el botón "Select video" ya no está (indicando carga exitosa)
        select_button = await page.query_selector('[data-e2e="select_video_button"]')
        if not select_button:
            print("✅ Botón de selección desapareció - video procesado")
            break
        else:
            print("⏳ Botón de selección aún presente - esperando más...")
    
    # Tiempo adicional final
    human_delay(5, 8)
    
    # Selectores actualizados y más comprehensivos
    selectors = [
        # Selectores más básicos primero
        '[contenteditable="true"]',
        'div[contenteditable="true"]',
        'textarea',
        '[data-testid*="caption"]',
        '[data-testid*="editor"]',
        # Selectores específicos
        '.caption-editor [contenteditable="true"]',
        '[contenteditable="true"][role="combobox"]',
        '.DraftEditor-root [contenteditable="true"]',
        '[data-testid="caption-editor"] [contenteditable="true"]',
        '.notranslate[contenteditable="true"]',
        # Selectores alternativos
        'div[role="textbox"]',
        '[aria-label*="caption"]',
        '[placeholder*="Describe"]',
        '[placeholder*="describe"]'
    ]
    
    caption_element = None
    working_selector = None
    
    for i, selector in enumerate(selectors):
        try:
            print(f"🔍 Probando selector {i+1}/{len(selectors)}: {selector}")
            
            # Primero verificar si existe
            element = await page.query_selector(selector)
            if element:
                # Verificar si es visible
                is_visible = await element.is_visible()
                if is_visible:
                    # Verificar si es editable
                    is_editable = await element.is_editable()
                    if is_editable:
                        caption_element = element
                        working_selector = selector
                        print(f"✅ Editor encontrado y funcional: {selector}")
                        break
                    else:
                        print(f"⚠️ Elemento no editable: {selector}")
                else:
                    print(f"⚠️ Elemento no visible: {selector}")
            else:
                print(f"⚠️ Elemento no encontrado: {selector}")
                
        except Exception as e:
            print(f"⚠️ Error con selector {selector}: {e}")
            continue
    
    if not working_selector:
        print("❌ No se pudo encontrar el editor de texto")
        
        # Debug: Tomar screenshot y guardar HTML
        try:
            await page.screenshot(path="debug_no_editor.png", full_page=True)
            html_content = await page.content()
            with open("debug_no_editor.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("📸 Debug guardado: debug_no_editor.png y debug_no_editor.html")
        except Exception:
            pass
            
        # Intentar esperar más tiempo por si acaso
        print("🔄 Intentando esperar más tiempo...")
        human_delay(10, 15)
        
        # Segundo intento con selector muy básico
        try:
            basic_selector = '[contenteditable="true"]'
            await page.wait_for_selector(basic_selector, timeout=30000)
            working_selector = basic_selector
            print(f"✅ Editor encontrado en segundo intento: {basic_selector}")
        except Exception:
            print("❌ Segundo intento fallido, abortando subida")
            return False
    
    # Comportamiento humano antes de escribir
    await human_scroll(page)
    human_delay(1, 3)
    
    # Usar el selector que funcionó
    print(f"📝 Usando selector para escribir: {working_selector}")
    
    try:
        await page.hover(working_selector)
        await page.click(working_selector)
        human_delay(1, 2)
        
        # Escribir texto usando diferentes métodos
        texto = f"{descripcion}\n{' '.join(hashtags)}"
        
        # Intentar método fill primero
        try:
            await page.fill(working_selector, texto)
            print("✅ Descripción ingresada con fill()")
        except Exception as e:
            print(f"⚠️ fill() falló: {e}, intentando type()")
            # Si fill falla, usar type como respaldo
            await page.type(working_selector, texto, delay=50)
            print("✅ Descripción ingresada con type()")
            
        print("✅ Descripción y hashtags ingresados")
        
    except Exception as e:
        print(f"❌ Error escribiendo en el editor: {e}")
        return False
    
    # CRITICAL: Activar etiqueta de contenido IA
    try:
        # Buscar y activar el switch de "AI-generated content"
        ai_switch_selector = 'div[data-e2e="aigc_container"] .switch, div[data-e2e="ai_label_container"] .switch'
        await page.wait_for_selector(ai_switch_selector, timeout=10000)
        
        ai_switch = await page.query_selector(ai_switch_selector)
        if ai_switch:
            is_checked = await ai_switch.get_attribute('aria-checked')
            if is_checked != 'true':
                await ai_switch.click()
                print("✅ Switch 'AI-generated content' activado")
                human_delay(1, 2)
        
    except Exception as e:
        print(f"⚠️ No se pudo activar el switch de AI content: {e}")
    
    # Tiempo de procesamiento MUY EXTENDIDO
    print("⏳ Esperando procesamiento completo del video (90 segundos)...")
    human_delay(90, 120)  # Tiempo crítico para evitar shadowban
    
    # Scroll y hover al botón Post con comportamiento natural
    await page.evaluate('window.scrollBy(0, 200)')
    human_delay(2, 4)
    
    await page.hover('button[data-e2e="post_video_button"]')
    human_delay(2, 4)  # Pausa antes del click final (reducido de 3-6 a 2-4)
    
    await page.click('button[data-e2e="post_video_button"]')
    print("✅ Botón Post clickeado")
    
    # Manejar modales de confirmación
    try:
        modal_selectors = [
            'text=Post now', 'text=Post Now', "button:has-text('Post now')",
            "button:has-text('Post Now')", 'text=Continue to post',
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
            try:
                dialog_btn = page.locator('[role="dialog"] button:has-text("Post now")')
                if await dialog_btn.count() > 0:
                    await dialog_btn.first.click()
                    print("✅ Modal 'Post now' clickeado (role dialog).")
            except Exception:
                pass
    except Exception as e:
        print(f"⚠️ Error manejando modal de confirmación: {e}")

    # Tiempo final para confirmación
    human_delay(2, 4)  # Reducido de 5-10 a 2-4

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
        human_delay(1, 2)  # Reducido de 2-4 a 1-2
        
        # Intentar encontrar y clicar el enlace "Upload" antes de ir por URL directa
        try:
            # Intentar clickear el boton upload (puede estar deshabilitado)
            clicked = await click_maybe_disabled(page, 'a:has-text("Upload"), button:has-text("Upload"), a[href*="/tiktokstudio/upload"]')
            if clicked:
                human_delay(0.5, 1)  # Reducido de 1-2 a 0.5-1
        except Exception:
            pass
            
        # Finalmente navegar a /upload si no redirigió
        try:
            await page.goto("https://www.tiktok.com/tiktokstudio/upload", timeout=60000, wait_until='domcontentloaded')  # Reducido timeout de 120000 a 60000
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
            await page.goto("https://www.tiktok.com/tiktokstudio/upload", timeout=60000, wait_until='domcontentloaded')  # Reducido de 120000 a 60000
            # esperar input aunque esté oculto
            try:
                await page.wait_for_selector('input[type="file"]', timeout=30000, state='attached')  # Reducido de 60000 a 30000
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
            
            # PASO 1: Limpiar metadatos de IA
            base, ext = os.path.splitext(video_path)
            clean_path = f"{base}_clean{ext}"
            
            if clean_video_metadata(video_path, clean_path):
                print(f"✅ Metadatos limpiados: {clean_path}")
                source_video = clean_path
            else:
                source_video = video_path
            
            # PASO 2: Convertir a formato TikTok (9:16) usando zoom logic
            converted_path = f"{base}_tiktok{ext}"
            if not os.path.exists(converted_path):
                print(f"🔁 Convirtiendo {source_video} -> {converted_path} (9:16 zoom)")
                try:
                    await asyncio.to_thread(convertir_a_9_16_zoom, source_video, converted_path)
                    print(f"✅ Conversión completada: {converted_path}")
                except Exception as e:
                    print(f"❌ Error convirtiendo video {source_video}: {e}. Usando archivo original.")
                    converted_path = source_video
            else:
                print(f"ℹ️ Video ya convertido encontrado: {converted_path}")
            
            # PASO 3: Generar contenido variado para evitar detección
            descripcion = generate_varied_description(prompt)
            hashtags = generate_varied_hashtags(prompt)
            
            print(f"📝 Descripción: {descripcion[:100]}...")
            print(f"🏷️ Hashtags: {' '.join(hashtags)}")
            
            # PASO 4: Subir con timing humano
            current_time = datetime.now().strftime("%H:%M")
            print(f"⏰ Subiendo video a las {current_time}")
            
            await subir_video_tiktok(page, converted_path, descripcion, hashtags)
            
            # TIMING CRÍTICO: Espera extendida entre videos (2-5 minutos)
            wait_time = random.randint(120, 300)  # 2-5 minutos
            print(f"⏳ Esperando {wait_time//60} minutos antes del siguiente video...")
            human_delay(wait_time, wait_time + 30)
            
            # Limpiar archivos temporales
            try:
                if os.path.exists(clean_path) and clean_path != video_path:
                    os.remove(clean_path)
            except Exception:
                pass
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
