#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 GENERADOR DE DESCRIPCIONES DINÁMICAS ULTRA INTELIGENTE
Analiza el prompt del video y genera descripciones completamente personalizadas
"""

import json
import os
import re
import random
from typing import Dict, List

class DynamicDescriptionGenerator:
    def __init__(self):
        # Elementos virales por categoría
        self.viral_hooks = {
            "asmr": [
                "🔥 ASMR VIRAL que te va a HIPNOTIZAR",
                "😱 NO PUEDES PARAR DE VER ESTO",
                "✨ ASMR que te va a hacer DORMIR en 30 segundos",
                "🤤 ASMR SATISFYING que está ROMPIENDO TikTok",
                "😍 SONIDOS que te van a ENAMORAR",
                "🎧 ASMR PERFECTO para relajarse"
            ],
            "food": [
                "🍽️ FOODTOK VIRAL",
                "😍 COMIDA que se ve IRREAL",
                "🔥 RECETA VIRAL de TikTok",
                "🤤 FOOD PORN que está ROMPIENDO TikTok",
                "😱 TÉCNICA de CHEF PROFESIONAL",
                "🍴 COCINA que parece MAGIA"
            ],
            "general": [
                "🤯 ESTO es lo más VIRAL de TikTok",
                "😱 NO VAS A CREER lo que acabas de ver",
                "✨ CONTENIDO que está ROMPIENDO Internet",
                "🔥 VIRAL que está EXPLOTANDO las redes",
                "😍 EFECTOS que parecen de otro PLANETA",
                "🎬 CONTENIDO ÉPICO que necesitas ver"
            ]
        }
        
        self.engagement_questions = [
            "¿Ya lo habías visto?",
            "¿Te quedaste hasta el final?",
            "¿Funcionó contigo?",
            "¿Se te antojó?",
            "¿Lo probarías?",
            "¿Te relajó?",
            "¿Te sorprendió?",
            "¿Qué opinas?",
            "¿Te gustó el efecto?",
            "¿Quién más se queda pegado viendo esto?"
        ]
        
        self.call_to_actions = [
            "Doble TAP si te gustó ✨",
            "Comenta 'SÍ' si funcionó 👇",
            "Guarda este video para después 📌",
            "Comparte con quien necesite ver esto 🔥",
            "Etiqueta a quien haría esto contigo 👥",
            "Sígueme para contenido así todos los días 📲",
            "Déjamelo en comentarios 💬",
            "Like si te sorprendió ⚡",
            "¡No te pierdas este contenido ÉPICO!"
        ]
        
        # Hashtags dinámicos por contenido
        self.hashtags_base = {
            "asmr": ["#ASMR", "#ASMRTikTok", "#Satisfying", "#Relax", "#ASMRSleep", "#SatisfyingVideo"],
            "food": ["#FoodTok", "#Food", "#Cooking", "#Recipe", "#FoodPorn", "#Chef"],
            "general": ["#Viral", "#Amazing", "#Incredible", "#Content", "#trending", "#ÉPICO"],
            "effects": ["#Effects", "#VFX", "#CGI", "#EditingSkills", "#VisualEffects", "#Digital"],
            "animal": ["#Animals", "#Cute", "#Pet", "#Wildlife", "#AnimalTok", "#Nature"],
            "crystal": ["#Crystal", "#Glass", "#Transparent", "#Aesthetic", "#Art", "#Design"],
            "cyberpunk": ["#Cyberpunk", "#Neon", "#Futuristic", "#SciFi", "#Digital", "#Tech"],
            "capibara": ["#Capybara", "#Animals", "#Cute", "#Pet", "#Wildlife", "#Chill"]
        }

    def normalize_text(self, text: str) -> str:
        """Normaliza el texto para eliminar tildes y caracteres especiales."""
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'ñ': 'n', 'Ñ': 'N'
        }
        for accented_char, base_char in replacements.items():
            text = text.replace(accented_char, base_char)
        return text
        
    def extract_key_elements(self, prompt: str) -> Dict:
        """Extrae elementos clave del prompt para personalización"""
        prompt_lower = prompt.lower()
        
        elements = {
            "subject": [],
            "action": [],
            "style": [],
            "effects": [],
            "materials": [],
            "colors": [],
            "category": "general"
        }
        
        # Detectar sujetos principales
        subjects = {
            "capibara": ["capibara", "capybara"],
            "chef": ["chef", "cocinero"],
            "vegetales": ["vegetales", "vegetables", "verduras"],
            "lima": ["lima", "lime", "citrico"],
            "helado": ["helado", "ice cream", "gelato"],
            "volcán": ["volcán", "volcano", "lava"],
            "waffle": ["waffle", "gofre"]
        }
        
        for key, keywords in subjects.items():
            if any(word in prompt_lower for word in keywords):
                elements["subject"].append(key)
        
        # Detectar acciones
        actions = {
            "cortando": ["cortando", "cutting", "slice", "slicing"],
            "derritiendo": ["derritiendo", "melting", "derretir"],
            "fluyendo": ["fluyendo", "flowing", "flow"],
            "brillando": ["brillando", "glowing", "bright", "shine"],
            "masticando": ["masticando", "chewing", "eating", "morder"]
        }
        
        for key, keywords in actions.items():
            if any(word in prompt_lower for word in keywords):
                elements["action"].append(key)
        
        # Detectar materiales especiales
        materials = {
            "cristal": ["cristal", "crystal", "glass", "vidrio"],
            "chocolate": ["chocolate", "cacao"],
            "neón": ["neón", "neon"],
            "holográfico": ["holográfico", "holographic", "holo"],
            "metálico": ["metálico", "metallic", "metal"]
        }
        
        for key, keywords in materials.items():
            if any(word in prompt_lower for word in keywords):
                elements["materials"].append(key)
        
        # Detectar categoría principal
        if any(word in prompt_lower for word in ['asmr', 'relajante', 'sonidos', 'crujientes', 'satisfying']):
            elements["category"] = "asmr"
        elif any(word in prompt_lower for word in ['food', 'comida', 'chef', 'cocina', 'recipe', 'cooking']):
            elements["category"] = "food"
        
        return elements
    
    def generate_content_description(self, elements: Dict) -> str:
        """Genera descripción del contenido basada en los elementos extraídos"""
        parts = []
        
        # Construir descripción natural del contenido
        if "capibara" in elements["subject"]:
            if "chef" in elements["subject"]:
                parts.append("Capibara chef")
            else:
                parts.append("Capibara gigante")
        
        if "cortando" in elements["action"] and "vegetales" in elements["subject"]:
            if "cristal" in elements["materials"]:
                parts.append("cortando vegetales de cristal")
            else:
                parts.append("cortando vegetales")
        
        if "chocolate" in elements["materials"] and "derritiendo" in elements["action"]:
            parts.append("con chocolate derretido")
        
        if "volcán" in elements["subject"] and "lima" in elements["subject"]:
            parts.append("volcán de lima miniatura")
        
        # Agregar efectos (solo uno para evitar repetición)
        effects_added = False
        if "neón" in elements["materials"] and not effects_added:
            parts.append("con efectos neón increíbles")
            effects_added = True
        elif "holográfico" in elements["materials"] and not effects_added:
            parts.append("con efectos holográficos")
            effects_added = True
        
        # Si no hay elementos específicos, usar descripción genérica mejorada
        if not parts:
            if elements["category"] == "asmr":
                parts.append("con sonidos ASMR perfectos")
            elif elements["category"] == "food":
                parts.append("con técnicas de cocina increíbles")
            else:
                parts.append("con efectos visuales impresionantes")
        
        return " ".join(parts)
    
    def generate_hashtags(self, elements: Dict) -> List[str]:
        """Genera hashtags dinámicos basados en el contenido"""
        hashtags = set()
        
        # Hashtags base por categoría
        category_hashtags = self.hashtags_base.get(elements["category"], self.hashtags_base["general"])
        hashtags.update(random.sample(category_hashtags, min(3, len(category_hashtags))))
        
        # Hashtags específicos por elementos
        if "subject" in elements:
            for subject in elements["subject"]:
                if subject in self.hashtags_base:
                    hashtags.update(random.sample(self.hashtags_base[subject], min(2, len(self.hashtags_base[subject]))))
        
        if "materials" in elements:
            for material in elements["materials"]:
                if material in self.hashtags_base:
                    hashtags.update(random.sample(self.hashtags_base[material], min(2, len(self.hashtags_base[material]))))
        
        # Normalizar y eliminar duplicados
        normalized_hashtags = {self.normalize_text(h) for h in hashtags}
        
        # Rellenar con hashtags universales hasta llegar a 5
        universal = ["#fyp", "#foryou", "#viral", "#trending", "#explorepage"]
        
        # Asegurarse de que los universales no estén ya en la lista
        universal_to_add = [h for h in universal if h not in normalized_hashtags]
        
        while len(normalized_hashtags) < 5 and universal_to_add:
            normalized_hashtags.add(universal_to_add.pop(0))
            
        unique_hashtags = list(normalized_hashtags)
        random.shuffle(unique_hashtags) # Mezclar para que no sean siempre los mismos
        
        return unique_hashtags[:5]  # Máximo 5 hashtags

    def generate_dynamic_description(self, video_path: str, prompt_original: str = "") -> str:
        """Genera descripción completamente dinámica basada en el prompt del video"""
        print(f"🎯 Generando descripción ULTRA DINÁMICA para: {os.path.basename(video_path)}")
        print(f"📋 Prompt original: {prompt_original[:100]}...")
        
        if not prompt_original:
            # Descripción genérica si no hay prompt
            hook = random.choice(self.viral_hooks["general"])
            content = "contenido ÉPICO"
            question = random.choice(self.engagement_questions)
            cta = "¡No te pierdas este contenido ÉPICO!"
            hashtags_list = self.generate_hashtags({"category": "general", "subject": [], "materials": []})
            hashtags = " ".join(hashtags_list)
            descripcion = f"{hook} {content}\n\n{question} 🔥\n{cta}\n\n{hashtags}"
        else:
            # Análisis inteligente del prompt
            elements = self.extract_key_elements(prompt_original)
            
            # Generar componentes dinámicos
            hook = random.choice(self.viral_hooks[elements["category"]])
            content_desc = self.generate_content_description(elements)
            question = random.choice(self.engagement_questions)
            cta = random.choice(self.call_to_actions)
            hashtags = " ".join(self.generate_hashtags(elements))
            
            # Líneas adicionales específicas por categoría
            if elements["category"] == "asmr":
                extra_line = "Este ASMR está ROMPIENDO TikTok 🔥"
            elif elements["category"] == "food":
                extra_line = "Esto parece de otro planeta 🌟"
            else:
                extra_line = "Efectos que no vas a creer 🤯"
            
            # Construir descripción final
            if content_desc and not content_desc.startswith("con"):
                descripcion = f"{hook} con {content_desc}\n\n{extra_line}\n{question} 👀\n{cta}\n\n{hashtags}"
            elif content_desc:
                descripcion = f"{hook} {content_desc}\n\n{extra_line}\n{question} 👀\n{cta}\n\n{hashtags}"
            else:
                descripcion = f"{hook}\n\n{extra_line}\n{question} 👀\n{cta}\n\n{hashtags}"
        
        final_description = self.normalize_text(descripcion)

        print(f"✅ Descripción ULTRA DINÁMICA generada: {len(final_description)} caracteres")
        print(f"📄 Preview completo:")
        print("=" * 50)
        print(final_description)
        print("=" * 50)
        
        return final_description

def test_generator():
    """Función de prueba para el generador"""
    generator = DynamicDescriptionGenerator()
    
    prompts_test = [
        "Genera una imagen digital hiperrealista de Capibara gigante relajado en playa surrealista de fresas gigantes, estilo fotorrealista hiperdetallado, colores vibrantes, lava de chocolate fluyendo sobre las fresas, sonido crujiente ASMR al morder una fresa, música relajante de fondo.",
        "Video ASMR terapéutico con sonidos envolventes de Capibara chef cortando vegetales de cristal sobre lava fría en cocina cyberpunk con luces neón.",
        "Volcán miniatura de lima con efectos holográficos y chocolate derretido fluyendo como lava."
    ]
    
    for i, prompt in enumerate(prompts_test, 1):
        print(f"\n🧪 PRUEBA {i}:")
        print("-" * 60)
        desc = generator.generate_dynamic_description(f"test_video_{i}.mp4", prompt)
        print("\n")

if __name__ == "__main__":
    test_generator()
