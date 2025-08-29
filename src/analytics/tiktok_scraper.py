import json
import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

from ..utils.logger import get_logger
from ..utils.config import config
from ..utils.helpers import load_json_file, save_json_file, random_delay, calculate_engagement_rate

class TikTokScraper:
    """Scraper para extraer métricas de videos de TikTok"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.driver = None
        self.cookies = self._load_cookies()
        
    def _load_cookies(self) -> List[Dict]:
        """Cargar cookies de TikTok"""
        cookies_path = config.get_cookies_path()
        cookies_data = load_json_file(cookies_path)
        
        if not cookies_data or 'cookies' not in cookies_data:
            self.logger.warning("No se encontraron cookies de TikTok")
            return []
        
        return cookies_data.get('cookies', [])
    
    def _setup_driver(self) -> webdriver.Chrome:
        """Configurar driver de Chrome sin detección"""
        self.logger.info("Configurando driver de Chrome...")
        
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Modo headless opcional (comentar para debug)
        # options.add_argument("--headless")
        
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _load_cookies_to_driver(self):
        """Cargar cookies en el driver"""
        if not self.cookies:
            return
        
        # Ir a TikTok primero
        self.driver.get("https://www.tiktok.com")
        time.sleep(3)
        
        # Cargar cookies
        for cookie in self.cookies:
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                self.logger.warning(f"No se pudo cargar cookie {cookie.get('name', 'unknown')}: {e}")
        
        # Refrescar página
        self.driver.refresh()
        time.sleep(3)
    
    def scrape_user_videos(self, username: str, max_videos: int = 50) -> List[Dict[str, Any]]:
        """Scrapear videos de un usuario específico"""
        self.logger.info(f"Scrapeando videos del usuario: @{username}")
        
        try:
            self.driver = self._setup_driver()
            self._load_cookies_to_driver()
            
            # Ir al perfil del usuario
            profile_url = f"https://www.tiktok.com/@{username}"
            self.driver.get(profile_url)
            
            # Esperar a que cargue la página
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='user-post-item']"))
            )
            
            videos = []
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-e2e='user-post-item']")
            
            self.logger.info(f"Encontrados {len(video_elements)} videos")
            
            for i, video_element in enumerate(video_elements[:max_videos]):
                try:
                    # Click en el video para obtener métricas
                    video_link = video_element.find_element(By.TAG_NAME, "a")
                    video_url = video_link.get_attribute("href")
                    
                    # Abrir video en nueva pestaña
                    self.driver.execute_script("window.open(arguments[0]);", video_url)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    
                    # Esperar a que cargue
                    time.sleep(3)
                    
                    # Extraer métricas
                    video_data = self._extract_video_metrics()
                    if video_data:
                        video_data['url'] = video_url
                        video_data['scraped_at'] = datetime.now().isoformat()
                        videos.append(video_data)
                        self.logger.info(f"Video {i+1}/{min(max_videos, len(video_elements))} procesado")
                    
                    # Cerrar pestaña y volver al perfil
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    
                    # Delay para evitar detección
                    random_delay(2, 4)
                    
                except Exception as e:
                    self.logger.error(f"Error procesando video {i+1}: {e}")
                    # Asegurar que volvemos a la pestaña principal
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    continue
            
            self.logger.success(f"Scraping completado: {len(videos)} videos procesados")
            return videos
            
        except Exception as e:
            self.logger.error(f"Error en scraping: {e}")
            return []
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def _extract_video_metrics(self) -> Optional[Dict[str, Any]]:
        """Extraer métricas de un video individual"""
        try:
            # Esperar a que carguen los elementos de métricas
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='like-count']"))
            )
            
            # Extraer título/descripción
            title_element = self.driver.find_element(By.CSS_SELECTOR, "[data-e2e='browse-video-desc']")
            title = title_element.text if title_element else ""
            
            # Extraer métricas de interacción
            likes = self._extract_count("[data-e2e='like-count']")
            comments = self._extract_count("[data-e2e='comment-count']")
            shares = self._extract_count("[data-e2e='share-count']")
            
            # Extraer vistas (más difícil, puede no estar disponible)
            views = self._extract_views()
            
            # Extraer hashtags
            hashtags = self._extract_hashtags()
            
            # Calcular engagement rate
            engagement_rate = calculate_engagement_rate(likes, comments, shares, views) if views > 0 else 0
            
            return {
                'title': title,
                'likes': likes,
                'comments': comments,
                'shares': shares,
                'views': views,
                'engagement_rate': engagement_rate,
                'hashtags': hashtags,
                'extracted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error extrayendo métricas: {e}")
            return None
    
    def _extract_count(self, selector: str) -> int:
        """Extraer conteo de métricas"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            text = element.text.strip()
            
            # Convertir texto a número (ej: "1.2K" -> 1200)
            if 'K' in text.upper():
                return int(float(text.upper().replace('K', '')) * 1000)
            elif 'M' in text.upper():
                return int(float(text.upper().replace('M', '')) * 1000000)
            else:
                return int(text) if text.isdigit() else 0
                
        except Exception:
            return 0
    
    def _extract_views(self) -> int:
        """Extraer número de vistas"""
        try:
            # TikTok a veces no muestra las vistas públicamente
            # Intentar diferentes selectores
            selectors = [
                "[data-e2e='video-views']",
                ".view-count",
                "[data-e2e='browse-video-views']"
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    text = element.text.strip()
                    
                    if 'K' in text.upper():
                        return int(float(text.upper().replace('K', '')) * 1000)
                    elif 'M' in text.upper():
                        return int(float(text.upper().replace('M', '')) * 1000000)
                    else:
                        return int(text) if text.isdigit() else 0
                except:
                    continue
            
            # Si no encontramos vistas, estimar basado en likes (ratio aproximado 10:1)
            likes = self._extract_count("[data-e2e='like-count']")
            return likes * 10 if likes > 0 else 0
            
        except Exception:
            return 0
    
    def _extract_hashtags(self) -> List[str]:
        """Extraer hashtags del video"""
        try:
            description_element = self.driver.find_element(By.CSS_SELECTOR, "[data-e2e='browse-video-desc']")
            description = description_element.text if description_element else ""
            
            # Extraer hashtags usando regex
            import re
            hashtags = re.findall(r'#\w+', description)
            return hashtags
            
        except Exception:
            return []
    
    def save_metrics(self, videos: List[Dict[str, Any]], username: str):
        """Guardar métricas en archivo JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"metrics_{username}_{timestamp}.json"
        filepath = config.get_data_dir('metrics')
        filepath = f"{filepath}/{filename}"
        
        data = {
            'username': username,
            'scraped_at': datetime.now().isoformat(),
            'total_videos': len(videos),
            'videos': videos
        }
        
        if save_json_file(data, filepath):
            self.logger.success(f"Métricas guardadas en: {filename}")
            return filepath
        else:
            self.logger.error("Error guardando métricas")
            return None

# Función auxiliar para uso directo
def scrape_tiktok_metrics(username: str, max_videos: int = 50) -> List[Dict[str, Any]]:
    """Función auxiliar para scrapear métricas de TikTok"""
    scraper = TikTokScraper()
    videos = scraper.scrape_user_videos(username, max_videos)
    
    if videos:
        scraper.save_metrics(videos, username)
    
    return videos
