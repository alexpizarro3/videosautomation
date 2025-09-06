#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ANALIZADOR Y PREPARADOR DE PIPELINE DE VIDEO VIRAL
Script auxiliar para preparar el pipeline completo de generación de videos virales
Analiza imágenes existentes y prepara metadatos para optimizar los prompts de video
"""

import os
import sys
import json
from datetime import datetime
from image_metadata_analyzer import ImageMetadataAnalyzer, analyze_existing_images, save_image_analysis_report
from viral_video_prompt_generator import ViralVideoPromptGenerator

def analyze_images_for_video_pipeline():
    """
    Analiza todas las imágenes existentes para preparar el pipeline de video
    """
    print("🔍 PREPARADOR DE PIPELINE DE VIDEO VIRAL")
    print("=" * 60)
    
    print("🎯 PASO 1: Analizando imágenes existentes...")
    
    # Analizar todas las imágenes
    analysis = analyze_existing_images()
    
    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        return False
    
    # Guardar reporte detallado
    report_path = save_image_analysis_report(analysis)
    
    print(f"\n📊 RESULTADOS DEL ANÁLISIS:")
    print(f"   Total de imágenes: {analysis['total_images']}")
    print(f"   Análisis exitosos: {analysis['successful_analyses']}")
    print(f"   Errores: {analysis['failed_analyses']}")
    
    # Mostrar temáticas detectadas
    if analysis['successful_analyses'] > 0:
        print(f"\n🎭 TEMÁTICAS DETECTADAS:")
        themes = []
        colors = []
        moods = []
        
        for image_path, data in analysis['images'].items():
            if data.get('analysis_success'):
                theme = data.get('tema_principal', 'N/A')
                image_colors = data.get('colores_dominantes', [])
                mood = data.get('mood', 'N/A')
                
                themes.append(theme)
                colors.extend(image_colors)
                moods.append(mood)
                
                print(f"   • {os.path.basename(image_path)}:")
                print(f"     Tema: {theme}")
                print(f"     Colores: {', '.join(image_colors[:3])}")
                print(f"     Mood: {mood}")
                print(f"     Categoría viral: {data.get('categoria_viral', 'N/A')}")
        
        # Resumen consolidado
        print(f"\n📈 RESUMEN CONSOLIDADO:")
        
        # Temáticas más comunes
        theme_counts = {}
        for theme in themes:
            if theme and theme != 'N/A':
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        if theme_counts:
            most_common_theme = max(theme_counts.items(), key=lambda x: x[1])[0]
            print(f"   🎯 Tema dominante: {most_common_theme}")
        
        # Colores más usados
        color_counts = {}
        for color in colors:
            if color:
                color_counts[color] = color_counts.get(color, 0) + 1
        
        if color_counts:
            top_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"   🎨 Colores principales: {', '.join([c[0] for c in top_colors])}")
        
        # Moods más frecuentes
        mood_counts = {}
        for mood in moods:
            if mood and mood != 'N/A':
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        if mood_counts:
            most_common_mood = max(mood_counts.items(), key=lambda x: x[1])[0]
            print(f"   🎭 Mood dominante: {most_common_mood}")
    
    print(f"\n💾 Reporte guardado: {report_path}")
    
    return True

def check_pipeline_readiness():
    """
    Verifica si el pipeline está listo para generar videos virales
    """
    print(f"\n🔧 PASO 2: Verificando preparación del pipeline...")
    
    # Verificar archivos necesarios
    required_files = [
        "data/analytics/fusion_prompts_auto.json",
        "viral_video_prompt_generator.py",
        "image_metadata_analyzer.py",
        "generate_veo_video_from_image.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    
    # Verificar imágenes disponibles
    images = [f"data/images/gemini_image_{i+1}.png" for i in range(6)]
    available_images = [img for img in images if os.path.exists(img)]
    
    if not available_images:
        print(f"❌ No se encontraron imágenes para procesar")
        return False
    
    print(f"✅ Pipeline listo para generar videos virales")
    print(f"   📁 Archivos necesarios: ✅")
    print(f"   🖼️  Imágenes disponibles: {len(available_images)}")
    print(f"   🎬 Generador de prompts: ✅")
    print(f"   🔍 Analizador de metadatos: ✅")
    
    return True

def generate_enhanced_prompts():
    """
    Genera prompts profesionales usando el sistema viral
    """
    print(f"\n🎬 PASO 3: Generando prompts profesionales...")
    
    try:
        # Cargar prompts base
        with open("data/analytics/fusion_prompts_auto.json", "r", encoding="utf-8") as f:
            prompts_data = json.load(f)
        
        base_prompts = prompts_data.get("prompts", [])
        if not base_prompts:
            print("❌ No se encontraron prompts base")
            return False
        
        # Inicializar generador
        generator = ViralVideoPromptGenerator()
        
        # Generar prompts profesionales
        enhanced_prompts = []
        
        print(f"   Procesando {len(base_prompts[:3])} prompts base...")
        
        for i, base_prompt in enumerate(base_prompts[:3]):
            print(f"   Generando prompt profesional {i+1}/3...")
            
            # Generar prompt profesional
            result = generator.generate_professional_prompt(
                base_image_prompt=base_prompt,
                viral_category="asmr",  # Categoría por defecto
                style_preference="dreamy_pastels",
                complexity_level="professional"
            )
            
            enhanced_prompts.append(result)
        
        # Guardar prompts mejorados
        os.makedirs("data/analytics", exist_ok=True)
        output_file = "data/analytics/fusion_prompts_auto_enhanced.json"
        
        enhanced_data = {
            "enhanced_prompts": enhanced_prompts,
            "generation_info": {
                "total_prompts": len(enhanced_prompts),
                "generation_date": datetime.now().isoformat(),
                "system_version": "Professional Viral Prompts v2.0"
            }
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {len(enhanced_prompts)} prompts profesionales generados")
        print(f"💾 Guardados en: {output_file}")
        
        # Mostrar resumen de scores
        scores = [p["metadata"]["predicted_engagement"] for p in enhanced_prompts]
        avg_score = sum(scores) / len(scores)
        
        print(f"📊 Score viral promedio: {avg_score:.1f}/100")
        print(f"🏆 Mejor score: {max(scores)}/100")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando prompts: {e}")
        return False

def main():
    """
    Función principal del preparador de pipeline
    """
    print("🚀 INICIANDO PREPARACIÓN COMPLETA DEL PIPELINE")
    print("=" * 60)
    
    # Paso 1: Analizar imágenes
    step1_success = analyze_images_for_video_pipeline()
    
    if not step1_success:
        print("❌ Error en análisis de imágenes. Abortando.")
        return
    
    # Paso 2: Verificar preparación
    step2_success = check_pipeline_readiness()
    
    if not step2_success:
        print("❌ Pipeline no está listo. Revisar archivos faltantes.")
        return
    
    # Paso 3: Generar prompts profesionales
    step3_success = generate_enhanced_prompts()
    
    if not step3_success:
        print("❌ Error generando prompts profesionales.")
        return
    
    # Resumen final
    print(f"\n🎉 PIPELINE COMPLETAMENTE PREPARADO")
    print("=" * 60)
    print("✅ Análisis de imágenes completado")
    print("✅ Archivos verificados")
    print("✅ Prompts profesionales generados")
    print(f"\n🎬 PRÓXIMO PASO:")
    print("   Ejecutar: python generate_veo_video_from_image.py")
    print("   para generar videos virales profesionales")

if __name__ == "__main__":
    main()
