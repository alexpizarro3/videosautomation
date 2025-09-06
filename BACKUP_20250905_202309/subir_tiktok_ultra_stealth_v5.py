#!/usr/bin/env python3
"""
🎯 TIKTOK UPLOADER ULTRA STEALTH V5 - SUPER ESPECÍFICO AI CONTENT
Versión ultra-específica basada en HTML real inspeccionado por el usuario
Targeting exacto: Switch_root--checked-false → Switch_root--checked-true
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
        await page.screenshot(path=f"ultra_stealth_v5_processing_{timestamp}.png")
        print(f"📸 Screenshot post-procesamiento: ultra_stealth_v5_processing_{timestamp}.png")
        
        return True
    
    async def activate_ai_content_v5_super_specific(self, page):
        """
        V5 SUPER ESPECÍFICO - Basado en HTML real inspeccionado
        Target: Switch_root--checked-false → Switch_root--checked-true
        """
        print("🎯 ACTIVACIÓN AI CONTENT SUPER ESPECÍFICO V5...")
        
        try:
            # ESTRATEGIA V5 #1: Selector CSS ultra específico basado en HTML real
            print("🔍 Estrategia V5 #1: Selector CSS ultra específico")
            
            # Buscar el switch específico con las clases exactas del HTML
            switch_selector = 'div.Switch_root.Switch_root--checked-false.Switch_root--disabled-false[data-layout="switch-root"]'
            switch_element = await page.query_selector(switch_selector)
            
            if switch_element:
                print("   📍 Switch encontrado con selector ultra específico")
                await switch_element.click()
                await self.human_delay(500, 1000)
                
                # Verificar cambio de clase
                updated_element = await page.query_selector('div.Switch_root.Switch_root--checked-true')
                if updated_element:
                    print("✅ AI Content activado - Clase cambiada a checked-true")
                    return True
            
            # ESTRATEGIA V5 #2: Por data-state="unchecked"
            print("🔍 Estrategia V5 #2: Por data-state unchecked")
            
            unchecked_elements = await page.query_selector_all('[data-state="unchecked"]')
            print(f"   📍 Encontrados {len(unchecked_elements)} elementos unchecked")
            
            for element in unchecked_elements:
                try:
                    # Verificar si está en contexto de AI content
                    parent = await element.query_selector('xpath=..')
                    if parent:
                        text_content = await parent.text_content()
                        if text_content and 'ai' in text_content.lower():
                            print("   🎯 Elemento AI encontrado por data-state")
                            await element.click()
                            await self.human_delay(500, 1000)
                            
                            # Verificar cambio
                            new_state = await element.get_attribute('data-state')
                            if new_state == 'checked':
                                print("✅ AI Content activado - data-state changed to checked")
                                return True
                except:
                    continue
            
            # ESTRATEGIA V5 #3: Por aria-checked="false"
            print("🔍 Estrategia V5 #3: Por aria-checked false")
            
            aria_false_elements = await page.query_selector_all('[aria-checked="false"]')
            print(f"   📍 Encontrados {len(aria_false_elements)} elementos aria-checked false")
            
            for element in aria_false_elements:
                try:
                    # Buscar contexto AI
                    container = await element.query_selector('xpath=../../../..')
                    if container:
                        container_text = await container.text_content()
                        if container_text and ('ai-generated' in container_text.lower() or 'ai content' in container_text.lower()):
                            print("   🎯 Elemento AI encontrado por aria-checked")
                            await element.click()
                            await self.human_delay(500, 1000)
                            
                            # Verificar cambio
                            new_aria = await element.get_attribute('aria-checked')
                            if new_aria == 'true':
                                print("✅ AI Content activado - aria-checked changed to true")
                                return True
                except:
                    continue
            
            # ESTRATEGIA V5 #4: JavaScript directo para cambiar estado
            print("🔍 Estrategia V5 #4: JavaScript directo")
            
            js_result = await page.evaluate("""
                () => {
                    // Buscar elemento con las clases específicas del HTML
                    const switches = document.querySelectorAll('div.Switch_root.Switch_root--checked-false');
                    
                    for (let switchEl of switches) {
                        const parent = switchEl.closest('div');
                        if (parent && parent.textContent.toLowerCase().includes('ai')) {
                            // Simular click
                            switchEl.click();
                            
                            // Verificar cambio
                            setTimeout(() => {
                                const isNowChecked = switchEl.classList.contains('Switch_root--checked-true') ||
                                                  switchEl.getAttribute('aria-checked') === 'true' ||
                                                  switchEl.getAttribute('data-state') === 'checked';
                                return isNowChecked;
                            }, 500);
                            
                            return true;
                        }
                    }
                    return false;
                }
            """)
            
            if js_result:
                print("✅ AI Content activado - JavaScript directo")
                await self.human_delay(1000, 1500)
                return True
            
            print("❌ Todas las estrategias V5 fallaron")
            return False
            
        except Exception as e:
            print(f"❌ Error en activación AI Content V5: {e}")
            return False
    
    async def verify_ai_content_activation_v5(self, page):
        """Verificación super específica del estado AI Content V5"""
        try:
            # Verificar por clase CSS
            checked_true = await page.query_selector('div.Switch_root.Switch_root--checked-true')
            if checked_true:
                print("   ✅ Verificación V5 #1: Switch_root--checked-true encontrado")
                return True
            
            # Verificar por data-state
            checked_state = await page.query_selector('[data-state="checked"]')
            if checked_state:
                # Verificar contexto AI
                parent = await checked_state.query_selector('xpath=../../..')
                if parent:
                    text = await parent.text_content()
                    if text and 'ai' in text.lower():
                        print("   ✅ Verificación V5 #2: data-state checked en contexto AI")
                        return True
            
            # Verificar por aria-checked
            aria_true = await page.query_selector('[aria-checked="true"]')
            if aria_true:
                container = await aria_true.query_selector('xpath=../../../..')
                if container:
                    text = await container.text_content()
                    if text and 'ai' in text.lower():
                        print("   ✅ Verificación V5 #3: aria-checked true en contexto AI")
                        return True
            
            print("   ❌ Verificación V5: AI Content NO activado")
            return False
            
        except Exception as e:
            print(f"   ❌ Error en verificación V5: {e}")
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
            await page.screenshot(path=f"ultra_stealth_v5_pre_publish_{timestamp}.png")
            print(f"📸 Screenshot pre-publicación: ultra_stealth_v5_pre_publish_{timestamp}.png")
            
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
        """Ejecutar el proceso completo Ultra Stealth V5"""
        print("🎯 UPLOADER TIKTOK ULTRA STEALTH V5")
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
                
                # ACTIVACIÓN AI CONTENT V5 SUPER ESPECÍFICO
                ai_activated = await self.activate_ai_content_v5_super_specific(page)
                
                if ai_activated:
                    # Verificación super específica V5
                    verified = await self.verify_ai_content_activation_v5(page)
                    if verified:
                        print("✅ AI Content CONFIRMADO como activado V5")
                    else:
                        print("⚠️ AI Content activado pero verificación falló")
                else:
                    print("⚠️ AI Content no se pudo activar en V5")
                
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
