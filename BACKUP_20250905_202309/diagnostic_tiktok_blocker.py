#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO AVANZADO DE BLOQUEOS DE TIKTOK
Detecta qué está bloqueando TikTok y cómo evadirlo
"""

import asyncio
import json
import os
import time
from playwright.async_api import async_playwright

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

async def diagnostico_completo():
    """Diagnóstico completo de TikTok"""
    print("🔍 DIAGNÓSTICO COMPLETO DE BLOQUEOS DE TIKTOK")
    print("=" * 60)
    
    cookies_path = "config/upload_cookies_playwright.json"
    user_data_dir = os.path.join(os.getcwd(), "browser_profile")
    
    async with async_playwright() as p:
        # Usar contexto persistente
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            channel="chrome",
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            locale='es-MX',
            timezone_id='America/Mexico_City',
            geolocation={'latitude': 19.4326, 'longitude': -99.1332},
            permissions=['geolocation', 'microphone', 'camera', 'notifications'],
            color_scheme='light',
            reduced_motion='no-preference',
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
                '--start-maximized'
            ],
            ignore_default_args=['--enable-automation'],
        )
        
        await cargar_cookies(context, cookies_path)
        page = await context.new_page()
        
        # Interceptar requests para detectar bloqueos
        blocked_requests = []
        failed_requests = []
        
        async def handle_request(request):
            if any(blocked in request.url for blocked in ['bot', 'automation', 'selenium', 'playwright']):
                blocked_requests.append(request.url)
                print(f"🚫 REQUEST BLOQUEADO: {request.url}")
        
        async def handle_response(response):
            if response.status >= 400:
                failed_requests.append({
                    'url': response.url,
                    'status': response.status,
                    'headers': dict(response.headers)
                })
                print(f"❌ RESPONSE ERROR {response.status}: {response.url}")
        
        page.on('request', handle_request)
        page.on('response', handle_response)
        
        try:
            print("\n1️⃣ NAVEGANDO A TIKTOK CREATOR CENTER...")
            await page.goto('https://www.tiktok.com/creator-center/upload', wait_until='networkidle')
            await asyncio.sleep(5)
            
            # Diagnóstico 1: Verificar autenticación
            print("\n2️⃣ DIAGNÓSTICO DE AUTENTICACIÓN...")
            
            # Verificar si está logueado
            login_indicators = await page.query_selector_all('text="Log in", text="Sign up"')
            if login_indicators:
                print("❌ NO ESTÁ LOGUEADO - Se requiere login manual")
                return False
            else:
                print("✅ AUTENTICADO CORRECTAMENTE")
            
            # Diagnóstico 2: Verificar elementos de upload
            print("\n3️⃣ DIAGNÓSTICO DE ELEMENTOS DE UPLOAD...")
            
            # Buscar inputs de archivo
            file_inputs = await page.query_selector_all('input[type="file"]')
            print(f"📁 Inputs de archivo encontrados: {len(file_inputs)}")
            
            if len(file_inputs) == 0:
                print("❌ NO SE ENCONTRARON INPUTS DE ARCHIVO")
                
                # Analizar por qué no aparecen
                print("🔍 Analizando por qué no aparecen inputs...")
                
                # Verificar si la página cargó completamente
                page_title = await page.title()
                page_url = page.url
                print(f"📄 Título: {page_title}")
                print(f"🌐 URL: {page_url}")
                
                # Buscar mensajes de error
                error_messages = await page.query_selector_all('[class*="error"], [class*="warning"], [class*="blocked"]')
                for error in error_messages:
                    error_text = await error.text_content()
                    if error_text and len(error_text.strip()) > 0:
                        print(f"⚠️ ERROR DETECTADO: {error_text[:100]}")
                
                # Verificar si hay redirects o bloqueos
                if 'login' in page_url or 'blocked' in page_url:
                    print("❌ PÁGINA REDIRIGIDA - POSIBLE BLOQUEO")
                
                return False
            else:
                print("✅ INPUTS DE ARCHIVO ENCONTRADOS")
            
            # Diagnóstico 3: Simular carga de archivo
            print("\n4️⃣ SIMULANDO CARGA DE ARCHIVO...")
            
            # Crear archivo de prueba temporal
            test_video_path = "test_video.mp4"
            if not os.path.exists(test_video_path):
                # Crear un archivo pequeño de prueba
                with open(test_video_path, 'wb') as f:
                    f.write(b'fake video content for testing')
            
            try:
                await file_inputs[0].set_input_files(test_video_path)
                print("✅ ARCHIVO DE PRUEBA CARGADO")
                await asyncio.sleep(10)  # Esperar procesamiento
                
                # Verificar si aparecieron elementos de preview
                preview_elements = await page.query_selector_all('canvas, video, [class*="preview"], [class*="player"]')
                print(f"🎬 Elementos de preview encontrados: {len(preview_elements)}")
                
                if len(preview_elements) == 0:
                    print("❌ NO APARECIERON ELEMENTOS DE PREVIEW")
                    
                    # Buscar mensajes de error específicos
                    error_selectors = [
                        '[class*="error"]',
                        '[class*="fail"]',
                        '[class*="invalid"]',
                        'text="Error"',
                        'text="Failed"',
                        'text="Invalid"'
                    ]
                    
                    for selector in error_selectors:
                        errors = await page.query_selector_all(selector)
                        for error in errors:
                            error_text = await error.text_content()
                            if error_text and 'error' in error_text.lower():
                                print(f"🚫 ERROR DE CARGA: {error_text}")
                
                else:
                    print("✅ ELEMENTOS DE PREVIEW APARECIERON")
                    
                    # Diagnóstico 4: Buscar botón Post
                    print("\n5️⃣ DIAGNÓSTICO DEL BOTÓN POST...")
                    
                    # Esperar un poco más para que cargue todo
                    await asyncio.sleep(5)
                    
                    # Buscar todos los botones
                    all_buttons = await page.query_selector_all('button')
                    print(f"🔘 Total de botones encontrados: {len(all_buttons)}")
                    
                    # Analizar cada botón
                    post_candidates = []
                    for i, btn in enumerate(all_buttons):
                        try:
                            text = await btn.text_content() or ""
                            classes = await btn.get_attribute('class') or ""
                            is_visible = await btn.is_visible()
                            is_enabled = await btn.is_enabled()
                            
                            # Si contiene palabras relacionadas con publicar
                            if any(word in text.lower() for word in ['post', 'publish', 'publicar', 'subir']):
                                post_candidates.append({
                                    'index': i,
                                    'text': text,
                                    'classes': classes[:50],
                                    'visible': is_visible,
                                    'enabled': is_enabled
                                })
                                print(f"🎯 CANDIDATO POST #{i}: '{text}' - Visible: {is_visible}, Enabled: {is_enabled}")
                        except:
                            continue
                    
                    if len(post_candidates) == 0:
                        print("❌ NO SE ENCONTRARON BOTONES POST")
                        
                        # Analizar por qué no aparece el botón Post
                        print("\n🔍 ANALIZANDO FALTA DE BOTÓN POST...")
                        
                        # Verificar si faltan campos obligatorios
                        required_fields = [
                            'textarea',
                            'input[placeholder*="escrib"]',
                            'div[contenteditable="true"]'
                        ]
                        
                        for field_selector in required_fields:
                            fields = await page.query_selector_all(field_selector)
                            print(f"📝 {field_selector}: {len(fields)} encontrados")
                        
                        # Verificar si hay elementos de configuración sin completar
                        incomplete_configs = await page.query_selector_all('[class*="incomplete"], [class*="required"], [class*="missing"]')
                        if incomplete_configs:
                            print(f"⚠️ Configuraciones incompletas detectadas: {len(incomplete_configs)}")
                        
                        # Buscar mensajes que indiquen qué falta
                        warning_messages = await page.query_selector_all('[class*="warning"], [class*="hint"], [class*="required"]')
                        for warning in warning_messages:
                            warning_text = await warning.text_content()
                            if warning_text and len(warning_text.strip()) > 5:
                                print(f"⚠️ ADVERTENCIA: {warning_text[:100]}")
                    
                    else:
                        print(f"✅ ENCONTRADOS {len(post_candidates)} CANDIDATOS POST")
                        
                        # Verificar por qué no están habilitados
                        enabled_candidates = [c for c in post_candidates if c['enabled']]
                        visible_candidates = [c for c in post_candidates if c['visible']]
                        
                        print(f"👁️ Botones visibles: {len(visible_candidates)}")
                        print(f"✅ Botones habilitados: {len(enabled_candidates)}")
                        
                        if len(enabled_candidates) == 0:
                            print("❌ NINGÚN BOTÓN POST ESTÁ HABILITADO")
                            print("💡 POSIBLES CAUSAS:")
                            print("   - Falta completar descripción")
                            print("   - Falta seleccionar configuraciones")
                            print("   - Video aún procesándose")
                            print("   - Términos de servicio no aceptados")
            
            except Exception as e:
                print(f"❌ ERROR EN SIMULACIÓN DE CARGA: {e}")
            
            finally:
                # Limpiar archivo de prueba
                if os.path.exists(test_video_path):
                    os.remove(test_video_path)
            
            # Diagnóstico 5: Análisis de red
            print(f"\n6️⃣ ANÁLISIS DE RED:")
            print(f"🚫 Requests bloqueados: {len(blocked_requests)}")
            print(f"❌ Requests fallidos: {len(failed_requests)}")
            
            for req in failed_requests:
                if req['status'] in [403, 429, 503]:
                    print(f"🚫 BLOQUEO DETECTADO: {req['status']} - {req['url'][:100]}")
            
            # Screenshot final para análisis
            timestamp = int(time.time())
            await page.screenshot(path=f"diagnostic_final_{timestamp}.png", full_page=True)
            print(f"📸 Screenshot completo: diagnostic_final_{timestamp}.png")
            
            # Diagnóstico 6: Verificar detección de automation
            print("\n7️⃣ VERIFICANDO DETECCIÓN DE AUTOMATION...")
            
            automation_detected = await page.evaluate('''
                () => {
                    // Verificar si hay indicadores de automation
                    const indicators = [];
                    
                    if (window.navigator.webdriver) {
                        indicators.push('navigator.webdriver detected');
                    }
                    
                    if (window.chrome && window.chrome.runtime && window.chrome.runtime.onConnect) {
                        indicators.push('Chrome automation detected');
                    }
                    
                    if (window.callPhantom || window._phantom) {
                        indicators.push('Phantom detection');
                    }
                    
                    if (window.selenium) {
                        indicators.push('Selenium detected');
                    }
                    
                    // Verificar propiedades sospechosas
                    const props = Object.getOwnPropertyNames(window);
                    const suspicious = props.filter(prop => 
                        prop.includes('selenium') || 
                        prop.includes('webdriver') || 
                        prop.includes('playwright') ||
                        prop.includes('automation')
                    );
                    
                    if (suspicious.length > 0) {
                        indicators.push(`Suspicious properties: ${suspicious.join(', ')}`);
                    }
                    
                    return indicators;
                }
            ''')
            
            if automation_detected and len(automation_detected) > 0:
                print("❌ AUTOMATION DETECTADA:")
                for indicator in automation_detected:
                    print(f"   🚫 {indicator}")
            else:
                print("✅ NO SE DETECTÓ AUTOMATION")
            
            print("\n" + "=" * 60)
            print("🏁 DIAGNÓSTICO COMPLETADO")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ Error en diagnóstico: {e}")
            return False
        
        finally:
            await asyncio.sleep(3)
            await context.close()

if __name__ == "__main__":
    asyncio.run(diagnostico_completo())
