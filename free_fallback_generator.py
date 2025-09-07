#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POLLINATIONS.AI FREE FALLBACK GENERATOR
Fallback 100% GRATUITO para generación de imágenes cuando Gemini no está disponible
"""

import os
import requests
import time
import logging
import urllib.parse
from typing import Optional, Dict, Any, List
from pathlib import Path
import hashlib

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PollinationsFallbackGenerator:
    """
    Generador de imágenes usando Pollinations.AI - 100% GRATUITO
    """
    
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt"
        
        # Configuración optimizada para contenido viral ASMR
        self.default_params = {
            "width": 1024,
            "height": 1024,
            "model": "flux",  # Modelo más moderno
            "nologo": True,   # Sin watermark
            "enhance": True,  # Mejora automática
        }
        
        # Enhancers virales para ASMR content
        self.viral_enhancers = [
            "hiperrealista",
            "aesthetic pleasing", 
            "trending on social media",
            "satisfying visual",
            "ASMR friendly",
            "ultra detailed",
            "cinematographic lighting",
            "professional photography"
        ]
    
    def is_available(self) -> bool:
        """
        Verifica si Pollinations.AI está disponible
        """
        try:
            # Test simple de conectividad
            test_url = f"{self.base_url}/test"
            response = requests.get(test_url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"❌ Error verificando Pollinations: {e}")
            return False
    
    def generate_image(
        self, 
        prompt: str, 
        output_path: str,
        width: int = 1024,
        height: int = 1024,
        model: str = "flux"
    ) -> bool:
        """
        Genera una imagen usando Pollinations.AI
        
        Args:
            prompt: Descripción de la imagen a generar
            output_path: Ruta donde guardar la imagen
            width: Ancho de la imagen
            height: Alto de la imagen
            model: Modelo a usar (flux, turbo, etc.)
        
        Returns:
            bool: True si la generación fue exitosa
        """
        try:
            logger.info(f"🎨 Generando imagen con Pollinations: {prompt[:50]}...")
            
            # Optimizar prompt para mejor calidad
            optimized_prompt = self._optimize_prompt(prompt)
            
            # Codificar prompt para URL
            encoded_prompt = urllib.parse.quote(optimized_prompt)
            
            # Construir URL con parámetros
            params = {
                "width": width,
                "height": height,
                "model": model,
                "nologo": "true",
                "enhance": "true"
            }
            
            # URL completa
            url = f"{self.base_url}/{encoded_prompt}"
            
            logger.info(f"🔗 URL generación: {url}")
            
            # Hacer petición con reintentos
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(
                        url, 
                        params=params,
                        timeout=60,  # 60 segundos para generación
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                    )
                    
                    if response.status_code == 200:
                        # Verificar que es una imagen válida
                        content_type = response.headers.get('content-type', '')
                        if 'image' in content_type:
                            return self._save_image(response.content, output_path)
                        else:
                            logger.warning(f"⚠️ Respuesta no es imagen: {content_type}")
                            
                    elif response.status_code == 429:
                        wait_time = (attempt + 1) * 5
                        logger.warning(f"⚠️ Rate limit. Esperando {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                        
                    else:
                        logger.error(f"❌ Error HTTP {response.status_code}: {response.text[:200]}")
                        
                except requests.exceptions.Timeout:
                    logger.warning(f"⚠️ Timeout en intento {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"❌ Error de conexión: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
            
            logger.error("❌ Todos los intentos fallaron")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error inesperado en Pollinations: {e}")
            return False
    
    def _optimize_prompt(self, original_prompt: str) -> str:
        """
        Optimiza el prompt para mejor calidad viral
        """
        # Limpiar prompt
        prompt = original_prompt.strip()
        
        # Agregar enhancers virales (máximo 3 para no saturar)
        selected_enhancers = self.viral_enhancers[:3]
        enhanced_prompt = f"{prompt}, {', '.join(selected_enhancers)}"
        
        # Agregar términos de calidad
        quality_terms = [
            "high quality",
            "detailed",
            "vibrant colors"
        ]
        
        final_prompt = f"{enhanced_prompt}, {', '.join(quality_terms)}"
        
        logger.info(f"📝 Prompt optimizado: {final_prompt[:100]}...")
        return final_prompt
    
    def _save_image(self, image_data: bytes, output_path: str) -> bool:
        """
        Guarda los datos de imagen en archivo
        """
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Guardar imagen
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            # Verificar que el archivo se guardó correctamente
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:  # Al menos 1KB
                file_size = os.path.getsize(output_path)
                logger.info(f"✅ Imagen guardada: {output_path} ({file_size/1024:.1f} KB)")
                return True
            else:
                logger.error(f"❌ Archivo inválido o muy pequeño: {output_path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error guardando imagen: {e}")
            return False
    
    def generate_viral_image(self, prompt: str, output_path: str) -> bool:
        """
        Genera imagen optimizada para contenido viral ASMR
        """
        return self.generate_image(
            prompt=prompt,
            output_path=output_path,
            width=1024,
            height=1024,
            model="flux"  # Mejor modelo para calidad
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Prueba la conexión con Pollinations.AI
        """
        result = {
            "available": False,
            "error": None,
            "test_generation": False
        }
        
        try:
            # Test de disponibilidad
            if not self.is_available():
                result["error"] = "Servicio no disponible"
                return result
            
            # Test de generación
            test_prompt = "A simple red circle"
            test_path = "test_pollinations_fallback.png"
            
            success = self.generate_image(test_prompt, test_path)
            
            if success and os.path.exists(test_path):
                result["available"] = True
                result["test_generation"] = True
                
                # Limpiar archivo de prueba
                try:
                    os.remove(test_path)
                except:
                    pass
            else:
                result["error"] = "Fallo en generación de prueba"
                
        except Exception as e:
            result["error"] = str(e)
        
        return result

class HuggingFaceFallbackGenerator:
    """
    Fallback secundario usando HuggingFace Inference API (también gratuito)
    """
    
    def __init__(self):
        self.api_token = os.getenv('HUGGINGFACE_TOKEN')  # Opcional, mejora limits
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.headers = {}
        
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"
    
    def is_available(self) -> bool:
        """
        Verifica si HuggingFace está disponible
        """
        try:
            response = requests.get(
                "https://huggingface.co/api/models/stabilityai/stable-diffusion-xl-base-1.0",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def generate_image(self, prompt: str, output_path: str) -> bool:
        """
        Genera imagen usando HuggingFace
        """
        try:
            logger.info(f"🤗 Generando con HuggingFace: {prompt[:50]}...")
            
            payload = {"inputs": prompt}
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return self._save_image(response.content, output_path)
            else:
                logger.error(f"❌ HuggingFace error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error HuggingFace: {e}")
            return False
    
    def _save_image(self, image_data: bytes, output_path: str) -> bool:
        """
        Guarda imagen de HuggingFace
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                logger.info(f"✅ Imagen HuggingFace guardada: {output_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error guardando HuggingFace: {e}")
            return False

# Función de conveniencia para uso directo
def generate_image_free_fallback(prompt: str, output_path: str) -> bool:
    """
    Genera imagen usando fallbacks gratuitos en orden de preferencia
    """
    # Fallback 1: Pollinations.AI
    pollinations = PollinationsFallbackGenerator()
    if pollinations.is_available():
        logger.info("🌸 Usando Pollinations.AI fallback")
        success = pollinations.generate_viral_image(prompt, output_path)
        if success:
            return True
    
    # Fallback 2: HuggingFace
    huggingface = HuggingFaceFallbackGenerator()
    if huggingface.is_available():
        logger.info("🤗 Usando HuggingFace fallback")
        success = huggingface.generate_image(prompt, output_path)
        if success:
            return True
    
    logger.error("❌ Todos los fallbacks gratuitos fallaron")
    return False

# Test básico si se ejecuta directamente
if __name__ == "__main__":
    print("🧪 TESTING FALLBACKS GRATUITOS")
    print("=" * 50)
    
    # Test Pollinations
    print("\n🌸 Testing Pollinations.AI...")
    pollinations = PollinationsFallbackGenerator()
    available = pollinations.is_available()
    print(f"✅ Disponible: {available}")
    
    if available:
        test_result = pollinations.test_connection()
        print(f"📊 Test completo: {test_result}")
        
        if test_result.get("available"):
            print("\n🎨 Generando imagen real...")
            success = pollinations.generate_viral_image(
                "A cute cat with rainbow colors, aesthetic ASMR style",
                "test_pollinations_real.png"
            )
            print(f"✅ Generación: {success}")
    
    # Test HuggingFace
    print("\n🤗 Testing HuggingFace...")
    huggingface = HuggingFaceFallbackGenerator()
    hf_available = huggingface.is_available()
    print(f"✅ Disponible: {hf_available}")
    
    print("\n" + "=" * 50)
    print("🎯 Test completado")
