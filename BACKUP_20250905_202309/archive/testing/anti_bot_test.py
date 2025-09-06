import asyncio
from playwright.async_api import async_playwright
import json

async def compare_browser_behavior():
    """Comparar comportamiento entre navegador normal vs automatizado"""
    
    print("🔍 Analizando diferencias entre navegador normal y automatizado...")
    
    async with async_playwright() as p:
        # Configuración más humana
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',  # Ocultar automatización
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['camera', 'microphone'],
            extra_http_headers={
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }
        )
        
        page = await context.new_page()
        
        # Inyectar scripts anti-detección
        await page.add_init_script("""
            // Remover webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Mockear plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Mockear idiomas
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Remover automation flags
            window.chrome = {
                runtime: {},
            };
            
            // Mockear permisos
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
        """)
        
        try:
            # Cargar cookies
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
        
        # Simular comportamiento humano antes de ir a upload
        print("🌐 Navegando como humano...")
        
        # Ir primero a homepage
        await page.goto("https://www.tiktok.com")
        await page.wait_for_load_state('networkidle')
        print("📱 En homepage de TikTok")
        
        # Simular scroll y movimiento
        for i in range(3):
            await page.mouse.move(500 + i*100, 300 + i*50)
            await page.mouse.wheel(0, 200)
            await page.wait_for_timeout(1000 + i*500)
        
        # Ahora ir a upload
        print("📤 Navegando a upload...")
        await page.goto("https://www.tiktok.com/upload")
        await page.wait_for_load_state('networkidle')
        
        # Esperar extra
        await page.wait_for_timeout(3000)
        
        # Analizar la página
        print("🔍 Analizando elementos de la página...")
        
        # Buscar input de archivo
        file_inputs = await page.query_selector_all('input[type="file"]')
        print(f"📁 Inputs de archivo encontrados: {len(file_inputs)}")
        
        # Verificar si hay mensajes de error o bloqueo
        error_messages = [
            'div:has-text("Something went wrong")',
            'div:has-text("Try again")',
            'div:has-text("Error")',
            'div:has-text("blocked")',
            'div:has-text("detected")',
            '.error-message',
            '[data-testid="error"]'
        ]
        
        for error_selector in error_messages:
            error_element = await page.query_selector(error_selector)
            if error_element and await error_element.is_visible():
                error_text = await error_element.text_content()
                print(f"⚠️ Posible bloqueo detectado: {error_text}")
        
        # Tomar screenshot para comparar
        await page.screenshot(path="anti_bot_test.png")
        print("📸 Screenshot guardado como anti_bot_test.png")
        
        # Verificar características del navegador desde JavaScript
        browser_info = await page.evaluate("""
            () => {
                return {
                    userAgent: navigator.userAgent,
                    webdriver: navigator.webdriver,
                    plugins: navigator.plugins.length,
                    languages: navigator.languages,
                    platform: navigator.platform,
                    cookieEnabled: navigator.cookieEnabled,
                    onLine: navigator.onLine,
                    hardwareConcurrency: navigator.hardwareConcurrency,
                    deviceMemory: navigator.deviceMemory || 'undefined',
                    connection: navigator.connection ? navigator.connection.effectiveType : 'undefined'
                };
            }
        """)
        
        print("\n📋 Información del navegador automatizado:")
        for key, value in browser_info.items():
            print(f"  {key}: {value}")
        
        # Verificar si los inputs están realmente funcionales
        if file_inputs:
            first_input = file_inputs[0]
            
            # Verificar propiedades
            input_style = await first_input.get_attribute('style')
            input_class = await first_input.get_attribute('class')
            input_accept = await first_input.get_attribute('accept')
            
            print(f"\n📝 Propiedades del input de archivo:")
            print(f"  Style: {input_style}")
            print(f"  Class: {input_class}")
            print(f"  Accept: {input_accept}")
            
            # Verificar si está realmente oculto por CSS
            is_hidden = await page.evaluate("""
                (input) => {
                    const style = window.getComputedStyle(input);
                    return {
                        display: style.display,
                        visibility: style.visibility,
                        opacity: style.opacity,
                        position: style.position,
                        width: style.width,
                        height: style.height,
                        overflow: style.overflow
                    };
                }
            """, first_input)
            
            print(f"  Computed styles: {is_hidden}")
        
        print("\n⏳ Manteniendo navegador abierto 60 segundos para inspección manual...")
        await page.wait_for_timeout(60000)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(compare_browser_behavior())
