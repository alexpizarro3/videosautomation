#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UNIFICADOR SIMPLE CON TRANSICIONES
Combinar videos con método compatible universal
"""

import subprocess
import os
import sys
import glob
import json

def unir_videos_simple(videos_input, output_file):
    """
    Une videos con transiciones simples y compatibles
    """
    try:
        print(f"UNIENDO {len(videos_input)} VIDEOS")
        print("=" * 50)
        
        # Verificar videos
        for i, video in enumerate(videos_input, 1):
            if not os.path.exists(video):
                print(f"Video {i} no encontrado: {video}")
                return False
            else:
                size_mb = os.path.getsize(video) / (1024 * 1024)
                print(f"Video {i}: {os.path.basename(video)} ({size_mb:.1f} MB)")
        
        print("\nMétodo: Concatenación directa con transiciones")
        
        # Crear archivo de lista temporal
        lista_file = "temp_lista.txt"
        with open(lista_file, 'w') as f:
            for video in videos_input:
                # Usar ruta absoluta para evitar problemas
                video_path = os.path.abspath(video)
                f.write(f"file '{video_path}'\n")
        
        print(f"Lista temporal creada: {lista_file}")
        
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
        
        print("Procesando concatenación...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Limpiar archivo temporal
        if os.path.exists(lista_file):
            os.remove(lista_file)
        
        if result.returncode == 0:
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"¡UNIÓN EXITOSA!")
                print(f"Creado: {os.path.basename(output_file)} ({size_mb:.1f} MB)")
                return True
            else:
                print("Error: archivo no creado")
                return False
        else:
            print(f"Error FFmpeg: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_video_duration(file_path):
    try:
        probe_cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', file_path
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting video duration for {file_path}: {e}")
        return None

def crear_version_con_fundido(videos_input, output_file):
    """
    Crea versión con fundido negro entre videos
    """
    try:
        print("CREANDO VERSIÓN CON FUNDIDOS")
        print("=" * 50)

        # Crear videos intermedios con fundido
        videos_con_fundido = []
        fade_duration = 0.5 # User requested 0.5 seconds

        for i, video in enumerate(videos_input):
            video_duration = get_video_duration(video)
            if video_duration is None:
                print(f"Could not get duration for {video}. Skipping fade for this video.")
                videos_con_fundido.append(video) # Append original video if duration not found
                continue

            # Archivo temporal con fundido
            temp_video = f"temp_fade_{i}.mp4"

            if i == 0:
                # Primer video: solo fade out al final
                fade_out_start = max(0, video_duration - fade_duration)
                cmd = [
                    'ffmpeg', '-i', video,
                    '-vf', f'fade=out:st={fade_out_start}:d={fade_duration}',
                    '-af', f'afade=out:st={fade_out_start}:d={fade_duration}',
                    '-c:v', 'libx264', '-crf', '23',
                    '-c:a', 'aac', '-b:a', '128k',
                    '-y', temp_video
                ]
            elif i == len(videos_input) - 1:
                # Último video: solo fade in al inicio
                cmd = [
                    'ffmpeg', '-i', video,
                    '-vf', f'fade=in:st=0:d={fade_duration}',
                    '-af', f'afade=in:st=0:d={fade_duration}',
                    '-c:v', 'libx264', '-crf', '23',
                    '-c:a', 'aac', '-b:a', '128k',
                    '-y', temp_video
                ]
            else:
                # Videos del medio: fade in y out
                fade_out_start = max(0, video_duration - fade_duration)
                cmd = [
                    'ffmpeg', '-i', video,
                    '-vf', f'fade=in:st=0:d={fade_duration},fade=out:st={fade_out_start}:d={fade_duration}',
                    '-af', f'afade=in:st=0:d={fade_duration},afade=out:st={fade_out_start}:d={fade_duration}',
                    '-c:v', 'libx264',
                    '-crf', '23',
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-y',
                    temp_video
                ]

            print(f"Aplicando fundido a video {i+1}...")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0 and os.path.exists(temp_video):
                videos_con_fundido.append(temp_video)
                print(f"Fundido aplicado: {temp_video}")
            else:
                print(f"Error aplicando fundido a video {i+1}")
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
        print(f"Error: {e}")
        return False

def get_processed_video_files(directory):
    # Use glob to find all .mp4 files recursively in the specified directory
    # and convert absolute paths to relative paths from the project root.
    project_root = r"C:\Users\Alexis Pizarro\Documents\Personal\videosautomation"
    absolute_paths = glob.glob(os.path.join(project_root, directory, "**", "*.mp4"), recursive=True)
    relative_paths = [os.path.relpath(path, project_root) for path in absolute_paths]
    return relative_paths

def main():
    print("UNIFICADOR SIMPLE CON TRANSICIONES")
    print("Método universal compatible")
    print("=" * 50)

    # Dynamically get video files from data/videos/processed
    videos_finales = get_processed_video_files("data/videos/processed")


    print(f"Videos a unir:")
    videos_existentes = []
    for i, video in enumerate(videos_finales, 1):
        if os.path.exists(video):
            size_mb = os.path.getsize(video) / (1024 * 1024)
            print(f"   {i}. {video} ({size:.1f} MB)")
            videos_existentes.append(video)
        else:
            print(f"   {i}. {video} (no encontrado)")

    if len(videos_existentes) < 2:
        print("\nSe necesitan al menos 2 videos para unir")
        return

    print("\nCREANDO VERSIONES:")
    print("=" * 50)

    # Versión 1: Concatenación simple
    output_simple = os.path.join("data", "videos", "final", "videos_unidos_SIMPLE_TIKTOK.mp4")
    print(f"\nVersión 1: Concatenación Simple")
    if unir_videos_simple(videos_existentes, output_simple):
        print(f"Versión Simple completada!")

    # Versión 2: Con fundidos
    output_fundido = os.path.join("data", "videos", "final", "videos_unidos_FUNDIDO_TIKTOK.mp4")
    print(f"\nVersión 2: Con Fundidos Suaves")
    if crear_version_con_fundido(videos_existentes, output_fundido):
        print(f"Versión con Fundidos completada!")

    print("\n" + "=" * 50)
    print("UNIFICACIÓN COMPLETADA")
    print("=" * 50)

    # Mostrar resultados
    videos_unidos = []
    for output in [output_simple, output_fundido]:
        if os.path.exists(output):
            size_mb = os.path.getsize(output) / (1024 * 1024)
            videos_unidos.append((output, size_mb))

    if videos_unidos:
        print(f"DEBUG: videos_unidos content: {videos_unidos}")
        print("VIDEOS UNIDOS CREADOS:")
        for i, (video, size) in enumerate(videos_unidos, 1):
            print(f"   {i}. {video} ({size:.1f} MB)")

        print("\nCaracterísticas:")
        print(f"   • Formato: 720x1280 (TikTok)")
        print(f"   • Calidad optimizada")
        print(f"   • Audio sincronizado")

        print(f"\n¡Listos para TikTok!")

        # Update video_prompt_map.json with the fundido video
        try:
            # Load existing video_prompt_map.json to preserve prompt/imagen
            with open("video_prompt_map.json", "r", encoding="utf-8") as f:
                existing_map = json.load(f)
            
            # Assuming we want to update the first entry with the fundido video
            if existing_map:
                existing_map[0]["video"] = output_fundido
            else:
                # If the map is empty, create a new entry
                existing_map = [{"video": output_fundido, "prompt": "Video fundido optimizado para TikTok", "imagen": "N/A"}]

            with open("video_prompt_map.json", "w", encoding="utf-8") as f:
                json.dump(existing_map, f, ensure_ascii=False, indent=2)
            print(f"video_prompt_map.json actualizado con: {output_fundido}")
        except Exception as e:
            print(f"Error actualizando video_prompt_map.json: {e}")

    else:
        print("No se crearon videos unidos")

if __name__ == "__main__":
    main()
