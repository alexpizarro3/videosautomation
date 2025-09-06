#!/usr/bin/env python3
"""
🎯 TIKTOK UPLOADER ULTRA STEALTH V7 - BASADO EN V5 + XPATH EXACTO
Basado en V5 con XPath específico del usuario
XPath: //*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div
"""

import asyncio
import json
import os
import time
import random
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

class TikTokUltraStealth:
    def __init__(self):
        self.video_path = "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4"
        self.cookies_path = "config/upload_cookies_playwright.json"
        # XPath exacto del usuario
        self.ai_content_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div'
        
    async def human_delay(self, min_ms=100, max_ms=300):
        """Delay humano variable"""
        await asyncio.sleep(random.uniform(min_ms/1000, max_ms/1000))
    
    async def human_typing(self, page, selector, text, delay=50):
        """Escritura humana con delays variables"""
        await page.click(selector)
        await self.human_delay(200, 400)
        
        for char in text:
            await page.keyboard.type(char)
            await asyncio.sleep(random.uniform(delay/1000, (delay*2)/1000))
    
    async def load_cookies(self, context):
        """Cargar cookies guardadas - V5 style"""
        try:
            if os.path.exists(self.cookies_path):
                with open(self.cookies_path, 'r') as f:
                    cookies = json.load(f)
                
                # Fix sameSite como en V5
                for cookie in cookies:
                    if 'sameSite' in cookie:
                        val = cookie['sameSite']
                        if val not in ["Strict", "Lax", "None"]:
                            cookie["sameSite"] = "None"
                
                await context.add_cookies(cookies)
                print("✅ Cookies cargadas desde", self.cookies_path)
                return True
        except Exception as e:
            print(f"⚠️ Error cargando cookies: {e}")
        return False
    
    async def wait_for_upload_page(self, page):
        """Esperar a que la página de upload esté lista - V5 style"""
        try:
            # Esperar por el input de archivo
            await page.wait_for_selector('input[type="file"]', timeout=10000)
            print("✅ Página de upload cargada")
            return True
        except:
            print("❌ Timeout esperando página de upload")
            return False
    
    async def upload_file_human(self, page):
        """Upload de archivo con comportamiento humano - V5 style"""
        try:
            print("📁 Cargando archivo como humano...")
            
            # Buscar inputs de archivo
            file_inputs = await page.query_selector_all('input[type="file"]')
            print(f"📁 Encontrados {len(file_inputs)} inputs de archivo")
            
            if not file_inputs:
                print("❌ No se encontraron inputs de archivo")
                return False
            
            # Intentar cada input hasta que funcione
            for i, file_input in enumerate(file_inputs, 1):
                try:
                    print(f"🎯 Intentando input #{i}...")
                    await file_input.set_input_files(self.video_path)
                    await self.human_delay(1000, 2000)
                    print(f"✅ ARCHIVO CARGADO con input #{i}")
                    return True
                except Exception as e:
                    print(f"❌ Input #{i} falló: {str(e)[:100]}")
                    continue
            
            print("❌ Todos los inputs fallaron")
            return False
            
        except Exception as e:
            print(f"❌ Error en upload: {e}")
            return False
    
    async def wait_processing_optimized(self, page):
        """Espera optimizada de 30 segundos con verificación - V5 style"""
        print("⏳ Procesamiento optimizado (30 segundos)...")
        
        for i in range(0, 31, 5):
            print(f"⏳ Procesando... {i}/30s")
            await asyncio.sleep(5)
        
        # Verificación final
        print("🔍 Verificación final de procesamiento...")
        
        indicators = {
            'canvas': await page.query_selector_all('canvas'),
            '[class*="preview"]': await page.query_selector_all('[class*="preview"]'),
            '[class*="player"]': await page.query_selector_all('[class*="player"]')
        }
        
        print("✅ Indicadores encontrados:")
        for name, elements in indicators.items():
            print(f"   - {name} ({len(elements)})")
        
        # Screenshot de verificación
        timestamp = int(time.time())
        await page.screenshot(path=f"ultra_stealth_v7_processing_{timestamp}.png")
        print(f"📸 Screenshot post-procesamiento: ultra_stealth_v7_processing_{timestamp}.png")
        
        return True
    
    async def activate_ai_content_v7_xpath_focused(self, page):
        """
        V7 XPATH FOCUSED - Basado en V5 + XPath específico del usuario
        Combinando lo mejor de V5 con targeting exacto de XPath
        """
        print("🎯 ACTIVACIÓN AI CONTENT V7 - XPATH FOCUSED...")
        print(f"🔗 XPath objetivo: {self.ai_content_xpath}")
        
        try:
            # ESTRATEGIA V7 #1: XPath directo (como solicitaste)
            print("🔍 Estrategia V7 #1: XPath directo del usuario")
            
            xpath_element = await page.query_selector(f'xpath={self.ai_content_xpath}')
            if xpath_element:
                print("   📍 Elemento encontrado con XPath exacto")
                
                # Obtener información del elemento antes del click
                try:
                    tag_name = await xpath_element.evaluate('el => el.tagName')
                    class_name = await xpath_element.get_attribute('class')
                    aria_checked = await xpath_element.get_attribute('aria-checked')
                    data_state = await xpath_element.get_attribute('data-state')
                    
                    print(f"   📋 Tag: {tag_name}")
                    print(f"   📋 Class: {class_name}")
                    print(f"   📋 Aria-checked ANTES: {aria_checked}")
                    print(f"   📋 Data-state ANTES: {data_state}")
                    
                    # Click en el elemento
                    await xpath_element.click()
                    await self.human_delay(1000, 2000)
                    
                    # Verificar cambios después del click
                    new_aria_checked = await xpath_element.get_attribute('aria-checked')
                    new_data_state = await xpath_element.get_attribute('data-state')
                    new_class = await xpath_element.get_attribute('class')
                    
                    print(f"   🔄 Aria-checked DESPUÉS: {new_aria_checked}")
                    print(f"   🔄 Data-state DESPUÉS: {new_data_state}")
                    print(f"   🔄 Class DESPUÉS: {new_class}")
                    
                    # Determinar si se activó (lógica de V5 mejorada)
                    activated = (
                        (aria_checked == 'false' and new_aria_checked == 'true') or
                        (data_state == 'unchecked' and new_data_state == 'checked') or
                        ('checked-false' in str(class_name) and 'checked-true' in str(new_class))
                    )
                    
                    if activated:
                        print("✅ AI Content activado - XPath directo V7")
                        return True
                    else:
                        print("⚠️ XPath encontrado pero estado no cambió")
                        
                except Exception as e:
                    print(f"   ❌ Error procesando elemento XPath: {e}")
            else:
                print("   ❌ Elemento XPath no encontrado")
            
            # ESTRATEGIA V7 #2: Combinar XPath con selectores V5 (híbrido)
            print("🔍 Estrategia V7 #2: XPath + selectores V5 híbridos")
            
            # Primero intentar encontrar el área general con XPath
            xpath_area = await page.query_selector(f'xpath={self.ai_content_xpath}/..')
            if xpath_area:
                print("   📍 Área padre de XPath encontrada")
                
                # Buscar switches dentro del área usando selectores V5
                switch_selectors = [
                    'div.Switch_root.Switch_root--checked-false',
                    '[data-state="unchecked"]',
                    '[aria-checked="false"]',
                    '[class*="Switch"]'
                ]
                
                for selector in switch_selectors:
                    switches = await xpath_area.query_selector_all(selector)
                    print(f"   📍 Encontrados {len(switches)} switches con {selector}")
                    
                    for i, switch in enumerate(switches):
                        try:
                            # Verificar contexto AI
                            parent_text = await switch.evaluate('''
                                el => {
                                    let current = el;
                                    for (let i = 0; i < 5; i++) {
                                        if (current.textContent && current.textContent.toLowerCase().includes('ai')) {
                                            return current.textContent;
                                        }
                                        current = current.parentElement;
                                        if (!current) break;
                                    }
                                    return '';
                                }
                            ''')
                            
                            if 'ai' in parent_text.lower():
                                print(f"   🎯 Switch #{i+1} en contexto AI - clickeando")
                                await switch.click()
                                await self.human_delay(1000, 2000)
                                
                                # Verificar activación
                                verified = await self.verify_ai_content_activation_v7(page)
                                if verified:
                                    print("✅ AI Content activado - XPath+V5 híbrido")
                                    return True
                        except Exception as e:
                            print(f"     ❌ Error con switch #{i+1}: {str(e)[:50]}")
                            continue
            
            # ESTRATEGIA V7 #3: JavaScript con XPath (de V5 pero enfocado)
            print("🔍 Estrategia V7 #3: JavaScript con XPath específico")
            
            js_result = await page.evaluate(f'''
                () => {{
                    const xpath = "{self.ai_content_xpath}";
                    const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    
                    if (element) {{
                        console.log("V7: Elemento XPath encontrado:", element);
                        
                        // Método 1: Click directo
                        element.click();
                        
                        // Método 2: Buscar switches dentro
                        const switches = element.querySelectorAll('[role="switch"], [aria-checked], [data-state], [class*="Switch"]');
                        console.log("V7: Switches encontrados:", switches.length);
                        
                        for (let sw of switches) {{
                            try {{
                                sw.click();
                                console.log("V7: Switch clickeado");
                            }} catch (e) {{
                                console.log("V7: Error clicking switch:", e);
                            }}
                        }}
                        
                        // Método 3: Forzar cambio de estado
                        if (element.setAttribute) {{
                            element.setAttribute('aria-checked', 'true');
                            element.setAttribute('data-state', 'checked');
                            if (element.classList) {{
                                element.classList.remove('Switch_root--checked-false');
                                element.classList.add('Switch_root--checked-true');
                            }}
                        }}
                        
                        return true;
                    }}
                    
                    return false;
                }}
            ''')
            
            if js_result:
                print("   📍 JavaScript XPath ejecutado")
                await self.human_delay(1500, 2500)
                
                # Verificar activación
                verified = await self.verify_ai_content_activation_v7(page)
                if verified:
                    print("✅ AI Content activado - JavaScript XPath V7")
                    return True
            
            # ESTRATEGIA V7 #4: Fallback a método V5 original
            print("🔍 Estrategia V7 #4: Fallback a método V5 original")
            
            # Texto exacto como en V5
            ai_text_elements = await page.query_selector_all('text="AI-generated content"')
            if ai_text_elements:
                print(f"   📍 Encontrados {len(ai_text_elements)} elementos con texto AI")
                
                for element in ai_text_elements:
                    try:
                        # Buscar el container como en V5
                        container = await element.query_selector('xpath=../../../..')
                        if container:
                            toggles = await container.query_selector_all('[role="switch"], [aria-checked], [data-state]')
                            print(f"   🎛️ Encontrados {len(toggles)} toggles en el contenedor")
                            
                            for j, toggle in enumerate(toggles, 1):
                                try:
                                    is_checked = await toggle.get_attribute('aria-checked')
                                    state = await toggle.get_attribute('data-state')
                                    print(f"     🔘 Toggle #{j} - Checked: {is_checked}, State: {state}")
                                    
                                    if is_checked == 'false' or state == 'unchecked':
                                        await toggle.click()
                                        await self.human_delay(1000, 2000)
                                        
                                        # Verificar cambio
                                        new_checked = await toggle.get_attribute('aria-checked')
                                        new_state = await toggle.get_attribute('data-state')
                                        
                                        if new_checked == 'true' or new_state == 'checked':
                                            print(f"✅ AI Content activado - Toggle #{j} V5 fallback")
                                            return True
                                except Exception as e:
                                    print(f"     ❌ Error con toggle #{j}: {str(e)[:50]}")
                                    continue
                    except Exception as e:
                        print(f"   ❌ Error con elemento texto AI: {str(e)[:50]}")
                        continue
            
            print("❌ Todas las estrategias V7 fallaron")
            return False
            
        except Exception as e:
            print(f"❌ Error en activación AI Content V7: {e}")
            return False
    
    async def verify_ai_content_activation_v7(self, page):
        """Verificación V7 - Combina XPath específico + verificación V5"""
        try:
            # Verificación #1: XPath directo
            xpath_element = await page.query_selector(f'xpath={self.ai_content_xpath}')
            if xpath_element:
                aria_checked = await xpath_element.get_attribute('aria-checked')
                data_state = await xpath_element.get_attribute('data-state')
                class_name = await xpath_element.get_attribute('class')
                
                activated = (
                    aria_checked == 'true' or
                    data_state == 'checked' or
                    (class_name and 'checked-true' in class_name)
                )
                
                if activated:
                    print("   ✅ Verificación V7 #1: XPath directo ACTIVADO")
                    return True
            
            # Verificación #2: Método V5 general
            checked_elements = await page.query_selector_all('[aria-checked="true"], [data-state="checked"]')
            for element in checked_elements:
                try:
                    # Verificar si está en contexto AI
                    parent_text = await element.evaluate('''
                        el => {
                            let current = el;
                            for (let i = 0; i < 10; i++) {
                                if (current.textContent && current.textContent.toLowerCase().includes('ai')) {
                                    return current.textContent;
                                }
                                current = current.parentElement;
                                if (!current) break;
                            }
                            return '';
                        }
                    ''')
                    
                    if parent_text and 'ai' in parent_text.lower():
                        print("   ✅ Verificación V7 #2: AI Content en contexto general")
                        return True
                except:
                    continue
            
            # Verificación #3: Clase CSS específica
            switch_true = await page.query_selector('div.Switch_root.Switch_root--checked-true')
            if switch_true:
                print("   ✅ Verificación V7 #3: Switch_root--checked-true encontrado")
                return True
            
            print("   ❌ Verificación V7: AI Content NO activado")
            return False
            
        except Exception as e:
            print(f"   ❌ Error en verificación V7: {e}")
            return False
    
    async def setup_privacy(self, page):
        """Configurar privacidad a Everyone - V5 style"""
        try:
            print("🔒 Configurando Privacy (Everyone)...")
            
            # Buscar y clickear Everyone
            everyone_button = await page.query_selector('text="Everyone"')
            if everyone_button:
                await everyone_button.click()
                await self.human_delay(300, 600)
                print("✅ Privacy configurado: text=\"Everyone\"")
                return True
            
            # Alternativa por aria-label
            everyone_alt = await page.query_selector('[aria-label*="Everyone"]')
            if everyone_alt:
                await everyone_alt.click()
                await self.human_delay(300, 600)
                print("✅ Privacy configurado: aria-label Everyone")
                return True
            
            print("⚠️ No se pudo configurar Privacy")
            return False
            
        except Exception as e:
            print(f"❌ Error configurando Privacy: {e}")
            return False
    
    async def add_description(self, page):
        """Agregar descripción con escritura humana - V5 style"""
        try:
            print("📝 Agregando descripción...")
            
            description = "🎬 Contenido creativo e innovador"
            
            # Buscar textarea de descripción
            desc_selectors = [
                'textarea[placeholder*="escrib"]',
                'textarea[placeholder*="Describ"]',
                'div[contenteditable="true"]',
                '[data-testid*="caption"]'
            ]
            
            for selector in desc_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        await self.human_typing(page, selector, description)
                        print("✅ Descripción agregada con escritura humana")
                        return True
                except:
                    continue
            
            print("⚠️ No se pudo agregar descripción")
            return False
            
        except Exception as e:
            print(f"❌ Error agregando descripción: {e}")
            return False
    
    async def publish_video(self, page):
        """Publicar el video - V5 style"""
        try:
            # Screenshot pre-publicación
            timestamp = int(time.time())
            await page.screenshot(path=f"ultra_stealth_v7_pre_publish_{timestamp}.png")
            print(f"📸 Screenshot pre-publicación: ultra_stealth_v7_pre_publish_{timestamp}.png")
            
            print("⏳ Espera antes de publicar...")
            await self.human_delay(2000, 4000)
            
            print("🚀 Publicando video...")
            
            # Buscar botón de publicar
            publish_selectors = [
                'button:has-text("Publicar")',
                'button:has-text("Post")',
                '[data-e2e="publish-button"]',
                'button[type="submit"]'
            ]
            
            for selector in publish_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button:
                        await button.click()
                        await self.human_delay(1000, 2000)
                        print("✅ Video publicado con comportamiento humano")
                        return True
                except:
                    continue
            
            print("⚠️ No se encontró botón de publicar")
            return False
            
        except Exception as e:
            print(f"❌ Error publicando: {e}")
            return False
    
    async def run(self):
        """Ejecutar el proceso completo Ultra Stealth V7"""
        print("🎯 UPLOADER TIKTOK ULTRA STEALTH V7")
        print("=" * 60)
        print("🔧 BASADO EN V5 + XPATH ESPECÍFICO")
        print(f"🔗 XPath AI Content: {self.ai_content_xpath}")
        print("=" * 60)
        
        # Verificar archivo
        if not os.path.exists(self.video_path):
            print(f"❌ Archivo no encontrado: {self.video_path}")
            return False
        
        file_size = os.path.getsize(self.video_path) / (1024*1024)
        print(f"📹 Video: {self.video_path}")
        print(f"📏 Tamaño: {file_size:.1f} MB")
        
        async with async_playwright() as p:
            # Configuración de navegador con máximo stealth (como V5)
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
                    '--disable-infobars',
                    '--disable-extensions-except',
                    '--disable-extensions',
                    '--disable-default-apps',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
            )
            
            # Crear contexto con configuración humana (como V5)
            context = await browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='es-ES',
                timezone_id='America/Mexico_City'
            )
            
            # Cargar cookies
            await self.load_cookies(context)
            
            page = await context.new_page()
            
            try:
                print("🌐 Navegando como humano a TikTok...")
                await page.goto('https://www.tiktok.com', wait_until='networkidle')
                await self.human_delay(2000, 3000)
                
                print("📱 Simulando actividad humana...")
                await page.mouse.move(
                    random.randint(100, 500), 
                    random.randint(100, 400)
                )
                await self.human_delay(1000, 2000)
                
                print("📤 Navegando a Creator Center...")
                await page.goto(
                    'https://www.tiktok.com/creator-center/upload', 
                    wait_until='networkidle'
                )
                
                # Esperar página de upload
                if not await self.wait_for_upload_page(page):
                    print("❌ Error: Página de upload no cargó")
                    return False
                
                # Upload de archivo
                if not await self.upload_file_human(page):
                    print("❌ Error: No se pudo cargar el archivo")
                    return False
                
                # Esperar procesamiento optimizado
                await self.wait_processing_optimized(page)
                
                # Buscar opciones avanzadas
                print("🔍 Buscando opciones avanzadas...")
                try:
                    show_more = await page.query_selector('text="Show More"')
                    if show_more:
                        await show_more.click()
                        await self.human_delay(1000, 2000)
                        print("✅ Show More clickeado")
                except:
                    print("⚠️ Show More no encontrado, continuando...")
                
                # ACTIVACIÓN AI CONTENT V7 - XPATH FOCUSED
                ai_activated = await self.activate_ai_content_v7_xpath_focused(page)
                
                if ai_activated:
                    # Verificación V7
                    verified = await self.verify_ai_content_activation_v7(page)
                    if verified:
                        print("✅ AI Content CONFIRMADO como activado V7")
                    else:
                        print("⚠️ AI Content activado pero verificación falló")
                else:
                    print("⚠️ AI Content no se pudo activar en V7")
                
                # Configurar privacy
                await self.setup_privacy(page)
                
                # Agregar descripción
                await self.add_description(page)
                
                # Publicar
                await self.publish_video(page)
                
                # Espera final
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"❌ Error en proceso principal: {e}")
                return False
            
            finally:
                await browser.close()
        
        return True

# Ejecutar
if __name__ == "__main__":
    uploader = TikTokUltraStealth()
    asyncio.run(uploader.run())
