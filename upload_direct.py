#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 UPLOAD DIRECTO YOUTUBE SHORTS
Script simplificado para upload directo sin dependencias complejas
"""

import os
import json
import logging
from datetime import datetime
import random

# YouTube API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_authenticated_service():
    """
    Obtener servicio autenticado de YouTube
    """
    credentials = None
    token_file = "config/youtube_token.json"
    
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            # Guardar credenciales actualizadas
            with open(token_file, 'w') as f:
                f.write(credentials.to_json())
        else:
            print("❌ Credenciales no válidas. Ejecuta test_youtube_direct.py primero")
            return None
    
    return build('youtube', 'v3', credentials=credentials)

def generate_viral_title():
    """
    Generar título viral aleatorio
    """
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

def upload_video():
    """
    Subir video a YouTube Shorts
    """
    print("🚀 UPLOAD DIRECTO YOUTUBE SHORTS")
    print("=" * 60)
    
    # Configuración del video
    video_file = "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4"
    
    if not os.path.exists(video_file):
        print(f"❌ Video no encontrado: {video_file}")
        return False
    
    print(f"📁 Video encontrado: {os.path.basename(video_file)}")
    print(f"📊 Tamaño: {os.path.getsize(video_file)/1024/1024:.1f} MB")
    
    # Obtener servicio YouTube
    youtube = get_authenticated_service()
    if not youtube:
        return False
    
    print("✅ Servicio YouTube autenticado")
    
    # Generar metadata
    title = generate_viral_title()
    description = """🔥 Contenido viral creado con IA! 

🎯 ¡No te pierdas este increíble contenido!
🚀 Dale like y comparte para más videos como este

#Shorts #Viral #Trending #IA #Contenido #TikTok #YouTube
#ViralContent #Increible #Bomba #Fuego #Explosivo"""

    tags = [
        "shorts", "viral", "trending", "ia", "contenido", "tiktok", 
        "increible", "bomba", "fuego", "explosivo", "youtube", "short"
    ]
    
    # Configuración crítica: NO para niños
    metadata = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '24'  # Entertainment
        },
        'status': {
            'privacyStatus': 'public',
            'madeForKids': False,  # CRÍTICO: NO para niños
            'selfDeclaredMadeForKids': False  # Declaración explícita
        }
    }
    
    print(f"\n📝 METADATA:")
    print(f"   📰 Título: {title}")
    print(f"   📂 Categoría: Entertainment")
    print(f"   👁️ Privacidad: public") 
    print(f"   ⚠️ CRÍTICO: madeForKids=False (NO para niños)")
    print(f"   🏷️ Tags: {', '.join(tags[:5])}...")
    
    try:
        # Configurar upload
        media = MediaFileUpload(
            video_file,
            chunksize=-1,
            resumable=True,
            mimetype='video/mp4'
        )
        
        print(f"\n🚀 INICIANDO UPLOAD...")
        
        # Ejecutar upload
        request = youtube.videos().insert(
            part=','.join(metadata.keys()),
            body=metadata,
            media_body=media
        )
        
        response = request.execute()
        
        if response:
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            shorts_url = f"https://www.youtube.com/shorts/{video_id}"
            
            print(f"\n🎉 ¡UPLOAD EXITOSO!")
            print(f"   ✅ Video ID: {video_id}")
            print(f"   🔗 URL: {video_url}")
            print(f"   📺 Shorts URL: {shorts_url}")
            print(f"   📝 Título: {title}")
            print(f"   ⏰ Subido: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   ⚠️ Configuración: NO para niños (madeForKids=False)")
            
            print(f"\n📊 CANAL YOUTUBE:")
            print(f"   🆔 ID: UCeL3EES7F5v_kDyiZz_F-6A")
            print(f"   📺 Nombre: ChakakitaFreakyVideos")
            print(f"   🌐 URL: https://www.youtube.com/channel/UCeL3EES7F5v_kDyiZz_F-6A")
            
            # Guardar resultado
            result = {
                'video_id': video_id,
                'url': video_url,
                'shorts_url': shorts_url,
                'title': title,
                'uploaded_at': datetime.now().isoformat(),
                'made_for_kids': False,
                'success': True
            }
            
            # Crear log
            log_file = "logs/upload_result.json"
            os.makedirs("logs", exist_ok=True)
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Resultado guardado en: {log_file}")
            
            return True
        else:
            print("❌ Upload falló - No response")
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante upload: {e}")
        logger.error(f"Upload error: {e}")
        return False

def main():
    """
    Función principal
    """
    print("🚀 UPLOAD DIRECTO YOUTUBE SHORTS")
    print("=" * 50)
    
    success = upload_video()
    
    if success:
        print(f"\n🎉 ¡VIDEO SUBIDO EXITOSAMENTE!")
        print(f"🔗 Tu video está ahora en YouTube Shorts")
        print(f"⚠️ Configuración: NO marcado como contenido para niños")
    else:
        print(f"\n❌ Upload falló.")

if __name__ == "__main__":
    main()
