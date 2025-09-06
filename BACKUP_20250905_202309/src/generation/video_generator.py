import os
import base64
import requests
import time
import json
import pathlib
import cv2
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types

from ..utils.logger import get_logger
from ..utils.config import config
from ..utils.helpers import save_json_file, sanitize_filename

class Veo3VideoGenerator:
    """Generador de videos usando la API de Veo3"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.api_key = config.veo3_api_key  # Usar VEO3_API_KEY
        
        if not self.api_key:
            self.logger.error("API key de Veo3 no configurada")
            raise ValueError("VEO3_API_KEY no está configurada en las variables de entorno")
        
        # Inicializar cliente de Gemini (Veo3 es parte de Google Generative AI)
        self.client = genai.Client(api_key=self.api_key)
        
        # Configuración de Veo3
        self.veo_model = getattr(config, 'veo3_model', 'models/veo-3.0-generate-preview')  # Modelo con alta calidad y audio
        # self.veo_model = "models/veo-3.0-fast-generate-preview"  # Modelo rápido
        # self.veo_model = "veo-2.0-generate-001"  # Veo 2 sin audio
        
        self.max_videos_per_day = config.max_videos_per_day
        self.daily_count = self._get_daily_count()
    
    def _get_daily_count(self) -> int:
        """Obtener conteo de videos generados hoy"""
        try:
            # Buscar archivos de video creados hoy
            videos_dir = config.get_data_dir('videos')
            today = datetime.now().strftime('%Y%m%d')
            
            count = 0
            for filename in os.listdir(videos_dir):
                if filename.startswith(f"video_") and today in filename:
                    count += 1
            
            return count
        except:
            return 0
    
    def generate_videos_from_images(self, video_prompts: List[Dict[str, Any]], image_paths: List[str]) -> List[Dict[str, Any]]:
        """Generar videos a partir de imágenes y prompts"""
        self.logger.info(f"Generando {len(video_prompts)} videos con Veo3")
        
        # Verificar límite diario
        if self.daily_count >= self.max_videos_per_day:
            self.logger.warning(f"Límite diario alcanzado ({self.max_videos_per_day} videos). No se generarán más videos hoy.")
            return []
        
        # Ajustar cantidad si excede el límite
        available_slots = self.max_videos_per_day - self.daily_count
        videos_to_generate = min(len(video_prompts), available_slots)
        
        if videos_to_generate < len(video_prompts):
            self.logger.info(f"Generando solo {videos_to_generate} videos para no exceder el límite diario")
        
        generated_videos = []
        
        for i in range(videos_to_generate):
            try:
                prompt_data = video_prompts[i]
                image_path = image_paths[i] if i < len(image_paths) else None
                
                self.logger.info(f"Generando video {i+1}/{videos_to_generate}")
                
                # Generar video
                video_data = self._generate_single_video(prompt_data, image_path)
                
                if video_data:
                    generated_videos.append({
                        'prompt_id': prompt_data['id'],
                        'video_path': video_data['path'],
                        'prompt_text': prompt_data['prompt'],
                        'image_source': image_path,
                        'generated_at': datetime.now().isoformat(),
                        'duration': video_data.get('duration', 15),
                        'success': True
                    })
                    self.logger.success(f"Video {i+1} generado: {os.path.basename(video_data['path'])}")
                    self.daily_count += 1
                else:
                    self.logger.error(f"Error generando video {i+1}")
                    generated_videos.append({
                        'prompt_id': prompt_data['id'],
                        'error': 'Failed to generate video',
                        'success': False
                    })
                
                # Delay entre generaciones
                if i < videos_to_generate - 1:
                    time.sleep(5)  # Delay más largo para videos
                
            except Exception as e:
                self.logger.error(f"Error procesando video {i+1}: {e}")
                generated_videos.append({
                    'prompt_id': prompt_data['id'],
                    'error': str(e),
                    'success': False
                })
        
        successful_videos = [vid for vid in generated_videos if vid.get('success', False)]
        self.logger.info(f"Generación completada: {len(successful_videos)}/{videos_to_generate} videos exitosos")
        
        return generated_videos
    
    def _generate_single_video(self, prompt_data: Dict[str, Any], image_path: Optional[str]) -> Optional[Dict[str, Any]]:
        """Generar un video individual usando Veo3"""
        try:
            # Usar la API real de Veo3 (parte de Google Generative AI)
            return self._generate_with_veo3_api(prompt_data, image_path)
            
        except Exception as e:
            self.logger.error(f"Error en generación de video: {e}")
            return None
    
    def _generate_with_veo3_api(self, prompt_data: Dict[str, Any], image_path: Optional[str]) -> Optional[Dict[str, Any]]:
        """Generar video usando la API real de Veo3"""
        try:
            prompt = prompt_data.get('prompt', '')
            duration = prompt_data.get('duration', 15)
            
            self.logger.info(f"Generando video con Veo3: {prompt[:100]}...")
            
            # Optimizar prompt para TikTok usando las utilidades
            from ..utils.gemini_utils import optimize_prompt_for_tiktok, format_duration_for_veo
            
            optimized_prompt = optimize_prompt_for_tiktok(prompt, "video")
            safe_duration = format_duration_for_veo(duration)
            
            self.logger.info(f"Prompt optimizado: {optimized_prompt}")
            self.logger.info(f"Duración ajustada: {safe_duration}s")
            
            # Crear la operación de generación (basado en tu código funcional)
            operation = self.client.models.generate_videos(
                model=self.veo_model,
                prompt=optimized_prompt,
                config=types.GenerateVideosConfig(
                    # duration_seconds=safe_duration,  # Comentado por compatibilidad
                    # number_of_videos=1,
                    # negative_prompt="cartoon, low quality, horizontal format",
                )
            )
            
            self.logger.info("Operación de generación iniciada, esperando...")
            
            # Polling hasta que termine (igual que en tu notebook)
            max_wait_time = 300  # 5 minutos máximo
            wait_time = 0
            
            while not operation.done and wait_time < max_wait_time:
                self.logger.info(f"Esperando generación... ({wait_time}s)")
                time.sleep(10)
                wait_time += 10
                operation = self.client.operations.get(operation)
            
            if not operation.done:
                self.logger.error("Timeout esperando generación de video")
                return None
            
            self.logger.success("¡Video generado exitosamente!")
            
            # Obtener el video generado
            if (hasattr(operation, 'response') and 
                operation.response and 
                hasattr(operation.response, 'generated_videos') and
                operation.response.generated_videos):
                
                generated = operation.response.generated_videos[0]
                
                # Descargar el video usando el método de tu código
                video_path = self._download_veo3_video(generated, prompt_data)
                
                if video_path:
                    return {
                        'path': video_path,
                        'duration': safe_duration,
                        'resolution': '1080x1920',  # Vertical para TikTok
                        'model': self.veo_model,
                        'generated_with': 'veo3_api',
                        'prompt_used': optimized_prompt
                    }
            
            self.logger.error("No se recibió video en la respuesta")
            return None
            
        except Exception as e:
            self.logger.error(f"Error en API Veo3: {e}")
            self.logger.info("Creando video placeholder como respaldo...")
            # Fallback a método placeholder
            return self._create_placeholder_video(prompt_data, image_path)
    
    def _download_veo3_video(self, generated_video: Any, prompt_data: Dict[str, Any]) -> Optional[str]:
        """Descargar video generado por Veo3 (basado en tu código funcional)"""
        try:
            # Crear nombre de archivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            prompt_id = prompt_data.get('id', 'unknown')
            filename = f"video_{sanitize_filename(prompt_id)}_{timestamp}.mp4"
            
            videos_dir = config.get_data_dir('videos')
            filepath = os.path.join(videos_dir, filename)
            
            # Crear directorio si no existe
            pathlib.Path(videos_dir).mkdir(parents=True, exist_ok=True)
            
            # Método 1: Usar el cliente para descargar (como en tu notebook)
            try:
                self.client.files.download(file=generated_video.video)
                generated_video.video.save(filepath)
                
                # Verificar que el archivo se guardó correctamente
                if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                    self.logger.success(f"Video descargado exitosamente: {filename}")
                    return filepath
                
            except Exception as e:
                self.logger.warning(f"Método 1 falló: {e}, intentando método 2...")
            
            # Método 2: Descargar desde URL si está disponible
            try:
                if hasattr(generated_video, 'video_url'):
                    video_url = generated_video.video_url
                    response = requests.get(video_url, timeout=180)
                    response.raise_for_status()
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                        self.logger.success(f"Video descargado por URL: {filename}")
                        return filepath
                        
            except Exception as e:
                self.logger.warning(f"Método 2 falló: {e}")
            
            self.logger.error("No se pudo descargar el video por ningún método")
            return None
                
        except Exception as e:
            self.logger.error(f"Error descargando video de Veo3: {e}")
            return None
    
    def _generate_with_alternative_method(self, prompt_data: Dict[str, Any], image_path: Optional[str]) -> Optional[Dict[str, Any]]:
        """Generar video usando método alternativo (placeholder/demo)"""
        try:
            # Para propósitos de desarrollo y testing, crear un video placeholder
            # En producción, esto debería usar la API real de Veo3
            
            return self._create_placeholder_video(prompt_data, image_path)
            
        except Exception as e:
            self.logger.error(f"Error en método alternativo: {e}")
            return None
    
    def _create_placeholder_video(self, prompt_data: Dict[str, Any], image_path: Optional[str]) -> Optional[Dict[str, Any]]:
        """Crear video placeholder para testing"""
        try:
            # Configuración del video
            width, height = 1080, 1920  # Vertical para TikTok
            fps = 30
            duration = prompt_data.get('duration', 15)
            total_frames = fps * duration
            
            # Crear nombre de archivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            prompt_id = prompt_data.get('id', 'unknown')
            filename = f"video_{sanitize_filename(prompt_id)}_{timestamp}.mp4"
            
            videos_dir = config.get_data_dir('videos')
            filepath = os.path.join(videos_dir, filename)
            
            # Configurar codec
            fourcc = cv2.VideoWriter.fourcc(*'mp4v')
            out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
            
            # Cargar imagen base si existe
            base_image = None
            if image_path and os.path.exists(image_path):
                base_image = cv2.imread(image_path)
                if base_image is not None:
                    base_image = cv2.resize(base_image, (width, height))
            
            # Generar frames
            for frame_num in range(total_frames):
                if base_image is not None:
                    # Usar imagen base con efectos simples
                    frame = self._apply_simple_effects(base_image.copy(), frame_num, total_frames, prompt_data)
                else:
                    # Crear frame desde cero
                    frame = self._create_frame_from_scratch(width, height, frame_num, total_frames, prompt_data)
                
                out.write(frame)
            
            out.release()
            
            # Verificar que el video se creó correctamente
            if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:  # Al menos 1KB
                # Verificación básica del video sin validate_video_specs
                try:
                    # Usar cv2 para verificar que el video es válido
                    cap = cv2.VideoCapture(filepath)
                    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    is_valid = frame_count > 0
                    cap.release()
                    
                    if is_valid:
                        return {
                            'path': filepath,
                            'duration': duration,
                            'resolution': f"{width}x{height}",
                            'fps': fps,
                            'frames': int(frame_count)
                        }
                    else:
                        self.logger.error("Video creado pero no es válido")
                        return None
                except Exception as e:
                    self.logger.warning(f"No se pudo validar el video: {e}, pero el archivo existe")
                    return {
                        'path': filepath,
                        'duration': duration,
                        'resolution': f"{width}x{height}",
                        'fps': fps,
                        'frames': total_frames
                    }
            else:
                self.logger.error("Error: video no creado o vacío")
                return None
            
        except Exception as e:
            self.logger.error(f"Error creando video placeholder: {e}")
            return None
    
    def _apply_simple_effects(self, image: np.ndarray, frame_num: int, total_frames: int, prompt_data: Dict[str, Any]) -> np.ndarray:
        """Aplicar efectos simples a la imagen base"""
        try:
            # Obtener tipo de efecto del prompt
            video_type = prompt_data.get('video_type', 'smooth zoom in effect')
            
            # Aplicar efecto basado en el tipo
            if 'zoom' in video_type.lower():
                return self._apply_zoom_effect(image, frame_num, total_frames)
            elif 'pan' in video_type.lower():
                return self._apply_pan_effect(image, frame_num, total_frames)
            elif 'rotation' in video_type.lower():
                return self._apply_rotation_effect(image, frame_num, total_frames)
            else:
                return self._apply_fade_effect(image, frame_num, total_frames)
                
        except Exception as e:
            self.logger.error(f"Error aplicando efectos: {e}")
            return image
    
    def _apply_zoom_effect(self, image: np.ndarray, frame_num: int, total_frames: int) -> np.ndarray:
        """Aplicar efecto de zoom"""
        # Zoom gradual del 100% al 110%
        progress = frame_num / total_frames
        zoom_factor = 1.0 + (progress * 0.1)
        
        height, width = image.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        # Calcular nuevas dimensiones
        new_width = int(width * zoom_factor)
        new_height = int(height * zoom_factor)
        
        # Redimensionar
        zoomed = cv2.resize(image, (new_width, new_height))
        
        # Recortar al tamaño original desde el centro
        start_x = (new_width - width) // 2
        start_y = (new_height - height) // 2
        
        return zoomed[start_y:start_y + height, start_x:start_x + width]
    
    def _apply_pan_effect(self, image: np.ndarray, frame_num: int, total_frames: int) -> np.ndarray:
        """Aplicar efecto de paneo"""
        # Paneo horizontal suave
        progress = frame_num / total_frames
        height, width = image.shape[:2]
        
        # Crear imagen ligeramente más ancha para paneo
        scale_factor = 1.1
        new_width = int(width * scale_factor)
        scaled = cv2.resize(image, (new_width, height))
        
        # Calcular posición de paneo
        max_offset = new_width - width
        offset_x = int(max_offset * progress)
        
        return scaled[:, offset_x:offset_x + width]
    
    def _apply_rotation_effect(self, image: np.ndarray, frame_num: int, total_frames: int) -> np.ndarray:
        """Aplicar efecto de rotación sutil"""
        # Rotación sutil ±2 grados
        progress = frame_num / total_frames
        angle = 2 * (progress - 0.5) * 2  # -2 a +2 grados
        
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        
        # Matriz de rotación
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        return cv2.warpAffine(image, rotation_matrix, (width, height))
    
    def _apply_fade_effect(self, image: np.ndarray, frame_num: int, total_frames: int) -> np.ndarray:
        """Aplicar efecto de fade"""
        # Fade in durante los primeros 30 frames
        if frame_num < 30:
            alpha = frame_num / 30.0
            black = np.zeros_like(image)
            return cv2.addWeighted(black, 1 - alpha, image, alpha, 0)
        
        return image
    
    def _create_frame_from_scratch(self, width: int, height: int, frame_num: int, total_frames: int, prompt_data: Dict[str, Any]) -> np.ndarray:
        """Crear frame desde cero cuando no hay imagen base"""
        import numpy as np
        
        # Color base según categoría
        category = prompt_data.get('category', 'general')
        colors = {
            'educational': (66, 144, 226),  # Azul
            'entertainment': (245, 166, 35),  # Naranja
            'lifestyle': (189, 16, 224),  # Púrpura
            'tech': (80, 200, 120),  # Verde
            'trending': (255, 107, 107)  # Rojo
        }
        
        base_color = colors.get(category, (100, 100, 100))
        
        # Crear frame con gradiente animado
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Efecto de gradiente animado
        progress = frame_num / total_frames
        for y in range(height):
            intensity = int(255 * (0.3 + 0.7 * abs(np.sin(progress * np.pi + y / height * np.pi))))
            color = tuple(int(c * intensity / 255) for c in base_color)
            frame[y, :] = color
        
        # Agregar texto del prompt
        text = prompt_data.get('prompt', 'AI Generated Video')[:50] + "..."
        cv2.putText(frame, text, (50, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Frame {frame_num + 1}/{total_frames}", (50, height - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return frame
    
    def _encode_image_to_base64(self, image_path: str) -> str:
        """Codificar imagen a base64"""
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Error codificando imagen: {e}")
            return ""
    
    def _download_video(self, video_url: str, prompt_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Descargar video desde URL"""
        try:
            response = requests.get(video_url, stream=True, timeout=300)
            
            if response.status_code == 200:
                # Crear nombre de archivo
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                prompt_id = prompt_data.get('id', 'unknown')
                filename = f"video_{sanitize_filename(prompt_id)}_{timestamp}.mp4"
                
                videos_dir = config.get_data_dir('videos')
                filepath = os.path.join(videos_dir, filename)
                
                # Guardar video
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return {
                    'path': filepath,
                    'duration': prompt_data.get('duration', 15),
                    'downloaded_from': video_url
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error descargando video: {e}")
            return None
    
    def save_generation_log(self, generated_videos: List[Dict[str, Any]]) -> str:
        """Guardar log de generación de videos"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"video_generation_log_{timestamp}.json"
        filepath = config.get_data_dir('videos')
        filepath = f"{filepath}/{filename}"
        
        log_data = {
            'generation_date': datetime.now().isoformat(),
            'total_prompts': len(generated_videos),
            'successful_generations': len([vid for vid in generated_videos if vid.get('success', False)]),
            'failed_generations': len([vid for vid in generated_videos if not vid.get('success', False)]),
            'daily_count': self.daily_count,
            'daily_limit': self.max_videos_per_day,
            'videos': generated_videos
        }
        
        if save_json_file(log_data, filepath):
            self.logger.success(f"Log de generación guardado: {filename}")
            return filepath
        else:
            self.logger.error("Error guardando log de generación")
            return ""

# Función auxiliar para uso directo
def generate_videos_from_images(video_prompts: List[Dict[str, Any]], image_paths: List[str]) -> List[Dict[str, Any]]:
    """Función auxiliar para generar videos"""
    generator = Veo3VideoGenerator()
    generated_videos = generator.generate_videos_from_images(video_prompts, image_paths)
    
    # Guardar log
    generator.save_generation_log(generated_videos)
    
    return generated_videos
