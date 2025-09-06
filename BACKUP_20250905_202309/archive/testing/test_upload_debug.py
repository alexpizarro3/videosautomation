import asyncio
import os
from playwright.async_api import async_playwright
import json

async def debug_upload_process():
    """Script de diagnóstico para entender por qué no cargan los previews"""
    
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
            
            # Limpiar cookies para evitar errores
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
        
        # Ir a página de upload
        await page.goto("https://www.tiktok.com/upload")
        await page.wait_for_load_state('networkidle')
        
        # Screenshot inicial
        await page.screenshot(path="debug_1_initial_page.png")
        print("📸 Screenshot inicial tomado")
        
        # Esperar input de archivo
        file_input = await page.wait_for_selector('input[type="file"]', timeout=20000)
        
        # Probar con archivo original
        original_file = "data/videos/veo_video_20250901_190803.mp4"
        if os.path.exists(original_file):
            print(f"🔍 Probando archivo original: {original_file}")
            
            await file_input.set_input_files(original_file)
            print("📤 Archivo subido")
            
            # Screenshots durante el proceso
            await asyncio.sleep(5)
            await page.screenshot(path="debug_2_after_upload.png")
            
            await asyncio.sleep(10)
            await page.screenshot(path="debug_3_after_10s.png")
            
            await asyncio.sleep(15)
            await page.screenshot(path="debug_4_after_25s.png")
            
            await asyncio.sleep(20)
            await page.screenshot(path="debug_5_after_45s.png")
            
            # Verificar elementos en la página
            print("\n🔍 Diagnóstico de elementos en la página:")
            
            # 1. Verificar botón select video
            select_btn = await page.query_selector('[data-e2e="select_video_button"]')
            if select_btn and await select_btn.is_visible():
                print("❌ Botón 'Select video' aún visible")
            else:
                print("✅ Botón 'Select video' no visible")
            
            # 2. Verificar editor de texto
            editor = await page.query_selector('[contenteditable="true"]')
            if editor and await editor.is_visible():
                print("✅ Editor de texto disponible")
            else:
                print("❌ Editor de texto no disponible")
            
            # 3. Verificar preview de video
            video_preview = await page.query_selector('video')
            if video_preview and await video_preview.is_visible():
                print("✅ Preview de video visible")
            else:
                print("❌ Preview de video no visible")
            
            # 4. Verificar indicadores de carga
            loading_indicators = [
                'div:has-text("Loading...")',
                'div:has-text("Processing...")',
                '.loading',
                '.spinner'
            ]
            
            for selector in loading_indicators:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    print(f"⏳ Indicador de carga activo: {selector}")
            
            # 5. Verificar errores
            error_selectors = [
                'div:has-text("Error")',
                'div:has-text("Failed")',
                '.error',
                '[data-testid="error"]'
            ]
            
            for selector in error_selectors:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    error_text = await element.text_content()
                    print(f"❌ Error detectado: {error_text}")
            
            # 6. Listar todos los elementos visibles para diagnóstico
            print("\n📋 Elementos principales en la página:")
            all_elements = await page.query_selector_all('div, button, input, video, img')
            visible_count = 0
            for element in all_elements[:20]:  # Solo primeros 20 para no saturar
                if await element.is_visible():
                    tag = await element.evaluate('el => el.tagName')
                    class_name = await element.get_attribute('class') or ''
                    data_e2e = await element.get_attribute('data-e2e') or ''
                    text = (await element.text_content() or '')[:50]
                    print(f"  {tag}: class='{class_name[:30]}' data-e2e='{data_e2e}' text='{text}'")
                    visible_count += 1
            
            print(f"\n📊 Total elementos visibles revisados: {visible_count}")
            
            # Screenshot final
            await page.screenshot(path="debug_6_final_state.png")
            print("📸 Screenshot final tomado")
            
            # Esperar un poco más para observar
            print("\n⏳ Esperando 30 segundos más para observar...")
            await asyncio.sleep(30)
            await page.screenshot(path="debug_7_after_wait.png")
            
        await browser.close()
        print("\n✅ Diagnóstico completado. Revisa los screenshots generados.")

if __name__ == "__main__":
    asyncio.run(debug_upload_process())
