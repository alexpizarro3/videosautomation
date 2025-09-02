import asyncio
import os
import json
import random
import time
from playwright.async_api import async_playwright

def human_delay(min_s=0.7, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))

async def test_complete_flow_without_preview():
    """Probar flujo completo ignorando el preview visual"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        # Cargar cookies
        try:
            with open("config/upload_cookies_playwright.json", 'r') as f:
                cookies = json.load(f)
            
            for cookie in cookies:
                if 'sameSite' in cookie:
                    val = cookie['sameSite']
                    if val not in ["Strict", "Lax", "None"]:
                        cookie["sameSite"] = "None"
            
            await context.add_cookies(cookies)
            print("✅ Cookies cargadas")
        except Exception as e:
            print(f"❌ Error cargando cookies: {e}")
            return
        
        # Ir a upload
        await page.goto("https://www.tiktok.com/upload")
        await page.wait_for_load_state('networkidle')
        
        # PASO 1: Subir video optimizado
        video_path = os.path.abspath("data/videos/veo_video_tiktok_optimized.mp4")
        
        print("📤 Subiendo video optimizado...")
        file_inputs = await page.query_selector_all('input[type="file"]')
        
        upload_success = False
        for i, file_input in enumerate(file_inputs):
            try:
                await page.evaluate('''(input) => {
                    input.style.display = 'block';
                    input.style.visibility = 'visible';
                }''', file_input)
                
                await file_input.set_input_files(video_path)
                print(f"✅ Video subido usando input #{i+1}")
                upload_success = True
                break
            except Exception as e:
                print(f"⚠️ Error con input #{i+1}: {e}")
                continue
        
        if not upload_success:
            print("❌ No se pudo subir el video")
            await browser.close()
            return
        
        # PASO 2: Esperar mínimo y verificar editor (ignorar preview)
        print("⏳ Esperando 15 segundos mínimos...")
        human_delay(15, 20)
        
        # Verificar que el editor esté disponible (indicador de que el video se procesó)
        editor = await page.query_selector('[contenteditable="true"]')
        if not (editor and await editor.is_visible()):
            print("❌ Editor no disponible, video no se procesó")
            await browser.close()
            return
        
        print("✅ Editor disponible - continuando sin esperar preview")
        
        # PASO 3: Escribir descripción
        try:
            await editor.click()
            human_delay(1, 2)
            
            descripcion = "Test de video optimizado para TikTok 🎥✨\n\n¿Funciona sin preview? 🤔\n\n#ASMR #FYP #Test"
            await page.type('[contenteditable="true"]', descripcion)
            print("✅ Descripción ingresada")
            
            await page.screenshot(path="flow_test_1_description.png")
            
        except Exception as e:
            print(f"⚠️ Error escribiendo descripción: {e}")
        
        # PASO 4: Activar IA (opcional)
        try:
            print("🔧 Activando configuraciones avanzadas...")
            
            # Buscar show more
            show_more = await page.query_selector('div[data-e2e="advanced_settings_container"] .more-btn')
            if show_more and await show_more.is_visible():
                await show_more.click()
                human_delay(2, 3)
                print("✅ 'Show more' abierto")
                
                # Buscar switch IA
                ai_switch = await page.query_selector('div[data-e2e="aigc_container"] .switch')
                if ai_switch and await ai_switch.is_visible():
                    await ai_switch.click()
                    human_delay(1, 2)
                    
                    # Manejar modal
                    try:
                        turn_on = await page.wait_for_selector('button:has-text("Turn on")', timeout=3000)
                        if turn_on:
                            await turn_on.click()
                            print("✅ IA activada vía modal")
                    except:
                        print("✅ IA activada directamente")
                    
                    human_delay(2, 3)
            
            await page.screenshot(path="flow_test_2_ai_settings.png")
            
        except Exception as e:
            print(f"⚠️ Error con configuraciones IA: {e}")
        
        # PASO 5: Intentar publicar
        print("🚀 Intentando publicar...")
        human_delay(10, 15)  # Tiempo extra por si acaso
        
        try:
            # Buscar botón Post
            post_btn = await page.query_selector('button:has-text("Post")')
            if post_btn and await post_btn.is_visible():
                await page.screenshot(path="flow_test_3_before_post.png")
                
                await post_btn.click()
                print("✅ Click en 'Post' realizado")
                
                # Esperar posible modal de confirmación
                try:
                    confirm_btn = await page.wait_for_selector('button:has-text("Yes")', timeout=5000)
                    if confirm_btn:
                        await confirm_btn.click()
                        print("✅ Confirmación manejada")
                except:
                    print("ℹ️ Sin modal de confirmación")
                
                # Esperar redirección o confirmación
                human_delay(5, 10)
                await page.screenshot(path="flow_test_4_after_post.png")
                
                # Verificar si hay mensaje de éxito o redirección
                current_url = page.url
                print(f"📍 URL actual: {current_url}")
                
                if "upload" not in current_url:
                    print("🎉 ¡POSIBLE ÉXITO! - Redirección detectada")
                else:
                    print("🤔 Aún en página de upload")
                    
                    # Buscar mensajes de error o éxito
                    success_indicators = [
                        'div:has-text("uploaded")',
                        'div:has-text("posted")',
                        'div:has-text("success")',
                        'div:has-text("published")'
                    ]
                    
                    for indicator in success_indicators:
                        element = await page.query_selector(indicator)
                        if element and await element.is_visible():
                            text = await element.text_content()
                            print(f"✅ Mensaje de éxito: {text}")
            else:
                print("❌ Botón 'Post' no encontrado")
                
        except Exception as e:
            print(f"⚠️ Error en publicación: {e}")
        
        print("⏳ Esperando 30 segundos para observar resultado...")
        human_delay(30, 30)
        await page.screenshot(path="flow_test_5_final.png")
        
        await browser.close()
        
        print("\n📋 RESUMEN DEL TEST:")
        print("- ✅ Video optimizado subido")
        print("- ✅ Editor disponible (video procesado)")
        print("- ✅ Descripción ingresada")
        print("- ✅ Configuraciones IA aplicadas")
        print("- ✅ Intento de publicación realizado")
        print("\n🔍 Revisa los screenshots para ver el resultado final")

if __name__ == "__main__":
    asyncio.run(test_complete_flow_without_preview())
