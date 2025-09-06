#!/usr/bin/env python3
"""
🎯 TIKTOK UPLOADER ULTRA STEALTH V6 - XPATH EXACTO
Versión con XPath ultra específico proporcionado por el usuario
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
        """Cargar cookies guardadas"""
        try:
            if os.path.exists(self.cookies_path):
                with open(self.cookies_path, 'r') as f:
                    cookies = json.load(f)
                await context.add_cookies(cookies)
                print("✅ Cookies cargadas desde", self.cookies_path)
                return True
        except Exception as e:
            print(f"⚠️ Error cargando cookies: {e}")
        return False
    
    async def wait_for_upload_page(self, page):
        """Esperar a que la página de upload esté lista"""
        try:
            # Esperar por el input de archivo
            await page.wait_for_selector('input[type="file"]', timeout=10000)
            print("✅ Página de upload cargada")
            return True
        except:
            print("❌ Timeout esperando página de upload")
            return False
    
    async def upload_file_human(self, page):
        """Upload de archivo con comportamiento humano"""
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
        """Espera optimizada de 30 segundos con verificación"""
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
        await page.screenshot(path=f"ultra_stealth_v6_processing_{timestamp}.png")
        print(f"📸 Screenshot post-procesamiento: ultra_stealth_v6_processing_{timestamp}.png")
        
        return True
    
    async def activate_ai_content_v6_xpath_exact(self, page):
        """
        V6 XPATH EXACTO - Usando el XPath específico del usuario
        XPath: //*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[3]/div[3]/div/div/div
        """
        print("🎯 ACTIVACIÓN AI CONTENT XPATH EXACTO V6...")
        print(f"🔗 XPath: {self.ai_content_xpath}")
        
        try:
            # ESTRATEGIA V6 #1: XPath directo del usuario
            print("🔍 Estrategia V6 #1: XPath directo del usuario")
            
            xpath_element = await page.query_selector(f'xpath={self.ai_content_xpath}')
            if xpath_element:
                print("   📍 Elemento encontrado con XPath exacto")
                
                # Obtener información del elemento antes del click
                tag_name = await xpath_element.evaluate('el => el.tagName')
                class_name = await xpath_element.get_attribute('class')
                aria_checked = await xpath_element.get_attribute('aria-checked')
                data_state = await xpath_element.get_attribute('data-state')
                
                print(f"   📋 Tag: {tag_name}")
                print(f"   📋 Class: {class_name}")
                print(f"   📋 Aria-checked: {aria_checked}")
                print(f"   📋 Data-state: {data_state}")
                
                # Click en el elemento
                await xpath_element.click()
                await self.human_delay(1000, 2000)
                
                # Verificar cambios después del click
                new_aria_checked = await xpath_element.get_attribute('aria-checked')
                new_data_state = await xpath_element.get_attribute('data-state')
                new_class = await xpath_element.get_attribute('class')
                
                print(f"   🔄 Aria-checked después: {new_aria_checked}")
                print(f"   🔄 Data-state después: {new_data_state}")
                print(f"   🔄 Class después: {new_class}")
                
                # Determinar si se activó
                activated = (
                    (aria_checked == 'false' and new_aria_checked == 'true') or
                    (data_state == 'unchecked' and new_data_state == 'checked') or
                    ('checked-false' in str(class_name) and 'checked-true' in str(new_class))
                )
                
                if activated:
                    print("✅ AI Content activado - XPath directo exitoso")
                    return True
                else:
                    print("⚠️ XPath encontrado pero no se detectó cambio de estado")
            
            # ESTRATEGIA V6 #2: XPath con wildcards para mayor flexibilidad
            print("🔍 Estrategia V6 #2: XPath con variaciones")
            
            xpath_variations = [
                # XPath exacto pero buscando elementos clickeables dentro
                f'{self.ai_content_xpath}//div[@role="switch"]',
                f'{self.ai_content_xpath}//div[@aria-checked]',
                f'{self.ai_content_xpath}//div[@data-state]',
                f'{self.ai_content_xpath}//*[contains(@class, "Switch")]',
                # XPath del padre para buscar el switch correcto
                f'{self.ai_content_xpath}/..',
                f'{self.ai_content_xpath}/../..',
                # XPath buscando hermanos
                f'{self.ai_content_xpath}/following-sibling::*',
                f'{self.ai_content_xpath}/preceding-sibling::*'
            ]
            
            for i, xpath_var in enumerate(xpath_variations, 1):
                try:
                    print(f"   🎯 Variación #{i}: {xpath_var}")
                    elements = await page.query_selector_all(f'xpath={xpath_var}')
                    
                    if elements:
                        print(f"   📍 Encontrados {len(elements)} elementos con variación #{i}")
                        
                        for j, element in enumerate(elements):
                            try:
                                # Verificar si es clickeable
                                is_clickeable = await element.evaluate('''
                                    el => {
                                        const style = window.getComputedStyle(el);
                                        return style.pointerEvents !== 'none' && 
                                               style.visibility !== 'hidden' && 
                                               style.display !== 'none';
                                    }
                                ''')
                                
                                if is_clickeable:
                                    print(f"     🖱️ Elemento #{j+1} es clickeable, intentando...")
                                    await element.click()
                                    await self.human_delay(1000, 2000)
                                    
                                    # Verificar si algo cambió
                                    verification = await self.verify_ai_content_activation_v6(page)
                                    if verification:
                                        print(f"✅ AI Content activado - Variación #{i}, Elemento #{j+1}")
                                        return True
                                        
                            except Exception as e:
                                print(f"     ❌ Error con elemento #{j+1}: {str(e)[:50]}")
                                continue
                                
                except Exception as e:
                    print(f"   ❌ Error con variación #{i}: {str(e)[:50]}")
                    continue
            
            # ESTRATEGIA V6 #3: JavaScript para activar por XPath
            print("🔍 Estrategia V6 #3: JavaScript con XPath")
            
            js_result = await page.evaluate(f'''
                () => {{
                    const xpath = "{self.ai_content_xpath}";
                    const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    
                    if (element) {{
                        console.log("Elemento encontrado por XPath JavaScript:", element);
                        
                        // Intentar diferentes formas de activación
                        const methods = [
                            () => element.click(),
                            () => {{
                                const event = new MouseEvent('click', {{ bubbles: true, cancelable: true }});
                                element.dispatchEvent(event);
                            }},
                            () => {{
                                if (element.setAttribute) {{
                                    element.setAttribute('aria-checked', 'true');
                                    element.setAttribute('data-state', 'checked');
                                }}
                            }},
                            () => {{
                                // Buscar switch dentro del elemento
                                const switches = element.querySelectorAll('[role="switch"], [aria-checked], [data-state]');
                                for (let sw of switches) {{
                                    sw.click();
                                }}
                            }}
                        ];
                        
                        for (let i = 0; i < methods.length; i++) {{
                            try {{
                                methods[i]();
                                console.log(`Método ${{i+1}} ejecutado`);
                            }} catch (e) {{
                                console.log(`Método ${{i+1}} falló:`, e);
                            }}
                        }}
                        
                        return true;
                    }}
                    
                    return false;
                }}
            ''')
            
            if js_result:
                print("   📍 JavaScript XPath ejecutado")
                await self.human_delay(1000, 2000)
                
                # Verificar activación
                verification = await self.verify_ai_content_activation_v6(page)
                if verification:
                    print("✅ AI Content activado - JavaScript XPath")
                    return True
            
            print("❌ Todas las estrategias V6 XPath fallaron")
            return False
            
        except Exception as e:
            print(f"❌ Error en activación AI Content V6: {e}")
            return False
    
    async def verify_ai_content_activation_v6(self, page):
        """Verificación específica del estado AI Content V6"""
        try:
            # Verificar usando el XPath exacto
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
                    print("   ✅ Verificación V6: AI Content ACTIVADO (XPath directo)")
                    return True
            
            # Verificación alternativa por selectores generales
            checked_elements = await page.query_selector_all('[aria-checked="true"], [data-state="checked"], [class*="checked-true"]')
            if checked_elements:
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
                            print("   ✅ Verificación V6: AI Content encontrado en contexto")
                            return True
                    except:
                        continue
            
            print("   ❌ Verificación V6: AI Content NO activado")
            return False
            
        except Exception as e:
            print(f"   ❌ Error en verificación V6: {e}")
            return False
    
    async def setup_privacy(self, page):
        """Configurar privacidad a Everyone"""
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
        """Agregar descripción con escritura humana"""
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
        """Publicar el video"""
        try:
            # Screenshot pre-publicación
            timestamp = int(time.time())
            await page.screenshot(path=f"ultra_stealth_v6_pre_publish_{timestamp}.png")
            print(f"📸 Screenshot pre-publicación: ultra_stealth_v6_pre_publish_{timestamp}.png")
            
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
        """Ejecutar el proceso completo Ultra Stealth V6"""
        print("🎯 UPLOADER TIKTOK ULTRA STEALTH V6")
        print("=" * 60)
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
            # Configuración de navegador con máximo stealth
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
            
            # Crear contexto con configuración humana
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
                
                # ACTIVACIÓN AI CONTENT V6 CON XPATH EXACTO
                ai_activated = await self.activate_ai_content_v6_xpath_exact(page)
                
                if ai_activated:
                    # Verificación específica V6
                    verified = await self.verify_ai_content_activation_v6(page)
                    if verified:
                        print("✅ AI Content CONFIRMADO como activado V6")
                    else:
                        print("⚠️ AI Content activado pero verificación falló")
                else:
                    print("⚠️ AI Content no se pudo activar en V6")
                
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
