import asyncio
import os
import json
import random
import time
from playwright.async_api import async_playwright

def human_delay(min_s=0.7, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))

async def test_optimized_video():
    """Probar el video optimizado en TikTok"""
    
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
            await browser.close()
            return
        
        # Ir a upload
        await page.goto("https://www.tiktok.com/upload")
        await page.wait_for_load_state('networkidle')
        
        print("📸 Tomando screenshot inicial...")
        await page.screenshot(path="test_1_initial.png")
        
        # Buscar input de archivo y hacerlo visible
        video_path = os.path.abspath("data/videos/veo_video_tiktok_optimized.mp4")
        
        try:
            print("🔍 Buscando input de archivo...")
            file_inputs = await page.query_selector_all('input[type="file"]')
            
            for i, file_input in enumerate(file_inputs):
                print(f"📁 Probando input #{i+1}")
                
                # Hacer visible el input
                await page.evaluate('''(input) => {
                    input.style.display = 'block';
                    input.style.visibility = 'visible';
                    input.style.opacity = '1';
                    input.style.position = 'relative';
                    input.style.width = '200px';
                    input.style.height = '50px';
                    input.style.zIndex = '9999';
                    input.style.background = 'red';
                }''', file_input)
                
                await page.screenshot(path=f"test_2_input_visible_{i}.png")
                human_delay(1, 2)
                
                try:
                    await file_input.set_input_files(video_path)
                    print(f"✅ Archivo subido con input #{i+1}")
                    
                    # Ocultar input
                    await page.evaluate('''(input) => {
                        input.style.display = 'none';
                    }''', file_input)
                    
                    break
                    
                except Exception as e:
                    print(f"⚠️ Error con input #{i+1}: {e}")
                    continue
            
            # Esperar y monitorear carga
            print("⏳ Esperando carga del video...")
            
            for check in range(20):
                await page.screenshot(path=f"test_3_loading_{check:02d}.png")
                
                # Verificar botón select video
                select_btn = await page.query_selector('[data-e2e="select_video_button"]')
                if select_btn and await select_btn.is_visible():
                    print(f"  [{check:02d}/20] Botón 'Select video' aún visible")
                else:
                    print(f"  [{check:02d}/20] Botón 'Select video' desapareció ✅")
                
                # Verificar editor
                editor = await page.query_selector('[contenteditable="true"]')
                if editor and await editor.is_visible():
                    print(f"  [{check:02d}/20] Editor disponible ✅")
                
                # Verificar preview de video
                video_preview = await page.query_selector('video')
                if video_preview and await video_preview.is_visible():
                    print(f"  [{check:02d}/20] Preview de video visible ✅")
                
                # Verificar loading
                loading = await page.query_selector('div:has-text("Loading")')
                if loading and await loading.is_visible():
                    print(f"  [{check:02d}/20] Aún cargando...")
                
                human_delay(3, 4)
                
                # Si todo está listo, salir del loop
                if (not (select_btn and await select_btn.is_visible()) and
                    editor and await editor.is_visible()):
                    print("🎉 ¡Video cargado exitosamente!")
                    break
            
            await page.screenshot(path="test_4_final_state.png")
            
            # Si llegó aquí, probar escribir algo
            try:
                editor = await page.query_selector('[contenteditable="true"]')
                if editor:
                    await editor.click()
                    await page.type('[contenteditable="true"]', "¡Test de video optimizado! #ASMR #FYP")
                    print("✅ Descripción de prueba ingresada")
                    await page.screenshot(path="test_5_description_added.png")
            except Exception as e:
                print(f"⚠️ Error escribiendo descripción: {e}")
            
        except Exception as e:
            print(f"❌ Error general: {e}")
        
        print("⏳ Esperando 30 segundos para observar...")
        human_delay(30, 30)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_optimized_video())
