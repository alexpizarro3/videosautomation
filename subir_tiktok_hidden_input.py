#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK HIDDEN INPUT - MANEJO DE ELEMENTOS OCULTOS
Versión especializada para inputs ocultos de TikTok
"""

import asyncio
import json
import os
import random
from playwright.async_api import async_playwright
from dotenv import load_dotenv

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

async def subir_video_hidden_input(video_path, descripcion):
    """Subir video manejando inputs ocultos específicamente"""
    print("🎯 UPLOADER TIKTOK - HIDDEN INPUT HANDLER")
    print("=" * 60)
    print(f"📹 Video: {os.path.basename(video_path)}")
    print(f"📏 Tamaño: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--exclude-switches=enable-automation'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # Anti-detección
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        try:
            # Cargar cookies
            if not await cargar_cookies(context, "config/upload_cookies_playwright.json"):
                return False
            
            # Navegar directamente a upload
            print("\n📤 Navegando a TikTok Upload...")
            await page.goto("https://www.tiktok.com/creator-center/upload", timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(5)
            
            # Cerrar banner si aparece
            try:
                close_btn = await page.query_selector('button[aria-label="Close"]')
                if close_btn:
                    await close_btn.click()
                    await asyncio.sleep(2)
            except:
                pass
            
            print("✅ Página de upload cargada")
            
            # Buscar TODOS los inputs file, incluso ocultos
            print("\n🔍 Buscando inputs de archivo (incluyendo ocultos)...")
            
            # Usar query_selector_all para encontrar TODOS los inputs
            all_inputs = await page.query_selector_all('input[type="file"]')
            print(f"📁 Encontrados {len(all_inputs)} inputs de archivo")
            
            upload_success = False
            
            for i, input_elem in enumerate(all_inputs):
                try:
                    print(f"\n🎯 Probando input #{i+1}...")
                    
                    # Verificar atributos del input
                    accept_attr = await input_elem.get_attribute('accept')
                    class_attr = await input_elem.get_attribute('class')
                    
                    print(f"   Accept: {accept_attr}")
                    print(f"   Class: {class_attr}")
                    
                    # Intentar cargar archivo (incluso si está oculto)
                    await input_elem.set_input_files(video_path)
                    print(f"✅ ARCHIVO CARGADO EXITOSAMENTE con input #{i+1}")
                    upload_success = True
                    break
                    
                except Exception as e:
                    print(f"❌ Error con input #{i+1}: {e}")
                    continue
            
            if not upload_success:
                print("❌ No se pudo cargar el archivo con ningún input")
                return False
            
            # Esperar procesamiento largo
            print("\n⏳ Esperando procesamiento del video (60 segundos)...")
            await asyncio.sleep(60)
            
            # Verificar procesamiento
            print("\n🔍 Verificando procesamiento...")
            try:
                # Buscar múltiples indicadores de video procesado
                processing_indicators = [
                    'video',  # Video preview
                    'canvas',  # Canvas preview
                    'img[src*="thumb"]',  # Thumbnail
                    '[class*="preview"]',  # Preview container
                    '[class*="thumbnail"]'  # Thumbnail container
                ]
                
                video_processed = False
                for indicator in processing_indicators:
                    elements = await page.query_selector_all(indicator)
                    if elements:
                        print(f"✅ Indicador encontrado: {indicator} ({len(elements)} elementos)")
                        video_processed = True
                
                if not video_processed:
                    print("⚠️ No se detectaron indicadores de procesamiento")
                    # Continuar de todos modos
                
            except Exception as e:
                print(f"⚠️ Error verificando procesamiento: {e}")
            
            # Tomar screenshot después del procesamiento
            screenshot_path = f"after_processing_{random.randint(1000,9999)}.png"
            await page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot post-procesamiento: {screenshot_path}")
            
            # Buscar "Show More"
            print("\n🔍 Buscando 'Show More'...")
            try:
                show_more = await page.wait_for_selector('text="Show more"', timeout=10000)
                if show_more:
                    await show_more.click()
                    print("✅ Click en Show More")
                    await asyncio.sleep(3)
            except:
                print("⚠️ Show More no encontrado o no necesario")
            
            # Habilitar AI Content
            print("\n🤖 Habilitando AI Content...")
            try:
                ai_checkbox = await page.wait_for_selector('text="AI-generated content"', timeout=10000)
                if ai_checkbox:
                    await ai_checkbox.click()
                    print("✅ AI Content habilitado")
                    await asyncio.sleep(2)
                    
                    # Manejar modal
                    try:
                        modal = await page.wait_for_selector('[role="dialog"]', timeout=5000)
                        if modal:
                            accept_btn = await modal.wait_for_selector('text="Accept"', timeout=3000)
                            if accept_btn:
                                await accept_btn.click()
                                print("✅ Modal AI aceptado")
                    except:
                        pass
            except:
                print("⚠️ AI Content no encontrado")
            
            # Agregar descripción
            print("\n📝 Agregando descripción...")
            desc_selectors = [
                '[data-e2e="video-caption"]',
                'div[contenteditable="true"]',
                'textarea[placeholder*="description"]'
            ]
            
            for selector in desc_selectors:
                try:
                    desc_input = await page.wait_for_selector(selector, timeout=5000)
                    if desc_input:
                        await desc_input.click()
                        await desc_input.fill(descripcion)
                        print(f"✅ Descripción agregada: {selector}")
                        await asyncio.sleep(2)
                        break
                except:
                    continue
            
            # Tomar screenshot antes de publicar
            screenshot_path = f"before_publish_{random.randint(1000,9999)}.png"
            await page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot pre-publicación: {screenshot_path}")
            
            # Esperar antes de publicar
            print("\n⏳ Esperando antes de publicar (30 segundos)...")
            await asyncio.sleep(30)
            
            # Verificar botón de publicar
            print("\n🔍 Verificando botón de publicar...")
            publish_selectors = [
                '[data-e2e="post-btn"]',
                'text="Post"',
                'button[type="submit"]',
                'button:has-text("Post")'
            ]
            
            post_button = None
            for selector in publish_selectors:
                try:
                    btn = await page.wait_for_selector(selector, timeout=5000)
                    if btn:
                        is_disabled = await btn.is_disabled()
                        print(f"✅ Botón encontrado: {selector} (Disabled: {is_disabled})")
                        if not is_disabled:
                            post_button = btn
                            break
                except:
                    continue
            
            if post_button:
                print("\n🚀 Publicando video...")
                await post_button.click()
                print("✅ Video publicado!")
                
                # Manejar modal post-publicación
                try:
                    await asyncio.sleep(5)
                    modal = await page.wait_for_selector('[role="dialog"]', timeout=10000)
                    if modal:
                        accept_btn = await modal.wait_for_selector('text="Accept"', timeout=5000)
                        if accept_btn:
                            await accept_btn.click()
                            print("✅ Modal post-publicación aceptado")
                except:
                    pass
                
                # Screenshot final
                screenshot_path = f"publish_success_{random.randint(1000,9999)}.png"
                await page.screenshot(path=screenshot_path)
                print(f"📸 Screenshot final: {screenshot_path}")
                
                print("\n🎉 ¡VIDEO SUBIDO EXITOSAMENTE!")
                await asyncio.sleep(20)
                return True
                
            else:
                print("❌ No se encontró botón de publicar habilitado")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la subida: {e}")
            return False
        finally:
            print("\n🔍 Manteniendo browser abierto 30s para inspección...")
            await asyncio.sleep(30)
            await browser.close()

async def main():
    """Función principal"""
    load_dotenv()
    
    # Video a subir
    video_path = os.path.join("data", "videos", "final", "videos_unidos_FUNDIDO_TIKTOK.mp4")
    
    if not os.path.exists(video_path):
        print(f"❌ Video no encontrado: {video_path}")
        return
    
    descripcion = "🎭 Video ASMR viral generado con IA | Contenido hipnótico y relajante para máximo engagement #ASMR #IA #Viral #Satisfying #TikTok"
    
    success = await subir_video_hidden_input(video_path, descripcion)
    
    if success:
        print("\n🎉 ¡MISIÓN CUMPLIDA! Video subido manejando inputs ocultos")
    else:
        print("\n❌ Subida no completada - revisar manualmente")

if __name__ == "__main__":
    asyncio.run(main())
