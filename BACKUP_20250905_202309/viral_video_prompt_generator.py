# -*- coding: utf-8 -*-
"""
🎬 GENERADOR DE PROMPTS VIRALES PROFESIONALES
Sistema avanzado para crear prompts de video optimizados para viralización en TikTok/Reels
"""

import json
import random
import re
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
import os

class ViralVideoPromptGenerator:
    """Generador profesional de prompts virales para videos ASMR/Satisfying"""
    
    def __init__(self):
        # 🎯 Elementos virales core basados en análisis de TikTok 2024-2025
        self.viral_hooks = {
            "asmr": [
                "Video ASMR hipnótico que desbloquea relajación instantánea",
                "Contenido ASMR adictivo con triggers perfectos",
                "Experiencia ASMR inmersiva de nivel profesional",
                "Video ASMR terapéutico con sonidos envolventes",
                "Momento ASMR ultra satisfying que genera tingles"
            ],
            "satisfying": [
                "Video ultra satisfying que no puedes dejar de ver",
                "Contenido perfectamente satisfying con timing hipnótico",
                "Momento satisfying orgásmico visualmente perfecto",
                "Video satisfying extremadamente adictivo",
                "Experiencia satisfying que relaja instantáneamente"
            ],
            "aesthetic": [
                "Video aesthetic dreamcore con vibes celestiales",
                "Contenido aesthetic pastel con energía kawaii",
                "Momento aesthetic ethereal ultra profesional",
                "Video aesthetic cottagecore perfectamente curado",
                "Experiencia aesthetic liminal space hipnótica"
            ]
        }
        
        # 🎨 Especificaciones técnicas profesionales
        self.technical_specs = {
            "cinematography": [
                "cinematografía profesional con movimientos fluidos de cámara",
                "shots macro ultra detallados con profundidad de campo perfecta",
                "ángulos dinámicos con transiciones seamless",
                "composición visual estudiada siguiendo regla de tercios",
                "iluminación cinematográfica con contraste perfecto"
            ],
            "motion": [
                "movimientos hipnóticos en slow motion a 120fps",
                "animaciones fluidas con physics realistas",
                "transformaciones graduales perfectamente timed",
                "movimientos pendulares rítmicos y meditativos",
                "secuencias de movimiento orgánico y natural"
            ],
            "visual_fx": [
                "efectos visuales sutiles que amplifican la experiencia",
                "partículas flotantes con física realista",
                "reflejos y refracciones hiperrealistas",
                "transiciones de color smoothly blended",
                "micro-animaciones que crean depth visual"
            ]
        }
        
        # 🎵 Audio design profesional
        self.audio_design = {
            "asmr_triggers": [
                "sonidos binaural 3D espacialmente diseñados",
                "frecuencias específicas que activan respuesta ASMR",
                "capas de audio minimalistas perfectamente balanceadas",
                "texturas sonoras que inducen relajación profunda",
                "triggers auditivos calibrados para máximo tingles"
            ],
            "satisfying_sounds": [
                "sonidos crujientes ultra definidos en alta fidelidad",
                "audio táctil que simula sensaciones reales",
                "sonidos de liquidez con viscosidad perfecta",
                "frecuencias que activan satisfacción neural",
                "foley design hiperrealista y envolvente"
            ]
        }
        
        # 🌈 Paletas de color virales 2025
        self.color_palettes = {
            "dreamy_pastels": ["rosa cuarzo suave", "lavanda etéreo", "mint fresco", "durazno cremoso"],
            "neon_vibes": ["fucsia eléctrico", "cyan vibrante", "verde neón", "violeta intenso"],
            "earth_tones": ["terracota cálido", "sage profundo", "caramelo dorado", "marfil cremoso"],
            "kawaii_core": ["rosa sakura", "azul cielo", "amarillo mantequilla", "blanco perla"],
            "cosmic_dreams": ["púrpura galáctico", "azul nebulosa", "dorado estelar", "plateado lunar"]
        }
        
        # 🔥 Elementos de engagement TikTok
        self.engagement_elements = [
            "diseñado para generar comentarios obsesivos",
            "optimizado para shares compulsivos",
            "calibrado para rewatching infinito",
            "estructurado para máximo retention rate",
            "engineered para algoritmo viral de TikTok"
        ]
        
        # 🏷️ Trending tags y conceptos
        self.trending_concepts = {
            "2025_trends": [
                "cottagecore industrial", "dark academia aesthetic", "liminal space vibes",
                "goblincore energy", "fairycore elements", "vintage futurism"
            ],
            "seasonal": [
                "autumn cozy vibes", "winter wonderland magic", "spring renewal energy",
                "summer golden hour", "back to school aesthetic"
            ],
            "micro_trends": [
                "texture play", "color gradient therapy", "miniature worlds",
                "food art fusion", "nature macro", "crystal healing vibes"
            ]
        }

    def generate_professional_prompt(
        self, 
        base_image_prompt: str, 
        viral_category: str = "asmr",
        style_preference: str = "dreamy_pastels",
        complexity_level: str = "professional",
        image_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Genera un prompt profesional optimizado para viralización
        
        Args:
            base_image_prompt: Prompt original de la imagen
            viral_category: "asmr", "satisfying", "aesthetic"
            style_preference: Paleta de colores/estilo
            complexity_level: "simple", "professional", "cinematic"
            image_context: Contexto analizado de la imagen (opcional)
        """
        
        # 1. 🎬 Hook viral principal (ajustado por contexto de imagen si está disponible)
        if image_context and image_context.get('viral_context', {}).get('category'):
            detected_category = image_context['viral_context']['category']
            # Mapear categorías detectadas a nuestras categorías
            category_mapping = {
                'motivacional': 'aesthetic',
                'educativo': 'satisfying',
                'humor': 'satisfying',
                'lifestyle': 'aesthetic',
                'comida': 'asmr',
                'belleza': 'aesthetic'
            }
            viral_category = category_mapping.get(detected_category, viral_category)
        
        hook = random.choice(self.viral_hooks.get(viral_category, self.viral_hooks["asmr"]))
        
        # 2. 🎨 Extraer elementos clave (combinar prompt original y análisis de imagen)
        key_elements = self._extract_key_elements(base_image_prompt)
        
        # Si tenemos contexto de imagen, enriquecer elementos clave
        additional_elements = []
        if image_context:
            image_analysis = image_context.get('image_analysis', {})
            if image_analysis.get('key_elements'):
                additional_elements.extend(image_analysis['key_elements'])
            
            # Agregar elementos de movimiento detectados
            if image_analysis.get('movement_potential'):
                additional_elements.extend([f"movimiento de {elem}" for elem in image_analysis['movement_potential']])
            
            # Integrar elementos adicionales en el diccionario
            if additional_elements:
                key_elements["image_context_elements"] = ", ".join(additional_elements)
        
        # 3. 🎥 Especificaciones técnicas según complejidad
        technical_specs = self._get_technical_specs(complexity_level)
        
        # 4. 🎵 Audio design matching
        audio_specs = self._get_audio_specs(viral_category)
        
        # 5. 🌈 Paleta de colores (priorizar colores detectados en imagen si están disponibles)
        colors = self.color_palettes.get(style_preference, self.color_palettes["dreamy_pastels"])
        
        if image_context and image_context.get('image_analysis', {}).get('dominant_colors'):
            detected_colors = image_context['image_analysis']['dominant_colors']
            # Integrar colores detectados en la paleta
            colors = f"Paleta principal: {', '.join(detected_colors[:3])}, complementada con {colors}"
        color_description = f"paleta de colores {', '.join(colors[:3])}"
        
        # 6. 🔥 Elementos de engagement
        engagement = random.choice(self.engagement_elements)
        
        # 7. 📱 Trending concepts
        trending = random.choice(self.trending_concepts["2025_trends"])
        
        # 8. 🎯 Construir prompt profesional
        professional_prompt = f"""
{hook} de {key_elements['main_subject']}.

CONCEPTO VISUAL:
{key_elements['scene_description']} con {color_description}, 
incorporando elementos de {trending} y {key_elements['aesthetic_style']}.

ESPECIFICACIONES TÉCNICAS:
- {technical_specs['cinematography']}
- {technical_specs['motion']}
- {technical_specs['visual_fx']}

DISEÑO DE AUDIO:
- {audio_specs['primary']}
- {audio_specs['secondary']}
- Masterizado para auriculares y altavoces móviles

ELEMENTOS VIRALES:
- {engagement}
- Optimizado para formato vertical 9:16
- Duración ideal 15-30 segundos con loop perfecto
- Timing calculado para máximo dopamine hit

ESTILO VISUAL:
{key_elements['visual_style']} con acabado profesional de estudio,
iluminación cinematográfica y post-producción premium.

OBJETIVO: Crear contenido viral que genere máximo engagement, 
shares orgánicos y retention rate superior al 85% en los primeros 3 segundos.
        """.strip()
        
        # 9. 📊 Metadata para análisis
        metadata = {
            "viral_category": viral_category,
            "style_preference": style_preference,
            "complexity_level": complexity_level,
            "predicted_engagement": self._calculate_viral_score(professional_prompt),
            "trending_elements": [trending],
            "target_demographics": self._get_target_demographics(viral_category),
            "optimal_posting_time": self._get_optimal_posting_time(),
            "hashtag_strategy": self._generate_hashtag_strategy(key_elements, viral_category)
        }
        
        return {
            "prompt": professional_prompt,
            "metadata": metadata,
            "original_prompt": base_image_prompt,
            "generation_timestamp": datetime.now().isoformat()
        }

    def _extract_key_elements(self, prompt: str) -> Dict[str, str]:
        """Extrae elementos clave del prompt original usando NLP básico"""
        
        # Sujetos principales comunes
        subjects = {
            "capibara": "capibaras kawaii ultra adorables",
            "gelatina": "gelatina cristalina hipnótica",
            "acuario": "ecosistema acuático dreamlike",
            "fruta": "frutas tropicales vibrantes", 
            "flores": "flores ethereal perfectas",
            "cristal": "cristales holográficos mágicos"
        }
        
        # Detectar sujeto principal
        main_subject = "elementos visuales cautivadores"
        for key, value in subjects.items():
            if key.lower() in prompt.lower():
                main_subject = value
                break
        
        # Extraer estilo visual
        style_indicators = {
            "hiperrealista": "renderizado hiperrealista cinematográfico",
            "kawaii": "estética kawaii profesional",
            "neon": "visual cyberpunk con neones vibrantes",
            "pastel": "aesthetic pastel dreamcore",
            "macro": "fotografía macro ultra detallada"
        }
        
        visual_style = "estilo visual premium"
        for indicator, style in style_indicators.items():
            if indicator.lower() in prompt.lower():
                visual_style = style
                break
        
        # Describir escena
        scene_description = "escena visualmente impactante"
        if "acuario" in prompt.lower():
            scene_description = "ambiente acuático sereno con movimiento fluido"
        elif "capibara" in prompt.lower():
            scene_description = "momento tierno con lighting perfecto"
        elif "gelatina" in prompt.lower():
            scene_description = "textura translúcida con physics realistas"
        
        return {
            "main_subject": main_subject,
            "scene_description": scene_description,
            "visual_style": visual_style,
            "aesthetic_style": "aesthetic ultra curado"
        }

    def _get_technical_specs(self, complexity: str) -> Dict[str, str]:
        """Selecciona specs técnicas según nivel de complejidad"""
        if complexity == "cinematic":
            return {
                "cinematography": random.choice(self.technical_specs["cinematography"]),
                "motion": random.choice(self.technical_specs["motion"]),
                "visual_fx": random.choice(self.technical_specs["visual_fx"])
            }
        elif complexity == "professional":
            return {
                "cinematography": "cinematografía fluida con movimientos suaves",
                "motion": "movimientos hipnóticos en timing perfecto",
                "visual_fx": "efectos visuales sutiles que amplifican"
            }
        else:  # simple
            return {
                "cinematography": "cámara estable con enfoque perfecto",
                "motion": "movimiento natural y orgánico",
                "visual_fx": "efectos minimalistas elegantes"
            }

    def _get_audio_specs(self, category: str) -> Dict[str, str]:
        """Selecciona especificaciones de audio según categoría viral"""
        if category == "asmr":
            return {
                "primary": random.choice(self.audio_design["asmr_triggers"]),
                "secondary": "ambiente sonoro inmersivo y relajante"
            }
        elif category == "satisfying":
            return {
                "primary": random.choice(self.audio_design["satisfying_sounds"]),
                "secondary": "diseño de audio perfectamente sincronizado"
            }
        else:  # aesthetic
            return {
                "primary": "diseño sonoro ambient ethereal",
                "secondary": "frecuencias que inducen estado contemplativo"
            }

    def _calculate_viral_score(self, prompt: str) -> int:
        """Calcula score de potencial viral basado en elementos del prompt"""
        viral_keywords = [
            "hipnótico", "adictivo", "viral", "profesional", "cinematográfico",
            "ultra", "perfecto", "premium", "inmersivo", "envolvente"
        ]
        
        score = 0
        prompt_lower = prompt.lower()
        
        for keyword in viral_keywords:
            score += prompt_lower.count(keyword) * 10
        
        # Bonus por elementos técnicos
        technical_terms = ["fps", "3d", "binaural", "hiperrealista", "timing"]
        for term in technical_terms:
            if term in prompt_lower:
                score += 15
        
        return min(score, 100)  # Cap at 100

    def _get_target_demographics(self, category: str) -> List[str]:
        """Define demografía target según categoría"""
        demographics = {
            "asmr": ["Gen Z wellness enthusiasts", "Millennials buswork stress", "ASMR community"],
            "satisfying": ["Stress relief seekers", "Procrastination audience", "Anxiety relief community"],
            "aesthetic": ["Art enthusiasts", "Aesthetic collectors", "Cottagecore community"]
        }
        return demographics.get(category, ["General viral audience"])

    def _get_optimal_posting_time(self) -> str:
        """Recomienda horario óptimo basado en algoritmo TikTok"""
        optimal_times = [
            "6:00-9:00 AM (morning scroll)",
            "12:00-3:00 PM (lunch break)",
            "7:00-9:00 PM (prime time)",
            "9:00-12:00 PM (night wind-down)"
        ]
        return random.choice(optimal_times)

    def _generate_hashtag_strategy(self, elements: Dict, category: str) -> List[str]:
        """Genera estrategia de hashtags optimizada"""
        base_tags = {
            "asmr": ["#ASMR", "#ASMRVideo", "#Tingles", "#Relaxing"],
            "satisfying": ["#Satisfying", "#OddlySatisfying", "#SatisfyingVideo"],
            "aesthetic": ["#Aesthetic", "#Vibes", "#Cottagecore", "#DreamCore"]
        }
        
        viral_tags = ["#FYP", "#ForYou", "#Viral", "#TikTokMadeMeBuyIt"]
        trending_tags = ["#September2025", "#BackToSchool", "#AutumnVibes"]
        
        strategy = base_tags.get(category, []) + viral_tags[:2] + trending_tags[:1]
        return strategy[:8]  # Límite óptimo para TikTok

def enhance_existing_prompts(input_file: str, output_file: Optional[str] = None):
    """
    Mejora prompts existentes con el sistema profesional
    """
    if not output_file:
        output_file = input_file.replace('.json', '_enhanced.json')
    
    generator = ViralVideoPromptGenerator()
    
    # Cargar prompts existentes
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    enhanced_prompts = []
    
    for i, original_prompt in enumerate(data.get("prompts", [])):
        print(f"🎬 Mejorando prompt {i+1}/{len(data['prompts'])}...")
        
        # Generar versión profesional
        enhanced = generator.generate_professional_prompt(
            base_image_prompt=original_prompt,
            viral_category=random.choice(["asmr", "satisfying", "aesthetic"]),
            style_preference=random.choice(list(generator.color_palettes.keys())),
            complexity_level="professional"
        )
        
        enhanced_prompts.append(enhanced)
    
    # Guardar resultados
    result = {
        "enhanced_prompts": enhanced_prompts,
        "generation_info": {
            "total_prompts": len(enhanced_prompts),
            "enhancement_date": datetime.now().isoformat(),
            "average_viral_score": sum(p["metadata"]["predicted_engagement"] for p in enhanced_prompts) / len(enhanced_prompts)
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(enhanced_prompts)} prompts mejorados guardados en {output_file}")
    print(f"📊 Score viral promedio: {result['generation_info']['average_viral_score']:.1f}/100")

def main():
    """Función principal - mejora prompts existentes"""
    input_file = "data/analytics/fusion_prompts_auto.json"
    
    if not os.path.exists(input_file):
        print(f"❌ No se encontró {input_file}")
        print("💡 Ejecuta primero el generador de prompts de imágenes")
        return
    
    print("🎬 GENERADOR DE PROMPTS VIRALES PROFESIONALES")
    print("=" * 60)
    
    enhance_existing_prompts(input_file)
    
    print("\n🎯 ¡Prompts optimizados para máxima viralización!")
    print("📱 Usar con Veo 3 para resultados profesionales")

if __name__ == "__main__":
    main()
