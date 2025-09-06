#!/usr/bin/env python3
"""
Generación completa de contenido basada en el análisis de métricas
de @chakakitafreakyvideos
"""

import os
import json
import time
from dotenv import load_dotenv

def analyze_performance_data():
    """Analizar los datos de rendimiento para optimizar contenido"""
    print("📊 ANÁLISIS DE RENDIMIENTO")
    print("=" * 40)
    
    # Buscar el archivo de métricas más reciente
    analytics_dir = "data/analytics"
    if not os.path.exists(analytics_dir):
        print("❌ No hay datos de métricas disponibles")
        return None
    
    # Encontrar archivo más reciente
    metric_files = [f for f in os.listdir(analytics_dir) if f.startswith('tiktok_metrics_')]
    if not metric_files:
        print("❌ No se encontraron archivos de métricas")
        return None
    
    latest_file = sorted(metric_files)[-1]
    file_path = os.path.join(analytics_dir, latest_file)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Analizando datos de: {data['timestamp']}")
        print(f"👤 Cuenta: @{data['username']}")
        
        # Extraer métricas clave
        profile_stats = data.get('profile_metrics', {}).get('profile_stats', {})
        videos_metrics = data.get('videos_metrics', [])
        
        # Análisis del perfil
        followers = int(profile_stats.get('followers-count', '0'))
        likes_total = int(profile_stats.get('likes-count', '0'))
        following = int(profile_stats.get('following-count', '0'))
        
        print(f"\n📈 ANÁLISIS DEL PERFIL:")
        print(f"   👥 Seguidores: {followers}")
        print(f"   ❤️ Likes totales: {likes_total}")
        print(f"   📊 Engagement ratio: {likes_total/max(followers,1):.1f} likes/seguidor")
        
        # Análisis de videos
        if videos_metrics:
            views = []
            for video in videos_metrics:
                for key, value in video['metrics'].items():
                    if key.startswith('metric_') and value.isdigit():
                        views.append(int(value))
            
            if views:
                avg_views = sum(views) / len(views)
                max_views = max(views)
                min_views = min(views)
                
                print(f"\n🎬 ANÁLISIS DE VIDEOS:")
                print(f"   📊 Promedio de views: {avg_views:.0f}")
                print(f"   🏆 Mejor video: {max_views} views")
                print(f"   📉 Menor video: {min_views} views")
                print(f"   📈 Rango de rendimiento: {max_views/max(min_views,1):.1f}x")
        
        # Generar recomendaciones
        recommendations = generate_content_recommendations(followers, likes_total, views if 'views' in locals() else [])
        
        return {
            'followers': followers,
            'likes_total': likes_total,
            'avg_views': avg_views if 'avg_views' in locals() else 0,
            'recommendations': recommendations
        }
        
    except Exception as e:
        print(f"❌ Error analizando datos: {e}")
        return None

def generate_content_recommendations(followers, likes_total, views):
    """Generar recomendaciones de contenido basadas en métricas"""
    recommendations = {}
    
    # Determinar tema principal basado en rendimiento
    if followers < 100:
        recommendations['strategy'] = 'growth_focus'
        recommendations['themes'] = ['motivacion_personal', 'tips_virales', 'contenido_aspiracional']
    elif likes_total / max(followers, 1) > 20:
        recommendations['strategy'] = 'engagement_optimization'
        recommendations['themes'] = ['mantener_engagement', 'contenido_similar', 'series_de_contenido']
    
    # Recomendaciones de estilo basadas en views promedio
    avg_views = sum(views) / len(views) if views else 0
    
    if avg_views > 300:
        recommendations['style'] = 'high_energy'
        recommendations['colors'] = ['vibrant_orange', 'electric_blue', 'neon_green']
    else:
        recommendations['style'] = 'aspirational'
        recommendations['colors'] = ['gold_black', 'royal_blue', 'elegant_purple']
    
    # Horarios optimizados (basado en análisis general de TikTok)
    recommendations['best_times'] = ['09:00', '15:00', '21:00']
    
    return recommendations

def generate_optimized_content():
    """Generar contenido optimizado basado en análisis"""
    print("\n🎨 GENERANDO CONTENIDO OPTIMIZADO")
    print("=" * 40)
    
    # Analizar datos
    analysis = analyze_performance_data()
    if not analysis:
        print("⚠️  Usando configuración por defecto")
        analysis = {
            'followers': 63,
            'likes_total': 1625,
            'avg_views': 297,
            'recommendations': {
                'strategy': 'growth_focus',
                'themes': ['motivacion_personal'],
                'style': 'aspirational',
                'colors': ['gold_black']
            }
        }
    
    # Crear prompt optimizado
    recommendations = analysis['recommendations']
    
    prompts = {
        'motivacion_personal': [
            "EL ÉXITO COMIENZA CON UNA DECISIÓN",
            "TU POTENCIAL ES ILIMITADO",
            "CADA DÍA ES UNA NUEVA OPORTUNIDAD",
            "CREE EN TI Y TODO ES POSIBLE",
            "TRANSFORMA TUS SUEÑOS EN REALIDAD"
        ],
        'tips_virales': [
            "5 HÁBITOS QUE CAMBIARÁN TU VIDA",
            "EL SECRETO DEL ÉXITO REVELADO",
            "ESTO ES LO QUE NO TE CUENTAN",
            "LA FÓRMULA DEL ÉXITO EN 30 SEGUNDOS",
            "CAMBIA TU MINDSET, CAMBIA TU VIDA"
        ]
    }
    
    # Seleccionar tema y texto
    theme = recommendations['themes'][0]
    texts = prompts.get(theme, prompts['motivacion_personal'])
    selected_text = texts[int(time.time()) % len(texts)]
    
    print(f"🎯 Tema seleccionado: {theme}")
    print(f"📝 Texto: {selected_text}")
    print(f"🎨 Estilo: {recommendations['style']}")
    
    # Generar imagen optimizada
    print("\n🖼️  GENERANDO IMAGEN...")
    
    try:
        import google.genai as genai
        
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("❌ GEMINI_API_KEY no disponible")
            return None
        
        client = genai.Client(api_key=api_key)
        
        # Prompt optimizado basado en análisis
        color_scheme = recommendations['colors'][0]
        style = recommendations['style']
        
        optimized_prompt = f"""
        Create a professional TikTok motivational image with the text "{selected_text}" 
        in bold, modern typography. 
        
        Style: {style}, vertical format (9:16 aspect ratio), 
        Color scheme: {color_scheme}, clean background with subtle gradient,
        typography should be eye-catching and readable on mobile,
        modern aesthetic that appeals to young entrepreneurs and motivational content followers.
        
        Make it perfect for a TikTok account with {analysis['followers']} followers that gets 
        an average of {analysis['avg_views']:.0f} views per video.
        """
        
        print("⏳ Enviando request a Gemini...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=optimized_prompt
        )
        
        if response and response.candidates:
            print("✅ Imagen conceptual generada")
            print("💡 Prompt optimizado creado basado en tu performance")
            
            # Guardar información del contenido generado
            content_info = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'theme': theme,
                'text': selected_text,
                'style': style,
                'color_scheme': color_scheme,
                'optimization_based_on': {
                    'followers': analysis['followers'],
                    'avg_views': analysis['avg_views'],
                    'strategy': recommendations['strategy']
                },
                'prompt_used': optimized_prompt
            }
            
            # Guardar info
            os.makedirs('data/generated_content', exist_ok=True)
            info_file = f"data/generated_content/content_info_{int(time.time())}.json"
            
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(content_info, f, indent=2, ensure_ascii=False)
            
            print(f"📁 Info guardada en: {info_file}")
            
            return content_info
        
        else:
            print("❌ No se pudo generar contenido")
            return None
            
    except Exception as e:
        print(f"❌ Error generando contenido: {e}")
        return None

def main():
    """Función principal"""
    print("🚀 GENERACIÓN DE CONTENIDO OPTIMIZADO")
    print("📊 Basado en análisis de @chakakitafreakyvideos")
    print("=" * 60)
    
    content_info = generate_optimized_content()
    
    if content_info:
        print("\n🎉 ¡CONTENIDO OPTIMIZADO GENERADO!")
        print(f"🎯 Tema: {content_info['theme']}")
        print(f"📝 Texto: {content_info['text']}")
        print(f"🎨 Estilo: {content_info['style']}")
        
        print("\n💡 PRÓXIMOS PASOS:")
        print("1. 🎬 Generar video con Veo3 usando esta imagen")
        print("2. 📱 Subir a TikTok con hashtags optimizados")
        print("3. 📊 Monitorear rendimiento y ajustar")
        print("4. 🔄 Repetir proceso automáticamente")
        
    else:
        print("\n⚠️  No se pudo generar contenido optimizado")
        print("💡 Verifica la configuración de APIs")

if __name__ == "__main__":
    main()
