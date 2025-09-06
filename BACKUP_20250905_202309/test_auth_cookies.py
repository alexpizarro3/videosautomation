#!/usr/bin/env python3
"""
🔍 TEST DE AUTENTICACIÓN CON COOKIES PARA TIKTOK
Verifica que las cookies funcionen correctamente y el usuario esté logueado
"""

import asyncio
import json
import os
from playwright.async_api import async_playwright

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

async def test_autenticacion():
    """Test de autenticación con cookies"""
    print("🔍 INICIANDO TEST DE AUTENTICACIÓN CON COOKIES")
    print("=" * 60)
    
    async with async_playwright() as p:
        # Configurar browser
        browser = await p.chromium.launch(
            headless=False,  # Mostrar browser para debug
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
        
        # Test 1: Cargar cookies
        print("\n📋 TEST 1: Cargando cookies...")
        cookies_loaded = await cargar_cookies(context, "config/upload_cookies_playwright.json")
        
        if not cookies_loaded:
            print("❌ FALLO: No se pudieron cargar las cookies")
            await browser.close()
            return False
        
        # Test 2: Ir a TikTok y verificar autenticación
        print("\n🌐 TEST 2: Verificando autenticación en TikTok...")
        try:
            await page.goto("https://www.tiktok.com/", timeout=30000)
            await page.wait_for_load_state('domcontentloaded', timeout=15000)
            print("✅ Página de TikTok cargada")
            
            # Esperar un poco para que se procesen las cookies
            await asyncio.sleep(3)
            
            # Verificar si hay elementos que indican que está logueado
            elementos_logueado = [
                '[data-e2e="nav-upload"]',  # Botón de upload
                '[data-e2e="profile-icon"]',  # Icono de perfil
                'button[data-e2e="upload-icon"]',  # Botón upload alternativo
                'a[href="/upload"]'  # Link de upload
            ]
            
            logueado = False
            for selector in elementos_logueado:
                try:
                    element = await page.wait_for_selector(selector, timeout=5000)
                    if element:
                        print(f"✅ Elemento de usuario logueado encontrado: {selector}")
                        logueado = True
                        break
                except:
                    continue
            
            if not logueado:
                print("⚠️  No se detectaron elementos de usuario logueado")
                # Intentar tomar screenshot para debug
                await page.screenshot(path="debug_not_logged.png")
                print("📸 Screenshot guardado: debug_not_logged.png")
            
        except Exception as e:
            print(f"❌ Error verificando autenticación: {e}")
            await browser.close()
            return False
        
        # Test 3: Intentar ir a página de upload
        print("\n📤 TEST 3: Intentando acceder a página de upload...")
        try:
            await page.goto("https://www.tiktok.com/creator-center/upload", timeout=30000)
            await page.wait_for_load_state('domcontentloaded', timeout=15000)
            
            # Verificar si llegamos a la página de upload o nos redirigen al login
            current_url = page.url
            print(f"📍 URL actual: {current_url}")
            
            if "upload" in current_url:
                print("✅ ÉXITO: Acceso a página de upload confirmado")
                
                # Buscar elementos de upload
                upload_elements = [
                    'input[type="file"]',
                    '[data-e2e="upload-input"]',
                    '.upload-btn',
                    'button[class*="upload"]'
                ]
                
                upload_found = False
                for selector in upload_elements:
                    try:
                        element = await page.wait_for_selector(selector, timeout=5000)
                        if element:
                            print(f"✅ Elemento de upload encontrado: {selector}")
                            upload_found = True
                            break
                    except:
                        continue
                
                if upload_found:
                    print("🎉 RESULTADO: Sistema de upload accesible")
                    result = True
                else:
                    print("⚠️  ADVERTENCIA: Página de upload cargada pero sin elementos de upload detectados")
                    await page.screenshot(path="debug_upload_page.png")
                    print("📸 Screenshot guardado: debug_upload_page.png")
                    result = False
                    
            elif "login" in current_url or "passport" in current_url:
                print("❌ FALLO: Redirigido a página de login - cookies no válidas")
                await page.screenshot(path="debug_login_redirect.png")
                print("📸 Screenshot guardado: debug_login_redirect.png")
                result = False
            else:
                print(f"⚠️  ADVERTENCIA: Redirigido a página inesperada: {current_url}")
                await page.screenshot(path="debug_unexpected_page.png")
                print("📸 Screenshot guardado: debug_unexpected_page.png")
                result = False
                
        except Exception as e:
            print(f"❌ Error accediendo a página de upload: {e}")
            result = False
        
        # Test 4: Verificar información de cookies válidas
        print("\n🍪 TEST 4: Verificando cookies válidas...")
        try:
            cookies = await context.cookies()
            session_cookies = [c for c in cookies if c.get('name') in ['sessionid', 'sid_guard', 'uid_tt']]
            
            if session_cookies:
                print(f"✅ {len(session_cookies)} cookies de sesión encontradas:")
                for cookie in session_cookies:
                    name = cookie.get('name', 'unknown')
                    value = cookie.get('value', '')
                    print(f"   - {name}: {value[:20]}...")
            else:
                print("❌ No se encontraron cookies de sesión válidas")
                
        except Exception as e:
            print(f"❌ Error verificando cookies: {e}")
        
        # Mantener browser abierto para inspección manual
        print("\n🔍 INSPECCIÓN MANUAL:")
        print("El browser se mantendrá abierto por 30 segundos para inspección manual...")
        print("Verifica manualmente si:")
        print("1. Estás logueado en TikTok")
        print("2. Puedes acceder a la página de upload")
        print("3. El botón de upload es visible")
        
        await asyncio.sleep(30)
        
        await browser.close()
        return result

async def main():
    """Función principal"""
    print("🚀 INICIANDO DIAGNÓSTICO DE AUTENTICACIÓN TIKTOK")
    print("=" * 60)
    
    # Verificar que existe el archivo de cookies
    cookies_path = "config/upload_cookies_playwright.json"
    if not os.path.exists(cookies_path):
        print(f"❌ ERROR: No se encontró el archivo de cookies: {cookies_path}")
        return
    
    result = await test_autenticacion()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO:")
    print("=" * 60)
    
    if result:
        print("🎉 ÉXITO: Autenticación funcionando correctamente")
        print("✅ Las cookies son válidas y el sistema de upload es accesible")
        print("💡 El problema puede estar en la verificación del video preview")
    else:
        print("❌ PROBLEMA DETECTADO: Autenticación no funciona")
        print("🔧 SOLUCIONES POSIBLES:")
        print("   1. Regenerar cookies desde navegador")
        print("   2. Verificar que la cuenta no esté bloqueada")
        print("   3. Comprobar cambios en la interfaz de TikTok")

if __name__ == "__main__":
    asyncio.run(main())
