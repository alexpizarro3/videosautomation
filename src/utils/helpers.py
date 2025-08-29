import json
import time
import random
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
import os

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Cargar archivo JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """Guardar archivo JSON"""
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def random_delay(min_seconds: int = 1, max_seconds: int = 5):
    """Delay aleatorio para evitar detección"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def sanitize_filename(filename: str) -> str:
    """Limpiar nombre de archivo para evitar caracteres inválidos"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:255]  # Limitar longitud

def calculate_engagement_rate(likes: int, comments: int, shares: int, views: int) -> float:
    """Calcular tasa de engagement"""
    if views == 0:
        return 0.0
    
    total_interactions = likes + comments + shares
    return (total_interactions / views) * 100

def format_number(number: int) -> str:
    """Formatear números grandes (1K, 1M, etc.)"""
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)

def get_trending_hashtags() -> List[str]:
    """Obtener hashtags trending básicos"""
    # En una implementación real, esto podría hacer scraping de hashtags trending
    base_hashtags = [
        "#fyp", "#viral", "#trending", "#foryou", "#foryoupage",
        "#ai", "#automation", "#tech", "#lifestyle", "#daily",
        "#content", "#creator", "#video", "#short", "#tiktok"
    ]
    
    # Agregar hashtags basados en fecha
    current_month = datetime.now().strftime("%B").lower()
    current_year = datetime.now().year
    
    seasonal_hashtags = [
        f"#{current_month}",
        f"#{current_year}",
        "#new",
        "#fresh"
    ]
    
    return base_hashtags + seasonal_hashtags

def clean_text(text: str) -> str:
    """Limpiar texto para uso en títulos y descripciones"""
    # Eliminar caracteres especiales problemáticos
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())  # Normalizar espacios
    return text[:280]  # Limitar longitud

def is_within_rate_limit(last_action_time: Optional[datetime], min_interval_minutes: int = 30) -> bool:
    """Verificar si podemos realizar una acción basada en rate limiting"""
    if last_action_time is None:
        return True
    
    time_diff = datetime.now() - last_action_time
    return time_diff >= timedelta(minutes=min_interval_minutes)

def get_optimal_posting_times() -> List[str]:
    """Obtener horarios óptimos para postear en TikTok"""
    # Horarios basados en estudios de engagement en TikTok
    optimal_times = [
        "06:00",  # Mañana temprano
        "09:00",  # Media mañana
        "12:00",  # Mediodía
        "15:00",  # Media tarde
        "18:00",  # Tarde
        "21:00",  # Noche
    ]
    return optimal_times

def validate_video_specs(file_path: str) -> Dict[str, Any]:
    """Validar especificaciones de video para TikTok"""
    import cv2
    
    try:
        cap = cv2.VideoCapture(file_path)
        
        # Obtener propiedades del video
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        
        cap.release()
        
        # Validaciones para TikTok
        is_valid_ratio = height > width  # Vertical
        is_valid_duration = 3 <= duration <= 180  # 3 segundos a 3 minutos
        is_valid_resolution = height >= 720  # Mínimo 720p
        
        return {
            "width": width,
            "height": height,
            "fps": fps,
            "duration": duration,
            "is_valid_ratio": is_valid_ratio,
            "is_valid_duration": is_valid_duration,
            "is_valid_resolution": is_valid_resolution,
            "is_valid": is_valid_ratio and is_valid_duration and is_valid_resolution
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "is_valid": False
        }

def create_progress_tracker():
    """Crear tracker de progreso simple"""
    class ProgressTracker:
        def __init__(self):
            self.steps = []
            self.current_step = 0
        
        def add_step(self, name: str):
            self.steps.append({"name": name, "completed": False})
        
        def complete_step(self):
            if self.current_step < len(self.steps):
                self.steps[self.current_step]["completed"] = True
                self.current_step += 1
        
        def get_progress(self) -> float:
            if not self.steps:
                return 0.0
            completed = sum(1 for step in self.steps if step["completed"])
            return (completed / len(self.steps)) * 100
        
        def get_current_step(self) -> Optional[str]:
            if self.current_step < len(self.steps):
                return self.steps[self.current_step]["name"]
            return None
    
    return ProgressTracker()
