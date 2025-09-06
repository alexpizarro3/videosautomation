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

async def debug_screenshot(page, name):
    """Tomar screenshot para depuración"""
    try:
        await page.screenshot(path=f"debug_{name}.png")
        print(f"📸 Screenshot guardado: debug_{name}.png")
    except Exception as e:
        print(f"⚠️ Error tomando screenshot: {e}")

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

async def upload_file_alternative_method(page, file_path):
    """Método alternativo para subir archivos usando JavaScript y eventos del DOM"""
    
    print(f"🔄 Probando método alternativo de subida para: {file_path}")
    
    # Método 1: Buscar input oculto y hacerlo visible temporalmente
    try:
        # Encontrar el input de archivo (aunque esté oculto)
        file_inputs = await page.query_selector_all('input[type="file"]')
        
        for i, file_input in enumerate(file_inputs):
            try:
                print(f"🔍 Probando input de archivo #{i+1}")
                
                # Hacer el input visible temporalmente usando JavaScript
                await page.evaluate('''(input) => {
                    input.style.display = 'block';
                    input.style.visibility = 'visible';
                    input.style.opacity = '1';
                    input.style.position = 'relative';
                    input.style.width = '200px';
                    input.style.height = '50px';
                    input.style.zIndex = '9999';
                }''', file_input)
                
                # Esperar un momento
                human_delay(1, 2)
                
                # Intentar subir el archivo
                await file_input.set_input_files(file_path)
                print(f"✅ Archivo subido usando input #{i+1}")
                
                # Ocultar el input de nuevo
                await page.evaluate('''(input) => {
                    input.style.display = 'none';
                }''', file_input)
                
                return True
                
            except Exception as e:
                print(f"⚠️ Error con input #{i+1}: {e}")
                continue
        
        return False
        
    except Exception as e:
        print(f"❌ Error en método alternativo: {e}")
        return False

async def wait_for_upload_completion(page, max_wait=120):
    """Espera a que la subida se complete verificando múltiples indicadores"""
    
    print("⏳ Esperando a que termine la subida...")
    
    for attempt in range(max_wait):
        print(f"🔍 Verificación {attempt + 1}/{max_wait}")
        
        # 1. Verificar que hay un editor de texto disponible
        editor = await page.query_selector('[contenteditable="true"]')
        if editor and await editor.is_visible() and await editor.is_editable():
            print("✅ Editor de texto disponible")
            
            # 2. Verificar que no hay botón "Select video" visible
            select_btn = await page.query_selector('[data-e2e="select_video_button"]')
            if not (select_btn and await select_btn.is_visible()):
                print("✅ Botón 'Select video' no visible")
                
                # 3. Verificar que no hay indicadores de carga críticos
                loading_selectors = [
                    'div:has-text("Uploading")',
                    'div:has-text("Processing")',
                    '.upload-progress'
                ]
                
                is_loading = False
                for selector in loading_selectors:
                    element = await page.query_selector(selector)
                    if element and await element.is_visible():
                        print(f"⏳ Aún subiendo: {selector}")
                        is_loading = True
                        break
                
                if not is_loading:
                    print("✅ Subida completada exitosamente")
                    return True
        
        human_delay(2, 3)
    
    print("⚠️ Timeout esperando completar subida")
    return False

def generate_varied_hashtags(prompt):
    """Genera hashtags trending y robustos para videos ASMR virales (máximo 5)"""
    
    # Hashtags ASMR trending actuales
    asmr_tags = ['#ASMR', '#ASMRVideo', '#ASMRCommunity', '#ASMRTriggers', '#ASMRRelax']
    
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

async def subir_video_tiktok_alternative(page, video_path, descripcion, hashtags):
    """Método alternativo para subir videos a TikTok"""
    
    print(f"🚀 Iniciando subida alternativa de: {video_path}")
    
    await page.goto("https://www.tiktok.com/upload", timeout=60000)
    await human_mouse_move(page)
    human_delay(2, 3)
    
    # Verificar que el archivo existe
    absolute_path = os.path.abspath(video_path)
    if not os.path.exists(absolute_path):
        print(f"❌ Archivo no encontrado: {absolute_path}")
        return False
    
    file_size_mb = os.path.getsize(absolute_path) / (1024 * 1024)
    print(f"📊 Archivo: {file_size_mb:.2f} MB")
    
    await debug_screenshot(page, "before_upload")
    
    # PASO 1: Subir archivo usando método alternativo
    upload_success = await upload_file_alternative_method(page, absolute_path)
    if not upload_success:
        print("❌ Falló la subida con método alternativo")
        return False
    
    await debug_screenshot(page, "after_upload_attempt")
    
    # PASO 2: Esperar a que la subida se complete
    upload_completed = await wait_for_upload_completion(page)
    if not upload_completed:
        print("❌ La subida no se completó correctamente")
        return False
    
    await debug_screenshot(page, "upload_completed")
    
    # PASO 3: Escribir descripción y hashtags
    try:
        # Buscar editor de texto
        text_selectors = [
            '[contenteditable="true"]',
            'textarea[placeholder*="caption"]',
            'textarea[placeholder*="Describe"]'
        ]
        
        editor_found = False
        for selector in text_selectors:
            try:
                editor = await page.wait_for_selector(selector, timeout=10000, state='visible')
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
            print("⚠️ No se encontró editor de texto")
        
    except Exception as e:
        print(f"⚠️ Error escribiendo descripción: {e}")
    
    await debug_screenshot(page, "description_added")
    
    # PASO 4: Activar etiqueta de IA (opcional)
    try:
        # Buscar y abrir "Show more"
        show_more_btn = await page.query_selector('div[data-e2e="advanced_settings_container"] .more-btn')
        if show_more_btn and await show_more_btn.is_visible():
            await show_more_btn.click()
            human_delay(2, 3)
            print("✅ Menú 'Show more' abierto")
            
            # Buscar switch de IA
            ai_switch = await page.query_selector('div[data-e2e="aigc_container"] .switch')
            if ai_switch and await ai_switch.is_visible():
                await ai_switch.click()
                human_delay(1, 2)
                
                # Manejar modal si aparece
                try:
                    turn_on_btn = await page.wait_for_selector('button:has-text("Turn on")', timeout=3000, state='visible')
                    if turn_on_btn:
                        await turn_on_btn.click()
                        print("✅ Etiqueta de IA activada")
                        human_delay(2, 3)
                except Exception:
                    print("✅ Switch IA activado directamente")
            
    except Exception as e:
        print(f"⚠️ Error activando IA: {e}")
    
    await debug_screenshot(page, "ai_activated")
    
    # PASO 5: Esperar antes de publicar
    print("⏳ Esperando antes de publicar...")
    human_delay(30, 45)
    
    # PASO 6: Publicar
    try:
        publish_btn = await page.query_selector('button:has-text("Post")')
        if publish_btn and await publish_btn.is_visible():
            await publish_btn.click()
            print("✅ Video publicado exitosamente")
            
            # Manejar posible modal de confirmación
            try:
                confirm_btn = await page.wait_for_selector('button:has-text("Yes")', timeout=3000, state='visible')
                if confirm_btn:
                    await confirm_btn.click()
                    print("✅ Confirmación manejada")
            except Exception:
                pass
            
            return True
        else:
            print("⚠️ Botón de publicar no encontrado")
            return True  # Video subido aunque no publicado
            
    except Exception as e:
        print(f"⚠️ Error publicando: {e}")
        return True

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
        
        # Procesar primer video como prueba
        video_data = video_prompt_map[0]
        video_file = video_data["video"]
        prompt = video_data["prompt"]
        
        print(f"🧪 Probando con video: {video_file}")
        
        # Usar archivo original directamente
        original_file = video_file.replace('_clean.mp4', '.mp4')
        if os.path.exists(original_file):
            test_file = original_file
            print(f"📁 Usando archivo original: {test_file}")
        else:
            test_file = video_file
            print(f"📁 Usando archivo: {test_file}")
        
        # Generar contenido
        descripcion = generate_varied_description(prompt)
        hashtags = generate_varied_hashtags(prompt)
        
        print(f"📝 Descripción: {descripcion[:100]}...")
        print(f"🏷️ Hashtags: {' '.join(hashtags)}")
        
        # Subir video con método alternativo
        current_time = datetime.now().strftime("%H:%M")
        print(f"⏰ Subiendo video a las {current_time}")
        
        success = await subir_video_tiktok_alternative(page, test_file, descripcion, hashtags)
        
        if success:
            print("✅ Proceso completado exitosamente")
        else:
            print("❌ Error en el proceso")
        
        # Esperar antes de cerrar para observar resultado
        print("⏳ Esperando 30 segundos antes de cerrar...")
        human_delay(30, 30)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
