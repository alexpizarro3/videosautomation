import os
import yaml
from dotenv import load_dotenv
from typing import Dict, Any

class Config:
    """Clase para manejar la configuración del proyecto"""
    
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()
        
        # Cargar configuración desde YAML
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.yml')
        with open(config_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)
    
    @property
    def gemini_api_key(self) -> str:
        return os.getenv('GEMINI_API_KEY', '')
    
    @property
    def veo3_api_key(self) -> str:
        return os.getenv('VEO3_API_KEY', '')
    
    @property
    def gemini_model(self) -> str:
        return os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-preview-image-generation')
    
    @property
    def veo3_model(self) -> str:
        return os.getenv('VEO3_MODEL', 'models/veo-3.0-generate-preview')
    
    @property
    def tiktok_username(self) -> str:
        return os.getenv('TIKTOK_USERNAME', '')
    
    @property
    def tiktok_password(self) -> str:
        return os.getenv('TIKTOK_PASSWORD', '')
    
    @property
    def max_videos_per_day(self) -> int:
        return int(os.getenv('MAX_VIDEOS_PER_DAY', 3))
    
    @property
    def max_images_per_day(self) -> int:
        return int(os.getenv('MAX_IMAGES_PER_DAY', 10))
    
    @property
    def scraping_delay(self) -> int:
        return int(os.getenv('SCRAPING_DELAY', 2))
    
    @property
    def upload_delay(self) -> int:
        return int(os.getenv('UPLOAD_DELAY', 30))
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Obtener configuración desde el archivo YAML"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_project_root(self) -> str:
        """Obtener la ruta raíz del proyecto"""
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    def get_data_dir(self, subdir: str = '') -> str:
        """Obtener directorio de datos"""
        data_dir = os.path.join(self.get_project_root(), 'data', subdir)
        os.makedirs(data_dir, exist_ok=True)
        return data_dir
    
    def get_cookies_path(self) -> str:
        """Obtener ruta de las cookies de TikTok"""
        return os.path.join(self.get_project_root(), 'config', 'tiktok_cookies.json')

# Instancia global de configuración
config = Config()
