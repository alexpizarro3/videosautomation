#!/usr/bin/env python3
"""
Prueba de extracción de métricas de TikTok
para la cuenta @chakakitafreakyvideos
"""

import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

def setup_driver():
    """Configurar Chrome driver con las cookies guardadas"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Para ver el proceso (quita esto si quieres headless)
    # chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def load_cookies(driver):
    """Cargar las cookies de TikTok guardadas"""
    cookies_file = "data/tiktok_cookies.json"
    
    if not os.path.exists(cookies_file):
        print(f"❌ Archivo de cookies no encontrado: {cookies_file}")
        return False
    
    try:
        # Ir a TikTok primero
        driver.get("https://www.tiktok.com")
        time.sleep(2)
        
        # Cargar cookies
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        # Añadir cada cookie
        for name, value in cookies.items():
            try:
                driver.add_cookie({
                    'name': name,
                    'value': value,
                    'domain': '.tiktok.com'
                })
            except Exception as e:
                # Algunas cookies pueden fallar, continuar
                pass
        
        print(f"✅ Cookies cargadas: {len(cookies)} cookies")
        return True
        
    except Exception as e:
        print(f"❌ Error cargando cookies: {e}")
        return False

def extract_profile_metrics(driver, username):
    """Extraer métricas del perfil de TikTok"""
    print(f"📊 Extrayendo métricas del perfil @{username}")
    
    try:
        # Ir al perfil
        profile_url = f"https://www.tiktok.com/@{username}"
        driver.get(profile_url)
        
        # Esperar a que cargue
        wait = WebDriverWait(driver, 10)
        
        # Esperar a que aparezcan las métricas del perfil
        time.sleep(5)
        
        metrics = {}
        
        # Intentar extraer seguidores, seguidos, likes
        try:
            # Buscar contenedores de estadísticas
            stats_selectors = [
                "[data-e2e='followers-count']",
                "[data-e2e='following-count']", 
                "[data-e2e='likes-count']",
                "strong[title]",  # Números con títulos
                "strong[data-e2e]"  # Otros números
            ]
            
            stats_found = {}
            
            for selector in stats_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        title = element.get_attribute('title')
                        data_e2e = element.get_attribute('data-e2e')
                        
                        if text and any(char.isdigit() for char in text):
                            key = data_e2e or title or "metric"
                            stats_found[key] = text
                            print(f"   📈 {key}: {text}")
                
                except Exception as e:
                    continue
            
            # También intentar con selectores más generales
            try:
                # Buscar cualquier elemento que contenga números grandes
                number_elements = driver.find_elements(By.XPATH, "//strong[contains(text(), 'K') or contains(text(), 'M') or string-length(text()) > 2]")
                
                for i, element in enumerate(number_elements[:10]):  # Limitar a 10
                    text = element.text.strip()
                    if text and any(char.isdigit() for char in text):
                        print(f"   📊 Métrica {i+1}: {text}")
                        stats_found[f"metric_{i+1}"] = text
            
            except Exception as e:
                print(f"⚠️  Error extrayendo números: {e}")
            
            metrics['profile_stats'] = stats_found
            
        except Exception as e:
            print(f"⚠️  Error extrayendo estadísticas del perfil: {e}")
        
        return metrics
        
    except Exception as e:
        print(f"❌ Error accediendo al perfil: {e}")
        return None

def extract_recent_videos_metrics(driver, username, max_videos=5):
    """Extraer métricas de videos recientes"""
    print(f"🎬 Extrayendo métricas de videos recientes (máximo {max_videos})")
    
    try:
        # Ya estamos en el perfil, buscar videos
        time.sleep(3)
        
        videos_metrics = []
        
        # Buscar contenedores de videos
        video_selectors = [
            "[data-e2e='user-post-item']",
            "div[class*='video']",
            "a[href*='/video/']"
        ]
        
        videos_found = []
        
        for selector in video_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                videos_found.extend(elements[:max_videos])
                if len(videos_found) >= max_videos:
                    break
            except:
                continue
        
        print(f"   🎥 Encontrados {len(videos_found)} videos")
        
        for i, video_element in enumerate(videos_found[:max_videos]):
            try:
                print(f"   📹 Analizando video {i+1}...")
                
                # Intentar hacer click o hover para mostrar métricas
                driver.execute_script("arguments[0].scrollIntoView();", video_element)
                time.sleep(1)
                
                # Buscar métricas dentro del video
                video_metrics = {}
                
                # Buscar números (likes, views, etc.)
                numbers = video_element.find_elements(By.XPATH, ".//strong | .//span[contains(@class, 'count')] | .//*[contains(text(), 'K')] | .//*[contains(text(), 'M')]")
                
                for j, num_element in enumerate(numbers):
                    text = num_element.text.strip()
                    if text and any(char.isdigit() for char in text):
                        video_metrics[f"metric_{j+1}"] = text
                        print(f"      📊 {text}")
                
                # Intentar obtener el link del video
                try:
                    link = video_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if link:
                        video_metrics['url'] = link
                        print(f"      🔗 URL: {link}")
                except:
                    pass
                
                if video_metrics:
                    videos_metrics.append({
                        'video_index': i + 1,
                        'metrics': video_metrics
                    })
                
            except Exception as e:
                print(f"      ⚠️  Error en video {i+1}: {e}")
                continue
        
        return videos_metrics
        
    except Exception as e:
        print(f"❌ Error extrayendo videos: {e}")
        return []

def test_tiktok_scraping():
    """Función principal de prueba"""
    print("🕷️  PRUEBA DE SCRAPING DE TIKTOK")
    print("👤 Cuenta: @chakakitafreakyvideos")
    print("=" * 50)
    
    # Cargar configuración
    load_dotenv()
    username = os.getenv('TIKTOK_USERNAME', 'chakakitafreakyvideos')
    
    driver = None
    
    try:
        # Configurar driver
        print("🌐 Configurando navegador...")
        driver = setup_driver()
        
        # Cargar cookies
        print("🍪 Cargando cookies de sesión...")
        if not load_cookies(driver):
            print("❌ No se pudieron cargar las cookies")
            return
        
        # Refrescar para aplicar cookies
        driver.refresh()
        time.sleep(3)
        
        # Verificar si estamos logueados
        try:
            # Buscar indicadores de que estamos logueados
            logged_in_indicators = driver.find_elements(By.XPATH, "//div[@data-e2e='profile-icon'] | //span[contains(@class, 'avatar')] | //a[contains(@href, '/@')]")
            
            if logged_in_indicators:
                print("✅ Sesión activa detectada")
            else:
                print("⚠️  No se detectó sesión activa, continuando...")
        
        except:
            print("⚠️  No se pudo verificar el estado de login")
        
        # Extraer métricas del perfil
        profile_metrics = extract_profile_metrics(driver, username)
        
        # Extraer métricas de videos
        videos_metrics = extract_recent_videos_metrics(driver, username, max_videos=3)
        
        # Guardar resultados
        results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'username': username,
            'profile_metrics': profile_metrics,
            'videos_metrics': videos_metrics
        }
        
        # Crear directorio de resultados
        os.makedirs('data/analytics', exist_ok=True)
        
        # Guardar en archivo JSON
        results_file = f"data/analytics/tiktok_metrics_{int(time.time())}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE EXTRACCIÓN")
        print("=" * 50)
        
        if profile_metrics and profile_metrics.get('profile_stats'):
            print("✅ Métricas del perfil extraídas")
            for key, value in profile_metrics['profile_stats'].items():
                print(f"   📈 {key}: {value}")
        else:
            print("⚠️  No se pudieron extraer métricas del perfil")
        
        if videos_metrics:
            print(f"✅ Métricas de {len(videos_metrics)} videos extraídas")
            for video in videos_metrics:
                print(f"   🎥 Video {video['video_index']}: {len(video['metrics'])} métricas")
        else:
            print("⚠️  No se pudieron extraer métricas de videos")
        
        print(f"\n📁 Resultados guardados en: {results_file}")
        
        # Mostrar próximos pasos
        print("\n💡 PRÓXIMOS PASOS:")
        if profile_metrics or videos_metrics:
            print("1. ✅ Scraping funcional - Integrar al sistema principal")
            print("2. 🔄 Programar extracción regular de métricas")
            print("3. 📈 Usar métricas para análisis de tendencias")
        else:
            print("1. 🔍 Revisar estructura del sitio de TikTok")
            print("2. 🍪 Verificar que las cookies sean válidas")
            print("3. 🛡️  Posible detección anti-bot")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
    
    finally:
        if driver:
            input("\n⏸️  Presiona ENTER para cerrar el navegador...")
            driver.quit()

if __name__ == "__main__":
    test_tiktok_scraping()
