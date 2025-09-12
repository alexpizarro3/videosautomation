import json
import os
from datetime import datetime
import asyncio
from dotenv import load_dotenv
from src.utils.gemini_web_client import GeminiWebClient

# Cargar variables de entorno
load_dotenv()

def load_scraping_data():
    """
    Carga los datos del scraping de TikTok para análisis de tendencias
    """
    # Buscar el archivo de métricas más reciente
    analytics_dir = 'data/analytics'
    tiktok_files = []
    
    if os.path.exists(analytics_dir):
        for file in os.listdir(analytics_dir):
            if file.startswith('tiktok_metrics_') and file.endswith('.json'):
                tiktok_files.append(os.path.join(analytics_dir, file))
    
    if not tiktok_files:
        return None
    
    # Obtener el archivo más reciente
    latest_file = max(tiktok_files, key=os.path.getmtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
            
    except Exception as e:
        print(f"[!] Error cargando {latest_file}: {e}")
        return None

def analyze_viral_patterns(data):
    """
    Analiza los patrones virales de los datos de TikTok
    """
    # Extraer elementos más virales
    viral_elements = {
        'high_engagement_keywords': ['ASMR', 'satisfying', 'relaxing', 'viral'],
        'successful_themes': ['mystery', 'fantasy', 'adventure', 'discovery'],
        'asmr_triggers': ['crujiente', 'suave', 'susurro', 'tapping', 'scratching'],
        'visual_patterns': ['texturas', 'colores intensos', 'movimientos fluidos']
    }
    
    # Analizar métricas de videos si están disponibles
    if 'videos' in data:
        videos = data['videos']
        
        # Obtener videos con más vistas
        high_view_videos = []
        for video in videos:
            views = video.get('views', 0)
            if isinstance(views, (int, str)):
                try:
                    view_count = int(str(views).replace(',', ''))
                    if view_count > 500:  # Umbral de viralidad
                        high_view_videos.append({
                            'views': view_count,
                            'url': video.get('url', ''),
                            'metrics': video.get('metrics', {})
                        })
                except ValueError:
                    continue
        
        print(f"[i] Videos analizados: {len(videos)}")
        print(f"[+] Videos virales encontrados: {len(high_view_videos)}")
        
        # Enriquecer patrones basados en videos exitosos
        if high_view_videos:
            avg_views = sum(v['views'] for v in high_view_videos) / len(high_view_videos)
            print(f"[+] Promedio de vistas de videos virales: {avg_views:.0f}")
            
            # Agregar elementos basados en el rendimiento
            viral_elements['high_engagement_keywords'].extend([
                'trending', 'viral', 'amazing', 'increíble'
            ])
    else:
        print("[i] Usando patrones de tendencias predeterminados")
    
    return viral_elements

def generate_narrative_stories(viral_patterns):
    """
    Genera 2 historias narrativas ASMR basadas en los patrones virales
    """
    
    # Prompt base para generación de historias
    base_prompt = f"""Eres un experto en contenido viral de TikTok especializado en ASMR visual.
Tu objetivo es crear 2 conceptos de historias narrativas ASMR que sean visualmente espectaculares, ultra coloridas y adictivas.
    
    PATRONES VIRALES DETECTADOS:
    - Triggers ASMR exitosos: {', '.join(viral_patterns['asmr_triggers'][:10])}
    - Temas exitosos: {', '.join(viral_patterns['successful_themes'][:5])}
    - Estilos visuales de alto rendimiento: {', '.join(viral_patterns['visual_patterns'])}
    
    REQUISITOS PARA CADA HISTORIA:
    1.  **Concepto Visualmente Adictivo:** La idea central debe ser hipnótica y memorable. Piensa en "dopamine hits" visuales.
    2.  **Ultra Colorido:** Describe paletas de colores vibrantes, saturadas y con contrastes fuertes que destaquen en el feed.
    3.  **Narrativa ASMR en 3 Actos:** La historia debe tener 3 secuencias/capítulos claros, con una progresión que enganche.
    4.  **Sonido Envolvente:** El audio debe ser el protagonista, con triggers específicos y una atmósfera inmersiva.
    5.  **Prompts de Imagen Cinematográficos:** Los prompts para generar las imágenes deben ser extremadamente detallados, especificando iluminación, texturas, composición y estilo (ej: "hyperrealistic, cinematic lighting, 4K, octane render").
    
    FORMATO DE RESPUESTA:
    {{
        "historia_1": {{
            "titulo": "Título creativo de la historia 1",
            "concepto_general": "Descripción general de la historia completa",
            "secuencia_1": {{
                "titulo": "Título de la primera secuencia",
                "descripcion_visual": "Descripción detallada de lo que se ve",
                "elementos_asmr": "Sonidos y texturas específicas (ej: crujidos cristalinos, susurros metálicos)",
                "prompt_imagen": "Prompt detallado para generar la imagen"
            }},
            "secuencia_2": {{...}},
            "secuencia_3": {{...}},
            "sonido_envolvente": "Descripción del audio continuo ASMR",
            "potencial_viral": "Por qué esta historia puede ser viral"
        }},
        "historia_2": {{...}}
    }}
    
    EJEMPLOS DE CONCEPTOS ASMR EXITOSOS:
    - Un alquimista creando pociones que brillan con colores neón y burbujean con sonidos satisfactorios.
    - Un relojero cósmico ensamblando un reloj con engranajes de cristal y arena de galaxias.
    - Un botánico descubriendo flores que cambian de color al tacto y emiten sonidos armónicos.
    
    Genera ahora las 2 historias más virales, coloridas y adictivas que puedas imaginar.
    """.strip()
    
    try:
        client = GeminiWebClient()
        stories_text = client.generate_text(base_prompt)
        client.close()
        
        # Limpiar el texto para extraer solo el JSON
        if '```json' in stories_text:
            stories_text = stories_text.split('```json')[1].split('```')[0]
        elif '```' in stories_text:
            stories_text = stories_text.split('```')[1]
        else:
            # Si no hay ```, asumimos que la respuesta es JSON puro
            stories_text = stories_text
        
        stories = json.loads(stories_text.strip())
        return stories
        
    except Exception as e:
        print(f"Error generando historias con Gemini: {e}")
        # Fallback: crear historias básicas
        return create_fallback_stories(viral_patterns)

def create_fallback_stories(viral_patterns):
    """
    Crea historias básicas en caso de error con la IA
    """
    return {
        "historia_1": {
            "titulo": "El Chef de Cristal ASMR",
            "concepto_general": "Un chef extraordinario que cocina con ingredientes de cristal que producen sonidos hipnóticos",
            "secuencia_1": {
                "titulo": "Preparación Cristalina",
                "descripcion_visual": "Chef preparando ingredientes translúcidos en una cocina minimalista",
                "elementos_asmr": "Sonidos de cristal tintineo, cortes precisos, superficies lisas",
                "prompt_imagen": "Hyperrealistic chef cutting translucent crystal vegetables, minimalist kitchen, soft lighting, ASMR aesthetic, satisfying textures"
            },
            "secuencia_2": {
                "titulo": "Cortes Precisos",
                "descripcion_visual": "Primer plano de manos cortando verduras de cristal con precisión",
                "elementos_asmr": "Crujidos delicados, respiración controlada, movimientos fluidos",
                "prompt_imagen": "Close-up hands cutting crystal-like vegetables, precise movements, satisfying sounds visualization, ASMR triggers, hyperdetailed"
            },
            "secuencia_3": {
                "titulo": "Creación Final",
                "descripcion_visual": "Plato final con ingredientes cristalinos perfectamente organizados",
                "elementos_asmr": "Toques finales suaves, sonidos de cristal, satisfacción visual",
                "prompt_imagen": "Perfectly arranged crystal dish, artistic plating, ASMR satisfaction, translucent ingredients, masterpiece presentation"
            },
            "sonido_envolvente": "Audio continuo de cristales, cortes precisos y ambiente de cocina sereno",
            "potencial_viral": "Combina cooking content con ASMR, visualmente único y auditivamente adictivo"
        },
        "historia_2": {
            "titulo": "Texturas Mágicas ASMR",
            "concepto_general": "Exploración de materiales únicos que se transforman con texturas satisfactorias",
            "secuencia_1": {
                "titulo": "Descubrimiento",
                "descripcion_visual": "Manos descubriendo materiales con texturas inusuales",
                "elementos_asmr": "Sonidos de exploración, texturas suaves, sorpresa táctil",
                "prompt_imagen": "Hands discovering unique textured materials, soft lighting, ASMR aesthetic, tactile exploration, satisfying surfaces"
            },
            "secuencia_2": {
                "titulo": "Transformación",
                "descripcion_visual": "Los materiales cambian de forma y textura de manera hipnótica",
                "elementos_asmr": "Sonidos de transformación, crujidos suaves, cambios graduales",
                "prompt_imagen": "Materials transforming texture, morphing surfaces, hypnotic changes, ASMR triggers, satisfying metamorphosis"
            },
            "secuencia_3": {
                "titulo": "Resultado Final",
                "descripcion_visual": "Creación final con texturas perfectas y satisfactorias",
                "elementos_asmr": "Toques finales, texturas perfectas, sonidos de satisfacción",
                "prompt_imagen": "Final textured creation, perfect satisfying surfaces, ASMR completion, tactile perfection, visual satisfaction"
            },
            "sonido_envolvente": "Audio de texturas cambiantes, transformaciones suaves y satisfacción táctil",
            "potencial_viral": "Enfoque en texturas satisfactorias, transformación visual y triggers ASMR únicos"
        }
    }

def save_stories(stories, viral_patterns):
    """
    Guarda las historias generadas en archivo JSON
    """
    # Crear directorio si no existe
    os.makedirs('data/analytics', exist_ok=True)
    
    # Estructura completa de datos
    story_data = {
        "timestamp": datetime.now().isoformat(),
        "viral_patterns_analyzed": viral_patterns,
        "stories_generated": stories,
        "generation_method": "AI-based narrative creation",
        "asmr_focus": True,
        "narrative_structure": {
            "sequences_per_story": 3,
            "total_stories": 2,
            "selection_pending": True
        }
    }
    
    # Guardar archivo principal
    output_file = 'data/analytics/story_prompts_narrative.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(story_data, f, indent=2, ensure_ascii=False)
    
    
    # Mostrar resumen
    print("\n[+] HISTORIAS GENERADAS:")
    for i, (key, story) in enumerate(stories.items(), 1):
        print(f"\n{i}. {story['titulo']}")
        print(f"   Concepto: {story['concepto_general']}")
        print(f"   Potencial: {story['potencial_viral']}")
    
    return output_file

def main():
    """
    Función principal que ejecuta todo el proceso
    """
    print(">> Iniciando generación de historias narrativas ASMR...")
    
    # 1. Cargar datos del scraping
    print(">> Cargando datos del scraping de TikTok...")
    scraping_data = load_scraping_data()
    
    if not scraping_data:
        print("[!] No se encontraron datos de scraping. Ejecuta test_tiktok_scraping.py primero.")
        return False
    
    # 2. Analizar patrones virales
    print(">> Analizando patrones virales...")
    viral_patterns = analyze_viral_patterns(scraping_data)
    
    # 3. Generar historias narrativas
    print(">> Generando 2 historias narrativas ASMR...")
    stories = generate_narrative_stories(viral_patterns)
    
    # 4. Guardar resultados
    print(">> Guardando historias generadas...")
    output_file = save_stories(stories, viral_patterns)
    
    print(f"\n ¡Proceso completado! Historias guardadas en: {output_file}")
    
    return True

if __name__ == "__main__":
    main()
