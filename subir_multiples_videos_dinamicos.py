#!/usr/bin/env python3
"""
🎯 UPLOADER MÚLTIPLES VIDEOS CON DESCRIPCIONES DINÁMICAS
Sistema que procesa automáticamente todos los videos del video_prompt_map.json
y genera descripciones únicas para cada uno basadas en su contenido específico.
"""

import json
import os
import time
from subir_tiktok_selenium_final_v5 import (
    subir_video_selenium_xpaths_definitivos,
    generar_descripcion_dinamica,
    cargar_video_prompt_map,
    obtener_prompt_para_video
)

def procesar_todos_los_videos():
    """Procesar todos los videos del mapeo con descripciones dinámicas"""
    print("🚀 SISTEMA DE UPLOAD MASIVO CON DESCRIPCIONES DINÁMICAS")
    print("=" * 70)
    
    # Cargar mapeo de videos
    video_map = cargar_video_prompt_map()
    
    if not video_map:
        print("❌ No se encontró video_prompt_map.json o está vacío")
        return
    
    print(f"📋 Videos encontrados en el mapeo: {len(video_map)}")
    
    videos_procesados = 0
    videos_exitosos = 0
    videos_fallidos = 0
    
    for i, video_entry in enumerate(video_map, 1):
        video_path = video_entry.get("video", "")
        prompt_original = video_entry.get("prompt", "")
        
        print(f"\n🎯 PROCESANDO VIDEO {i}/{len(video_map)}")
        print("=" * 50)
        print(f"📹 Video: {os.path.basename(video_path)}")
        
        # Verificar que el archivo existe
        if not os.path.exists(video_path):
            print(f"❌ Archivo no encontrado: {video_path}")
            videos_fallidos += 1
            continue
        
        # Generar descripción dinámica específica
        descripcion = generar_descripcion_dinamica(video_path, prompt_original)
        
        print(f"\n📝 DESCRIPCIÓN GENERADA:")
        print("-" * 30)
        print(descripcion)
        print("-" * 30)
        
        # Confirmar antes de subir
        respuesta = input(f"\n¿Subir este video? (s/n/q para salir): ").lower().strip()
        
        if respuesta == 'q':
            print("🛑 Proceso cancelado por el usuario")
            break
        elif respuesta != 's':
            print("⏭️ Video saltado")
            continue
        
        # Subir video
        print(f"\n🚀 Subiendo video {i}...")
        resultado = subir_video_selenium_xpaths_definitivos(video_path, descripcion)
        
        videos_procesados += 1
        
        if resultado:
            print(f"✅ Video {i} subido exitosamente!")
            videos_exitosos += 1
        else:
            print(f"❌ Error subiendo video {i}")
            videos_fallidos += 1
        
        # Pausa entre videos para evitar detección
        if i < len(video_map):
            print(f"\n⏳ Pausa de 60 segundos antes del siguiente video...")
            for j in range(12):
                print(f"   {60-j*5}s restantes...")
                time.sleep(5)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DEL PROCESO")
    print("=" * 70)
    print(f"Videos procesados: {videos_procesados}")
    print(f"Videos exitosos: {videos_exitosos}")
    print(f"Videos fallidos: {videos_fallidos}")
    print(f"Tasa de éxito: {videos_exitosos/videos_procesados*100 if videos_procesados > 0 else 0:.1f}%")

def subir_video_individual():
    """Subir un video individual con descripción dinámica"""
    print("🎯 UPLOAD INDIVIDUAL CON DESCRIPCIÓN DINÁMICA")
    print("=" * 50)
    
    # Mostrar videos disponibles
    video_map = cargar_video_prompt_map()
    
    if not video_map:
        print("❌ No se encontró video_prompt_map.json")
        return
    
    print("📋 Videos disponibles:")
    for i, entry in enumerate(video_map, 1):
        video_path = entry.get("video", "")
        print(f"{i}. {os.path.basename(video_path)}")
    
    # Seleccionar video
    try:
        seleccion = int(input(f"\nSelecciona un video (1-{len(video_map)}): "))
        if 1 <= seleccion <= len(video_map):
            video_entry = video_map[seleccion - 1]
            video_path = video_entry.get("video", "")
            prompt_original = video_entry.get("prompt", "")
            
            # Verificar archivo
            if not os.path.exists(video_path):
                print(f"❌ Archivo no encontrado: {video_path}")
                return
            
            # Generar descripción
            descripcion = generar_descripcion_dinamica(video_path, prompt_original)
            
            print(f"\n📝 DESCRIPCIÓN GENERADA:")
            print("-" * 30)
            print(descripcion)
            print("-" * 30)
            
            # Confirmar
            if input("\n¿Subir este video? (s/n): ").lower().strip() == 's':
                resultado = subir_video_selenium_xpaths_definitivos(video_path, descripcion)
                
                if resultado:
                    print("✅ ¡Video subido exitosamente!")
                else:
                    print("❌ Error subiendo el video")
            else:
                print("🛑 Upload cancelado")
        else:
            print("❌ Selección inválida")
    except ValueError:
        print("❌ Por favor ingresa un número válido")

def main():
    """Función principal del sistema de upload masivo"""
    print("🚀 SISTEMA DE UPLOAD CON DESCRIPCIONES DINÁMICAS")
    print("=" * 60)
    print("1. Subir todos los videos automáticamente")
    print("2. Subir un video individual")
    print("3. Salir")
    
    try:
        opcion = int(input("\nSelecciona una opción (1-3): "))
        
        if opcion == 1:
            procesar_todos_los_videos()
        elif opcion == 2:
            subir_video_individual()
        elif opcion == 3:
            print("👋 ¡Hasta luego!")
        else:
            print("❌ Opción inválida")
    except ValueError:
        print("❌ Por favor ingresa un número válido")

if __name__ == "__main__":
    main()
