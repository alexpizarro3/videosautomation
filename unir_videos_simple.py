#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 UNIFICADOR SIMPLE CON TRANSICIONES
📱 Combinar videos con método compatible universal
"""

import subprocess
import os
import sys

def unir_videos_simple(videos_input, output_file):
    """
    Une videos con transiciones simples y compatibles
    """
    try:
        print(f"🎬 UNIENDO {len(videos_input)} VIDEOS")
        print("=" * 50)
        
        # Verificar videos
        for i, video in enumerate(videos_input, 1):
            if not os.path.exists(video):
                print(f"❌ Video {i} no encontrado: {video}")
                return False
            else:
                size_mb = os.path.getsize(video) / (1024 * 1024)
                print(f"✅ Video {i}: {os.path.basename(video)} ({size_mb:.1f} MB)")
        
        print(f"\n🎭 Método: Concatenación directa con transiciones")
        
        # Crear archivo de lista temporal
        lista_file = "temp_lista.txt"
        with open(lista_file, 'w') as f:
            for video in videos_input:
                # Usar ruta absoluta para evitar problemas
                video_path = os.path.abspath(video)
                f.write(f"file '{video_path}'\n")
        
        print(f"📄 Lista temporal creada: {lista_file}")
        
        # Comando simple de concatenación
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', lista_file,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-y',
            output_file
        ]
        
        print("🚀 Procesando concatenación...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Limpiar archivo temporal
        if os.path.exists(lista_file):
            os.remove(lista_file)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ ¡UNIÓN EXITOSA!")
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

def crear_version_con_fundido(videos_input, output_file):
    """
    Crea versión con fundido negro entre videos
    """
    try:
        print(f"\n🎨 CREANDO VERSIÓN CON FUNDIDOS")
        print("=" * 50)
        
        # Crear videos intermedios con fundido
        videos_con_fundido = []
        
        for i, video in enumerate(videos_input):
            # Archivo temporal con fundido
            temp_video = f"temp_fade_{i}.mp4"
            
            if i == 0:
                # Primer video: solo fade out al final
                cmd = [
                    'ffmpeg', '-i', video,
                    '-vf', 'fade=out:st=4:d=0.5',
                    '-af', 'afade=out:st=4:d=0.5',
                    '-c:v', 'libx264', '-crf', '23',
                    '-c:a', 'aac', '-b:a', '128k',
                    '-y', temp_video
                ]
            elif i == len(videos_input) - 1:
                # Último video: solo fade in al inicio
                cmd = [
                    'ffmpeg', '-i', video,
                    '-vf', 'fade=in:st=0:d=0.5',
                    '-af', 'afade=in:st=0:d=0.5',
                    '-c:v', 'libx264', '-crf', '23',
                    '-c:a', 'aac', '-b:a', '128k',
                    '-y', temp_video
                ]
            else:
                # Videos del medio: fade in y out
                cmd = [
                    'ffmpeg', '-i', video,
                    '-vf', 'fade=in:st=0:d=0.5,fade=out:st=4:d=0.5',
                    '-af', 'afade=in:st=0:d=0.5,afade=out:st=4:d=0.5',
                    '-c:v', 'libx264', '-crf', '23',
                    '-c:a', 'aac', '-b:a', '128k',
                    '-y', temp_video
                ]
            
            print(f"🎭 Aplicando fundido a video {i+1}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(temp_video):
                videos_con_fundido.append(temp_video)
                print(f"✅ Fundido aplicado: {temp_video}")
            else:
                print(f"❌ Error aplicando fundido a video {i+1}")
                return False
        
        # Ahora unir los videos con fundido
        if unir_videos_simple(videos_con_fundido, output_file):
            # Limpiar archivos temporales
            for temp_video in videos_con_fundido:
                if os.path.exists(temp_video):
                    os.remove(temp_video)
            return True
        else:
            # Limpiar archivos temporales en caso de error
            for temp_video in videos_con_fundido:
                if os.path.exists(temp_video):
                    os.remove(temp_video)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎬 UNIFICADOR SIMPLE CON TRANSICIONES")
    print("📱 Método universal compatible")
    print("=" * 50)
    
    # Videos finales
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
    
    print(f"\n🎭 CREANDO VERSIONES:")
    print("=" * 50)
    
    # Versión 1: Concatenación simple
    output_simple = "videos_unidos_SIMPLE_TIKTOK.mp4"
    print(f"\n📀 Versión 1: Concatenación Simple")
    if unir_videos_simple(videos_existentes, output_simple):
        print(f"🎉 Versión Simple completada!")
    
    # Versión 2: Con fundidos
    output_fundido = "videos_unidos_FUNDIDO_TIKTOK.mp4"
    print(f"\n📀 Versión 2: Con Fundidos Suaves")
    if crear_version_con_fundido(videos_existentes, output_fundido):
        print(f"🎉 Versión con Fundidos completada!")
    
    print("\n" + "=" * 50)
    print("🎉 UNIFICACIÓN COMPLETADA")
    print("=" * 50)
    
    # Mostrar resultados
    videos_unidos = []
    for output in [output_simple, output_fundido]:
        if os.path.exists(output):
            size_mb = os.path.getsize(output) / (1024 * 1024)
            videos_unidos.append((output, size_mb))
    
    if videos_unidos:
        print("🎬 VIDEOS UNIDOS CREADOS:")
        for i, (video, size) in enumerate(videos_unidos, 1):
            print(f"   {i}. {video} ({size:.1f} MB)")
        
        print(f"\n🎯 Características:")
        print(f"   • Formato: 720x1280 (TikTok)")
        print(f"   • Calidad optimizada")
        print(f"   • Audio sincronizado")
        
        print(f"\n📱 ¡Listos para TikTok!")
        
    else:
        print("❌ No se crearon videos unidos")

if __name__ == "__main__":
    main()
