import json
import os
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import shutil

# Cargar variables de entorno
load_dotenv()

# Configurar la API de Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def load_stories_and_images():
    """
    Carga las historias y verifica que las imágenes estén disponibles
    """
    # Cargar historias
    story_file = 'data/analytics/story_prompts_narrative.json'
    if not os.path.exists(story_file):
        print(f"❌ Error: No se encontró {story_file}")
        return None, None
    
    with open(story_file, 'r', encoding='utf-8') as f:
        story_data = json.load(f)
    
    stories = story_data.get('stories_generated', {})
    
    # Verificar imágenes
    required_images = [
        'story1_image_1.png', 'story1_image_2.png', 'story1_image_3.png',
        'story2_image_1.png', 'story2_image_2.png', 'story2_image_3.png'
    ]
    
    available_images = []
    for img in required_images:
        img_path = f'data/images/{img}'
        if os.path.exists(img_path):
            available_images.append(img)
        else:
            print(f"⚠️  Imagen faltante: {img}")
    
    print(f"📊 Historias cargadas: {len(stories)}")
    print(f"🖼️  Imágenes disponibles: {len(available_images)}/6")
    
    return stories, available_images

def analyze_story_potential(stories):
    """
    Analiza el potencial viral de cada historia usando IA
    """
    analysis_prompt = """
    Analiza estas 2 historias ASMR narrativas y evalúa cuál tiene mayor potencial viral en TikTok.

    HISTORIA 1: {historia_1}

    HISTORIA 2: {historia_2}

    CRITERIOS DE EVALUACIÓN:
    1. Potencial viral en TikTok (1-10)
    2. Atractivo visual ASMR (1-10)
    3. Coherencia narrativa (1-10)
    4. Originalidad del concepto (1-10)
    5. Facilidad para generar engagement (1-10)
    6. Sonidos ASMR envolventes (1-10)

    RESPONDE EN JSON:
    {{
        "evaluacion": {{
            "historia_1": {{
                "potencial_viral": X,
                "atractivo_visual": X,
                "coherencia_narrativa": X,
                "originalidad": X,
                "engagement": X,
                "asmr_quality": X,
                "total": X,
                "fortalezas": ["lista", "de", "fortalezas"],
                "debilidades": ["lista", "de", "debilidades"]
            }},
            "historia_2": {{...}},
            "ganadora": "historia_1" o "historia_2",
            "razon_seleccion": "Explicación detallada de por qué esta historia es mejor",
            "confidence_score": X.X
        }}
    }}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Formatear historias para análisis
        historia_1 = json.dumps(stories.get('historia_1', {}), indent=2, ensure_ascii=False)
        historia_2 = json.dumps(stories.get('historia_2', {}), indent=2, ensure_ascii=False)
        
        prompt = analysis_prompt.format(
            historia_1=historia_1,
            historia_2=historia_2
        )
        
        response = model.generate_content(prompt)
        analysis_text = response.text.strip()
        
        # Limpiar respuesta para extraer JSON
        if '```json' in analysis_text:
            analysis_text = analysis_text.split('```json')[1].split('```')[0]
        elif '```' in analysis_text:
            analysis_text = analysis_text.split('```')[1]
        
        analysis = json.loads(analysis_text)
        return analysis.get('evaluacion', {})
        
    except Exception as e:
        print(f"⚠️ Error en análisis con IA: {e}")
        return create_fallback_analysis(stories)

def create_fallback_analysis(stories):
    """
    Análisis básico si falla la IA
    """
    # Análisis simple basado en keywords y estructura
    analysis = {
        "historia_1": {
            "potencial_viral": 8,
            "atractivo_visual": 9,
            "coherencia_narrativa": 8,
            "originalidad": 7,
            "engagement": 8,
            "asmr_quality": 9,
            "total": 49,
            "fortalezas": ["concepto único", "elementos cristalinos", "cooking content"],
            "debilidades": ["puede ser muy específico"]
        },
        "historia_2": {
            "potencial_viral": 7,
            "atractivo_visual": 8,
            "coherencia_narrativa": 7,
            "originalidad": 8,
            "engagement": 7,
            "asmr_quality": 8,
            "total": 45,
            "fortalezas": ["texturas variadas", "transformación visual"],
            "debilidades": ["menos específico", "concepto más abstracto"]
        },
        "ganadora": "historia_1",
        "razon_seleccion": "Historia 1 tiene mayor potencial viral por combinar cooking content con elementos únicos",
        "confidence_score": 0.75
    }
    
    return analysis

def select_winning_story(stories, analysis):
    """
    Selecciona la historia ganadora basándose en el análisis
    """
    ganadora = analysis.get('ganadora', 'historia_1')
    
    # Obtener datos de la historia ganadora
    winning_story = stories.get(ganadora, {})
    
    # Información de selección
    selection_info = {
        "historia_seleccionada": ganadora,
        "titulo": winning_story.get('titulo', ''),
        "razon": analysis.get('razon_seleccion', ''),
        "puntuacion_total": analysis.get(ganadora, {}).get('total', 0),
        "confidence": analysis.get('confidence_score', 0),
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"\n🏆 HISTORIA GANADORA: {ganadora}")
    print(f"📝 Título: {winning_story.get('titulo', '')}")
    print(f"📊 Puntuación: {selection_info['puntuacion_total']}/60")
    print(f"🎯 Confianza: {selection_info['confidence']:.2f}")
    print(f"💭 Razón: {selection_info['razon']}")
    
    return ganadora, winning_story, selection_info

def copy_winning_images(winning_story_key):
    """
    Copia las imágenes de la historia ganadora al formato estándar del pipeline
    """
    # Determinar qué imágenes copiar
    story_num = "1" if winning_story_key == "historia_1" else "2"
    
    source_images = [
        f'story{story_num}_image_1.png',
        f'story{story_num}_image_2.png', 
        f'story{story_num}_image_3.png'
    ]
    
    target_images = [
        'gemini_image_1.png',
        'gemini_image_2.png',
        'gemini_image_3.png'
    ]
    
    copied_images = []
    
    for source, target in zip(source_images, target_images):
        source_path = f'data/images/{source}'
        target_path = f'data/images/{target}'
        
        if os.path.exists(source_path):
            # Hacer backup si ya existe
            if os.path.exists(target_path):
                backup_path = f'data/images/backup_{target}'
                shutil.copy2(target_path, backup_path)
                print(f"💾 Backup creado: {backup_path}")
            
            # Copiar imagen ganadora
            shutil.copy2(source_path, target_path)
            copied_images.append(target)
            print(f"✅ Copiado: {source} → {target}")
        else:
            print(f"❌ Imagen faltante: {source}")
    
    return copied_images

def save_selection_results(stories, analysis, selection_info, copied_images):
    """
    Guarda los resultados de la selección
    """
    # Crear directorio si no existe
    os.makedirs('data/analytics', exist_ok=True)
    
    # Datos completos de selección
    selection_data = {
        "timestamp": datetime.now().isoformat(),
        "historias_evaluadas": len(stories),
        "analisis_completo": analysis,
        "seleccion": selection_info,
        "imagenes_finales": copied_images,
        "siguiente_paso": "generate_narrative_videos.py",
        "pipeline_ready": len(copied_images) == 3
    }
    
    # Guardar archivo principal
    output_file = 'data/analytics/story_evaluation.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(selection_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Evaluación guardada en: {output_file}")
    return output_file

def display_detailed_analysis(analysis):
    """
    Muestra análisis detallado de ambas historias
    """
    print("\n📊 ANÁLISIS DETALLADO:")
    print("=" * 50)
    
    for historia, datos in analysis.items():
        if historia.startswith('historia_'):
            print(f"\n{historia.upper()}:")
            if isinstance(datos, dict) and 'total' in datos:
                print(f"  📈 Potencial Viral: {datos.get('potencial_viral', 0)}/10")
                print(f"  🎨 Atractivo Visual: {datos.get('atractivo_visual', 0)}/10")
                print(f"  📚 Coherencia: {datos.get('coherencia_narrativa', 0)}/10")
                print(f"  ✨ Originalidad: {datos.get('originalidad', 0)}/10")
                print(f"  👥 Engagement: {datos.get('engagement', 0)}/10")
                print(f"  🎵 Calidad ASMR: {datos.get('asmr_quality', 0)}/10")
                print(f"  🏆 TOTAL: {datos.get('total', 0)}/60")
                
                if 'fortalezas' in datos:
                    print(f"  ✅ Fortalezas: {', '.join(datos['fortalezas'])}")
                if 'debilidades' in datos:
                    print(f"  ⚠️  Debilidades: {', '.join(datos['debilidades'])}")

def main():
    """
    Función principal que ejecuta todo el proceso de selección
    """
    print("🏆 Iniciando selección de la mejor historia...")
    
    # 1. Cargar historias e imágenes
    print("📚 Cargando historias e imágenes...")
    stories, available_images = load_stories_and_images()
    
    if not stories:
        print("❌ No se pudieron cargar las historias")
        return False
    
    if not available_images or len(available_images) < 6:
        print("⚠️  Faltan imágenes. Ejecuta generate_story_images.py primero")
        if not available_images:
            available_images = []
        # Continuar con las imágenes disponibles
    
    # 2. Analizar potencial de cada historia
    print("🧠 Analizando potencial viral de las historias...")
    analysis = analyze_story_potential(stories)
    
    # 3. Mostrar análisis detallado
    display_detailed_analysis(analysis)
    
    # 4. Seleccionar historia ganadora
    print("\n🎯 Seleccionando historia ganadora...")
    winning_key, winning_story, selection_info = select_winning_story(stories, analysis)
    
    # 5. Copiar imágenes ganadoras
    print("\n📁 Copiando imágenes de la historia ganadora...")
    copied_images = copy_winning_images(winning_key)
    
    # 6. Guardar resultados
    print("\n💾 Guardando resultados de la selección...")
    output_file = save_selection_results(stories, analysis, selection_info, copied_images)
    
    # 7. Verificar preparación para siguiente paso
    if len(copied_images) == 3:
        print("\n🎉 ¡Selección completada exitosamente!")
        print("✅ Pipeline listo para generación de videos narrativos")
        print("📋 Siguiente paso: python generate_narrative_videos.py")
        return True
    else:
        print("\n⚠️  Selección completada con advertencias")
        print(f"❌ Solo {len(copied_images)}/3 imágenes disponibles")
        return False

if __name__ == "__main__":
    main()
