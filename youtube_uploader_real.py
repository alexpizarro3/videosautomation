#!/usr/bin/env python3
"""
🎬 YOUTUBE SHORTS UPLOADER REAL - CON API
Sistema real para subir videos a YouTube Shorts usando YouTube Data API v3
"""

import os
import json
import random
import pickle
from pathlib import Path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class YouTubeShortsUploaderReal:
    """
    Uploader real para YouTube Shorts usando API oficial
    """
    
    def __init__(self):
        """
        Inicializar uploader
        """
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.credentials = None
        self.youtube = None
        
        print("🎬 Inicializando YouTube Shorts Uploader REAL")
    
    def authenticate(self):
        """
        Autenticar con YouTube API
        """
        creds = None
        
        # Buscar token existente
        if os.path.exists('config/youtube_token.json'):
            try:
                with open('config/youtube_token.json', 'r') as f:
                    token_data = json.load(f)
                
                creds = Credentials(
                    token=token_data['token'],
                    refresh_token=token_data.get('refresh_token'),
                    token_uri=token_data['token_uri'],
                    client_id=token_data['client_id'],
                    client_secret=token_data['client_secret'],
                    scopes=token_data['scopes']
                )
                print("✅ Token cargado desde config/youtube_token.json")
                
            except Exception as e:
                print(f"❌ Error cargando token: {e}")
                return False
        
        # Refrescar token si es necesario
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("🔄 Token refrescado")
            except Exception as e:
                print(f"❌ Error refrescando token: {e}")
                return False
        
        if not creds or not creds.valid:
            print("❌ Credenciales no válidas")
            return False
        
        # Construir servicio de YouTube
        try:
            self.youtube = build(self.API_SERVICE_NAME, self.API_VERSION, credentials=creds)
            self.credentials = creds
            print("✅ Autenticación exitosa con YouTube API")
            return True
        except Exception as e:
            print(f"❌ Error construyendo servicio YouTube: {e}")
            return False
    
    def generar_titulo_viral(self, video_path):
        """
        Generar título viral para YouTube Shorts
        """
        plantillas = [
            "🔥 ASMR VIRAL que te va a HIPNOTIZAR",
            "😱 NO PUEDES PARAR DE VER ESTO",
            "✨ HISTORIA que te va a hacer SOÑAR",
            "🤯 NARRATIVA ÉPICA que está ROMPIENDO Internet",
            "🎯 CONTENIDO ADICTIVO que NECESITAS VER",
            "🚀 ESTO VA A SER TENDENCIA en 24 HORAS",
            "💎 ASMR GOLD: La HISTORIA del momento",
            "🌟 NARRATIVA ULTRA COLORIDA",
            "🔥 BREAKING: NUEVO HIT NARRATIVO",
            "⚡ HISTORIA que está EXPLOTANDO en redes"
        ]
        
        titulo = random.choice(plantillas)
        
        # Detectar si es narrativo
        if "narrative" in video_path.lower():
            titulo += " | Historia ASMR Completa"
        elif "fundido" in video_path.lower():
            titulo += " | Efectos Hipnóticos"
        
        titulo += " #Shorts #ASMR #Viral"
        
        return titulo[:100]  # YouTube limit
    
    def generar_descripcion(self, video_path):
        """
        Generar descripción optimizada
        """
        descripciones = [
            "✨ ¡La HISTORIA ASMR del momento que todos están viendo!\n\n",
            "🔥 NARRATIVA ULTRA COLORIDA que te va a HIPNOTIZAR\n\n",
            "😱 CONTENIDO ADICTIVO que NO PUEDES parar de ver\n\n",
            "🌟 La HISTORIA más VIRAL del momento\n\n"
        ]
        
        descripcion = random.choice(descripciones)
        descripcion += "COMENTA qué te pareció y SUSCRÍBETE para no perderte más historias ÉPICAS como esta!\n\n"
        descripcion += "🔔 ACTIVA LA CAMPANITA para ser el primero en ver nuestro contenido\n"
        descripcion += "👍 DALE LIKE si te gustó esta historia\n"
        descripcion += "📢 COMPARTE con tus amigos\n\n"
        descripcion += "#ASMR #Storytelling #Viral #Shorts #Trending #Amazing #Incredible #Content"
        
        return descripcion[:5000]  # YouTube limit
    
    def upload_video(self, video_path, title=None, description=None):
        """
        Subir video real a YouTube Shorts
        """
        if not self.youtube:
            print("❌ YouTube API no autenticado")
            return None
        
        if not os.path.exists(video_path):
            print(f"❌ Video no encontrado: {video_path}")
            return None
        
        # Generar título y descripción si no se proporcionan
        if not title:
            title = self.generar_titulo_viral(video_path)
        if not description:
            description = self.generar_descripcion(video_path)
        
        # Configurar metadata del video
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['ASMR', 'Shorts', 'Viral', 'Storytelling', 'Amazing', 'Incredible', 'Trending'],
                'categoryId': '24',  # Entertainment
                'defaultLanguage': 'es',
                'defaultAudioLanguage': 'es'
            },
            'status': {
                'privacyStatus': 'public',
                'madeForKids': False,  # CRÍTICO: NO para niños
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Configurar upload
        media = MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True,
            mimetype='video/mp4'
        )
        
        try:
            print(f"🚀 Subiendo: {Path(video_path).name}")
            print(f"📝 Título: {title}")
            print(f"👶 CRÍTICO: madeForKids=False (NO para niños)")
            
            # Ejecutar upload
            insert_request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            error = None
            retry = 0
            
            while response is None:
                try:
                    print(f"📤 Enviando datos... (intento {retry + 1})")
                    status, response = insert_request.next_chunk()
                    if status:
                        print(f"📊 Progreso: {int(status.progress() * 100)}%")
                        
                except HttpError as e:
                    if e.resp.status in [500, 502, 503, 504]:
                        error = f"Error del servidor: {e}"
                        retry += 1
                        if retry > 3:
                            print(f"❌ {error}")
                            return None
                    else:
                        print(f"❌ Error HTTP: {e}")
                        return None
                        
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")
                    return None
            
            if response:
                video_id = response['id']
                video_url = f"https://youtube.com/shorts/{video_id}"
                
                print(f"🎉 ¡VIDEO SUBIDO EXITOSAMENTE!")
                print(f"🔗 ID: {video_id}")
                print(f"🌐 URL: {video_url}")
                print(f"👶 CONFIRMADO: NO para niños ✅")
                
                return {
                    'id': video_id,
                    'url': video_url,
                    'title': title,
                    'madeForKids': False
                }
            
        except Exception as e:
            print(f"❌ Error subiendo video: {e}")
            return None
    
    def process_uploads(self, max_uploads=3):
        """
        Procesar uploads masivos
        """
        if not self.authenticate():
            print("❌ Error de autenticación")
            return 0
        
        # Buscar videos FUNDIDO
        video_folder = Path("data/videos/final")
        videos = list(video_folder.glob("*FUNDIDO*.mp4"))
        
        if not videos:
            print("❌ No se encontraron videos FUNDIDO para YouTube")
            return 0
        
        print(f"📁 Videos encontrados: {len(videos)}")
        
        uploaded_count = 0
        for i, video_path in enumerate(videos[:max_uploads]):
            print(f"\n🎬 PROCESANDO {i+1}/{min(len(videos), max_uploads)}: {video_path.name}")
            
            result = self.upload_video(str(video_path))
            if result:
                uploaded_count += 1
                print(f"✅ Upload {i+1} completado")
            else:
                print(f"❌ Falló upload {i+1}")
            
            # Esperar entre uploads
            if i < min(len(videos), max_uploads) - 1:
                print("⏰ Esperando 60 segundos...")
                import time
                time.sleep(60)
        
        print(f"\n📊 RESUMEN: {uploaded_count}/{min(len(videos), max_uploads)} videos subidos")
        return uploaded_count

def main():
    """
    Función principal
    """
    print("🎬 YOUTUBE SHORTS UPLOADER REAL")
    print("=" * 60)

    uploader = YouTubeShortsUploaderReal()

    # Buscar videos
    video_folder = Path("data/videos/final")
    videos = list(video_folder.glob("*FUNDIDO*.mp4"))

    if not videos:
        print("❌ No se encontraron videos FUNDIDO")
        return

    print(f"📁 Videos disponibles: {len(videos)}")
    for i, video in enumerate(videos, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f} MB)")

    # Subir automáticamente el primer video
    video_seleccionado = videos[0]
    print(f"\n🚀 Subiendo automáticamente: {video_seleccionado.name}")
    if uploader.authenticate():
        result = uploader.upload_video(str(video_seleccionado))
        if result:
            print(f"🎉 ¡Video subido a YouTube Shorts!")
            print(f"🔗 URL: {result['url']}")
        else:
            print("❌ Falló la subida del video")
    else:
        print("❌ Error de autenticación")

if __name__ == "__main__":
    main()
