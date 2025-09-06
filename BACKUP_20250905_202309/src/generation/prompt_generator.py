import json
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests

from ..utils.logger import get_logger
from ..utils.config import config
from ..utils.helpers import save_json_file, clean_text

class PromptGenerator:
    """Generador de prompts para imágenes y videos basado en análisis de tendencias"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.base_image_styles = [
            "photorealistic",
            "cinematic",
            "vibrant colors",
            "high contrast",
            "modern aesthetic",
            "trending style",
            "social media optimized",
            "eye-catching"
        ]
        
        self.content_themes = {
            'educational': [
                "step-by-step tutorial",
                "informative graphics",
                "learning concept visualization",
                "educational infographic style"
            ],
            'entertainment': [
                "fun and energetic",
                "playful atmosphere",
                "dynamic composition",
                "engaging visual storytelling"
            ],
            'lifestyle': [
                "aesthetic lifestyle",
                "daily routine vibes",
                "cozy atmosphere",
                "aspirational content"
            ],
            'tech': [
                "futuristic design",
                "clean tech aesthetic",
                "modern digital style",
                "innovative visualization"
            ],
            'trending': [
                "viral content style",
                "trending aesthetic",
                "popular culture reference",
                "current trend adaptation"
            ]
        }
    
    def generate_image_prompts(self, analysis: Dict[str, Any], count: int = 3) -> List[Dict[str, Any]]:
        """Generar prompts para imágenes basados en análisis de tendencias"""
        self.logger.info(f"Generando {count} prompts para imágenes")
        
        prompts = []
        
        # Obtener información del análisis
        top_hashtags = self._extract_top_hashtags(analysis)
        successful_category = self._extract_successful_category(analysis)
        trending_words = self._extract_trending_words(analysis)
        
        for i in range(count):
            prompt_data = self._create_image_prompt(
                top_hashtags, successful_category, trending_words, i
            )
            prompts.append(prompt_data)
        
        self.logger.success(f"Generados {len(prompts)} prompts para imágenes")
        return prompts
    
    def _create_image_prompt(self, hashtags: List[str], category: str, words: List[str], index: int) -> Dict[str, Any]:
        """Crear un prompt individual para imagen"""
        # Seleccionar tema base
        if category and category in self.content_themes:
            theme_options = self.content_themes[category]
        else:
            theme_options = self.content_themes['trending']
        
        base_theme = random.choice(theme_options)
        
        # Seleccionar estilo visual
        visual_style = random.choice(self.base_image_styles)
        
        # Construir prompt principal
        main_elements = []
        
        # Agregar palabras trending si están disponibles
        if words:
            selected_words = random.sample(words, min(2, len(words)))
            main_elements.extend(selected_words)
        
        # Agregar elementos específicos según categoría
        category_elements = self._get_category_elements(category)
        if category_elements:
            main_elements.append(random.choice(category_elements))
        
        # Construir prompt final
        prompt_parts = [
            f"Create a {visual_style} image",
            f"with {base_theme}",
            f"featuring {', '.join(main_elements)}" if main_elements else "",
            "optimized for TikTok vertical format",
            "engaging and eye-catching composition",
            "suitable for social media"
        ]
        
        prompt = ", ".join(filter(None, prompt_parts))
        
        # Prompt de respaldo más simple
        fallback_prompt = f"Create a {visual_style} vertical image for TikTok about {category or 'trending topic'}"
        
        return {
            'id': f"image_prompt_{index + 1}",
            'prompt': prompt,
            'fallback_prompt': fallback_prompt,
            'category': category or 'general',
            'hashtags': hashtags[:5],  # Top 5 hashtags
            'style': visual_style,
            'theme': base_theme,
            'created_at': datetime.now().isoformat()
        }
    
    def _get_category_elements(self, category: str) -> List[str]:
        """Obtener elementos específicos por categoría"""
        elements = {
            'educational': [
                "clear infographic elements",
                "step-by-step visual guide",
                "educational diagrams",
                "learning-focused composition"
            ],
            'entertainment': [
                "dynamic action",
                "expressive characters",
                "vibrant entertainment scene",
                "fun and playful elements"
            ],
            'lifestyle': [
                "aesthetic lifestyle elements",
                "daily life scenario",
                "cozy home environment",
                "stylish personal items"
            ],
            'tech': [
                "modern technology",
                "sleek digital interfaces",
                "futuristic gadgets",
                "innovation showcase"
            ],
            'fashion': [
                "trendy outfit",
                "stylish accessories",
                "fashion-forward look",
                "style inspiration"
            ],
            'food': [
                "delicious food presentation",
                "appetizing cuisine",
                "cooking process",
                "food styling"
            ]
        }
        
        return elements.get(category, [])
    
    def generate_video_prompts(self, image_paths: List[str], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generar prompts para videos basados en las imágenes creadas"""
        self.logger.info(f"Generando prompts de video para {len(image_paths)} imágenes")
        
        video_prompts = []
        
        # Obtener información del análisis
        successful_patterns = self._extract_successful_patterns(analysis)
        trending_movements = self._get_trending_movements()
        
        for i, image_path in enumerate(image_paths):
            video_prompt = self._create_video_prompt(
                image_path, successful_patterns, trending_movements, i
            )
            video_prompts.append(video_prompt)
        
        self.logger.success(f"Generados {len(video_prompts)} prompts para videos")
        return video_prompts
    
    def _create_video_prompt(self, image_path: str, patterns: List[str], movements: List[str], index: int) -> Dict[str, Any]:
        """Crear un prompt individual para video"""
        # Tipos de video para TikTok
        video_types = [
            "smooth zoom in effect",
            "dynamic pan across the image",
            "subtle parallax movement",
            "gentle floating effect",
            "smooth rotation transition",
            "fade in with movement",
            "cinematic reveal effect"
        ]
        
        # Seleccionar tipo de movimiento
        video_type = random.choice(video_types)
        
        # Seleccionar movimiento trending si está disponible
        trending_movement = random.choice(movements) if movements else ""
        
        # Construir prompt de video
        prompt_parts = [
            f"Transform this image into a dynamic {video_type}",
            "maintain the original composition and style",
            "add subtle but engaging motion",
            trending_movement,
            "optimize for TikTok vertical format",
            "15-second duration",
            "smooth and professional animation",
            "keep visual quality high"
        ]
        
        prompt = ", ".join(filter(None, prompt_parts))
        
        # Prompt de respaldo
        fallback_prompt = f"Create a dynamic video with {video_type} from this image, 15 seconds duration"
        
        return {
            'id': f"video_prompt_{index + 1}",
            'prompt': prompt,
            'fallback_prompt': fallback_prompt,
            'image_path': image_path,
            'video_type': video_type,
            'duration': 15,
            'trending_movement': trending_movement,
            'created_at': datetime.now().isoformat()
        }
    
    def _extract_top_hashtags(self, analysis: Dict[str, Any]) -> List[str]:
        """Extraer top hashtags del análisis"""
        try:
            hashtag_analysis = analysis.get('hashtag_analysis', {})
            top_by_engagement = hashtag_analysis.get('top_by_engagement', [])
            
            return [item['hashtag'] for item in top_by_engagement[:10]]
        except:
            return ['#fyp', '#viral', '#trending']
    
    def _extract_successful_category(self, analysis: Dict[str, Any]) -> str:
        """Extraer categoría más exitosa del análisis"""
        try:
            content_patterns = analysis.get('content_patterns', {})
            content_types = content_patterns.get('content_types', {})
            return content_types.get('most_successful_category', 'trending')
        except:
            return 'trending'
    
    def _extract_trending_words(self, analysis: Dict[str, Any]) -> List[str]:
        """Extraer palabras trending del análisis"""
        try:
            content_patterns = analysis.get('content_patterns', {})
            word_frequency = content_patterns.get('word_frequency', [])
            
            return [item['word'] for item in word_frequency[:5]]
        except:
            return ['trending', 'viral', 'amazing', 'new', 'cool']
    
    def _extract_successful_patterns(self, analysis: Dict[str, Any]) -> List[str]:
        """Extraer patrones exitosos del análisis"""
        try:
            content_patterns = analysis.get('content_patterns', {})
            return content_patterns.get('title_patterns', [])
        except:
            return []
    
    def _get_trending_movements(self) -> List[str]:
        """Obtener movimientos trending para videos"""
        # Estos podrían obtenerse de APIs de tendencias o bases de datos actualizadas
        return [
            "popular transition effect",
            "trending camera movement",
            "viral visual style",
            "current motion trend",
            "popular animation style"
        ]
    
    def create_content_plan(self, analysis: Dict[str, Any], video_count: int = 3) -> Dict[str, Any]:
        """Crear plan completo de contenido"""
        self.logger.info(f"Creando plan de contenido para {video_count} videos")
        
        # Generar prompts de imágenes
        image_prompts = self.generate_image_prompts(analysis, video_count)
        
        # Para video prompts, necesitamos las rutas de las imágenes generadas
        # Por ahora, creamos paths placeholder
        placeholder_image_paths = [
            f"image_{i+1}.jpg" for i in range(video_count)
        ]
        
        video_prompts = self.generate_video_prompts(placeholder_image_paths, analysis)
        
        # Generar títulos y descripciones sugeridas
        content_suggestions = self._generate_content_suggestions(analysis, video_count)
        
        plan = {
            'plan_id': f"content_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'video_count': video_count,
            'image_prompts': image_prompts,
            'video_prompts': video_prompts,
            'content_suggestions': content_suggestions,
            'analysis_summary': {
                'top_hashtags': self._extract_top_hashtags(analysis)[:5],
                'successful_category': self._extract_successful_category(analysis),
                'trending_words': self._extract_trending_words(analysis)[:3]
            }
        }
        
        self.save_content_plan(plan)
        
        self.logger.success("Plan de contenido creado exitosamente")
        return plan
    
    def _generate_content_suggestions(self, analysis: Dict[str, Any], count: int) -> List[Dict[str, Any]]:
        """Generar sugerencias de contenido (títulos, descripciones, hashtags)"""
        suggestions = []
        
        top_hashtags = self._extract_top_hashtags(analysis)
        trending_words = self._extract_trending_words(analysis)
        category = self._extract_successful_category(analysis)
        
        for i in range(count):
            # Generar título sugerido
            title_templates = self._get_title_templates(category)
            title_template = random.choice(title_templates)
            
            # Reemplazar placeholders con palabras trending
            title = title_template
            if trending_words:
                for j, word in enumerate(trending_words[:2]):
                    title = title.replace(f"{{{j}}}", word)
            
            # Limpiar título
            title = clean_text(title)
            
            # Seleccionar hashtags
            selected_hashtags = random.sample(
                top_hashtags, min(8, len(top_hashtags))
            ) if top_hashtags else ['#fyp', '#viral', '#trending']
            
            suggestions.append({
                'video_id': f"video_{i+1}",
                'suggested_title': title,
                'hashtags': selected_hashtags,
                'category': category,
                'optimal_posting_time': self._get_optimal_time()
            })
        
        return suggestions
    
    def _get_title_templates(self, category: str) -> List[str]:
        """Obtener templates de títulos por categoría"""
        templates = {
            'educational': [
                "How to {0} in just minutes! 📚",
                "Learn {0} with this simple trick ✨",
                "The {0} hack everyone needs to know 🔥",
                "Master {0} with this easy method 💡"
            ],
            'entertainment': [
                "This {0} will make you laugh 😂",
                "Wait for the {0} part! 🤯",
                "The most {0} thing you'll see today ✨",
                "You won't believe this {0} trick! 😱"
            ],
            'lifestyle': [
                "My daily {0} routine ✨",
                "The {0} aesthetic we all need 💫",
                "Living my best {0} life 🌟",
                "This {0} changed everything for me 💖"
            ],
            'tech': [
                "This {0} app will blow your mind 🤯",
                "The {0} tech hack you need 📱",
                "Future of {0} is here! 🚀",
                "This {0} feature is game-changing ⚡"
            ]
        }
        
        return templates.get(category, [
            "This {0} is amazing! ✨",
            "You need to see this {0} 🔥",
            "The best {0} content 💯",
            "This {0} is going viral! 🚀"
        ])
    
    def _get_optimal_time(self) -> str:
        """Obtener hora óptima para postear"""
        optimal_times = config.get_config('tiktok.upload_schedule', ['09:00', '15:00', '21:00'])
        return random.choice(optimal_times)
    
    def save_content_plan(self, plan: Dict[str, Any]) -> str:
        """Guardar plan de contenido"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"content_plan_{timestamp}.json"
        filepath = config.get_data_dir('prompts')
        filepath = f"{filepath}/{filename}"
        
        if save_json_file(plan, filepath):
            self.logger.success(f"Plan de contenido guardado: {filename}")
            return filepath
        else:
            self.logger.error("Error guardando plan de contenido")
            return ""

# Función auxiliar para uso directo
def create_content_plan(analysis: Dict[str, Any], video_count: int = 3) -> Dict[str, Any]:
    """Función auxiliar para crear plan de contenido"""
    generator = PromptGenerator()
    return generator.create_content_plan(analysis, video_count)
