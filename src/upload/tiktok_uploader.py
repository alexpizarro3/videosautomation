import os
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc

from ..utils.logger import get_logger
from ..utils.config import config
from ..utils.helpers import load_json_file, save_json_file, random_delay, get_optimal_posting_times

class TikTokUploader:
    """Subidor automático de videos a TikTok"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.driver = None
        self.cookies = self._load_cookies()
        self.upload_delay = config.upload_delay
        
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
        self.logger.info("Configurando driver para subida...")
        
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Configurar para permitir subida de archivos
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option("prefs", prefs)
        
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _load_cookies_to_driver(self):
        """Cargar cookies en el driver"""
        if not self.cookies:
            self.logger.warning("No hay cookies para cargar")
            return False
        
        try:
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
            
            # Verificar si estamos logueados
            return self._verify_login()
            
        except Exception as e:
            self.logger.error(f"Error cargando cookies: {e}")
            return False
    
    def _verify_login(self) -> bool:
        """Verificar si estamos logueados correctamente"""
        try:
            # Buscar elementos que indiquen que estamos logueados
            login_indicators = [
                "[data-e2e='upload-icon']",
                "[data-e2e='nav-upload']",
                "//a[@href='/upload']",
                ".upload-btn"
            ]
            
            for indicator in login_indicators:
                try:
                    if indicator.startswith("//"):
                        element = self.driver.find_element(By.XPATH, indicator)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, indicator)
                    
                    if element:
                        self.logger.success("Login verificado exitosamente")
                        return True
                except:
                    continue
            
            self.logger.warning("No se pudo verificar el login")
            return False
            
        except Exception as e:
            self.logger.error(f"Error verificando login: {e}")
            return False
    
    def upload_videos(self, videos_data: List[Dict[str, Any]], content_suggestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Subir múltiples videos a TikTok"""
        self.logger.info(f"Iniciando subida de {len(videos_data)} videos")
        
        upload_results = []
        
        try:
            self.driver = self._setup_driver()
            
            if not self._load_cookies_to_driver():
                self.logger.error("No se pudo establecer sesión en TikTok")
                return upload_results
            
            for i, video_data in enumerate(videos_data):
                if not video_data.get('success', False):
                    self.logger.warning(f"Saltando video {i+1} (no se generó exitosamente)")
                    continue
                
                video_path = video_data.get('video_path')
                if not video_path or not os.path.exists(video_path):
                    self.logger.error(f"Video {i+1} no encontrado: {video_path}")
                    continue

                # Convertir el video a formato TikTok con zoom y centrado antes de subir
                try:
                    from convertir_video_tiktok import convertir_a_9_16_zoom
                    tiktok_video_path = video_path.replace('.mp4', '_tiktok.mp4')
                    convertir_a_9_16_zoom(video_path, tiktok_video_path)
                    self.logger.info(f"Video convertido a formato TikTok: {tiktok_video_path}")
                except Exception as e:
                    self.logger.error(f"Error convirtiendo video {video_path}: {e}")
                    tiktok_video_path = video_path  # Si falla, sube el original

                # Usar el video convertido para la subida
                result = self._upload_single_video(tiktok_video_path, content, i+1)
                upload_results.append(result)
                
                # Obtener sugerencias de contenido
                content = content_suggestions[i] if i < len(content_suggestions) else {}
                
                self.logger.info(f"Subiendo video {i+1}/{len(videos_data)}")
                
                # Subir video individual
                result = self._upload_single_video(video_path, content, i+1)
                upload_results.append(result)
                
                # Delay entre subidas para evitar detección
                if i < len(videos_data) - 1:
                    delay_time = self.upload_delay + random.randint(10, 30)
                    self.logger.info(f"Esperando {delay_time} segundos antes del siguiente video...")
                    time.sleep(delay_time)
            
            successful_uploads = [r for r in upload_results if r.get('success', False)]
            self.logger.success(f"Subida completada: {len(successful_uploads)}/{len(videos_data)} videos exitosos")
            
        except Exception as e:
            self.logger.error(f"Error en proceso de subida: {e}")
        
        finally:
            if self.driver:
                self.driver.quit()
        
        return upload_results
    
    def _upload_single_video(self, video_path: str, content: Dict[str, Any], video_number: int) -> Dict[str, Any]:
        """Subir un video individual"""
        try:
            # Ir a la página de subida
            self.driver.get("https://www.tiktok.com/upload")
            
            # Esperar a que cargue la página
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            
            # Encontrar el input de archivo
            file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            
            # Subir archivo
            file_input.send_keys(video_path)
            
            # Esperar a que se procese el video
            self._wait_for_video_processing()
            
            # Completar información del video
            self._fill_video_information(content)
            
            # Publicar video
            success = self._publish_video()
            
            result = {
                'video_number': video_number,
                'video_path': video_path,
                'title': content.get('suggested_title', ''),
                'hashtags': content.get('hashtags', []),
                'uploaded_at': datetime.now().isoformat(),
                'success': success
            }
            
            if success:
                self.logger.success(f"Video {video_number} subido exitosamente")
            else:
                self.logger.error(f"Error subiendo video {video_number}")
                result['error'] = 'Upload failed'
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error subiendo video {video_number}: {e}")
            return {
                'video_number': video_number,
                'video_path': video_path,
                'error': str(e),
                'success': False
            }
    
    def _wait_for_video_processing(self):
        """Esperar a que el video se procese"""
        self.logger.info("Esperando procesamiento del video...")
        
        try:
            # Esperar a que aparezca el preview del video o elementos de edición
            processing_indicators = [
                "[data-e2e='video-upload-progress']",
                ".video-preview",
                "[data-e2e='edit-video']",
                "video",
                ".upload-progress"
            ]
            
            for _ in range(60):  # Máximo 2 minutos
                for indicator in processing_indicators:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, indicator)
                        if element and element.is_displayed():
                            self.logger.success("Video procesado correctamente")
                            return
                    except:
                        continue
                
                time.sleep(2)
            
            self.logger.warning("Timeout esperando procesamiento del video")
            
        except Exception as e:
            self.logger.error(f"Error esperando procesamiento: {e}")
    
    def _fill_video_information(self, content: Dict[str, Any]):
        """Completar información del video"""
        try:
            # Completar título/descripción
            title = content.get('suggested_title', 'AI Generated Content')
            hashtags = content.get('hashtags', [])
            
            # Crear descripción completa
            description = f"{title} {' '.join(hashtags)}"
            
            # Buscar campo de descripción
            description_selectors = [
                "[data-e2e='video-caption']",
                "textarea[placeholder*='Describe your video']",
                "textarea[placeholder*='descripción']",
                ".public-DraftEditor-content",
                "div[contenteditable='true']"
            ]
            
            description_field = None
            for selector in description_selectors:
                try:
                    description_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if description_field and description_field.is_displayed():
                        break
                except:
                    continue
            
            if description_field:
                # Limpiar campo y escribir descripción
                description_field.clear()
                description_field.send_keys(description[:300])  # Límite de caracteres
                self.logger.info("Descripción completada")
                time.sleep(2)
            else:
                self.logger.warning("No se encontró campo de descripción")
            
            # Configurar privacidad (público)
            self._set_privacy_settings()
            
            # Configurar otras opciones
            self._set_additional_options()
            
        except Exception as e:
            self.logger.error(f"Error completando información: {e}")
    
    def _set_privacy_settings(self):
        """Configurar privacidad del video"""
        try:
            # Buscar opciones de privacidad
            privacy_selectors = [
                "[data-e2e='privacy-public']",
                "input[value='0']",  # Público suele ser valor 0
                ".privacy-option[data-value='public']"
            ]
            
            for selector in privacy_selectors:
                try:
                    privacy_option = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if privacy_option:
                        privacy_option.click()
                        self.logger.info("Privacidad configurada como pública")
                        return
                except:
                    continue
            
            self.logger.warning("No se pudo configurar privacidad")
            
        except Exception as e:
            self.logger.error(f"Error configurando privacidad: {e}")
    
    def _set_additional_options(self):
        """Configurar opciones adicionales"""
        try:
            # Permitir comentarios
            self._toggle_option("comments", True)
            
            # Permitir duetos
            self._toggle_option("duet", True)
            
            # Permitir reacciones
            self._toggle_option("stitch", True)
            
        except Exception as e:
            self.logger.error(f"Error configurando opciones adicionales: {e}")
    
    def _toggle_option(self, option_name: str, enable: bool):
        """Activar/desactivar una opción específica"""
        try:
            option_selectors = [
                f"[data-e2e='{option_name}-toggle']",
                f"input[name='{option_name}']",
                f".{option_name}-toggle"
            ]
            
            for selector in option_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    # Verificar estado actual
                    is_checked = element.is_selected() if element.tag_name == 'input' else 'checked' in element.get_attribute('class')
                    
                    # Cambiar estado si es necesario
                    if is_checked != enable:
                        element.click()
                        self.logger.info(f"Opción {option_name} {'activada' if enable else 'desactivada'}")
                    
                    return
                except:
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error configurando opción {option_name}: {e}")
    
    def _publish_video(self) -> bool:
        """Publicar el video"""
        try:
            # Buscar botón de publicar
            publish_selectors = [
                "[data-e2e='post-button']",
                "button[data-e2e='video-post-save-button']",
                "button:contains('Post')",
                "button:contains('Publicar')",
                ".btn-post",
                ".publish-btn"
            ]
            
            publish_button = None
            for selector in publish_selectors:
                try:
                    if ":contains(" in selector:
                        # XPath para texto
                        xpath = f"//button[contains(text(), '{selector.split(':contains(')[1][:-2]}')]"
                        publish_button = self.driver.find_element(By.XPATH, xpath)
                    else:
                        publish_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if publish_button and publish_button.is_enabled():
                        break
                except:
                    continue
            
            if publish_button:
                # Scroll para asegurar que el botón esté visible
                self.driver.execute_script("arguments[0].scrollIntoView();", publish_button)
                time.sleep(1)
                
                # Click en publicar
                publish_button.click()
                self.logger.info("Botón de publicar clickeado")
                
                # Esperar confirmación de publicación
                return self._wait_for_upload_confirmation()
            else:
                self.logger.error("No se encontró botón de publicar")
                return False
                
        except Exception as e:
            self.logger.error(f"Error publicando video: {e}")
            return False
    
    def _wait_for_upload_confirmation(self) -> bool:
        """Esperar confirmación de que el video se subió"""
        try:
            # Esperar mensajes de confirmación o redirección
            confirmation_indicators = [
                "Your video is being uploaded",
                "Video uploaded successfully",
                "Tu video se está subiendo",
                "Video subido exitosamente"
            ]
            
            for _ in range(30):  # Esperar hasta 1 minuto
                page_text = self.driver.page_source.lower()
                
                for indicator in confirmation_indicators:
                    if indicator.lower() in page_text:
                        self.logger.success("Confirmación de subida recibida")
                        return True
                
                # También verificar si fuimos redirigidos al perfil
                current_url = self.driver.current_url
                if "/upload" not in current_url:
                    self.logger.success("Redirigido después de subida exitosa")
                    return True
                
                time.sleep(2)
            
            # Si llegamos aquí, asumir que se subió (TikTok no siempre muestra confirmación clara)
            self.logger.info("No se recibió confirmación explícita, pero probablemente se subió")
            return True
            
        except Exception as e:
            self.logger.error(f"Error esperando confirmación: {e}")
            return False
    
    def save_upload_log(self, upload_results: List[Dict[str, Any]]) -> str:
        """Guardar log de subidas"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"upload_log_{timestamp}.json"
        filepath = config.get_data_dir('videos')
        filepath = f"{filepath}/{filename}"
        
        log_data = {
            'upload_date': datetime.now().isoformat(),
            'total_videos': len(upload_results),
            'successful_uploads': len([r for r in upload_results if r.get('success', False)]),
            'failed_uploads': len([r for r in upload_results if not r.get('success', False)]),
            'uploads': upload_results
        }
        
        if save_json_file(log_data, filepath):
            self.logger.success(f"Log de subidas guardado: {filename}")
            return filepath
        else:
            self.logger.error("Error guardando log de subidas")
            return ""

# Función auxiliar para uso directo
def upload_videos_to_tiktok(videos_data: List[Dict[str, Any]], content_suggestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Función auxiliar para subir videos a TikTok"""
    uploader = TikTokUploader()
    upload_results = uploader.upload_videos(videos_data, content_suggestions)
    
    # Guardar log
    uploader.save_upload_log(upload_results)
    
    return upload_results
