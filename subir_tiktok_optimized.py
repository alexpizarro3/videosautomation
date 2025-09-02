import asyncio
import random
import time
import subprocess
import os
import json
from datetime import datetime
from playwright.async_api import async_playwright
from dotenv import load_dotenv

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
    for _ in range(random.randint(3, 8)):
        x = random.randint(100, 1400)
        y = random.randint(100, 800)
        try:
            await page.mouse.move(x, y, steps=random.randint(15, 35))
        except Exception:
            pass
        human_delay(0.3, 0.8)

async def human_scroll(page):
    """Hace scroll de forma humana."""
    for _ in range(random.randint(2, 4)):
        px = random.randint(100, 400)
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
    
    # Seleccionar hashtags de forma inteligente (máximo 5)
    selected_tags = []
    
    # Siempre incluir al menos 1 tag ASMR
    selected_tags.append(random.choice(asmr_tags))
    
    # Siempre incluir FYP o ForYou
    selected_tags.append(random.choice(['#FYP', '#ForYou', '#ForYouPage']))
    
    # Añadir tags específicos de contenido (máximo 2)
    if content_specific:
        selected_tags.extend(random.sample(content_specific, min(2, len(content_specific))))
    
    # Completar con tags virales hasta llegar a 5
    remaining_pools = viral_tags + seasonal_tags
    while len(selected_tags) < 5 and remaining_pools:
        tag = random.choice(remaining_pools)
        if tag not in selected_tags:
            selected_tags.append(tag)
            remaining_pools.remove(tag)
    
    return selected_tags[:5]  # Asegurar máximo 5 hashtags

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
            "Capybara aesthetic porque son los animales más zen del mundo 💚"
        ])
    
    if any(word in prompt_lower for word in ['acuario', 'agua', 'nadan']):
        content_descriptions.extend([
            "Sonidos de agua que te van a hipnotizar 🌊",
            "Underwater ASMR hits different ✨",
            "El sonido del agua es mi terapia favorita 💙"
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

async def debug_screenshot(page, name):
    """Tomar screenshot para depuración"""
    try:
        await page.screenshot(path=f"debug_{name}.png")
        print(f"📸 Screenshot guardado: debug_{name}.png")
    except Exception as e:
        print(f"⚠️ Error tomando screenshot: {e}")

async def verificar_video_cargado(page, max_attempts=20):
    """Verifica si el video se cargó correctamente - versión simplificada"""
    
    for attempt in range(max_attempts):
        print(f"🔍 Verificación {attempt + 1}/{max_attempts}")
        
        # 1. Verificar que desapareció el botón "Select video"
        select_button = await page.query_selector('[data-e2e="select_video_button"]')
        if select_button and await select_button.is_visible():
            print("⏳ Botón 'Select video' aún visible, esperando...")
            human_delay(4, 6)
            continue
        
        # 2. Verificar que el editor de texto esté disponible
        editor_available = False
        text_selectors = [
            '[contenteditable="true"]',
            'textarea[placeholder*="caption"]',
            'textarea[placeholder*="Describe"]'
        ]
        
        for selector in text_selectors:
            try:
                element = await page.query_selector(selector)
                if element and await element.is_visible() and await element.is_editable():
                    print(f"✅ Editor disponible: {selector}")
                    editor_available = True
                    break
            except Exception:
                continue
        
        # 3. Buscar cualquier elemento de video preview
        video_preview_found = False
        elementos_video = [
            'video',
            '[data-testid="video-preview"]',
            '.video-preview'
        ]
        
        for selector in elementos_video:
            try:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    print(f"✅ Video preview encontrado: {selector}")
                    video_preview_found = True
                    break
            except Exception:
                continue
        
        # Si tenemos editor y no hay botón de seleccionar, consideramos exitoso
        if editor_available and not select_button:
            print("✅ Video cargado - editor disponible y sin botón de selección")
            return True
        
        # Si también hay preview, mejor aún
        if editor_available and video_preview_found:
            print("✅ Video completamente cargado - editor y preview disponibles")
            return True
        
        print(f"⏳ Esperando... Editor: {editor_available}, Preview: {video_preview_found}")
        human_delay(3, 5)
    
    print("⚠️ Timeout esperando video cargado")
    return False

async def subir_video_tiktok_optimized(page, video_path, descripcion, hashtags):
    """Versión optimizada que funciona en GitHub Actions y localmente"""
    
    print(f"🚀 Iniciando subida optimizada de: {video_path}")
    
    await page.goto("https://www.tiktok.com/upload", timeout=60000)
    await human_mouse_move(page)
    human_delay(1, 2)
    
    # Verificar que el archivo existe
    absolute_path = os.path.abspath(video_path)
    if not os.path.exists(absolute_path):
        print(f"❌ Archivo no encontrado: {absolute_path}")
        return False
    
    file_size_mb = os.path.getsize(absolute_path) / (1024 * 1024)
    print(f"📊 Archivo: {file_size_mb:.2f} MB")
    
    # PASO 1: Subir archivo usando método robusto
    try:
        # Esperar a que la página esté lista
        await page.wait_for_load_state('networkidle', timeout=30000)
        
        # Buscar input de archivo
        file_input = await page.wait_for_selector('input[type="file"]', timeout=20000, state='attached')
        if not file_input:
            print("❌ Input de archivo no encontrado")
            return False
        
        print("📤 Subiendo archivo...")
        await file_input.set_input_files(absolute_path)
        
        # PASO 2: Verificar que el video se cargó
        video_loaded = await verificar_video_cargado(page)
        if not video_loaded:
            await debug_screenshot(page, "video_failed_to_load")
            print("❌ El video no se cargó correctamente")
            return False
        
        print("✅ Video cargado exitosamente")
        await debug_screenshot(page, "video_loaded_successfully")
        
        # PASO 3: Buscar editor de texto
        human_delay(3, 5)
        
        # Selectores para el editor
        text_selectors = [
            '[contenteditable="true"]',
            'textarea[placeholder*="caption"]',
            'textarea[placeholder*="Describe"]',
            '.caption-editor [contenteditable="true"]',
            '[data-testid="caption-editor"] [contenteditable="true"]'
        ]
        
        editor_found = False
        for selector in text_selectors:
            try:
                await page.wait_for_selector(selector, timeout=10000, state='visible')
                editor = await page.query_selector(selector)
                if editor and await editor.is_editable():
                    print(f"✅ Editor encontrado: {selector}")
                    
                    # Escribir descripción y hashtags
                    texto = f"{descripcion}\n{' '.join(hashtags)}"
                    await page.click(selector)
                    human_delay(1, 2)
                    await page.fill(selector, texto)
                    print("✅ Descripción y hashtags ingresados")
                    editor_found = True
                    break
                    
            except Exception as e:
                print(f"⚠️ Error con editor {selector}: {e}")
                continue
        
        if not editor_found:
            print("⚠️ No se encontró editor de texto, pero el video se subió")
        
        # PASO 4: Activar etiqueta de IA y publicar
        try:
            await debug_screenshot(page, "before_show_more_search")
            
            # Primero buscar el botón "Show more" o "Ver más"
            show_more_selectors = [
                'div[data-e2e="advanced_settings_container"] .more-btn',
                '.jsx-3335848873.more-btn',
                'div.more-btn',
                'button:has-text("Show more")',
                'button:has-text("Ver más")',
                '[data-testid="show-more-button"]',
                '.show-more-btn',
                'button[aria-label*="Show more"]',
                'button[aria-label*="Ver más"]'
            ]
            
            show_more_clicked = False
            for selector in show_more_selectors:
                try:
                    # Primero intentar encontrar el elemento
                    show_more_btn = await page.query_selector(selector)
                    if show_more_btn and await show_more_btn.is_visible():
                        # Intentar click normal primero
                        try:
                            await show_more_btn.click()
                            print(f"✅ Menú 'Show more' abierto con: {selector}")
                            human_delay(1, 2)
                            show_more_clicked = True
                            break
                        except Exception:
                            # Si falla, usar JavaScript click
                            try:
                                await page.evaluate('(element) => element.click()', show_more_btn)
                                print(f"✅ Menú 'Show more' abierto con JS: {selector}")
                                human_delay(1, 2)
                                show_more_clicked = True
                                break
                            except Exception as e:
                                print(f"⚠️ Error con selector {selector}: {e}")
                                continue
                except Exception:
                    continue
            
            if not show_more_clicked:
                await debug_screenshot(page, "show_more_not_found")
                print("ℹ️ No se encontró botón 'Show more', buscando directamente switch IA")
            else:
                await debug_screenshot(page, "show_more_opened")
            
            # Buscar switch de contenido IA con múltiples selectores
            ai_selectors = [
                'div[data-e2e="aigc_container"] .switch',
                'div[data-e2e="ai_label_container"] .switch',
                '[data-testid="ai-content-toggle"]',
                'input[type="checkbox"][aria-label*="AI"]',
                'input[type="checkbox"][aria-label*="artificial"]',
                '.ai-content-switch',
                '.aigc-switch',
                'button[aria-label*="AI-generated"]',
                'div:has-text("AI-generated content") input',
                'div:has-text("Contenido generado por IA") input',
                # Selector específico para el elemento "Checks"
                '.TUXText:has-text("Checks")',
                'div[class*="TUXText"]:has-text("Checks")',
                'div:has-text("Checks")'
            ]
            
            ai_activated = False
            for selector in ai_selectors:
                try:
                    ai_element = await page.query_selector(selector)
                    if ai_element and await ai_element.is_visible():
                        # Para elementos que contienen "Checks", hacer click directamente
                        if 'Checks' in selector:
                            await ai_element.click()
                            print(f"✅ Click en elemento Checks: {selector}")
                            human_delay(2, 3)
                            
                            # Ahora buscar el modal y el botón "Turn on"
                            try:
                                await page.wait_for_selector('button:has-text("Turn on")', timeout=5000)
                                turn_on_btn = await page.query_selector('button:has-text("Turn on")')
                                if turn_on_btn and await turn_on_btn.is_visible():
                                    await turn_on_btn.click()
                                    print("✅ Etiqueta de IA activada con botón 'Turn on' del modal")
                                    human_delay(2, 3)
                                    ai_activated = True
                                    break
                                else:
                                    print("⚠️ Botón 'Turn on' no encontrado en modal")
                            except Exception as e:
                                print(f"⚠️ Error esperando modal: {e}")
                            continue
                        
                        # Para otros elementos (checkboxes, switches)
                        element_type = await ai_element.get_attribute('type')
                        if element_type == 'checkbox':
                            is_checked = await ai_element.get_attribute('checked') == 'true'
                            if not is_checked:
                                await ai_element.click()
                                print(f"✅ Etiqueta de IA activada usando: {selector}")
                                human_delay(1, 2)
                                ai_activated = True
                                break
                            else:
                                print("ℹ️ Etiqueta de IA ya estaba activada")
                                ai_activated = True
                                break
                        else:
                            await ai_element.click()
                            print(f"✅ Click en switch IA: {selector}")
                            human_delay(1, 2)
                            
                            # Después de hacer click, verificar si aparece el modal
                            try:
                                # Esperar a que aparezca el modal con "Turn on"
                                modal_appeared = await page.wait_for_selector('button:has-text("Turn on")', timeout=3000, state='visible')
                                if modal_appeared:
                                    print("📋 Modal de IA detectado, haciendo click en 'Turn on'")
                                    await modal_appeared.click()
                                    print("✅ Etiqueta de IA activada con botón 'Turn on' del modal")
                                    human_delay(2, 3)
                                    ai_activated = True
                                    break
                                else:
                                    print("✅ Switch activado sin modal")
                                    ai_activated = True
                                    break
                            except Exception:
                                # Si no aparece modal, asumir que el switch se activó directamente
                                print("✅ Switch IA activado directamente")
                                ai_activated = True
                                break
                except Exception as e:
                    print(f"⚠️ Error con selector {selector}: {e}")
                    continue
            
            if not ai_activated:
                await debug_screenshot(page, "ai_label_not_found")
                print("⚠️ No se pudo encontrar o activar la etiqueta de IA")
            else:
                await debug_screenshot(page, "ai_label_activated")
                
        except Exception as e:
            print(f"⚠️ Error general activando etiqueta IA: {e}")

        # Esperar tiempo adicional para que el video termine de procesar
        print("⏳ Esperando 45 segundos para que el video termine de procesar...")
        human_delay(45, 50)
        
        # Buscar y hacer click en botón de publicar
        human_delay(2, 3)  # Tiempo reducido para testing (cambiar a 90-120 en producción)
        
        publish_selectors = [
            'button:has-text("Post")',
            '[data-e2e="publish-button"]',
            'button[type="submit"]',
            '.publish-btn'
        ]
        
        await debug_screenshot(page, "before_publish_click")
        
        published = False
        for selector in publish_selectors:
            try:
                publish_btn = await page.query_selector(selector)
                if publish_btn and await publish_btn.is_visible():
                    await publish_btn.click()
                    print(f"✅ Click en botón publicar: {selector}")
                    
                    # Verificar si aparece modal de confirmación
                    try:
                        # Esperar posible modal de "¿Estás seguro?"
                        confirmation_selectors = [
                            'button:has-text("Yes")',
                            'button:has-text("Confirm")',
                            'button:has-text("Continue")',
                            'button:has-text("Sí")',
                            'button:has-text("Confirmar")',
                            'button:has-text("Continuar")',
                            '[data-testid="confirm-button"]'
                        ]
                        
                        modal_handled = False
                        for confirm_selector in confirmation_selectors:
                            try:
                                confirm_btn = await page.wait_for_selector(confirm_selector, timeout=3000, state='visible')
                                if confirm_btn:
                                    await confirm_btn.click()
                                    print(f"✅ Modal de confirmación manejado: {confirm_selector}")
                                    modal_handled = True
                                    break
                            except Exception:
                                continue
                        
                        if not modal_handled:
                            print("ℹ️ No se detectó modal de confirmación")
                        
                    except Exception as e:
                        print(f"ℹ️ Sin modal de confirmación: {e}")
                    
                    published = True
                    break
                    
            except Exception as e:
                print(f"⚠️ Error con botón {selector}: {e}")
                continue
        
        if published:
            print("✅ Video publicado exitosamente")
            return True
        else:
            print("⚠️ No se encontró botón de publicar")
            return True  # Video subido aunque no se publicó
        
    except Exception as e:
        print(f"❌ Error en subida: {e}")
        return False

async def cargar_cookies(context, cookies_path):
    """Cargar cookies de sesión"""
    try:
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
        
        # Limpiar cookies para evitar errores
        for cookie in cookies:
            if 'sameSite' in cookie:
                val = cookie['sameSite']
                if val not in ["Strict", "Lax", "None"]:
                    cookie["sameSite"] = "None"
        
        await context.add_cookies(cookies)
        print(f"✅ Cookies cargadas desde {cookies_path}")
        return True
    except Exception as e:
        print(f"❌ Error cargando cookies: {e}")
        return False

async def main():
    load_dotenv()
    
    # Cargar mapeo de videos
    with open("video_prompt_map.json", "r", encoding="utf-8") as f:
        video_prompt_map = json.load(f)
    
    async with async_playwright() as p:
        # Configuración del navegador
        browser = await p.chromium.launch(
            headless=False,  # Cambiar a True para GitHub Actions
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # Cargar cookies
        cookies_loaded = await cargar_cookies(context, "config/upload_cookies_playwright.json")
        if not cookies_loaded:
            print("❌ No se pudieron cargar las cookies")
            await browser.close()
            return
        
        # Procesar cada video
        for video_data in video_prompt_map:
            video_file = video_data["video"]
            prompt = video_data["prompt"]
            
            # Verificar si existe el archivo
            if not os.path.exists(video_file):
                print(f"⚠️ Video no encontrado: {video_file}")
                continue
            
            # PROBAR CON ARCHIVO ORIGINAL PRIMERO
            print(f"🧪 Probando con archivo original: {video_file}")
            
            # Generar contenido
            descripcion = generate_varied_description(prompt)
            hashtags = generate_varied_hashtags(prompt)
            
            print(f"📝 Descripción: {descripcion[:100]}...")
            print(f"🏷️ Hashtags: {' '.join(hashtags)}")
            
            # Subir video original
            current_time = datetime.now().strftime("%H:%M")
            print(f"⏰ Subiendo video original a las {current_time}")
            
            success = await subir_video_tiktok_optimized(page, video_file, descripcion, hashtags)
            
            if success:
                print("✅ Video procesado exitosamente")
            else:
                print("❌ Error procesando video")
            
            # Esperar entre videos
            if len(video_prompt_map) > 1:
                wait_time = random.randint(120, 300)  # 2-5 minutos
                print(f"⏳ Esperando {wait_time//60} minutos antes del siguiente video...")
                human_delay(wait_time, wait_time + 30)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
