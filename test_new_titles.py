#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST NUEVOS TÍTULOS VIRALES
Probar los nuevos títulos mejorados para YouTube Shorts
"""

from youtube_shorts_uploader import YouTubeShortsUploader

def test_new_titles():
    """
    Probar los nuevos títulos virales
    """
    print("🧪 TEST: NUEVOS TÍTULOS VIRALES")
    print("=" * 60)
    
    uploader = YouTubeShortsUploader()
    
    # Test con diferentes nombres de archivo
    test_files = [
        "videos_unidos_FUNDIDO_TIKTOK.mp4",
        "content_viral_FUNDIDO.mp4", 
        "amazing_video_FUNDIDO.mp4"
    ]
    
    print("📰 NUEVOS TÍTULOS GENERADOS:")
    print("-" * 50)
    
    for i, filename in enumerate(test_files, 1):
        title = uploader.generate_title_from_filename(filename)
        print(f"{i}. Archivo: {filename}")
        print(f"   Título: {title}")
        print()
    
    print("✅ CARACTERÍSTICAS DE LOS NUEVOS TÍTULOS:")
    print("   🎯 NO revelan contenido específico")
    print("   🔥 Palabras virales (VIRAL, INCREÍBLE, BOMBA)")
    print("   😱 Emojis llamativos")
    print("   📱 Optimizados para #Shorts")
    print("   🚀 Generan curiosidad")
    print("   ⚠️ CRÍTICO: madeForKids=False (NO para niños)")
    
    print("\n🆚 COMPARACIÓN:")
    print("   ❌ ANTES: '🔥 videos unidos TIKTOK | Contenido Viral IA #Shorts'")
    print("   ✅ AHORA: '🤯 ESTO TE VA A VOLAR LA MENTE | Contenido Viral #Shorts'")

def test_multiple_title_generation():
    """
    Generar múltiples títulos para el mismo archivo
    """
    print("\n🔄 TEST: MÚLTIPLES TÍTULOS PARA EL MISMO ARCHIVO")
    print("=" * 60)
    
    uploader = YouTubeShortsUploader()
    filename = "videos_unidos_FUNDIDO_TIKTOK.mp4"
    
    print(f"📁 Archivo: {filename}")
    print("📰 Generando 5 títulos diferentes:\n")
    
    for i in range(5):
        title = uploader.generate_title_from_filename(filename)
        print(f"{i+1}. {title}")
    
    print("\n💡 NOTA: Cada título es único gracias a la selección aleatoria")

if __name__ == "__main__":
    test_new_titles()
    test_multiple_title_generation()
