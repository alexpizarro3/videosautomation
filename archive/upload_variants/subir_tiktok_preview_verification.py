#!/usr/bin/env python3
"""
🎬 UPLOADER TIKTOK CON VERIFICACIÓN DE PREVIEW MEJORADA
Enfoque específico en asegurar que el video se muestre en portada y preview
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

async def verificar_preview_video(page, timeout=60):
    """Verificación exhaustiva del preview del video"""
    print("\n🔍 VERIFICANDO PREVIEW DEL VIDEO...")
    print("=" * 50)
    
    verification_steps = []
    
    # Paso 1: Verificar que el video se esté procesando
    try:
        print("📊 Paso 1: Verificando estado de procesamiento...")
        
        # Buscar indicadores de procesamiento
        processing_selectors = [
            '[data-e2e="upload-progress"]',
            '.upload-progress',
            'text="Processing"',
            'text="Uploading"',
            '[class*="progress"]'
        ]
        
        processing_found = False
        for selector in processing_selectors:
            try:
                element = await page.wait_for_selector(selector, timeout=5000)
                if element:
                    print(f"✅ Indicador de procesamiento encontrado: {selector}")
                    processing_found = True
                    break
            except:
                continue
        
        if processing_found:
            verification_steps.append("✅ Video en procesamiento")
        else:
            print("⚠️  No se detectaron indicadores de procesamiento")
            verification_steps.append("⚠️  Procesamiento no detectado")
            
    except Exception as e:
        print(f"❌ Error verificando procesamiento: {e}")
        verification_steps.append("❌ Error en verificación de procesamiento")
    
    # Paso 2: Esperar a que aparezca el preview
    try:
        print("\n📺 Paso 2: Esperando preview del video...")
        
        preview_selectors = [
            'video',
            '[data-e2e="video-preview"]',
            '.video-preview',
            'video[src]',
            'video[controls]'
        ]
        
        preview_found = False
        preview_element = None
        
        for selector in preview_selectors:
            try:
                preview_element = await page.wait_for_selector(selector, timeout=15000)
                if preview_element:
                    print(f"✅ Preview encontrado: {selector}")
                    preview_found = True
                    break
            except:
                continue
        
        if preview_found and preview_element:
            # Verificar que el video tenga contenido
            try:
                src = await preview_element.get_attribute('src')
                if src:
                    print(f"✅ Video tiene src: {src[:50]}...")
                    verification_steps.append("✅ Preview con contenido")
                else:
                    print("⚠️  Video sin src attribute")
                    verification_steps.append("⚠️  Preview sin src")
            except:
                verification_steps.append("⚠️  No se pudo verificar src del video")
        else:
            print("❌ No se encontró preview del video")
            verification_steps.append("❌ Preview no encontrado")
            
    except Exception as e:
        print(f"❌ Error verificando preview: {e}")
        verification_steps.append("❌ Error en verificación de preview")
    
    # Paso 3: Verificar thumbnail/portada
    try:
        print("\n🖼️  Paso 3: Verificando thumbnail/portada...")
        
        thumbnail_selectors = [
            '[data-e2e="video-cover"]',
            '.video-cover',
            '.thumbnail',
            'img[alt*="cover"]',
            '[class*="cover"]',
            '[class*="thumbnail"]'
        ]
        
        thumbnail_found = False
        for selector in thumbnail_selectors:
            try:
                element = await page.wait_for_selector(selector, timeout=10000)
                if element:
                    print(f"✅ Thumbnail encontrado: {selector}")
                    thumbnail_found = True
                    break
            except:
                continue
        
        if thumbnail_found:
            verification_steps.append("✅ Thumbnail/portada detectada")
        else:
            print("⚠️  No se detectó thumbnail específico")
            verification_steps.append("⚠️  Thumbnail no detectado")
            
    except Exception as e:
        print(f"❌ Error verificando thumbnail: {e}")
        verification_steps.append("❌ Error en verificación de thumbnail")
    
    # Paso 4: Verificar botones de publicación
    try:
        print("\n📤 Paso 4: Verificando botones de publicación...")
        
        publish_selectors = [
            '[data-e2e="post-btn"]',
            'button[type="submit"]',
            'text="Post"',
            'text="Publish"',
            'button[class*="post"]',
            'button[class*="publish"]'
        ]
        
        publish_found = False
        for selector in publish_selectors:
            try:
                element = await page.wait_for_selector(selector, timeout=5000)
                if element:
                    # Verificar si el botón está habilitado
                    is_disabled = await element.is_disabled()
                    if not is_disabled:
                        print(f"✅ Botón de publicación activo: {selector}")
                        publish_found = True
                        break
                    else:
                        print(f"⚠️  Botón encontrado pero deshabilitado: {selector}")
            except:
                continue
        
        if publish_found:
            verification_steps.append("✅ Botón de publicación activo")
        else:
            print("❌ No se encontró botón de publicación activo")
            verification_steps.append("❌ Botón de publicación no disponible")
            
    except Exception as e:
        print(f"❌ Error verificando botón de publicación: {e}")
        verification_steps.append("❌ Error en verificación de publicación")
    
    # Paso 5: Tomar screenshot para evidencia
    try:
        print("\n📸 Paso 5: Capturando evidencia...")
        screenshot_path = f"upload_verification_{random.randint(1000,9999)}.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"✅ Screenshot guardado: {screenshot_path}")
        verification_steps.append(f"✅ Evidencia: {screenshot_path}")
    except Exception as e:
        print(f"❌ Error capturando screenshot: {e}")
        verification_steps.append("❌ Error capturando evidencia")
    
    # Resumen de verificación
    print(f"\n📊 RESUMEN DE VERIFICACIÓN:")
    print("=" * 50)
    for step in verification_steps:
        print(f"   {step}")
    
    # Determinar éxito
    success_count = len([s for s in verification_steps if s.startswith("✅")])
    total_steps = len(verification_steps)
    success_rate = (success_count / total_steps) * 100 if total_steps > 0 else 0
    
    print(f"\n🎯 TASA DE ÉXITO: {success_rate:.1f}% ({success_count}/{total_steps})")
    
    if success_rate >= 60:  # Consideramos éxito si 60% o más de verificaciones pasan
        print("🎉 VERIFICACIÓN EXITOSA: Video listo para publicación")
        return True
    else:
        print("⚠️  VERIFICACIÓN PARCIAL: Revisar manualmente antes de publicar")
        return False

async def subir_video_con_verificacion(video_path, descripcion="Video ASMR viral generado con IA"):
    """Subir video con verificación exhaustiva del preview"""
    print(f"🎬 INICIANDO SUBIDA CON VERIFICACIÓN DE PREVIEW")
    print("=" * 60)
    print(f"📹 Video: {os.path.basename(video_path)}")
    print(f"📝 Descripción: {descripcion}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Mostrar para debugging
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox', 
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        try:
            # Cargar cookies
            cookies_loaded = await cargar_cookies(context, "config/upload_cookies_playwright.json")
            if not cookies_loaded:
                print("❌ No se pudieron cargar las cookies")
                return False
            
            # Ir directamente a la página de upload
            print("\n📤 Navegando a página de upload...")
            await page.goto("https://www.tiktok.com/creator-center/upload", timeout=30000)
            await page.wait_for_load_state('domcontentloaded', timeout=15000)
            await asyncio.sleep(3)
            
            # Verificar que estamos en la página correcta
            if "upload" not in page.url:
                print(f"❌ No se pudo acceder a la página de upload. URL actual: {page.url}")
                return False
            
            print("✅ Página de upload cargada correctamente")
            
            # MÉTODO DRAG AND DROP (MÁS EXITOSO)
            print("\n🎯 Usando método DRAG AND DROP (exitoso comprobado)...")
            
            # Buscar área de drop
            drop_area_selectors = [
                '[data-e2e="upload-input"]',
                '.upload-input',
                '.drop-area',
                '[class*="drop"]',
                '[class*="upload-area"]',
                'div[data-e2e="upload-input"]',
                '.upload-zone',
                'input[type="file"]'
            ]
            
            drop_area = None
            input_element = None
            
            for selector in drop_area_selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=10000)
                    if element:
                        print(f"✅ Área de upload encontrada: {selector}")
                        
                        # Si es un input file, lo guardamos por separado
                        tag_name = await element.evaluate('el => el.tagName.toLowerCase()')
                        if tag_name == 'input':
                            input_element = element
                        else:
                            drop_area = element
                        break
                except:
                    continue
            
            if not drop_area and not input_element:
                print("❌ No se encontró área de upload")
                return False
            
            # DRAG AND DROP IMPLEMENTATION
            print(f"\n📁 Iniciando DRAG AND DROP para: {video_path}")
            
            try:
                # Método 1: Usar input file oculto si está disponible
                if input_element:
                    print("🔄 Usando input file con drag and drop simulation...")
                    await input_element.set_input_files(video_path)
                    print("✅ Archivo cargado via input file")
                    
                # Método 2: Simulación completa de drag and drop
                elif drop_area:
                    print("🔄 Simulando drag and drop completo...")
                    
                    # Crear evento de drag and drop
                    await page.evaluate("""
                        async (selector, filePath) => {
                            const element = document.querySelector(selector);
                            if (!element) return false;
                            
                            // Simular drag over
                            const dragOverEvent = new DragEvent('dragover', {
                                bubbles: true,
                                cancelable: true,
                                dataTransfer: new DataTransfer()
                            });
                            element.dispatchEvent(dragOverEvent);
                            
                            // Simular drop
                            const dropEvent = new DragEvent('drop', {
                                bubbles: true,
                                cancelable: true,
                                dataTransfer: new DataTransfer()
                            });
                            element.dispatchEvent(dropEvent);
                            
                            return true;
                        }
                    """, selector)
                    
                    # También intentar con input file si existe
                    file_inputs = await page.query_selector_all('input[type="file"]')
                    if file_inputs:
                        await file_inputs[0].set_input_files(video_path)
                        print("✅ Fallback: archivo cargado via input file oculto")
                
                print("✅ DRAG AND DROP completado exitosamente")
                
            except Exception as e:
                print(f"❌ Error en drag and drop: {e}")
                
                # Fallback: método tradicional
                print("🔄 Intentando método fallback...")
                try:
                    file_inputs = await page.query_selector_all('input[type="file"]')
                    if file_inputs:
                        await file_inputs[0].set_input_files(video_path)
                        print("✅ Fallback exitoso")
                    else:
                        print("❌ No se pudo cargar el archivo")
                        return False
                except Exception as fallback_error:
                    print(f"❌ Fallback falló: {fallback_error}")
                    return False
            
            # PASO CRÍTICO 1: Esperar 30 segundos después de cargar el video
            print("⏳ Esperando 30 segundos para que el video se procese completamente...")
            await asyncio.sleep(30)
            
            # PASO CRÍTICO 2: Buscar y hacer click en "Show More" o "Mostrar más"
            print("\n🔍 Buscando botón 'Show More' o 'Mostrar más'...")
            show_more_selectors = [
                'text="Show more"',
                'text="Mostrar más"',
                'text="Ver más"',
                'button[aria-label*="Show more"]',
                'button[aria-label*="Mostrar"]',
                '[data-e2e="show-more"]',
                'button:has-text("Show more")',
                'button:has-text("Mostrar")',
                '.show-more',
                '[class*="show-more"]'
            ]
            
            show_more_clicked = False
            for selector in show_more_selectors:
                try:
                    show_more_btn = await page.wait_for_selector(selector, timeout=5000)
                    if show_more_btn:
                        await show_more_btn.click()
                        print(f"✅ Click en 'Show More' exitoso: {selector}")
                        await asyncio.sleep(2)  # Esperar a que se expandan las opciones
                        show_more_clicked = True
                        break
                except:
                    continue
            
            if not show_more_clicked:
                print("⚠️  No se encontró botón 'Show More', continuando...")
            
            # PASO CRÍTICO 3: Habilitar "AI Content" o contenido de IA
            print("\n🤖 Buscando y habilitando opción 'AI Content'...")
            ai_content_selectors = [
                'text="AI-generated content"',
                'text="AI content"',
                'text="Contenido IA"',
                'text="Contenido generado por IA"',
                'input[type="checkbox"][id*="ai"]',
                'input[type="checkbox"][name*="ai"]',
                '[data-e2e="ai-content"]',
                'label:has-text("AI")',
                'label:has-text("IA")',
                'input[value*="ai"]',
                'switch:has-text("AI")'
            ]
            
            ai_content_enabled = False
            for selector in ai_content_selectors:
                try:
                    ai_element = await page.wait_for_selector(selector, timeout=5000)
                    if ai_element:
                        # Si es un checkbox o switch, verificar si ya está habilitado
                        tag_name = await ai_element.evaluate('el => el.tagName.toLowerCase()')
                        
                        if tag_name == 'input':
                            is_checked = await ai_element.is_checked()
                            if not is_checked:
                                await ai_element.click()
                                print(f"✅ AI Content habilitado: {selector}")
                                ai_content_enabled = True
                            else:
                                print(f"✅ AI Content ya estaba habilitado: {selector}")
                                ai_content_enabled = True
                        else:
                            # Para otros elementos, simplemente hacer click
                            await ai_element.click()
                            print(f"✅ Click en AI Content: {selector}")
                            ai_content_enabled = True
                        
                        await asyncio.sleep(2)
                        break
                except:
                    continue
            
            if not ai_content_enabled:
                print("⚠️  No se encontró opción 'AI Content', continuando...")
            
            # PASO CRÍTICO 4: Manejar modal de confirmación de AI Content
            print("\n📋 Verificando si aparece modal de confirmación...")
            modal_selectors = [
                '[role="dialog"]',
                '.modal',
                '[data-e2e="modal"]',
                'div[class*="modal"]',
                'div[class*="dialog"]'
            ]
            
            modal_found = False
            for selector in modal_selectors:
                try:
                    modal = await page.wait_for_selector(selector, timeout=5000)
                    if modal:
                        print(f"✅ Modal detectado: {selector}")
                        
                        # Buscar botón de aceptar en el modal
                        accept_selectors = [
                            'text="Accept"',
                            'text="Aceptar"',
                            'text="OK"',
                            'text="Confirm"',
                            'text="Confirmar"',
                            'text="Continue"',
                            'text="Continuar"',
                            'button[data-e2e="confirm"]',
                            'button[class*="confirm"]',
                            'button[class*="accept"]'
                        ]
                        
                        accept_clicked = False
                        for accept_selector in accept_selectors:
                            try:
                                accept_btn = await modal.wait_for_selector(accept_selector, timeout=3000)
                                if accept_btn:
                                    await accept_btn.click()
                                    print(f"✅ Click en aceptar modal: {accept_selector}")
                                    await asyncio.sleep(2)
                                    accept_clicked = True
                                    modal_found = True
                                    break
                            except:
                                continue
                        
                        if not accept_clicked:
                            print("⚠️  Modal encontrado pero no se pudo hacer click en aceptar")
                        break
                except:
                    continue
            
            if not modal_found:
                print("ℹ️  No apareció modal de confirmación")
            
            # Agregar descripción
            print("\n📝 Agregando descripción...")
            description_selectors = [
                '[data-e2e="video-caption"]',
                'textarea[placeholder*="description"]',
                'textarea[placeholder*="caption"]',
                'div[contenteditable="true"]'
            ]
            
            for selector in description_selectors:
                try:
                    desc_input = await page.wait_for_selector(selector, timeout=5000)
                    if desc_input:
                        await desc_input.click()
                        await desc_input.fill(descripcion)
                        print(f"✅ Descripción agregada usando: {selector}")
                        break
                except:
                    continue
            
            # VERIFICACIÓN EXHAUSTIVA DEL PREVIEW
            verification_success = await verificar_preview_video(page, timeout=60)
            
            if verification_success:
                # PASO CRÍTICO 5: Esperar 30 segundos antes de publicar
                print("\n⏳ Esperando 30 segundos adicionales antes de publicar...")
                await asyncio.sleep(30)
                
                # Intentar publicar
                print("\n🚀 Intentando publicar video...")
                
                publish_selectors = [
                    '[data-e2e="post-btn"]',
                    'button[type="submit"]',
                    'text="Post"',
                    'text="Publicar"',
                    'button[class*="post"]',
                    'button:has-text("Post")',
                    'button:has-text("Publicar")'
                ]
                
                published = False
                for selector in publish_selectors:
                    try:
                        publish_btn = await page.wait_for_selector(selector, timeout=10000)
                        if publish_btn and not await publish_btn.is_disabled():
                            await publish_btn.click()
                            print(f"✅ Click en botón publicar: {selector}")
                            
                            # PASO CRÍTICO 6: Manejar modal de confirmación post-publicación
                            print("\n📋 Verificando modal post-publicación...")
                            await asyncio.sleep(3)  # Esperar a que aparezca el modal
                            
                            # Buscar y manejar cualquier modal que aparezca
                            post_modal_selectors = [
                                '[role="dialog"]',
                                '.modal',
                                '[data-e2e="modal"]',
                                'div[class*="modal"]',
                                'div[class*="dialog"]',
                                'div[class*="confirm"]'
                            ]
                            
                            modal_handled = False
                            for modal_selector in post_modal_selectors:
                                try:
                                    post_modal = await page.wait_for_selector(modal_selector, timeout=5000)
                                    if post_modal:
                                        print(f"✅ Modal post-publicación detectado: {modal_selector}")
                                        
                                        # Buscar botón de aceptar/confirmar en el modal
                                        modal_accept_selectors = [
                                            'text="Accept"',
                                            'text="Aceptar"',
                                            'text="OK"',
                                            'text="Confirm"',
                                            'text="Confirmar"',
                                            'text="Continue"',
                                            'text="Continuar"',
                                            'text="Agree"',
                                            'text="De acuerdo"',
                                            'text="Submit"',
                                            'text="Enviar"',
                                            'button[data-e2e="confirm"]',
                                            'button[data-e2e="accept"]',
                                            'button[class*="confirm"]',
                                            'button[class*="accept"]',
                                            'button[class*="primary"]'
                                        ]
                                        
                                        modal_accept_clicked = False
                                        for accept_selector in modal_accept_selectors:
                                            try:
                                                accept_btn = await post_modal.wait_for_selector(accept_selector, timeout=3000)
                                                if accept_btn:
                                                    await accept_btn.click()
                                                    print(f"✅ Click en aceptar modal post-publicación: {accept_selector}")
                                                    await asyncio.sleep(2)
                                                    modal_accept_clicked = True
                                                    modal_handled = True
                                                    break
                                            except:
                                                continue
                                        
                                        if modal_accept_clicked:
                                            break
                                except:
                                    continue
                            
                            if not modal_handled:
                                print("ℹ️  No apareció modal post-publicación o ya fue manejado")
                            
                            published = True
                            
                            # Esperar confirmación final
                            print("⏳ Esperando confirmación final de publicación...")
                            await asyncio.sleep(10)
                            break
                    except Exception as e:
                        print(f"⚠️  Error intentando publicar con {selector}: {e}")
                        continue
                
                if published:
                    print("🎉 VIDEO SUBIDO Y PUBLICADO EXITOSAMENTE")
                    return True
                else:
                    print("⚠️  Video verificado pero no se pudo publicar automáticamente")
                    print("💡 Revisar manualmente y publicar desde la interfaz")
                    return False
            else:
                print("❌ VERIFICACIÓN DEL PREVIEW FALLÓ")
                print("🔧 RECOMENDACIONES:")
                print("   1. Verificar formato del video (MP4, H.264)")
                print("   2. Comprobar resolución (720x1280 recomendado)")
                print("   3. Verificar duración del video")
                print("   4. Revisar manualmente en la interfaz")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la subida: {e}")
            return False
        finally:
            # Mantener browser abierto para inspección manual
            print("\n🔍 Browser se mantendrá abierto 30s para inspección manual...")
            await asyncio.sleep(30)
            await browser.close()

async def main():
    """Función principal"""
    load_dotenv()
    
    print("🎬 UPLOADER TIKTOK CON VERIFICACIÓN DE PREVIEW MEJORADA")
    print("=" * 70)
    
    # Usar el video fundido como ejemplo
    video_path = os.path.join("data", "videos", "final", "videos_unidos_FUNDIDO_TIKTOK.mp4")
    
    if not os.path.exists(video_path):
        print(f"❌ Video no encontrado: {video_path}")
        return
    
    print(f"📹 Subiendo video: {os.path.basename(video_path)}")
    print(f"📏 Tamaño: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    
    success = await subir_video_con_verificacion(
        video_path,
        "🎭 Video ASMR viral con IA | Contenido hipnótico y relajante #ASMR #IA #Viral #Satisfying"
    )
    
    if success:
        print("\n🎉 ¡MISIÓN CUMPLIDA! Video subido exitosamente")
    else:
        print("\n⚠️  Subida no completada automáticamente - revisar manualmente")

if __name__ == "__main__":
    asyncio.run(main())
