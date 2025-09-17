#!/usr/bin/env python3
"""
Orquestador de Subida Dual Automática
======================================
Este script gestiona la subida de videos a TikTok y YouTube Shorts,
reutilizando la lógica probada de los scripts individuales.
"""
import os
import time
import json
import random
from pathlib import Path
from datetime import datetime

def create_dynamic_description(video_path, video_map):
    """
    Genera una descripción dinámica y hashtags a partir del mapa de video.
    (Esta función es un duplicado de la que está en subir_tiktok_selenium_final_v5.py,
    idealmente debería estar en un módulo de utilidades para no repetir código).
    """
    video_filename = Path(video_path).name
    video_data = video_map.get(video_filename)

    if not video_data:
        # Si no hay datos, usar plantilla genérica
        return "Disfruta de esta experiencia visual y sonora.\n#asmr #satisfying #visuals #relax #fyp"

    prompt = video_data.get("prompt", "").lower()
    category = video_data.get("category", "asmr")
    # Extraer palabras clave del prompt
    keywords = []
    for word in ["asmr", "satisfying", "relax", "visual", "viral", "hipnótico", "adictivo", "colorido", "crujiente", "susurros", "tacto", "magia", "capibara", "miniatura", "dulce", "chocolate", "sonido", "arte", "cinematográfico"]:
        if word in prompt and word not in keywords:
            keywords.append(word)

    # Limitar a máximo 5 hashtags únicos y relevantes
    hashtags = [category] + keywords
    hashtags = [h.replace(" ", "") for h in hashtags if h]
    hashtags = list(dict.fromkeys(hashtags))[:5]
    hashtags_str = " ".join([f"#{tag}" for tag in hashtags])

    # Generar descripción dinámica basada en el prompt
    description_templates = [
        f"{video_data.get('title', 'Descubre una experiencia ASMR única')}. {prompt[:80]}...",
        f"¿Listo para relajarte? {prompt[:60]}...",
        f"Sumérgete en sonidos y visuales: {prompt[:60]}...",
        f"{video_data.get('sequence_title', 'Visuales hipnóticos y relajantes')}. {prompt[:60]}...",
        f"¿Te gustó este video? Comenta tu parte favorita."
    ]
    # Si el prompt es vacío, usar plantilla genérica, si no, usar dinámica
    if prompt.strip():
        description_text = random.choice(description_templates)
        return f'{description_text}\n\n{hashtags_str}'
    else:
        return "Disfruta de esta experiencia visual y sonora.\n#asmr #satisfying #visuals #relax #fyp"

def upload_tiktok_videos(video_map):
    """Sube todos los videos procesados a TikTok automáticamente."""
    print("\n[+] Iniciando subida a TikTok...")
    
    try:
        # Importar la lógica de subida probada
        from subir_tiktok_selenium_final_v5 import subir_video_selenium_xpaths_definitivos
        
        processed_folder = Path("data/videos/processed")
        videos_to_upload = list(processed_folder.glob("*.mp4"))
        
        if not videos_to_upload:
            print("[!] No se encontraron videos procesados para TikTok")
            return 0
        
        print(f"[i] Videos encontrados: {len(videos_to_upload)}")
        uploaded_count = 0
        for i, video_path in enumerate(videos_to_upload, 1):
            try:
                print(f"\n   -> Subiendo a TikTok {i}/{len(videos_to_upload)}: {video_path.name}")
                descripcion = create_dynamic_description(video_path, video_map)
                print(f"   -> Descripción generada: {descripcion.splitlines()[0]}...")

                if subir_video_selenium_xpaths_definitivos(str(video_path), descripcion):
                    print(f"   -> [+] TikTok upload {i} completado")
                    uploaded_count += 1
                else:
                    print(f"[!] Falló TikTok upload {i}")
                
                if i < len(videos_to_upload):
                    print("   -> Esperando 30 segundos...")
                    time.sleep(30)
            except Exception as e:
                print(f"[!] Error subiendo {video_path.name}: {e}")
        
        print(f"\n[+] Resumen TikTok: {uploaded_count}/{len(videos_to_upload)} videos subidos.")
        return uploaded_count
    except Exception as e:
        print(f"[!] Error general en la subida a TikTok: {e}")
        return 0

def upload_youtube_videos():
    """Sube todos los videos compilados a YouTube Shorts usando la lógica probada."""
    print("\n[+] Iniciando subida a YouTube Shorts...")
    
    try:
        # Importar la lógica de subida probada
        from upload_shorts_now import upload_single_video
        from youtube_uploader_real import YouTubeShortsUploaderReal as Uploader
        
        uploader = Uploader()
        if not uploader.auth_ok:
            print("[!] Error autenticando YouTube")
            return 0
        
        final_folder = Path("data/videos/final")
        fundido_videos = list(final_folder.glob("*FUNDIDO*.mp4"))
        
        if not fundido_videos:
            print("[!] No se encontraron videos compilados para YouTube")
            return 0
            
        print(f"[i] Videos encontrados: {len(fundido_videos)}")
        uploaded_count = 0
        for i, video_path in enumerate(fundido_videos, 1):
            try:
                print(f"\n   -> Subiendo a YouTube {i}/{len(fundido_videos)}: {video_path.name}")
                
                # Usar la función del script que ya funciona
                if upload_single_video(uploader, str(video_path)):
                    print(f"   -> [+] YouTube upload {i} completado")
                    uploaded_count += 1
                else:
                    print(f"[!] Falló YouTube upload {i}")

                if i < len(fundido_videos):
                    time.sleep(60)
            except Exception as e:
                print(f"[!] Error subiendo {video_path.name}: {e}")

        print(f"\n[+] Resumen YouTube: {uploaded_count}/{len(fundido_videos)} videos subidos.")
        return uploaded_count
    except Exception as e:
        print(f"[!] Error general en la subida a YouTube: {e}")
        return 0

def main():
    """Orquesta el proceso de subida dual."""
    print(">> INICIANDO ORQUESTADOR DE SUBIDA DUAL")
    print("========================================")
    start_time = datetime.now()
    print(f"   -> Iniciado: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        with open("video_prompt_map.json", "r", encoding="utf-8") as f:
            video_data_list = json.load(f)
        video_map = {Path(item["video"]).name: item for item in video_data_list}
    except Exception as e:
        print(f"[!] No se pudo cargar video_prompt_map.json ({e}).")
        video_map = {}

    tiktok_uploaded = upload_tiktok_videos(video_map)
    if tiktok_uploaded > 0:
        print("\n>> PAUSA ENTRE PLATAFORMAS (1 minuto)...")
        time.sleep(60)
    
    youtube_uploaded = upload_youtube_videos()
    
    end_time = datetime.now()
    print("\n" + "="*40)
    print("[+] REPORTE FINAL DE SUBIDA DUAL")
    print("="*40)
    print(f"   -> Finalizado: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   -> TikTok uploads: {tiktok_uploaded}")
    print(f"   -> YouTube uploads: {youtube_uploaded}")
    
    if (tiktok_uploaded + youtube_uploaded) > 0:
        print("\n[+] ¡Subida dual completada exitosamente!")
    else:
        print("[!] No se procesaron videos en esta ejecución.")

if __name__ == "__main__":
    main()
