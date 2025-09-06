import os
import base64
import requests
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from PIL import Image
import io
from google import genai
from google.genai import types

from ..utils.logger import get_logger
from ..utils.config import config
from ..utils.helpers import save_json_file, sanitize_filename

class GeminiImageGenerator:
    """Generador de imágenes usando la API de Gemini 2.0 Flash"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.api_key = config.gemini_api_key
        self.model_name = getattr(config, 'gemini_model', 'gemini-2.0-flash-preview-image-generation')
        
        if not self.api_key:
            self.logger.error("API key de Gemini no configurada")
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
        
        # Inicializar cliente de Gemini
        self.client = genai.Client(api_key=self.api_key)
    
    def generate_images_from_prompts(self, prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generar imágenes a partir de prompts"""
        self.logger.info(f"Generando {len(prompts)} imágenes con Gemini")
        
        generated_images = []
        
        for i, prompt_data in enumerate(prompts):
            try:
                self.logger.info(f"Generando imagen {i+1}/{len(prompts)}")
                
                # Generar imagen
                image_data = self._generate_single_image(prompt_data)
                
                if image_data:
                    # Guardar imagen
                    image_path = self._save_image(image_data, prompt_data, i)
                    
                    if image_path:
                        generated_images.append({
                            'prompt_id': prompt_data['id'],
                            'image_path': image_path,
                            'prompt_text': prompt_data['prompt'],
                            'generated_at': datetime.now().isoformat(),
                            'success': True
                        })
                        self.logger.success(f"Imagen {i+1} generada: {os.path.basename(image_path)}")
                    else:
                        self.logger.error(f"Error guardando imagen {i+1}")
                        generated_images.append({
                            'prompt_id': prompt_data['id'],
                            'error': 'Failed to save image',
                            'success': False
                        })
                else:
                    self.logger.error(f"Error generando imagen {i+1}")
                    generated_images.append({
                        'prompt_id': prompt_data['id'],
                        'error': 'Failed to generate image',
                        'success': False
                    })
                
                # Delay entre generaciones para evitar rate limiting
                if i < len(prompts) - 1:  # No hacer delay después de la última imagen
                    time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"Error procesando prompt {i+1}: {e}")
                generated_images.append({
                    'prompt_id': prompt_data['id'],
                    'error': str(e),
                    'success': False
                })
        
        successful_images = [img for img in generated_images if img.get('success', False)]
        self.logger.info(f"Generación completada: {len(successful_images)}/{len(prompts)} imágenes exitosas")
        
        return generated_images
    
    def _generate_single_image(self, prompt_data: Dict[str, Any]) -> Optional[bytes]:
        """Generar una imagen individual usando Gemini 2.0 Flash"""
        try:
            prompt = prompt_data.get('prompt', '')
            self.logger.info(f"Generando imagen con prompt: {prompt[:100]}...")
            
            # Optimizar prompt para TikTok
            from ..utils.gemini_utils import optimize_prompt_for_tiktok
            optimized_prompt = optimize_prompt_for_tiktok(prompt, "image")
            
            # Usar el modelo de generación de imágenes de Gemini 2.0 Flash
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=optimized_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )
            
            self.logger.debug(f"Respuesta de Gemini: {response}")
            
            # Extraer imagen de la respuesta
            if response and response.candidates:
                candidate = response.candidates[0]
                if candidate and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                    for part in candidate.content.parts:
                        # Buscar parte con imagen
                        if (hasattr(part, 'inline_data') and 
                            part.inline_data is not None and 
                            hasattr(part.inline_data, 'data') and
                            part.inline_data.data is not None):
                            
                            # Obtener datos de imagen
                            image_data = part.inline_data.data
                            
                            # Convertir a imagen PIL para procesamiento
                            image = Image.open(io.BytesIO(image_data))
                            
                            # Optimizar para TikTok (9:16 ratio)
                            image = self._optimize_for_tiktok(image)
                            
                            # Convertir de vuelta a bytes
                            img_byte_arr = io.BytesIO()
                            image.save(img_byte_arr, format='JPEG', quality=95)
                            
                            self.logger.success("Imagen generada exitosamente con Gemini 2.0 Flash")
                            return img_byte_arr.getvalue()
            
            self.logger.warning("No se encontró imagen en la respuesta de Gemini")
            # Fallback a placeholder si no hay imagen
            return self._create_placeholder_image(prompt_data)
            
        except Exception as e:
            self.logger.error(f"Error generando imagen con Gemini: {e}")
            # Fallback a método placeholder
            return self._create_placeholder_image(prompt_data)
    
    def _optimize_for_tiktok(self, image: Image.Image) -> Image.Image:
        """Optimizar imagen para formato TikTok (9:16)"""
        try:
            # TikTok recomienda 1080x1920 (9:16)
            target_width, target_height = 1080, 1920
            
            # Calcular ratios
            img_ratio = image.width / image.height
            target_ratio = target_width / target_height
            
            if img_ratio > target_ratio:
                # Imagen más ancha, ajustar por altura
                new_height = target_height
                new_width = int(target_height * img_ratio)
            else:
                # Imagen más alta, ajustar por ancho
                new_width = target_width
                new_height = int(target_width / img_ratio)
            
            # Redimensionar manteniendo calidad
            image_resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crear imagen final con fondo negro si es necesario
            if new_width != target_width or new_height != target_height:
                final_image = Image.new('RGB', (target_width, target_height), (0, 0, 0))
                
                # Centrar imagen
                x = (target_width - new_width) // 2
                y = (target_height - new_height) // 2
                final_image.paste(image_resized, (x, y))
                
                return final_image
            else:
                return image_resized
                
        except Exception as e:
            self.logger.error(f"Error optimizando imagen: {e}")
            return image
    
    def _create_placeholder_image(self, prompt_data: Dict[str, Any]) -> Optional[bytes]:
        """Crear imagen placeholder para testing"""
        try:
            # Crear imagen simple con el prompt como texto
            from PIL import Image, ImageDraw, ImageFont
            
            # Crear imagen vertical para TikTok (9:16)
            width, height = 1080, 1920
            
            # Color de fondo basado en categoría
            bg_colors = {
                'educational': '#4A90E2',
                'entertainment': '#F5A623',
                'lifestyle': '#BD10E0',
                'tech': '#50C878',
                'trending': '#FF6B6B'
            }
            
            category = prompt_data.get('category', 'trending')
            bg_color = bg_colors.get(category, '#4A90E2')
            
            # Crear imagen
            image = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(image)
            
            # Agregar texto del prompt (simplificado)
            prompt_text = prompt_data.get('prompt', 'AI Generated Image')
            # Tomar solo las primeras palabras para que quepa
            words = prompt_text.split()[:10]
            display_text = ' '.join(words)
            
            # Intentar usar fuente del sistema, si no usar fuente por defecto
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            # Agregar texto centrado
            bbox = draw.textbbox((0, 0), display_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            draw.text((x, y), display_text, fill='white', font=font)
            
            # Agregar etiqueta "AI Generated"
            try:
                small_font = ImageFont.truetype("arial.ttf", 40)
            except:
                small_font = ImageFont.load_default()
            
            draw.text((50, height - 100), "AI Generated Content", fill='white', font=small_font)
            draw.text((50, height - 150), f"Category: {category}", fill='white', font=small_font)
            
            # Convertir a bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=95)
            return img_byte_arr.getvalue()
            
        except Exception as e:
            self.logger.error(f"Error creando imagen placeholder: {e}")
            return None
    
    def _generate_with_stable_diffusion_free(self, prompt_data: Dict[str, Any]) -> Optional[bytes]:
        """Generar imagen usando Stable Diffusion gratuito (implementación futura)"""
        # Ejemplo de integración con un servicio gratuito de Stable Diffusion
        # Podrías usar servicios como:
        # - Hugging Face Inference API (gratuito con límites)
        # - Replicate (con tier gratuito)
        # - RunPod (con créditos gratuitos)
        
        try:
            # Ejemplo con Hugging Face (requiere token gratuito)
            # API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
            # headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            
            # payload = {
            #     "inputs": prompt_data['prompt'],
            #     "parameters": {
            #         "num_inference_steps": 30,
            #         "guidance_scale": 7.5,
            #         "width": 1080,
            #         "height": 1920
            #     }
            # }
            
            # response = requests.post(API_URL, headers=headers, json=payload)
            # if response.status_code == 200:
            #     return response.content
            
            # Por ahora, devolver None para usar placeholder
            return None
            
        except Exception as e:
            self.logger.error(f"Error con Stable Diffusion: {e}")
            return None
    
    def _save_image(self, image_data: bytes, prompt_data: Dict[str, Any], index: int) -> Optional[str]:
        """Guardar imagen generada"""
        try:
            # Crear nombre de archivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            category = prompt_data.get('category', 'general')
            safe_category = sanitize_filename(category)
            filename = f"image_{safe_category}_{timestamp}_{index+1}.jpg"
            
            # Ruta completa
            images_dir = config.get_data_dir('images')
            filepath = os.path.join(images_dir, filename)
            
            # Guardar archivo
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            # Verificar que se guardó correctamente
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                return filepath
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error guardando imagen: {e}")
            return None
    
    def optimize_image_for_tiktok(self, image_path: str) -> bool:
        """Optimizar imagen para TikTok (9:16 ratio, calidad adecuada)"""
        try:
            with Image.open(image_path) as img:
                # TikTok recomienda 1080x1920 (9:16)
                target_width, target_height = 1080, 1920
                
                # Redimensionar manteniendo aspecto
                img_ratio = img.width / img.height
                target_ratio = target_width / target_height
                
                if img_ratio > target_ratio:
                    # Imagen más ancha, ajustar por altura
                    new_height = target_height
                    new_width = int(target_height * img_ratio)
                else:
                    # Imagen más alta, ajustar por ancho
                    new_width = target_width
                    new_height = int(target_width / img_ratio)
                
                # Redimensionar
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Crear imagen final con fondo si es necesario
                if new_width != target_width or new_height != target_height:
                    final_img = Image.new('RGB', (target_width, target_height), (0, 0, 0))
                    
                    # Centrar imagen
                    x = (target_width - new_width) // 2
                    y = (target_height - new_height) // 2
                    final_img.paste(img_resized, (x, y))
                else:
                    final_img = img_resized
                
                # Guardar imagen optimizada
                final_img.save(image_path, 'JPEG', quality=95, optimize=True)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error optimizando imagen: {e}")
            return False
    
    def save_generation_log(self, generated_images: List[Dict[str, Any]]) -> str:
        """Guardar log de generación de imágenes"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"image_generation_log_{timestamp}.json"
        filepath = config.get_data_dir('images')
        filepath = f"{filepath}/{filename}"
        
        log_data = {
            'generation_date': datetime.now().isoformat(),
            'total_prompts': len(generated_images),
            'successful_generations': len([img for img in generated_images if img.get('success', False)]),
            'failed_generations': len([img for img in generated_images if not img.get('success', False)]),
            'images': generated_images
        }
        
        if save_json_file(log_data, filepath):
            self.logger.success(f"Log de generación guardado: {filename}")
            return filepath
        else:
            self.logger.error("Error guardando log de generación")
            return ""

# Función auxiliar para uso directo
def generate_images_from_prompts(prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Función auxiliar para generar imágenes"""
    generator = GeminiImageGenerator()
    generated_images = generator.generate_images_from_prompts(prompts)
    
    # Optimizar imágenes para TikTok
    for img_data in generated_images:
        if img_data.get('success') and img_data.get('image_path'):
            generator.optimize_image_for_tiktok(img_data['image_path'])
    
    # Guardar log
    generator.save_generation_log(generated_images)
    
    return generated_images
