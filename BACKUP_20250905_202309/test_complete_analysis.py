#!/usr/bin/env python3
"""
Análisis COMPLETO de métricas de TikTok
Extrae TODOS los videos para análisis profundo
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
    """Configurar Chrome driver optimizado"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def load_cookies(driver):
    """Cargar cookies de TikTok"""
    cookies_file = "data/tiktok_cookies.json"
    
    if not os.path.exists(cookies_file):
        print(f"❌ Archivo de cookies no encontrado: {cookies_file}")
        return False
    
    try:
        driver.get("https://www.tiktok.com")
        time.sleep(2)
        
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        for name, value in cookies.items():
            try:
                driver.add_cookie({
                    'name': name,
                    'value': value,
                    'domain': '.tiktok.com'
                })
            except:
                pass
        
        print(f"✅ Cookies cargadas: {len(cookies)} cookies")
        return True
        
    except Exception as e:
        print(f"❌ Error cargando cookies: {e}")
        return False

def extract_all_videos_metrics(driver, username, max_scroll=10):
    """Extraer métricas de TODOS los videos disponibles"""
    print(f"🎬 Extrayendo métricas de TODOS los videos disponibles")
    print(f"📜 Máximo de scrolls: {max_scroll}")
    
    try:
        # Ir al perfil
        profile_url = f"https://www.tiktok.com/@{username}"
        driver.get(profile_url)
        time.sleep(5)
        
        all_videos = []
        videos_found_count = 0
        scroll_count = 0
        
        while scroll_count < max_scroll:
            print(f"   🔍 Scroll {scroll_count + 1}/{max_scroll}...")
            
            # Buscar todos los videos en la página actual
            video_selectors = [
                "[data-e2e='user-post-item']",
                "div[class*='video']",
                "a[href*='/video/']"
            ]
            
            current_videos = []
            for selector in video_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    current_videos.extend(elements)
                except:
                    continue
            
            # Procesar videos encontrados en este scroll
            new_videos_count = 0
            for i, video_element in enumerate(current_videos):
                try:
                    # Verificar si ya procesamos este video
                    link_element = video_element.find_element(By.TAG_NAME, "a")
                    video_url = link_element.get_attribute("href")
                    
                    if not video_url or any(v.get('url') == video_url for v in all_videos):
                        continue  # Video ya procesado
                    
                    # Hacer scroll al video para que cargue las métricas
                    driver.execute_script("arguments[0].scrollIntoView(true);", video_element)
                    time.sleep(0.5)
                    
                    # Extraer métricas del video
                    video_metrics = {
                        'url': video_url,
                        'video_id': video_url.split('/')[-1] if '/' in video_url else 'unknown',
                        'position': videos_found_count + new_videos_count + 1
                    }
                    
                    # Buscar números (views, likes, etc.)
                    try:
                        numbers = video_element.find_elements(By.XPATH, ".//strong | .//span[contains(@class, 'count')] | .//*[contains(text(), 'K')] | .//*[contains(text(), 'M')] | .//*[text()[string-length(.) > 0 and string-length(.) < 10 and translate(., '0123456789KM', '') = '']]")
                        
                        metrics_extracted = {}
                        for j, num_element in enumerate(numbers):
                            text = num_element.text.strip()
                            if text and (text.isdigit() or 'K' in text or 'M' in text):
                                metrics_extracted[f"metric_{j+1}"] = text
                        
                        video_metrics['metrics'] = metrics_extracted
                        
                        # Intentar obtener imagen thumbnail
                        try:
                            img_element = video_element.find_element(By.TAG_NAME, "img")
                            thumbnail = img_element.get_attribute("src")
                            if thumbnail:
                                video_metrics['thumbnail'] = thumbnail
                        except:
                            pass
                        
                    except Exception as e:
                        video_metrics['metrics'] = {}
                        video_metrics['error'] = str(e)
                    
                    all_videos.append(video_metrics)
                    new_videos_count += 1
                    
                    # Mostrar progreso cada 5 videos
                    if (videos_found_count + new_videos_count) % 5 == 0:
                        print(f"      📊 Procesados {videos_found_count + new_videos_count} videos...")
                    
                except Exception as e:
                    continue
            
            videos_found_count += new_videos_count
            
            if new_videos_count == 0:
                print(f"      ⚠️  No se encontraron videos nuevos en este scroll")
                # Intentar scroll más agresivo
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Si no encontramos videos en 2 scrolls consecutivos, parar
                if scroll_count > 0:
                    print(f"      🔚 No hay más videos disponibles")
                    break
            else:
                print(f"      ✅ Encontrados {new_videos_count} videos nuevos (Total: {videos_found_count})")
            
            # Hacer scroll hacia abajo para cargar más contenido
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Esperar a que cargue el contenido
            
            scroll_count += 1
        
        print(f"\n🎉 Análisis completo: {len(all_videos)} videos procesados")
        return all_videos
        
    except Exception as e:
        print(f"❌ Error extrayendo videos: {e}")
        return []

def analyze_complete_performance(videos_data):
    """Análisis profundo de todos los videos"""
    print(f"\n📈 ANÁLISIS PROFUNDO DE {len(videos_data)} VIDEOS")
    print("=" * 50)
    
    if not videos_data:
        print("❌ No hay datos para analizar")
        return None
    
    # Extraer todas las métricas numéricas
    all_views = []
    all_metrics = []
    
    for video in videos_data:
        metrics = video.get('metrics', {})
        for key, value in metrics.items():
            if isinstance(value, str):
                # Convertir K, M a números
                numeric_value = convert_to_number(value)
                if numeric_value > 0:
                    all_views.append(numeric_value)
                    all_metrics.append({
                        'video_id': video.get('video_id', 'unknown'),
                        'metric': key,
                        'value': numeric_value,
                        'original': value,
                        'url': video.get('url', '')
                    })
    
    if not all_views:
        print("❌ No se pudieron extraer métricas numéricas")
        return None
    
    # Estadísticas generales
    total_videos = len(videos_data)
    avg_views = sum(all_views) / len(all_views)
    max_views = max(all_views)
    min_views = min(all_views)
    median_views = sorted(all_views)[len(all_views)//2]
    
    print(f"📊 ESTADÍSTICAS GENERALES:")
    print(f"   🎬 Total de videos: {total_videos}")
    print(f"   📈 Promedio de views: {avg_views:.0f}")
    print(f"   🏆 Mejor video: {max_views:,} views")
    print(f"   📉 Menor video: {min_views:,} views")
    print(f"   🎯 Mediana: {median_views:.0f} views")
    print(f"   📊 Rango: {max_views/max(min_views,1):.1f}x diferencia")
    
    # Top 5 videos
    top_videos = sorted(all_metrics, key=lambda x: x['value'], reverse=True)[:5]
    print(f"\n🏆 TOP 5 VIDEOS:")
    for i, video in enumerate(top_videos, 1):
        print(f"   {i}. {video['value']:,} views - ID: {video['video_id']}")
    
    # Análisis de tendencias
    print(f"\n📈 ANÁLISIS DE TENDENCIAS:")
    
    # Categorizar videos por rendimiento
    high_performance = [v for v in all_views if v > avg_views * 1.5]
    low_performance = [v for v in all_views if v < avg_views * 0.5]
    
    print(f"   🔥 Videos high-performance: {len(high_performance)} ({len(high_performance)/total_videos*100:.1f}%)")
    print(f"   📉 Videos low-performance: {len(low_performance)} ({len(low_performance)/total_videos*100:.1f}%)")
    print(f"   ⭐ Videos average: {total_videos - len(high_performance) - len(low_performance)}")
    
    # Cálculo de consistency score
    import statistics
    try:
        std_dev = statistics.stdev(all_views)
        consistency_score = 1 - (std_dev / avg_views)
        print(f"   🎯 Consistency Score: {consistency_score:.2f} (0-1, más alto = más consistente)")
    except:
        consistency_score = 0
    
    return {
        'total_videos': total_videos,
        'avg_views': avg_views,
        'max_views': max_views,
        'min_views': min_views,
        'median_views': median_views,
        'high_performance_count': len(high_performance),
        'low_performance_count': len(low_performance),
        'consistency_score': consistency_score,
        'top_videos': top_videos,
        'all_metrics': all_metrics
    }

def convert_to_number(value_str):
    """Convertir strings como '1.2K', '500', '1M' a números"""
    if not isinstance(value_str, str):
        return 0
    
    value_str = value_str.strip().replace(',', '')
    
    try:
        if 'K' in value_str:
            return int(float(value_str.replace('K', '')) * 1000)
        elif 'M' in value_str:
            return int(float(value_str.replace('M', '')) * 1000000)
        elif value_str.isdigit():
            return int(value_str)
        else:
            return 0
    except:
        return 0

def main():
    """Función principal para análisis completo"""
    print("🔍 ANÁLISIS COMPLETO DE TIKTOK")
    print("👤 Cuenta: @chakakitafreakyvideos")
    print("🎯 Extrayendo TODOS los videos disponibles")
    print("=" * 60)
    
    load_dotenv()
    username = os.getenv('TIKTOK_USERNAME', 'chakakitafreakyvideos')
    
    driver = None
    
    try:
        # Configurar y cargar
        print("🌐 Configurando navegador...")
        driver = setup_driver()
        
        print("🍪 Cargando cookies...")
        if not load_cookies(driver):
            return
        
        driver.refresh()
        time.sleep(3)
        
        # Extraer TODOS los videos
        all_videos = extract_all_videos_metrics(driver, username, max_scroll=20)  # Aumentado a 20 scrolls
        
        if not all_videos:
            print("❌ No se pudieron extraer videos")
            return
        
        # Análisis profundo
        analysis = analyze_complete_performance(all_videos)
        
        # Guardar resultados completos
        complete_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'username': username,
            'total_videos_found': len(all_videos),
            'analysis': analysis,
            'all_videos_data': all_videos
        }
        
        os.makedirs('data/analytics', exist_ok=True)
        results_file = f"data/analytics/complete_analysis_{int(time.time())}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(complete_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Análisis completo guardado en: {results_file}")
        
        if analysis:
            print(f"\n💡 RECOMENDACIONES BASADAS EN {analysis['total_videos']} VIDEOS:")
            
            if analysis['consistency_score'] > 0.7:
                print("✅ Tu contenido es muy consistente")
            elif analysis['consistency_score'] > 0.4:
                print("⚠️  Tu contenido tiene rendimiento variable")
            else:
                print("🔄 Oportunidad de mejorar consistencia")
            
            if analysis['high_performance_count'] > analysis['total_videos'] * 0.3:
                print("🔥 Tienes buen porcentaje de videos virales")
            else:
                print("📈 Oportunidad de aumentar videos high-performance")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
    
    finally:
        if driver:
            input("\n⏸️  Presiona ENTER para cerrar el navegador...")
            driver.quit()

if __name__ == "__main__":
    main()
