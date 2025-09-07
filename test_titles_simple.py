#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST TÍTULOS SIMPLES
Versión simplificada para probar títulos sin dependencias complejas
"""

import random

def generate_viral_title():
    """
    Generar título viral sin importar la clase completa
    """
    # Templates de títulos virales
    viral_templates = [
        "🤯 ESTO TE VA A VOLAR LA MENTE | Contenido Viral #Shorts",
        "😱 NO VAS A CREER LO QUE PASÓ | Viral TikTok #Shorts", 
        "🔥 ESTO ES UNA BOMBA VIRAL | IA Increíble #Shorts",
        "💥 CONTENIDO QUE ROMPE INTERNET | Viral #Shorts",
        "🚀 ESTO VA A SER VIRAL | Increíble IA #Shorts",
        "⚡ CONTENIDO EXPLOSIVO VIRAL | TikTok #Shorts",
        "🎯 ESTO ES PURO FUEGO | Viral Content #Shorts",
        "🌟 INCREÍBLE CONTENIDO VIRAL | IA #Shorts",
        "🎭 ESTO TE VA A SORPRENDER | Viral #Shorts",
        "🔴 VIRAL: CONTENIDO ÉPICO | IA TikTok #Shorts"
    ]
    
    return random.choice(viral_templates)

def test_viral_titles():
    """
    Probar generación de títulos virales
    """
    print("🧪 TEST: TÍTULOS VIRALES SIMPLES")
    print("=" * 60)
    
    print("📰 TÍTULOS GENERADOS:")
    print("-" * 50)
    
    for i in range(5):
        title = generate_viral_title()
        print(f"{i+1}. {title}")
    
    print("\n✅ CARACTERÍSTICAS DE LOS TÍTULOS:")
    print("   🎯 NO revelan contenido específico")
    print("   🔥 Palabras virales (VIRAL, INCREÍBLE, BOMBA)")
    print("   😱 Emojis llamativos")
    print("   📱 Optimizados para #Shorts")
    print("   🚀 Generan curiosidad")
    print("   ⚠️ CRÍTICO: madeForKids=False (NO para niños)")

if __name__ == "__main__":
    test_viral_titles()
