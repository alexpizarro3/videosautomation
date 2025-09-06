#!/usr/bin/env python3
"""
Script para configurar las cookies de TikTok cuando usas login con Google.
Este script te ayudará a extraer las cookies necesarias para automatizar TikTok.
"""

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_chrome_driver():
    """Configurar Chrome driver para extraer cookies"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Mantener el navegador abierto para login manual
    chrome_options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def extract_tiktok_cookies():
    """Extraer cookies de TikTok después del login"""
    print("🍪 CONFIGURACIÓN DE COOKIES DE TIKTOK")
    print("=" * 50)
    print()
    
    print("📋 INSTRUCCIONES:")
    print("1. Se abrirá una ventana de Chrome")
    print("2. Inicia sesión en TikTok con tu cuenta de Google")
    print("3. Asegúrate de estar completamente logueado")
    print("4. Vuelve a esta terminal y presiona ENTER")
    print()
    
    # Configurar driver
    driver = setup_chrome_driver()
    
    try:
        # Ir a TikTok
        print("🌐 Abriendo TikTok...")
        driver.get("https://www.tiktok.com/login")
        
        # Esperar que el usuario se loguee
        input("✋ Inicia sesión en TikTok con Google y luego presiona ENTER aquí...")
        
        # Verificar que esté logueado
        print("🔍 Verificando login...")
        
        # Intentar encontrar elementos que indican que está logueado
        wait = WebDriverWait(driver, 10)
        try:
            # Buscar avatar o elementos de usuario logueado
            logged_in_indicators = [
                "//div[@data-e2e='profile-icon']",
                "//span[contains(@class, 'avatar')]",
                "//div[contains(@class, 'avatar')]",
                "//a[contains(@href, '/@')]"
            ]
            
            logged_in = False
            for indicator in logged_in_indicators:
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, indicator)))
                    logged_in = True
                    break
                except:
                    continue
            
            if not logged_in:
                print("⚠️  No se detectó login. Asegúrate de estar completamente logueado.")
                response = input("¿Continuar extrayendo cookies? (s/N): ")
                if response.lower() != 's':
                    return None
        
        except Exception as e:
            print(f"⚠️  No se pudo verificar el login automáticamente: {e}")
            response = input("¿Estás seguro de que estás logueado? (s/N): ")
            if response.lower() != 's':
                return None
        
        print("✅ Extrayendo cookies...")
        
        # Extraer todas las cookies
        cookies = driver.get_cookies()
        
        # Filtrar cookies importantes para TikTok
        important_cookies = {}
        cookie_names = [
            'sessionid', 'sessionid_ss', 'sid_guard', 'uid_tt', 'uid_tt_ss',
            'sid_tt', 'ssid_ucp_v1', 'csrf_session_id', 'tt_csrf_token',
            'msToken', 'ttwid', 'tt_chain_token', 'passport_csrf_token',
            'store-country-code', 'store-idc', 'tt_webid', 'tt_webid_v2'
        ]
        
        for cookie in cookies:
            if cookie['name'] in cookie_names:
                important_cookies[cookie['name']] = cookie['value']
        
        if not important_cookies:
            print("❌ No se encontraron cookies de TikTok")
            print("💡 Asegúrate de estar en tiktok.com y completamente logueado")
            return None
        
        # Guardar cookies
        cookies_file = "data/tiktok_cookies.json"
        os.makedirs("data", exist_ok=True)
        
        with open(cookies_file, 'w', encoding='utf-8') as f:
            json.dump(important_cookies, f, indent=2)
        
        print(f"✅ Cookies guardadas en: {cookies_file}")
        print(f"📊 Cookies extraídas: {len(important_cookies)}")
        
        # Mostrar cookies encontradas
        print("\n🔑 Cookies importantes encontradas:")
        for name in important_cookies:
            print(f"   ✅ {name}")
        
        return cookies_file
        
    except Exception as e:
        print(f"❌ Error extrayendo cookies: {e}")
        return None
    
    finally:
        input("\n⏸️  Presiona ENTER para cerrar el navegador...")
        driver.quit()

def verify_cookies():
    """Verificar que las cookies son válidas"""
    cookies_file = "data/tiktok_cookies.json"
    
    if not os.path.exists(cookies_file):
        print("❌ Archivo de cookies no encontrado")
        return False
    
    try:
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        # Verificar cookies esenciales
        essential_cookies = ['sessionid', 'sid_guard', 'uid_tt']
        missing_cookies = [cookie for cookie in essential_cookies if cookie not in cookies]
        
        if missing_cookies:
            print(f"⚠️  Cookies esenciales faltantes: {missing_cookies}")
            print("💡 Intenta extraer las cookies nuevamente")
            return False
        
        print("✅ Cookies válidas encontradas")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando cookies: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 CONFIGURACIÓN DE TIKTOK CON GOOGLE LOGIN")
    print("=" * 60)
    print()
    print("Como usas Google para loguearte en TikTok, necesitamos")
    print("extraer las cookies de tu sesión autenticada.")
    print()
    
    # Verificar si ya existen cookies
    if os.path.exists("data/tiktok_cookies.json"):
        print("🍪 Se encontraron cookies existentes")
        if verify_cookies():
            response = input("¿Quieres usar las cookies existentes? (S/n): ")
            if response.lower() != 'n':
                print("✅ Usando cookies existentes")
                return
        
        print("🔄 Extrayendo nuevas cookies...")
    
    # Extraer cookies
    cookies_file = extract_tiktok_cookies()
    
    if cookies_file:
        print("\n" + "=" * 60)
        print("🎉 CONFIGURACIÓN COMPLETADA")
        print("=" * 60)
        print()
        print("✅ Cookies de TikTok configuradas correctamente")
        print(f"📁 Archivo: {cookies_file}")
        print()
        print("💡 PRÓXIMOS PASOS:")
        print("1. Copia .env.template a .env")
        print("2. Ejecuta: python test_generators.py")
        print("3. Ejecuta el sistema: python src/main.py")
    else:
        print("\n❌ No se pudieron configurar las cookies")
        print("💡 Intenta el proceso nuevamente o contacta soporte")

if __name__ == "__main__":
    main()
