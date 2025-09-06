"""
Analizador de metadatos de imágenes para generar prompts de video coherentes
Permite extraer la temática y contexto de imágenes existentes para crear
prompts de video profesionales alineados con el contenido visual.
"""

import os
import json
import re
from typing import Dict, List, Any, Optional
from PIL import Image
from datetime import datetime
import base64
from io import BytesIO

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class ImageMetadataAnalyzer:
    """
    Analiza imágenes existentes para extraer metadatos y temáticas
    que pueden ser utilizados para generar prompts de video coherentes
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no configurada")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = 'gemini-2.0-flash-exp'
    
    def analyze_image_for_video_prompt(self, image_path: str) -> Dict[str, Any]:
        """
        Analiza una imagen para extraer metadatos útiles para prompts de video
        
        Args:
            image_path: Ruta a la imagen a analizar
            
        Returns:
            Dict con metadatos extraídos: tema, estilo, colores, mood, etc.
        """
        try:
            # Validar que la imagen existe
            if not os.path.exists(image_path):
                return {"error": f"Imagen no encontrada: {image_path}"}
            
            # Cargar y preparar imagen
            image_data = self._prepare_image_for_analysis(image_path)
            if not image_data:
                return {"error": "No se pudo procesar la imagen"}
            
            # Prompt especializado para análisis de imagen para video
            analysis_prompt = """
Analiza esta imagen para crear metadatos que ayuden a generar un prompt de video viral coherente.

EXTRAE LA SIGUIENTE INFORMACIÓN:

1. TEMA PRINCIPAL: ¿Cuál es el tema/concepto central?
2. ESTILO VISUAL: Describe el estilo artístico (realista, cartoon, minimalista, etc.)
3. COLORES DOMINANTES: Lista los 3-4 colores principales
4. MOOD/AMBIENTE: ¿Qué sensación transmite? (energético, relajante, misterioso, etc.)
5. ELEMENTOS CLAVE: Objetos, personas, textos visibles importantes
6. CATEGORÍA VIRAL: ¿A qué categoría de TikTok pertenece? (motivacional, humor, educativo, lifestyle, etc.)
7. TARGET DEMOGRÁFICO: ¿A quién está dirigido? (jóvenes, adultos, niños, etc.)
8. ELEMENTOS DE MOVIMIENTO: ¿Qué elementos podrían moverse en un video?
9. POTENCIAL VIRAL: ¿Qué elementos podrían hacerlo viral en video?
10. HOOKS VISUALES: ¿Qué llamaría la atención inmediatamente?

RESPONDE EN FORMATO JSON ESTRUCTURADO:
{
  "tema_principal": "descripción del tema",
  "estilo_visual": "descripción del estilo",
  "colores_dominantes": ["color1", "color2", "color3"],
  "mood": "descripción del ambiente",
  "elementos_clave": ["elemento1", "elemento2"],
  "categoria_viral": "categoría principal",
  "target_demografico": ["grupo1", "grupo2"],
  "elementos_movimiento": ["elemento que puede moverse"],
  "potencial_viral": "qué lo haría viral",
  "hooks_visuales": ["hook1", "hook2"],
  "texto_visible": "texto si hay alguno",
  "recomendaciones_video": "sugerencias para el video"
}
"""

            # Enviar a Gemini Vision
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    analysis_prompt,
                    image_data
                ]
            )
            
            if response and response.candidates and response.candidates[0].content:
                content_text = response.candidates[0].content.parts[0].text
                
                # Intentar extraer JSON de la respuesta
                metadata = self._extract_json_from_response(content_text)
                
                if metadata:
                    # Agregar información adicional
                    metadata.update({
                        "image_path": image_path,
                        "analyzed_at": datetime.now().isoformat(),
                        "image_info": self._get_image_info(image_path),
                        "analysis_success": True
                    })
                    return metadata
                else:
                    # Si no se puede extraer JSON, devolver análisis textual
                    return {
                        "analysis_text": content_text,
                        "image_path": image_path,
                        "analyzed_at": datetime.now().isoformat(),
                        "analysis_success": False,
                        "error": "No se pudo extraer JSON estructurado"
                    }
            
            return {"error": "No se recibió respuesta válida del análisis"}
            
        except Exception as e:
            return {
                "error": f"Error analizando imagen: {str(e)}",
                "image_path": image_path,
                "analyzed_at": datetime.now().isoformat(),
                "analysis_success": False
            }
    
    def _prepare_image_for_analysis(self, image_path: str) -> Optional[types.Image]:
        """Prepara imagen para análisis con Gemini Vision"""
        try:
            # Validar formato
            valid_formats = ['.jpg', '.jpeg', '.png', '.webp']
            if not any(image_path.lower().endswith(fmt) for fmt in valid_formats):
                return None
            
            # Leer imagen
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Determinar MIME type
            if image_path.lower().endswith('.png'):
                mime_type = 'image/png'
            elif image_path.lower().endswith('.webp'):
                mime_type = 'image/webp'
            else:
                mime_type = 'image/jpeg'
            
            return types.Image(image_bytes=image_data, mime_type=mime_type)
            
        except Exception as e:
            print(f"Error preparando imagen: {e}")
            return None
    
    def _extract_json_from_response(self, text: str) -> Optional[Dict[str, Any]]:
        """Extrae JSON de la respuesta de texto"""
        try:
            # Buscar JSON en la respuesta
            json_pattern = r'```json\s*(.*?)\s*```'
            json_match = re.search(json_pattern, text, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1)
            else:
                # Buscar JSON directo (sin markdown)
                json_pattern = r'\{.*\}'
                json_match = re.search(json_pattern, text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    return None
            
            # Parsear JSON
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Error extrayendo JSON: {e}")
            return None
    
    def _get_image_info(self, image_path: str) -> Dict[str, Any]:
        """Obtiene información básica de la imagen"""
        try:
            with Image.open(image_path) as img:
                return {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                    "size_bytes": os.path.getsize(image_path),
                    "aspect_ratio": round(img.width / img.height, 2)
                }
        except Exception:
            return {}
    
    def analyze_multiple_images(self, image_paths: List[str]) -> Dict[str, Any]:
        """
        Analiza múltiples imágenes y devuelve metadatos consolidados
        
        Args:
            image_paths: Lista de rutas de imágenes
            
        Returns:
            Dict con análisis de todas las imágenes
        """
        results = {}
        successful_analyses = 0
        
        print(f"🔍 Analizando {len(image_paths)} imágenes para metadatos de video...")
        
        for i, image_path in enumerate(image_paths, 1):
            print(f"   Analizando imagen {i}/{len(image_paths)}: {os.path.basename(image_path)}")
            
            analysis = self.analyze_image_for_video_prompt(image_path)
            results[image_path] = analysis
            
            if analysis.get("analysis_success"):
                successful_analyses += 1
                print(f"   ✅ Análisis exitoso - Tema: {analysis.get('tema_principal', 'N/A')}")
            else:
                print(f"   ❌ Error en análisis: {analysis.get('error', 'Error desconocido')}")
        
        # Crear resumen consolidado
        consolidated_report = {
            "total_images": len(image_paths),
            "successful_analyses": successful_analyses,
            "failed_analyses": len(image_paths) - successful_analyses,
            "analysis_date": datetime.now().isoformat(),
            "images": results
        }
        
        print(f"📊 Análisis completado: {successful_analyses}/{len(image_paths)} exitosos")
        
        return consolidated_report
    
    def get_video_prompt_context(self, image_path: str) -> Dict[str, Any]:
        """
        Obtiene contexto específico para generar prompt de video profesional
        
        Returns:
            Dict con contexto optimizado para el generador de prompts virales
        """
        analysis = self.analyze_image_for_video_prompt(image_path)
        
        if not analysis.get("analysis_success"):
            return {"error": "No se pudo analizar la imagen"}
        
        # Mapear análisis a formato esperado por el generador de prompts
        context = {
            "image_analysis": {
                "main_theme": analysis.get("tema_principal", ""),
                "visual_style": analysis.get("estilo_visual", ""),
                "dominant_colors": analysis.get("colores_dominantes", []),
                "mood": analysis.get("mood", ""),
                "key_elements": analysis.get("elementos_clave", []),
                "visible_text": analysis.get("texto_visible", ""),
                "movement_potential": analysis.get("elementos_movimiento", []),
                "viral_hooks": analysis.get("hooks_visuales", [])
            },
            "viral_context": {
                "category": analysis.get("categoria_viral", "general"),
                "target_demographics": analysis.get("target_demografico", ["general"]),
                "viral_potential": analysis.get("potencial_viral", ""),
                "video_recommendations": analysis.get("recomendaciones_video", "")
            },
            "technical_specs": {
                "source_image": image_path,
                "image_info": analysis.get("image_info", {}),
                "analyzed_at": analysis.get("analyzed_at")
            }
        }
        
        return context

# Funciones auxiliares para uso directo
def analyze_existing_images() -> Dict[str, Any]:
    """
    Analiza todas las imágenes gemini existentes en el directorio actual
    """
    analyzer = ImageMetadataAnalyzer()
    
    # Buscar imágenes generadas por Gemini
    image_patterns = ["data/images/gemini_image_*.png", "data/images/gemini_image_*.jpg", "data/images/gemini_image_*.jpeg"]
    found_images = []
    
    for pattern in image_patterns:
        import glob
        found_images.extend(glob.glob(pattern))
    
    if not found_images:
        return {"error": "No se encontraron imágenes para analizar"}
    
    print(f"📸 Encontradas {len(found_images)} imágenes para analizar")
    return analyzer.analyze_multiple_images(found_images)

def save_image_analysis_report(analysis_data: Dict[str, Any], filename: Optional[str] = None) -> str:
    """Guarda reporte de análisis de imágenes"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_analysis_report_{timestamp}.json"
    
    os.makedirs("data/image_analysis", exist_ok=True)
    filepath = os.path.join("data/image_analysis", filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Reporte guardado: {filepath}")
    return filepath

if __name__ == "__main__":
    # Ejemplo de uso
    print("🔍 ANALIZADOR DE METADATOS DE IMÁGENES PARA VIDEO")
    print("=" * 60)
    
    # Analizar todas las imágenes existentes
    analysis = analyze_existing_images()
    
    if "error" not in analysis:
        # Guardar reporte
        report_path = save_image_analysis_report(analysis)
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN DEL ANÁLISIS:")
        print(f"   Total de imágenes: {analysis['total_images']}")
        print(f"   Análisis exitosos: {analysis['successful_analyses']}")
        print(f"   Errores: {analysis['failed_analyses']}")
        print(f"   Reporte guardado: {report_path}")
        
        # Mostrar algunas temáticas encontradas
        print(f"\n🎭 TEMÁTICAS DETECTADAS:")
        for i, (image_path, data) in enumerate(analysis['images'].items()):
            if data.get('analysis_success') and i < 3:  # Mostrar solo las primeras 3
                print(f"   • {os.path.basename(image_path)}: {data.get('tema_principal', 'N/A')}")
    else:
        print(f"❌ Error: {analysis['error']}")
