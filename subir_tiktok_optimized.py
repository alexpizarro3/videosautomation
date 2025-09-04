import asyncio
import random
import time
import subprocess
import os
import json
import base64
from glob import glob
from datetime import datetime
from playwright.async_api import async_playwright
from dotenv import load_dotenv

def human_delay(min_s=0.7, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))

async def debug_screenshot(page, name):
    """Tomar screenshot para depuración"""
    try:
        await page.screenshot(path=f"debug_{name}.png")
        print(f"📸 Screenshot guardado: debug_{name}.png")
    except Exception as e:
        print(f"⚠️ Error tomando screenshot: {e}")

async def verificar_video_cargado(page):
    """Verifica que el video se haya cargado correctamente"""
    try:
        # Esperar que desaparezca el botón de seleccionar video
        print("⏳ Verificando que el video se cargó...")
        for i in range(30):  # 60 segundos máximo
            await page.wait_for_timeout(2000)
            
            # Verificar que el botón de "Select video" desapareció
            select_btn = await page.query_selector('[data-e2e="select_video_button"]')
            if not (select_btn and await select_btn.is_visible()):
                # Verificar que aparezca editor o preview
                editor_selectors = [
                    '[contenteditable="true"]',
                    'textarea[placeholder*="caption"]',
                    '[data-testid="caption-editor"]',
                    '.caption-editor',
                    '.video-preview'
                ]
                
                for selector in editor_selectors:
                    try:
                        element = await page.query_selector(selector)
                        if element and await element.is_visible():
                            print(f"✅ Editor/preview encontrado: {selector}")
                            return True
                    except Exception:
                        continue
                
                # Si no hay editor visible, aún considerar cargado si no hay botón select
                print("✅ Botón de selección desapareció, video probablemente cargado")
                return True
            
            print(f"⏳ Esperando carga del video... {i+1}/30")
        
        print("⚠️ Timeout verificando carga del video")
        return False
        
    except Exception as e:
        print(f"❌ Error verificando carga: {e}")
        return False

async def drag_and_drop_upload_fallback(page, video_path):
    """Método fallback usando drag & drop simulado"""
    try:
        print("🔄 Intentando subida por drag & drop...")
        
        # Cargar video como base64
        with open(video_path, 'rb') as f:
            video_data = f.read()
        
        video_base64 = base64.b64encode(video_data).decode()
        file_name = os.path.basename(video_path)
        
        # Ejecutar JavaScript para simular drag & drop
        success = await page.evaluate(f"""
            async () => {{
                const videoBase64 = "{video_base64}";
                const fileName = "{file_name}";
                
                try {{
                    // Convertir base64 a File
                    const byteCharacters = atob(videoBase64);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {{
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }}
                    const byteArray = new Uint8Array(byteNumbers);
                    const blob = new Blob([byteArray], {{ type: 'video/mp4' }});
                    const file = new File([blob], fileName, {{ type: 'video/mp4' }});
                    
                    // Crear DataTransfer
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    
                    // Buscar área de drop
                    const dropTarget = document.querySelector('[data-e2e="select_video_button"]') || 
                                     document.querySelector('.upload-area') ||
                                     document.querySelector('[role="button"]') ||
                                     document.body;
                    
                    // Simular eventos de drag & drop
                    const dragEnterEvent = new DragEvent('dragenter', {{
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    }});
                    
                    const dragOverEvent = new DragEvent('dragover', {{
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    }});
                    
                    const dropEvent = new DragEvent('drop', {{
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer
                    }});
                    
                    dropTarget.dispatchEvent(dragEnterEvent);
                    await new Promise(resolve => setTimeout(resolve, 100));
                    dropTarget.dispatchEvent(dragOverEvent);
                    await new Promise(resolve => setTimeout(resolve, 100));
                    dropTarget.dispatchEvent(dropEvent);
                    
                    // También intentar con input file
                    const fileInput = document.querySelector('input[type="file"]');
                    if (fileInput) {{
                        Object.defineProperty(fileInput, 'files', {{
                            value: dataTransfer.files,
                            configurable: true
                        }});
                        const changeEvent = new Event('change', {{ bubbles: true }});
                        fileInput.dispatchEvent(changeEvent);
                    }}
                    
                    return true;
                }} catch (error) {{
                    console.error('Error en drag & drop:', error);
                    return false;
                }}
            }}
        """)
        
        if success:
            print("✅ Drag & drop ejecutado")
            await page.wait_for_timeout(3000)  # Esperar un poco
            return True
        else:
            print("❌ Error en drag & drop")
            return False
            
    except Exception as e:
        print(f"❌ Error en fallback drag & drop: {e}")
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

async def realistic_drag_and_drop(page, video_path):
    """Drag & drop más realista con comportamiento humano"""
    try:
        print("🔄 Ejecutando drag & drop realista...")
        
        # Cargar video como base64
        with open(video_path, 'rb') as f:
            video_data = f.read()
        
        video_base64 = base64.b64encode(video_data).decode()
        file_name = os.path.basename(video_path)
        
        # Simular movimiento humano antes del drop
        await human_mouse_move(page)
        human_delay(1, 2)
        
        # Ejecutar drag & drop con timing más humano
        success = await page.evaluate(f"""
            async () => {{
                const videoBase64 = "{video_base64}";
                const fileName = "{file_name}";
                
                try {{
                    // Simular delay humano
                    await new Promise(resolve => setTimeout(resolve, {random.randint(500, 1500)}));
                    
                    // Convertir base64 a File
                    const byteCharacters = atob(videoBase64);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {{
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }}
                    const byteArray = new Uint8Array(byteNumbers);
                    const blob = new Blob([byteArray], {{ type: 'video/mp4' }});
                    const file = new File([blob], fileName, {{ 
                        type: 'video/mp4',
                        lastModified: Date.now()
                    }});
                    
                    // Crear DataTransfer más realista
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    
                    // Buscar múltiples targets posibles
                    const targets = [
                        document.querySelector('[data-e2e="select_video_button"]'),
                        document.querySelector('.upload-area'),
                        document.querySelector('[role="button"]'),
                        document.querySelector('input[type="file"]')?.parentElement,
                        document.body
                    ].filter(Boolean);
                    
                    const dropTarget = targets[0] || document.body;
                    
                    // Simular secuencia completa de eventos con delays
                    const events = ['dragenter', 'dragover', 'drop'];
                    
                    for (const eventType of events) {{
                        const event = new DragEvent(eventType, {{
                            bubbles: true,
                            cancelable: true,
                            dataTransfer: dataTransfer
                        }});
                        
                        dropTarget.dispatchEvent(event);
                        
                        // Delay entre eventos para simular comportamiento humano
                        await new Promise(resolve => setTimeout(resolve, {random.randint(100, 300)}));
                    }}
                    
                    // También activar input file si existe
                    const fileInputs = document.querySelectorAll('input[type="file"]');
                    for (const fileInput of fileInputs) {{
                        try {{
                            Object.defineProperty(fileInput, 'files', {{
                                value: dataTransfer.files,
                                configurable: true
                            }});
                            
                            // Disparar eventos de input y change
                            const inputEvent = new Event('input', {{ bubbles: true }});
                            const changeEvent = new Event('change', {{ bubbles: true }});
                            
                            fileInput.dispatchEvent(inputEvent);
                            await new Promise(resolve => setTimeout(resolve, 50));
                            fileInput.dispatchEvent(changeEvent);
                        }} catch (e) {{
                            console.log('Error con input:', e);
                        }}
                    }}
                    
                    return true;
                }} catch (error) {{
                    console.error('Error en drag & drop realista:', error);
                    return false;
                }}
            }}
        """)
        
        if success:
            print("✅ Drag & drop realista ejecutado")
            # Esperar un poco más para que procese
            human_delay(2, 4)
            return True
        else:
            print("❌ Error en drag & drop realista")
            return False
            
    except Exception as e:
        print(f"❌ Error en drag & drop realista: {e}")
        return False

async def verify_upload_with_patience(page):
    """Verificación de upload con más paciencia y anti-detección"""
    try:
        print("⏳ Verificando upload con paciencia...")
        
        # Múltiples indicadores de que el video se cargó
        success_indicators = [
            # Desaparición del botón de selección
            lambda: not page.query_selector('[data-e2e="select_video_button"]'),
            # Aparición del editor
            lambda: page.query_selector('[contenteditable="true"]'),
            # Aparición del preview
            lambda: page.query_selector('.video-preview, [data-testid="video-preview"]'),
            # Progress bar desaparecida
            lambda: not page.query_selector('.progress-bar, [role="progressbar"]')
        ]
        
        # Verificar durante más tiempo con paciencia
        for attempt in range(60):  # 2 minutos máximo
            await page.wait_for_timeout(2000)
            
            # Simular actividad humana ocasional
            if attempt % 10 == 0:
                await human_mouse_move(page)
            
            # Verificar múltiples indicadores
            success_count = 0
            for indicator in success_indicators:
                try:
                    if await indicator():
                        success_count += 1
                except Exception:
                    pass
            
            # Si al menos 2 indicadores sugieren éxito
            if success_count >= 2:
                print(f"✅ Upload verificado con {success_count} indicadores positivos")
                return True
            
            # Verificar específicamente si hay editor visible
            try:
                editor = await page.query_selector('[contenteditable="true"]')
                if editor and await editor.is_visible():
                    print("✅ Editor encontrado - video cargado")
                    return True
            except Exception:
                pass
            
            print(f"⏳ Verificando upload... {attempt+1}/60 ({success_count} indicadores)")
        
        print("⚠️ Timeout en verificación de upload")
        return False
        
    except Exception as e:
        print(f"❌ Error verificando upload: {e}")
        return False

async def complete_upload_flow(page, descripcion, hashtags):
    """Completar el flujo de upload con descripción, hashtags y publicación"""
    try:
        # PASO 3: Escribir descripción y hashtags
        human_delay(3, 5)
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
                    texto = f"{descripcion}\n{' '.join(hashtags)}"
                    
                    # Click más humano
                    await page.click(selector)
                    human_delay(1, 2)
                    
                    # Simular typing humano
                    await page.fill(selector, texto)
                    human_delay(1, 2)
                    
                    print("✅ Descripción y hashtags ingresados")
                    editor_found = True
                    break
            except Exception as e:
                print(f"⚠️ Error con editor {selector}: {e}")
                continue
        
        if not editor_found:
            print("⚠️ No se encontró editor de texto, pero el video se subió")

        # PASO 4: Abrir 'Show more' y activar etiqueta IA
        try:
            await debug_screenshot(page, "before_show_more_search")
            show_more_selectors = [
                'div[data-e2e="advanced_settings_container"] .more-btn',
                '.jsx-3335848873.more-btn',
                'div.more-btn',
                'button:has-text("Show more")',
                'button:has-text("Ver más")',
                '[data-testid="show-more-button"]',
                '.show-more-btn',
                'button[aria-label*="Show more"]',
                'button[aria-label*="Ver más"]',
                'button:has-text("More options")',
                'button:has-text("Más opciones")'
            ]
            show_more_clicked = False
            for selector in show_more_selectors:
                try:
                    show_more_btn = await page.query_selector(selector)
                    if show_more_btn and await show_more_btn.is_visible():
                        try:
                            await show_more_btn.click()
                            print(f"✅ Menú 'Show more' abierto con: {selector}")
                            human_delay(1, 2)
                            show_more_clicked = True
                            break
                        except Exception:
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
                '.TUXText:has-text("Checks")',
                'div[class*="TUXText"]:has-text("Checks")',
                'div:has-text("Checks")'
            ]
            ai_activated = False
            for selector in ai_selectors:
                try:
                    ai_element = await page.query_selector(selector)
                    if ai_element and await ai_element.is_visible():
                        if 'Checks' in selector:
                            await ai_element.click()
                            print(f"✅ Click en elemento Checks: {selector}")
                            human_delay(2, 3)
                            try:
                                await page.wait_for_selector('button:has-text("Turn on"), button:has-text("Activar")', timeout=5000)
                                turn_on_btn = await page.query_selector('button:has-text("Turn on"), button:has-text("Activar")')
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
                            try:
                                modal_appeared = await page.wait_for_selector('button:has-text("Turn on"), button:has-text("Activar")', timeout=3000, state='visible')
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

        # Regla: esperar 30s antes de publicar
        print("⏳ Esperando 30 segundos antes de publicar...")
        human_delay(30, 33)

        # Publicar
        human_delay(2, 3)
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
                    try:
                        confirmation_selectors = [
                            'button:has-text("Yes")',
                            'button:has-text("Confirm")',
                            'button:has-text("Continue")',
                            'button:has-text("Sí")',
                            'button:has-text("Confirmar")',
                            'button:has-text("Continuar")',
                            'button:has-text("Proceed")',
                            'button:has-text("Proceed to post")',
                            'button:has-text("Continuar para publicar")',
                            'button:has-text("Proceder a publicar")',
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
            return True
            
    except Exception as e:
        print(f"❌ Error completando upload: {e}")
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

async def subir_video_tiktok_optimized(page, video_path, descripcion, hashtags):
    """Versión optimizada con técnicas anti-detección"""

    print(f"🚀 Iniciando subida optimizada de: {video_path}")

    # Navegar a upload con comportamiento más humano
    print("🌐 Navegando a página de upload...")
    await page.goto("https://www.tiktok.com/upload", timeout=60000)
    
    # Esperar que la página cargue completamente
    await page.wait_for_load_state('networkidle', timeout=30000)
    
    # Simular comportamiento humano mientras la página carga
    await human_mouse_move(page)
    human_delay(2, 4)
    
    # Tomar screenshot para debug
    await debug_screenshot(page, "upload_page_loaded")

    # Verificar que el archivo existe
    absolute_path = os.path.abspath(video_path)
    if not os.path.exists(absolute_path):
        print(f"❌ Archivo no encontrado: {absolute_path}")
        return False

    file_size_mb = os.path.getsize(absolute_path) / (1024 * 1024)
    print(f"📊 Archivo: {file_size_mb:.2f} MB")

    try:
        # PASO 1: Esperar a que aparezcan los elementos de upload
        print("⏳ Esperando elementos de upload...")
        
        # Esperar por el área de upload específicamente
        upload_area_selectors = [
            '[data-e2e="select_video_button"]',
            'input[type="file"]',
            '.upload-area',
            '[role="button"]:has-text("Select video")',
            '[role="button"]:has-text("Seleccionar video")'
        ]
        
        upload_area = None
        for selector in upload_area_selectors:
            try:
                upload_area = await page.wait_for_selector(selector, timeout=10000, state='visible')
                if upload_area:
                    print(f"✅ Área de upload encontrada: {selector}")
                    break
            except Exception:
                continue
        
        if not upload_area:
            print("❌ No se encontró área de upload")
            await debug_screenshot(page, "no_upload_area")
            return False
        
        # Simular movimiento humano hacia el área de upload
        await human_mouse_move(page)
        human_delay(1, 3)
        
        # PASO 2: Intentar subida más natural
        uploaded = False
        
        # Método 1: Buscar input file y usarlo si está disponible
        try:
            file_inputs = await page.query_selector_all('input[type="file"]')
            for file_input in file_inputs:
                if await file_input.is_visible() and not await file_input.is_disabled():
                    print("📤 Subiendo archivo vía input visible...")
                    
                    # Mover mouse al input y hacer click humano
                    bbox = await file_input.bounding_box()
                    if bbox:
                        await page.mouse.move(
                            bbox['x'] + bbox['width']/2, 
                            bbox['y'] + bbox['height']/2,
                            steps=random.randint(10, 20)
                        )
                        human_delay(0.5, 1)
                    
                    await file_input.set_input_files(absolute_path)
                    uploaded = True
                    print("✅ Archivo subido vía input")
                    break
        except Exception as e:
            print(f"⚠️ Método input falló: {e}")
        
        # Método 2: Si input no funciona, usar drag & drop mejorado
        if not uploaded:
            print("↪️ Probando método drag & drop mejorado...")
            
            # Esperar un poco antes del drag & drop
            human_delay(2, 4)
            
            # Hacer drag & drop más realista
            success = await realistic_drag_and_drop(page, absolute_path)
            if success:
                uploaded = True
                print("✅ Archivo subido vía drag & drop")
            else:
                print("❌ Falló drag & drop")
        
        if not uploaded:
            print("❌ No se pudo subir el archivo con ningún método")
            await debug_screenshot(page, "upload_failed")
            return False
        
        # PASO 3: Verificación mejorada de carga
        print("⏳ Verificando carga del video con técnicas anti-detección...")
        
        # Esperar un poco para que inicie la carga
        human_delay(3, 5)
        
        # Verificar carga con múltiples indicadores
        video_loaded = await verify_upload_with_patience(page)
        
        if not video_loaded:
            print("⚠️ Video no se cargó correctamente - reintentando...")
            await debug_screenshot(page, "video_not_loaded")
            
            # Un reintento con paciencia extra
            human_delay(5, 8)
            await human_mouse_move(page)
            
            # Verificar de nuevo
            video_loaded = await verify_upload_with_patience(page)
            
            if not video_loaded:
                print("❌ Video definitivamente no se cargó")
                return False

        print("✅ Video cargado exitosamente")
        await debug_screenshot(page, "video_loaded_successfully")
        
        # Espera extra para estabilización (anti-detección)
        print("⏳ Esperando estabilización completa del video...")
        human_delay(30, 35)

        # Continuar con el resto del flujo...
        return await complete_upload_flow(page, descripcion, hashtags)

    except Exception as e:
        print(f"❌ Error en subida: {e}")
        await debug_screenshot(page, "upload_error")
        return False

        # PASO 3: Escribir descripción y hashtags
        human_delay(3, 5)
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

        # PASO 4: Abrir 'Show more' y activar etiqueta IA
        try:
            await debug_screenshot(page, "before_show_more_search")
            show_more_selectors = [
                'div[data-e2e="advanced_settings_container"] .more-btn',
                '.jsx-3335848873.more-btn',
                'div.more-btn',
                'button:has-text("Show more")',
                'button:has-text("Ver más")',
                '[data-testid="show-more-button"]',
                '.show-more-btn',
                'button[aria-label*="Show more"]',
                'button[aria-label*="Ver más"]',
                'button:has-text("More options")',
                'button:has-text("Más opciones")'
            ]
            show_more_clicked = False
            for selector in show_more_selectors:
                try:
                    show_more_btn = await page.query_selector(selector)
                    if show_more_btn and await show_more_btn.is_visible():
                        try:
                            await show_more_btn.click()
                            print(f"✅ Menú 'Show more' abierto con: {selector}")
                            human_delay(1, 2)
                            show_more_clicked = True
                            break
                        except Exception:
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
                '.TUXText:has-text("Checks")',
                'div[class*="TUXText"]:has-text("Checks")',
                'div:has-text("Checks")'
            ]
            ai_activated = False
            for selector in ai_selectors:
                try:
                    ai_element = await page.query_selector(selector)
                    if ai_element and await ai_element.is_visible():
                        if 'Checks' in selector:
                            await ai_element.click()
                            print(f"✅ Click en elemento Checks: {selector}")
                            human_delay(2, 3)
                            try:
                                await page.wait_for_selector('button:has-text("Turn on"), button:has-text("Activar")', timeout=5000)
                                turn_on_btn = await page.query_selector('button:has-text("Turn on"), button:has-text("Activar")')
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
                            try:
                                modal_appeared = await page.wait_for_selector('button:has-text("Turn on"), button:has-text("Activar")', timeout=3000, state='visible')
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

        # Regla: esperar 30s antes de publicar
        print("⏳ Esperando 30 segundos antes de publicar...")
        human_delay(30, 33)

        # Publicar
        human_delay(2, 3)
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
                    try:
                        confirmation_selectors = [
                            'button:has-text("Yes")',
                            'button:has-text("Confirm")',
                            'button:has-text("Continue")',
                            'button:has-text("Sí")',
                            'button:has-text("Confirmar")',
                            'button:has-text("Continuar")',
                            'button:has-text("Proceed")',
                            'button:has-text("Proceed to post")',
                            'button:has-text("Continuar para publicar")',
                            'button:has-text("Proceder a publicar")',
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
            return True
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
    # Construir lista de videos: primero el fundido final, luego todos los de processed
    videos_a_subir = []
    fundido_path = os.path.join("data", "videos", "final", "videos_unidos_FUNDIDO_TIKTOK.mp4")
    if os.path.exists(fundido_path):
        videos_a_subir.append({
            "video": fundido_path,
            "prompt": "Video ASMR viral (fundido final)"
        })
    else:
        print("ℹ️ No se encontró el video fundido final esperado.")

    processed_dir = os.path.join("data", "videos", "processed")
    processed_videos = sorted(glob(os.path.join(processed_dir, "*.mp4")))
    for vp in processed_videos:
        videos_a_subir.append({
            "video": vp,
            "prompt": "Video ASMR viral (procesado)"
        })
    
    if not videos_a_subir:
        print("❌ No hay videos para subir (fundido ni procesados)")
        return
    
    async with async_playwright() as p:
        # Configuración del navegador con técnicas anti-detección
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-blink-features=AutomationControlled',  # Anti-detección
                '--disable-features=VizDisplayCompositor',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                '--disable-extensions-except=',
                '--disable-extensions',
                '--no-first-run',
                '--disable-default-apps',
                '--disable-popup-blocking',
                '--disable-translate',
                '--disable-component-extensions-with-background-pages'
            ]
        )
        
        # Context con configuración más realista
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='es-ES',
            timezone_id='America/Mexico_City',
            permissions=['microphone', 'camera'],
            color_scheme='light',
            reduced_motion='no-preference',
            forced_colors='none'
        )
        
        # Ocultar que es un navegador automatizado
        await context.add_init_script("""
            // Eliminar indicadores de automatización
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Simular plugins reales
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Simular idiomas
            Object.defineProperty(navigator, 'languages', {
                get: () => ['es-ES', 'es', 'en'],
            });
            
            // Ocultar automation
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            
            // Simular comportamiento humano en eventos
            ['click', 'mousedown', 'mouseup', 'mousemove'].forEach(eventType => {
                const originalAddEventListener = EventTarget.prototype.addEventListener;
                EventTarget.prototype.addEventListener = function(type, listener, options) {
                    if (type === eventType) {
                        const wrappedListener = function(event) {
                            // Agregar pequeña variación temporal humana
                            setTimeout(() => listener.call(this, event), Math.random() * 50);
                        };
                        return originalAddEventListener.call(this, type, wrappedListener, options);
                    }
                    return originalAddEventListener.call(this, type, listener, options);
                };
            });
        """)
        
        page = await context.new_page()
        
        # Cargar cookies
        cookies_loaded = await cargar_cookies(context, "config/upload_cookies_playwright.json")
        if not cookies_loaded:
            print("❌ No se pudieron cargar las cookies")
            await browser.close()
            return
        
        # Visitar home y esperar 10s antes de ir a uploads (comportamiento natural)
        try:
            print("🌐 Navegando a TikTok con comportamiento humano...")
            await page.goto("https://www.tiktok.com/", timeout=60000)
            await page.wait_for_load_state('domcontentloaded', timeout=30000)
            
            # Simular actividad humana en la home
            await human_mouse_move(page)
            await human_scroll(page)
            human_delay(2, 4)
            
            # Simular click en algunos elementos para parecer humano
            try:
                # Intentar interactuar con elementos visibles
                await page.mouse.move(random.randint(100, 1000), random.randint(100, 600))
                human_delay(1, 2)
            except Exception:
                pass
            
            print("🏠 Página principal cargada, esperando 10s antes de ir a Upload...")
            await asyncio.sleep(10)
            
            # Más actividad humana antes de ir a upload
            await human_mouse_move(page)
            human_delay(1, 3)
            
        except Exception as e:
            print(f"⚠️ No se pudo cargar la home antes de subir: {e}")
        
        # Procesar cada video en orden (fundido primero, luego processed)
        for idx, video_data in enumerate(videos_a_subir, start=1):
            video_file = video_data["video"]
            prompt = video_data["prompt"]
            
            # Verificar si existe el archivo
            if not os.path.exists(video_file):
                print(f"⚠️ Video no encontrado: {video_file}")
                continue
            
            # PROCESAR ARCHIVO ORIGINAL DIRECTO (sin reconversión)
            print(f"🧪 ({idx}/{len(videos_a_subir)}) Preparando: {video_file}")
            
            # Generar contenido
            descripcion = generate_varied_description(prompt)
            hashtags = generate_varied_hashtags(prompt)
            
            print(f"📝 Descripción: {descripcion[:100]}...")
            print(f"🏷️ Hashtags: {' '.join(hashtags)}")
            
            # Subir video original
            current_time = datetime.now().strftime("%H:%M")
            print(f"⏰ Subiendo a las {current_time}")
            
            success = await subir_video_tiktok_optimized(page, video_file, descripcion, hashtags)
            
            if success:
                print("✅ Video procesado exitosamente")
            else:
                print("❌ Error procesando video")
            
            # Espera corta entre videos para naturalidad (60-90s)
            if idx < len(videos_a_subir):
                wait_time = random.randint(60, 90)
                print(f"⏳ Esperando {wait_time} segundos antes del siguiente video...")
                human_delay(wait_time, wait_time + 5)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
