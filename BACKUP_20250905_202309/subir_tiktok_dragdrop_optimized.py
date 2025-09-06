#!/usr/bin/env python3
"""
🎯 UPLOADER TIKTOK OPTIMIZADO PARA DRAG AND DROP
Método comprobado exitoso para subida de videos
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

async def drag_and_drop_upload(page, video_path):
    """Implementación optimizada de drag and drop"""
    print("🎯 INICIANDO DRAG AND DROP OPTIMIZADO")
    print("=" * 50)
    
    try:
        # Paso 1: Encontrar área de upload
        print("📍 Buscando área de upload...")
        
        upload_selectors = [
            '[data-e2e="upload-input"]',
            'input[type="file"]',
            '.upload-area',
            '.drop-zone',
            '[class*="upload"]',
            '[accept*="video"]'
        ]
        
        upload_element = None
        for selector in upload_selectors:
            try:
                element = await page.wait_for_selector(selector, timeout=10000)
                if element:
                    upload_element = element
                    print(f"✅ Elemento de upload encontrado: {selector}")
                    break
            except:
                continue
        
        if not upload_element:
            print("❌ No se encontró elemento de upload")
            return False
        
        # Paso 2: Implementar drag and drop
        print(f"📁 Ejecutando drag and drop: {os.path.basename(video_path)}")
        
        # Método probado exitoso: set_input_files en input file
        try:
            await upload_element.set_input_files(video_path)
            print("✅ DRAG AND DROP EXITOSO - Archivo cargado")
            return True
            
        except Exception as e:
            print(f"⚠️ Método directo falló: {e}")
            
            # Fallback: Buscar input file oculto
            print("🔄 Buscando input file oculto...")
            try:
                hidden_inputs = await page.query_selector_all('input[type="file"]')
                if hidden_inputs:
                    for input_elem in hidden_inputs:
                        try:
                            await input_elem.set_input_files(video_path)
                            print("✅ ÉXITO con input oculto")
                            return True
                        except:
                            continue
                
                print("❌ No se pudo usar inputs ocultos")
                return False
                
            except Exception as fallback_error:
                print(f"❌ Error en fallback: {fallback_error}")
                return False
                
    except Exception as e:
        print(f"❌ Error general en drag and drop: {e}")
        return False

async def subir_video_drag_drop(video_path, descripcion):
    """Subir video usando método drag and drop exitoso"""
    print("🎬 UPLOADER TIKTOK - MÉTODO DRAG AND DROP")
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
                '--disable-gpu'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        try:
            # Cargar cookies
            if not await cargar_cookies(context, "config/upload_cookies_playwright.json"):
                return False
            
            # Navegar a upload
            print("\n📤 Navegando a TikTok Upload...")
            await page.goto("https://www.tiktok.com/creator-center/upload", timeout=30000)
            await page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(3)
            
            # Verificar página
            if "upload" not in page.url:
                print(f"❌ URL incorrecta: {page.url}")
                return False
            
            print("✅ Página de upload cargada")
            
            # DRAG AND DROP
            upload_success = await drag_and_drop_upload(page, video_path)
            if not upload_success:
                print("❌ Fallo en drag and drop")
                return False
            
            # Esperar procesamiento (30 segundos)
            print("\n⏳ Esperando 30 segundos para procesamiento...")
            await asyncio.sleep(30)
            
            # Buscar "Show More"
            print("\n🔍 Buscando 'Show More'...")
            show_more_selectors = [
                'text="Show more"',
                'text="Mostrar más"',
                'button:has-text("Show")',
                'button:has-text("more")',
                '[class*="show-more"]'
            ]
            
            for selector in show_more_selectors:
                try:
                    btn = await page.wait_for_selector(selector, timeout=5000)
                    if btn:
                        await btn.click()
                        print(f"✅ Click en Show More: {selector}")
                        await asyncio.sleep(2)
                        break
                except:
                    continue
            
            # Habilitar AI Content
            print("\n🤖 Habilitando AI Content...")
            ai_selectors = [
                'text="AI-generated content"',
                'text="AI content"',
                'input[type="checkbox"]:near(text="AI")',
                'label:has-text("AI")'
            ]
            
            for selector in ai_selectors:
                try:
                    ai_elem = await page.wait_for_selector(selector, timeout=5000)
                    if ai_elem:
                        await ai_elem.click()
                        print(f"✅ AI Content habilitado: {selector}")
                        await asyncio.sleep(2)
                        
                        # Manejar modal si aparece
                        try:
                            modal = await page.wait_for_selector('[role="dialog"]', timeout=3000)
                            if modal:
                                accept_btn = await modal.wait_for_selector('text="Accept"', timeout=3000)
                                if accept_btn:
                                    await accept_btn.click()
                                    print("✅ Modal AI Content aceptado")
                        except:
                            pass
                        break
                except:
                    continue
            
            # Agregar descripción
            print("\n📝 Agregando descripción...")
            desc_selectors = [
                '[data-e2e="video-caption"]',
                'textarea[placeholder*="description"]',
                'div[contenteditable="true"]'
            ]
            
            for selector in desc_selectors:
                try:
                    desc_input = await page.wait_for_selector(selector, timeout=5000)
                    if desc_input:
                        await desc_input.click()
                        await desc_input.fill(descripcion)
                        print(f"✅ Descripción agregada: {selector}")
                        break
                except:
                    continue
            
            # Esperar antes de publicar
            print("\n⏳ Esperando 30 segundos antes de publicar...")
            await asyncio.sleep(30)
            
            # Verificar preview
            print("\n📺 Verificando preview...")
            try:
                video_preview = await page.wait_for_selector('video', timeout=10000)
                if video_preview:
                    print("✅ Preview del video detectado")
                else:
                    print("⚠️ Preview no detectado")
            except:
                print("⚠️ No se pudo verificar preview")
            
            # Publicar
            print("\n🚀 Publicando video...")
            publish_selectors = [
                '[data-e2e="post-btn"]',
                'text="Post"',
                'button[type="submit"]',
                'button:has-text("Post")'
            ]
            
            published = False
            for selector in publish_selectors:
                try:
                    post_btn = await page.wait_for_selector(selector, timeout=10000)
                    if post_btn and not await post_btn.is_disabled():
                        await post_btn.click()
                        print(f"✅ Video publicado: {selector}")
                        
                        # Manejar modal post-publicación
                        try:
                            await asyncio.sleep(3)
                            modal = await page.wait_for_selector('[role="dialog"]', timeout=5000)
                            if modal:
                                accept_btn = await modal.wait_for_selector('text="Accept"', timeout=3000)
                                if accept_btn:
                                    await accept_btn.click()
                                    print("✅ Modal post-publicación aceptado")
                        except:
                            pass
                        
                        published = True
                        break
                except:
                    continue
            
            if published:
                print("\n🎉 ¡VIDEO SUBIDO EXITOSAMENTE!")
                
                # Tomar screenshot final
                screenshot_path = f"upload_success_{random.randint(1000,9999)}.png"
                await page.screenshot(path=screenshot_path)
                print(f"📸 Screenshot final: {screenshot_path}")
                
                await asyncio.sleep(10)
                return True
            else:
                print("❌ No se pudo publicar el video")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la subida: {e}")
            return False
        finally:
            print("\n🔍 Manteniendo browser abierto 20s para inspección...")
            await asyncio.sleep(20)
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
    
    success = await subir_video_drag_drop(video_path, descripcion)
    
    if success:
        print("\n🎉 ¡MISIÓN CUMPLIDA! Video subido con drag and drop exitoso")
    else:
        print("\n❌ Subida no completada - revisar manualmente")

if __name__ == "__main__":
    asyncio.run(main())
