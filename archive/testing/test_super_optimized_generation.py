#!/usr/bin/env python3
"""
Generador de contenido OPTIMIZADO basado en análisis completo
Usa datos de 109+ videos para máxima efectividad
"""

import json
import os
import time
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

def load_complete_analysis():
    """Cargar el análisis completo más reciente"""
    analytics_dir = "data/analytics"
    
    if not os.path.exists(analytics_dir):
        print("❌ No se encontró directorio de analytics")
        return None
    
    # Buscar el archivo más reciente
    analysis_files = [f for f in os.listdir(analytics_dir) if f.startswith('complete_analysis_')]
    
    if not analysis_files:
        print("❌ No se encontró análisis completo")
        print("💡 Ejecuta primero: python test_complete_analysis.py")
        return None
    
    latest_file = max(analysis_files, key=lambda x: os.path.getctime(os.path.join(analytics_dir, x)))
    file_path = os.path.join(analytics_dir, latest_file)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Análisis cargado: {latest_file}")
        print(f"📊 Videos analizados: {data.get('total_videos_found', 0)}")
        return data
        
    except Exception as e:
        print(f"❌ Error cargando análisis: {e}")
        return None

def analyze_top_performing_content(analysis_data):
    """Analizar patrones en el contenido top-performing"""
    if not analysis_data or 'analysis' not in analysis_data:
        return None
    
    analysis = analysis_data['analysis']
    all_videos = analysis_data.get('all_videos_data', [])
    
    print(f"\n🔍 ANALIZANDO PATRONES DE ÉXITO")
    print("=" * 50)
    
    # Videos high-performance (sobre 1.5x el promedio)
    avg_views = analysis.get('avg_views', 0)
    high_threshold = avg_views * 1.5
    
    top_videos = []
    for video in all_videos:
        metrics = video.get('metrics', {})
        for key, value in metrics.items():
            try:
                if isinstance(value, str):
                    # Convertir K, M a números
                    if 'K' in value:
                        numeric_value = int(float(value.replace('K', '')) * 1000)
                    elif 'M' in value:
                        numeric_value = int(float(value.replace('M', '')) * 1000000)
                    elif value.isdigit():
                        numeric_value = int(value)
                    else:
                        continue
                    
                    if numeric_value > high_threshold:
                        top_videos.append({
                            'video_id': video.get('video_id', 'unknown'),
                            'url': video.get('url', ''),
                            'views': numeric_value,
                            'metrics': metrics
                        })
                        break  # Solo contar una vez por video
            except:
                continue
    
    # Eliminar duplicados por video_id
    seen_ids = set()
    unique_top_videos = []
    for video in top_videos:
        if video['video_id'] not in seen_ids:
            unique_top_videos.append(video)
            seen_ids.add(video['video_id'])
    
    print(f"🏆 Videos identificados como high-performance: {len(unique_top_videos)}")
    print(f"📊 Threshold usado: {high_threshold:.0f} views")
    
    # Analizar patrones de timing
    video_ids = [v['video_id'] for v in unique_top_videos[:10]]  # Top 10
    
    patterns = {
        'avg_performance': avg_views,
        'high_performance_threshold': high_threshold,
        'top_videos_count': len(unique_top_videos),
        'success_rate': len(unique_top_videos) / len(all_videos) * 100,
        'top_video_ids': video_ids,
        'max_views': analysis.get('max_views', 0),
        'consistency_score': analysis.get('consistency_score', 0)
    }
    
    return patterns

def generate_optimized_prompts(patterns):
    """Generar prompts basados en patrones de éxito"""
    if not patterns:
        return None
    
    print(f"\n🧠 GENERANDO PROMPTS OPTIMIZADOS")
    print("=" * 50)
    
    # Análisis de rendimiento
    success_rate = patterns.get('success_rate', 0)
    consistency = patterns.get('consistency_score', 0)
    max_views = patterns.get('max_views', 0)
    avg_views = patterns.get('avg_performance', 0)
    
    # Estrategia basada en datos
    if success_rate > 20:
        strategy = "aggressive_viral"  # Ya tienes buen éxito viral
    elif success_rate > 10:
        strategy = "moderate_growth"   # Crecimiento constante
    else:
        strategy = "foundation_building"  # Construir base
    
    print(f"📈 Estrategia seleccionada: {strategy}")
    print(f"🎯 Tasa de éxito actual: {success_rate:.1f}%")
    print(f"🏆 Mejor video: {max_views:,} views")
    
    # Prompts optimizados según estrategia
    prompts_by_strategy = {
        "aggressive_viral": {
            "theme": "contenido_viral_extremo",
            "style": "humor_absurdo_trending",
            "duration": "15-20_segundos",
            "hook": "primeros_3_segundos_impactantes",
            "description": "Contenido viral de alto impacto, humor absurdo que genere reacciones inmediatas"
        },
        "moderate_growth": {
            "theme": "comedia_relatable",
            "style": "humor_situacional",
            "duration": "20-30_segundos",
            "hook": "situacion_cotidiana_exagerada", 
            "description": "Comedia que la gente puede relacionar con su vida diaria"
        },
        "foundation_building": {
            "theme": "contenido_consistente",
            "style": "humor_simple_efectivo",
            "duration": "15-25_segundos",
            "hook": "pregunta_directa_audiencia",
            "description": "Contenido simple pero efectivo que construya audiencia leal"
        }
    }
    
    selected_prompt = prompts_by_strategy.get(strategy, prompts_by_strategy["moderate_growth"])
    
    # Hora del día para optimización
    current_hour = datetime.now().hour
    
    if 6 <= current_hour <= 12:
        time_context = "mañana_energia_positiva"
    elif 12 <= current_hour <= 18:
        time_context = "tarde_humor_trabajo"
    else:
        time_context = "noche_contenido_relajado"
    
    selected_prompt["time_context"] = time_context
    selected_prompt["target_views"] = str(max(int(max_views * 1.2), int(avg_views * 2)))  # Objetivo: superar el mejor o 2x promedio
    
    return selected_prompt

def create_optimized_content(prompt_data):
    """Crear imagen optimizada con Gemini"""
    load_dotenv()
    
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    
    if not prompt_data:
        print("❌ No hay datos de prompt")
        return None
    
    print(f"\n🎨 GENERANDO CONTENIDO OPTIMIZADO")
    print("=" * 50)
    
    # Prompt detallado basado en análisis
    target_views = int(prompt_data.get('target_views', '1000'))
    detailed_prompt = f"""
CREAR IMAGEN VIRAL PARA TIKTOK - OPTIMIZADA PARA MÁXIMAS VIEWS

CONTEXTO DEL ANÁLISIS:
- Objetivo de views: {target_views:,} views
- Estrategia: {prompt_data.get('theme', 'viral')}
- Estilo: {prompt_data.get('style', 'humor')}
- Momento: {prompt_data.get('time_context', 'universal')}

ESPECIFICACIONES TÉCNICAS:
- Formato: Vertical 9:16 (1080x1920 píxeles)
- Calidad: Ultra alta definición
- Colores: Vibrantes y contrastantes para captar atención

CONTENIDO:
{prompt_data.get('description', 'Contenido viral divertido')}

ELEMENTOS CLAVE:
1. HOOK VISUAL: {prompt_data.get('hook', 'Impacto inmediato')}
2. EXPRESIÓN: Exagerada, cómica, memorable
3. TEXTO: Mínimo pero impactante
4. COMPOSICIÓN: Centro de atención claro
5. TRENDING: Incorporar elementos actuales de TikTok

ESTILO ARTÍSTICO:
- Ilustración digital moderna
- Colores saturados (azul, rojo, amarillo neón)
- Líneas limpias y definidas
- Expresiones faciales exageradas
- Elementos de movimiento visual

EVITAR:
- Imágenes genéricas
- Colores apagados
- Composiciones aburridas
- Texto excesivo
- Elementos no apropiados para TikTok

OBJETIVO: Crear una imagen que haga que la gente se detenga a ver y comentar inmediatamente.
"""

    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        print(f"🎯 Objetivo de views: {target_views:,}")
        print(f"🎨 Generando imagen optimizada...")
        
        response = model.generate_content([detailed_prompt])
        
        if response and hasattr(response, 'candidates') and response.candidates:
            # Generar imagen
            image_response = model.generate_content([
                "Genera una imagen basada en esta descripción optimizada:",
                detailed_prompt
            ])
            
            # Guardar resultado
            timestamp = int(time.time())
            
            os.makedirs('data/optimized_content', exist_ok=True)
            
            # Guardar metadatos
            content_metadata = {
                'timestamp': timestamp,
                'strategy': prompt_data.get('theme', 'unknown'),
                'target_views': target_views,
                'prompt_used': detailed_prompt,
                'generated_at': datetime.now().isoformat(),
                'optimization_based_on': '109_videos_analysis'
            }
            
            metadata_file = f"data/optimized_content/content_metadata_{timestamp}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(content_metadata, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Contenido optimizado generado")
            print(f"📁 Metadatos guardados en: {metadata_file}")
            print(f"🎯 Estrategia aplicada: {prompt_data.get('theme', 'N/A')}")
            
            return {
                'content_metadata': content_metadata,
                'prompt': detailed_prompt,
                'timestamp': timestamp
            }
            
    except Exception as e:
        print(f"❌ Error generando contenido: {e}")
        return None

def main():
    """Función principal de optimización completa"""
    print("🚀 GENERACIÓN DE CONTENIDO OPTIMIZADO")
    print("📊 Basado en análisis de 109+ videos")
    print("=" * 60)
    
    # 1. Cargar análisis completo
    analysis_data = load_complete_analysis()
    if not analysis_data:
        return
    
    # 2. Analizar patrones de éxito
    patterns = analyze_top_performing_content(analysis_data)
    if not patterns:
        print("❌ No se pudieron analizar patrones")
        return
    
    # 3. Generar prompts optimizados
    optimized_prompt = generate_optimized_prompts(patterns)
    if not optimized_prompt:
        print("❌ No se pudieron generar prompts")
        return
    
    # 4. Crear contenido optimizado
    result = create_optimized_content(optimized_prompt)
    
    if result:
        print(f"\n🎉 CONTENIDO OPTIMIZADO GENERADO EXITOSAMENTE")
        print(f"📈 Basado en análisis de {analysis_data.get('total_videos_found', 0)} videos")
        print(f"🎯 Objetivo: {int(optimized_prompt.get('target_views', '0')):,} views")
        print(f"📊 Estrategia: {optimized_prompt.get('theme', 'N/A')}")
        
        # Mostrar recomendaciones
        print(f"\n💡 RECOMENDACIONES PARA MAXIMIZAR VIEWS:")
        print(f"⏰ Sube entre 19:00-21:00 hora local")
        print(f"📱 Usa hashtags: #fyp #viral #comedia #parati")
        print(f"🎵 Agrega audio trending del momento")
        print(f"💬 Responde TODOS los comentarios rápidamente")
        print(f"📊 Monitorea las primeras 2 horas después de subir")
        
    else:
        print("❌ No se pudo generar contenido optimizado")

if __name__ == "__main__":
    main()
