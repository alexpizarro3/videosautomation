#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK ULTRA STEALTH V6 MEJORADO - XPATH EXACTO
Basado en V4 exitoso + XPath específico del usuario
XPath: //*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div
"""

import asyncio
import json
import os
import random
import time
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# XPath específico del usuario
AI_CONTENT_XPATH = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div'

async def cargar_cookies(context, cookies_path):
    """Cargar cookies de sesión"""
    try:
        with open(cookies_path, 'r') as f:
            cookies = json.load(f)
        
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

async def movimiento_humano_realista(page):
    """Simula movimientos de mouse completamente humanos"""
    await page.mouse.move(
        random.randint(200, 1200), 
        random.randint(200, 800),
        steps=random.randint(10, 30)
    )
    await asyncio.sleep(random.uniform(0.5, 2.0))
    
    if random.random() < 0.3:
        await page.mouse.wheel(0, random.randint(-100, 100))
        await asyncio.sleep(random.uniform(0.3, 1.0))

async def escribir_como_humano(element, texto):
    """Escribe texto como un humano real"""
    await element.click()
    await asyncio.sleep(random.uniform(0.2, 0.8))
    
    for caracter in texto:
        await element.type(caracter)
        await asyncio.sleep(random.uniform(0.05, 0.15))

async def subir_archivo_ultra_stealth(page, ruta_archivo):
    """Subida ultra stealth de archivo"""
    print("📁 Cargando archivo como humano...")
    
    file_inputs = await page.query_selector_all('input[type="file"]')
    print(f"📁 Encontrados {len(file_inputs)} inputs de archivo")
    
    if not file_inputs:
        return False
    
    for i, file_input in enumerate(file_inputs, 1):
        try:
            print(f"🎯 Intentando input #{i}...")
            await file_input.set_input_files(ruta_archivo)
            await asyncio.sleep(random.uniform(1, 3))
            print(f"✅ ARCHIVO CARGADO con input #{i}")
            return True
        except Exception as e:
            print(f"❌ Input #{i} falló: {str(e)[:100]}")
            continue
    
    return False

async def activar_ai_content_xpath_v6(page):
    """
    V6 - Activación AI Content con XPath específico del usuario
    """
    print("🎯 ACTIVACIÓN AI CONTENT XPATH EXACTO V6...")
    print(f"🔗 XPath objetivo: {AI_CONTENT_XPATH}")
    
    try:
        # ESTRATEGIA #1: XPath directo del usuario
        print("🔍 Estrategia V6 #1: XPath directo")
        
        xpath_element = await page.query_selector(f'xpath={AI_CONTENT_XPATH}')
        if xpath_element:
            print("   📍 Elemento encontrado con XPath exacto")
            
            # Información del elemento
            try:
                tag_name = await xpath_element.evaluate('el => el.tagName')
                class_list = await xpath_element.evaluate('el => el.className')
                aria_checked = await xpath_element.get_attribute('aria-checked')
                data_state = await xpath_element.get_attribute('data-state')
                
                print(f"   📋 Tag: {tag_name}")
                print(f"   📋 Clases: {class_list}")
                print(f"   📋 aria-checked: {aria_checked}")
                print(f"   📋 data-state: {data_state}")
                
                # Click directo
                await xpath_element.click()
                await asyncio.sleep(2)
                
                # Verificar cambios
                new_aria = await xpath_element.get_attribute('aria-checked')
                new_state = await xpath_element.get_attribute('data-state')
                new_classes = await xpath_element.evaluate('el => el.className')
                
                print(f"   🔄 DESPUÉS - aria-checked: {new_aria}")
                print(f"   🔄 DESPUÉS - data-state: {new_state}")
                print(f"   🔄 DESPUÉS - clases: {new_classes}")
                
                # Determinar activación
                activated = (
                    (aria_checked == 'false' and new_aria == 'true') or
                    (data_state == 'unchecked' and new_state == 'checked') or
                    ('checked-false' in str(class_list) and 'checked-true' in str(new_classes))
                )
                
                if activated:
                    print("✅ AI Content activado - XPath directo V6")
                    return True
            except Exception as e:
                print(f"   ❌ Error procesando elemento XPath: {e}")
        
        # ESTRATEGIA #2: XPath con búsqueda en elementos hijos
        print("🔍 Estrategia V6 #2: XPath + elementos hijos")
        
        xpath_children = await page.query_selector_all(f'xpath={AI_CONTENT_XPATH}//*')
        print(f"   📍 Encontrados {len(xpath_children)} elementos hijos")
        
        for i, child in enumerate(xpath_children):
            try:
                tag = await child.evaluate('el => el.tagName')
                role = await child.get_attribute('role')
                aria_checked = await child.get_attribute('aria-checked')
                
                if role == 'switch' or aria_checked is not None:
                    print(f"   🎯 Elemento hijo #{i+1} clickeable: {tag} (role: {role})")
                    await child.click()
                    await asyncio.sleep(2)
                    
                    # Verificar cambio
                    new_aria = await child.get_attribute('aria-checked')
                    if aria_checked == 'false' and new_aria == 'true':
                        print("✅ AI Content activado - XPath hijo V6")
                        return True
            except:
                continue
        
        # ESTRATEGIA #3: XPath con JavaScript
        print("🔍 Estrategia V6 #3: JavaScript + XPath")
        
        js_result = await page.evaluate(f'''
            () => {{
                const xpath = "{AI_CONTENT_XPATH}";
                const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                
                if (element) {{
                    console.log("Elemento XPath encontrado:", element);
                    
                    // Buscar switches dentro del elemento
                    const switches = element.querySelectorAll('[role="switch"], [aria-checked], [data-state]');
                    console.log("Switches encontrados:", switches.length);
                    
                    for (let i = 0; i < switches.length; i++) {{
                        const sw = switches[i];
                        const beforeState = sw.getAttribute('aria-checked') || sw.getAttribute('data-state');
                        
                        // Intentar click
                        sw.click();
                        
                        // Esperar un poco
                        setTimeout(() => {{
                            const afterState = sw.getAttribute('aria-checked') || sw.getAttribute('data-state');
                            console.log(`Switch ${{i}}: ${{beforeState}} -> ${{afterState}}`);
                        }}, 500);
                    }}
                    
                    return switches.length > 0;
                }}
                
                return false;
            }}
        ''')
        
        if js_result:
            print("   📍 JavaScript XPath ejecutado")
            await asyncio.sleep(3)
            
            # Verificar activación
            verified = await verificar_ai_content_v6(page)
            if verified:
                print("✅ AI Content activado - JavaScript XPath V6")
                return True
        
        # ESTRATEGIA #4: XPath padres/hermanos
        print("🔍 Estrategia V6 #4: XPath padres y hermanos")
        
        xpath_variations = [
            f'{AI_CONTENT_XPATH}/..',
            f'{AI_CONTENT_XPATH}/../..',
            f'{AI_CONTENT_XPATH}/following-sibling::*',
            f'{AI_CONTENT_XPATH}/preceding-sibling::*'
        ]
        
        for i, xpath_var in enumerate(xpath_variations):
            try:
                elements = await page.query_selector_all(f'xpath={xpath_var}')
                print(f"   📍 Variación #{i+1}: {len(elements)} elementos")
                
                for element in elements:
                    switches = await element.query_selector_all('[role="switch"], [aria-checked="false"]')
                    for switch in switches:
                        try:
                            await switch.click()
                            await asyncio.sleep(1)
                            
                            # Verificar contexto AI
                            parent_text = await element.text_content()
                            if parent_text and 'ai' in parent_text.lower():
                                print(f"✅ AI Content activado - XPath variación #{i+1}")
                                return True
                        except:
                            continue
            except:
                continue
        
        print("❌ Todas las estrategias XPath V6 fallaron")
        return False
        
    except Exception as e:
        print(f"❌ Error en activación XPath V6: {e}")
        return False

async def verificar_ai_content_v6(page):
    """Verificación específica V6"""
    try:
        # Verificar XPath directo
        xpath_element = await page.query_selector(f'xpath={AI_CONTENT_XPATH}')
        if xpath_element:
            aria_checked = await xpath_element.get_attribute('aria-checked')
            data_state = await xpath_element.get_attribute('data-state')
            classes = await xpath_element.evaluate('el => el.className')
            
            if (aria_checked == 'true' or 
                data_state == 'checked' or 
                'checked-true' in str(classes)):
                print("   ✅ Verificación V6: AI Content ACTIVADO")
                return True
        
        # Verificación general
        ai_switches = await page.query_selector_all('[aria-checked="true"]')
        for switch in ai_switches:
            try:
                parent = await switch.query_selector('xpath=../../../..')
                if parent:
                    text = await parent.text_content()
                    if text and 'ai' in text.lower():
                        print("   ✅ Verificación V6: AI switch encontrado")
                        return True
            except:
                continue
        
        print("   ❌ Verificación V6: AI Content NO activado")
        return False
        
    except Exception as e:
        print(f"   ❌ Error verificación V6: {e}")
        return False

async def main():
    """Función principal Ultra Stealth V6"""
    print("🎯 UPLOADER TIKTOK ULTRA STEALTH V6 MEJORADO")
    print("=" * 60)
    print(f"🔗 XPath AI Content: {AI_CONTENT_XPATH}")
    print("=" * 60)
    
    video_path = "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4"
    cookies_path = "config/upload_cookies_playwright.json"
    
    if not os.path.exists(video_path):
        print(f"❌ Archivo no encontrado: {video_path}")
        return
    
    file_size = os.path.getsize(video_path) / (1024*1024)
    print(f"📹 Video: {video_path}")
    print(f"📏 Tamaño: {file_size:.1f} MB")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--disable-infobars'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        await cargar_cookies(context, cookies_path)
        
        page = await context.new_page()
        
        try:
            print("🌐 Navegando como humano a TikTok...")
            await page.goto('https://www.tiktok.com', wait_until='networkidle')
            await movimiento_humano_realista(page)
            
            print("📤 Navegando a Creator Center...")
            await page.goto('https://www.tiktok.com/creator-center/upload', wait_until='networkidle')
            await asyncio.sleep(2)
            
            # Verificar página cargada
            try:
                await page.wait_for_selector('input[type="file"]', timeout=10000)
                print("✅ Página de upload cargada")
            except:
                print("❌ Timeout - página no cargó")
                return
            
            # Upload archivo
            if not await subir_archivo_ultra_stealth(page, video_path):
                print("❌ Error subiendo archivo")
                return
            
            # Procesamiento optimizado 30s
            print("⏳ Procesamiento optimizado (30 segundos)...")
            for i in range(0, 31, 5):
                print(f"⏳ Procesando... {i}/30s")
                await asyncio.sleep(5)
            
            # Verificar procesamiento
            indicators = {
                'canvas': await page.query_selector_all('canvas'),
                '[class*="preview"]': await page.query_selector_all('[class*="preview"]'),
                '[class*="player"]': await page.query_selector_all('[class*="player"]')
            }
            
            print("✅ Indicadores encontrados:")
            for name, elements in indicators.items():
                print(f"   - {name} ({len(elements)})")
            
            timestamp = int(time.time())
            await page.screenshot(path=f"ultra_stealth_v6_processing_{timestamp}.png")
            print(f"📸 Screenshot: ultra_stealth_v6_processing_{timestamp}.png")
            
            # Show More
            try:
                show_more = await page.query_selector('text="Show More"')
                if show_more:
                    await show_more.click()
                    await asyncio.sleep(2)
                    print("✅ Show More clickeado")
            except:
                print("⚠️ Show More no encontrado")
            
            # ACTIVACIÓN AI CONTENT V6 CON XPATH
            ai_activated = await activar_ai_content_xpath_v6(page)
            
            if ai_activated:
                verified = await verificar_ai_content_v6(page)
                if verified:
                    print("✅ AI Content CONFIRMADO V6")
                else:
                    print("⚠️ AI Content activado pero verificación falló")
            else:
                print("⚠️ AI Content no activado en V6")
            
            # Privacy
            try:
                everyone_button = await page.query_selector('text="Everyone"')
                if everyone_button:
                    await everyone_button.click()
                    await asyncio.sleep(1)
                    print("✅ Privacy: Everyone")
            except:
                print("⚠️ Privacy no configurado")
            
            # Descripción
            try:
                desc_selectors = [
                    'textarea[placeholder*="escrib"]',
                    'div[contenteditable="true"]'
                ]
                
                for selector in desc_selectors:
                    element = await page.query_selector(selector)
                    if element:
                        await escribir_como_humano(element, "🎬 Contenido creativo")
                        print("✅ Descripción agregada")
                        break
            except:
                print("⚠️ Descripción no agregada")
            
            # Screenshot pre-publish
            timestamp = int(time.time())
            await page.screenshot(path=f"ultra_stealth_v6_pre_publish_{timestamp}.png")
            print(f"📸 Pre-publish: ultra_stealth_v6_pre_publish_{timestamp}.png")
            
            # Publicar
            await asyncio.sleep(3)
            print("🚀 Publicando video...")
            
            publish_selectors = [
                'button:has-text("Publicar")',
                'button:has-text("Post")',
                'button[type="submit"]'
            ]
            
            for selector in publish_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button:
                        await button.click()
                        await asyncio.sleep(2)
                        print("✅ Video publicado")
                        break
                except:
                    continue
            
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
