#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 UNIFICADOR DE VIDEOS CON TRANSICIONES
📱 Combinar los 3 videos optimizados con efectos de transición para TikTok
"""

import subprocess
import os
import sys

def unir_videos_con_transiciones(videos_input, output_file, duracion_transicion=0.5):
    """
    Une múltiples videos con efectos de transición suaves
    
    Args:
        videos_input: Lista de videos de entrada
        output_file: Video de salida unificado
        duracion_transicion: Duración de cada transición en segundos
    """
    try:
        print(f"🎬 UNIENDO {len(videos_input)} VIDEOS CON TRANSICIONES")
        print("=" * 60)
        
        # Verificar que todos los videos existen
        for i, video in enumerate(videos_input, 1):
            if not os.path.exists(video):
                print(f"❌ Video {i} no encontrado: {video}")
                return False
            else:
                size_mb = os.path.getsize(video) / (1024 * 1024)
                print(f"✅ Video {i}: {os.path.basename(video)} ({size_mb:.1f} MB)")
        
        print(f"\n🎭 Configuración de transiciones:")
        print(f"   • Duración transición: {duracion_transicion}s")
        print(f"   • Efecto: Fade suave entre videos")
        print(f"   • Formato final: 720x1280 (TikTok)")
        
        # Construir filtros complejos de FFmpeg para transiciones
        # Cada video necesita ser procesado con fade in/out
        filtros = []
        inputs = []
        
        # Preparar inputs
        for i, video in enumerate(videos_input):
            inputs.extend(['-i', video])
        
        # Crear filtros de fade para cada video
        video_filters = []
        for i in range(len(videos_input)):
            if i == 0:
                # Primer video: solo fade out al final
                video_filters.append(f"[{i}:v]fade=t=out:st=end-{duracion_transicion}:d={duracion_transicion}[v{i}]")
            elif i == len(videos_input) - 1:
                # Último video: solo fade in al inicio
                video_filters.append(f"[{i}:v]fade=t=in:st=0:d={duracion_transicion}[v{i}]")
            else:
                # Videos del medio: fade in y fade out
                video_filters.append(f"[{i}:v]fade=t=in:st=0:d={duracion_transicion},fade=t=out:st=end-{duracion_transicion}:d={duracion_transicion}[v{i}]")
        
        # Crear filtros de audio
        audio_filters = []
        for i in range(len(videos_input)):
            if i == 0:
                audio_filters.append(f"[{i}:a]afade=t=out:st=end-{duracion_transicion}:d={duracion_transicion}[a{i}]")
            elif i == len(videos_input) - 1:
                audio_filters.append(f"[{i}:a]afade=t=in:st=0:d={duracion_transicion}[a{i}]")
            else:
                audio_filters.append(f"[{i}:a]afade=t=in:st=0:d={duracion_transicion},afade=t=out:st=end-{duracion_transicion}:d={duracion_transicion}[a{i}]")
        
        # Concatenar videos y audios
        video_concat = "".join([f"[v{i}]" for i in range(len(videos_input))]) + f"concat=n={len(videos_input)}:v=1:a=0[vout]"
        audio_concat = "".join([f"[a{i}]" for i in range(len(videos_input))]) + f"concat=n={len(videos_input)}:v=0:a=1[aout]"
        
        # Filtro completo
        filter_complex = ";".join(video_filters + audio_filters + [video_concat, audio_concat])
        
        print(f"\n🚀 Procesando unión con transiciones...")
        print(f"📐 Aplicando {len(videos_input)-1} transiciones de {duracion_transicion}s cada una")
        
        # Comando FFmpeg completo
        cmd = inputs + [
            '-filter_complex', filter_complex,
            '-map', '[vout]',
            '-map', '[aout]',
            '-c:v', 'libx264',
            '-preset', 'medium', 
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-y',
            output_file
        ]
        
        # Ejecutar comando
        result = subprocess.run(['ffmpeg'] + cmd[1:], capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ ¡UNIÓN EXITOSA CON TRANSICIONES!")
                print(f"✅ Creado: {os.path.basename(output_file)} ({size_mb:.1f} MB)")
                return True
            else:
                print("❌ Error: archivo no creado")
                return False
        else:
            print(f"❌ Error FFmpeg: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def crear_version_alternativa(videos_input, output_file):
    """
    Versión alternativa con transición crossfade más avanzada
    """
    try:
        print(f"\n🎨 CREANDO VERSIÓN ALTERNATIVA CON CROSSFADE")
        print("=" * 60)
        
        # Método alternativo: crossfade entre videos
        inputs = []
        for video in videos_input:
            inputs.extend(['-i', video])
        
        # Filtro crossfade para 3 videos
        if len(videos_input) == 3:
            filter_complex = (
                "[0:v][1:v]xfade=transition=fade:duration=0.8:offset=5[vfade1];"
                "[vfade1][2:v]xfade=transition=fade:duration=0.8:offset=10[vout];"
                "[0:a][1:a]acrossfade=d=0.8:o1=5:o2=0[afade1];"
                "[afade1][2:a]acrossfade=d=0.8:o1=10:o2=0[aout]"
            )
        else:
            print("⚠️  Versión alternativa optimizada para 3 videos")
            return False
        
        cmd = ['ffmpeg'] + inputs + [
            '-filter_complex', filter_complex,
            '-map', '[vout]',
            '-map', '[aout]',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23', 
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-y',
            output_file
        ]
        
        print("🚀 Procesando crossfade avanzado...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ ¡CROSSFADE EXITOSO!")
                print(f"✅ Creado: {os.path.basename(output_file)} ({size_mb:.1f} MB)")
                return True
        
        print(f"❌ Error en crossfade: {result.stderr}")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎬 UNIFICADOR DE VIDEOS CON TRANSICIONES")
    print("📱 Combinar videos optimizados para TikTok")
    print("🎭 Efectos de transición profesionales")
    print("=" * 65)
    
    # Videos finales optimizados
    videos_finales = [
        "veo_video_20250901_190803_tiktok_FINAL.mp4",
        "veo_video_20250901_190857_tiktok_FINAL.mp4", 
        "veo_video_20250901_191001_tiktok_FINAL.mp4"
    ]
    
    print(f"🎬 Videos a unir:")
    videos_existentes = []
    for i, video in enumerate(videos_finales, 1):
        if os.path.exists(video):
            size_mb = os.path.getsize(video) / (1024 * 1024)
            print(f"   {i}. {video} ({size_mb:.1f} MB)")
            videos_existentes.append(video)
        else:
            print(f"   {i}. ❌ {video} (no encontrado)")
    
    if len(videos_existentes) < 2:
        print("\n❌ Se necesitan al menos 2 videos para unir")
        return
    
    print(f"\n🎭 CREANDO VERSIONES CON DIFERENTES TRANSICIONES:")
    print("=" * 65)
    
    # Versión 1: Fade suave
    output_fade = "videos_unidos_fade_TIKTOK.mp4"
    print(f"\n📀 Versión 1: Transiciones Fade Suaves")
    if unir_videos_con_transiciones(videos_existentes, output_fade, 0.5):
        print(f"🎉 Versión Fade completada!")
    
    # Versión 2: Crossfade avanzado
    output_crossfade = "videos_unidos_crossfade_TIKTOK.mp4"
    print(f"\n📀 Versión 2: Crossfade Avanzado")
    if crear_version_alternativa(videos_existentes, output_crossfade):
        print(f"🎉 Versión Crossfade completada!")
    
    print("\n" + "=" * 65)
    print("🎉 UNIFICACIÓN COMPLETADA")
    print("=" * 65)
    
    # Mostrar resultados
    videos_unidos = []
    for output in [output_fade, output_crossfade]:
        if os.path.exists(output):
            size_mb = os.path.getsize(output) / (1024 * 1024)
            videos_unidos.append((output, size_mb))
    
    if videos_unidos:
        print("🎬 VIDEOS UNIDOS CREADOS:")
        for i, (video, size) in enumerate(videos_unidos, 1):
            print(f"   {i}. {video} ({size:.1f} MB)")
        
        print(f"\n🎯 Características:")
        print(f"   • Formato: 720x1280 (TikTok)")
        print(f"   • Transiciones suaves entre videos")
        print(f"   • Audio sincronizado con fades")
        print(f"   • Optimizado para móvil")
        
        print(f"\n📱 ¡Listos para subir a TikTok!")
        print(f"💡 Elige la versión de transición que más te guste")
        
    else:
        print("❌ No se crearon videos unidos")

if __name__ == "__main__":
    main()
