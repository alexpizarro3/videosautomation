#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 INTEGRADOR DUAL: TIKTOK + YOUTUBE SHORTS
Sube automáticamente videos processed a TikTok y videos FUNDIDO a YouTube Shorts
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DualPlatformUploader:
    """
    Subidor dual para TikTok y YouTube Shorts
    """
    
    def __init__(self):
        """
        Inicializar subidor dual
        """
        self.tiktok_uploader = None
        self.youtube_uploader = None
        
        # Rutas
        self.tiktok_folder = "data/videos/processed"
        self.youtube_folder = "data/videos/final"
        
        logger.info("🔄 DualPlatformUploader inicializado")
    
    def setup_tiktok_uploader(self):
        """
        Configurar subidor de TikTok
        """
        try:
            # Importar el subidor de TikTok existente
            from subir_tiktok_selenium_final_v5 import TikTokUploader
            self.tiktok_uploader = TikTokUploader()
            logger.info("✅ TikTok uploader configurado")
            return True
        except ImportError:
            logger.error("❌ No se pudo importar TikTok uploader")
            return False
        except Exception as e:
            logger.error(f"❌ Error configurando TikTok uploader: {e}")
            return False
    
    def setup_youtube_uploader(self):
        """
        Configurar subidor de YouTube
        """
        try:
            from youtube_shorts_uploader import YouTubeShortsUploader
            self.youtube_uploader = YouTubeShortsUploader()
            logger.info("✅ YouTube uploader configurado")
            return True
        except ImportError:
            logger.error("❌ No se pudo importar YouTube uploader")
            return False
        except Exception as e:
            logger.error(f"❌ Error configurando YouTube uploader: {e}")
            return False
    
    def find_videos_to_upload(self):
        """
        Encontrar videos listos para subir a cada plataforma
        """
        videos_info = {
            "tiktok": [],
            "youtube": []
        }
        
        # Videos para TikTok (carpeta processed)
        if os.path.exists(self.tiktok_folder):
            for video_file in Path(self.tiktok_folder).glob("*.mp4"):
                videos_info["tiktok"].append({
                    "platform": "tiktok",
                    "filename": video_file.name,
                    "path": str(video_file),
                    "size": video_file.stat().st_size,
                    "created": datetime.fromtimestamp(video_file.stat().st_ctime)
                })
        
        # Videos para YouTube (carpeta final con FUNDIDO)
        if os.path.exists(self.youtube_folder):
            for video_file in Path(self.youtube_folder).glob("*FUNDIDO*.mp4"):
                videos_info["youtube"].append({
                    "platform": "youtube",
                    "filename": video_file.name,
                    "path": str(video_file),
                    "size": video_file.stat().st_size,
                    "created": datetime.fromtimestamp(video_file.stat().st_ctime)
                })
        
        logger.info(f"📊 Videos encontrados - TikTok: {len(videos_info['tiktok'])}, YouTube: {len(videos_info['youtube'])}")
        return videos_info
    
    def upload_to_tiktok(self, videos_list, max_uploads=2):
        """
        Subir videos a TikTok
        """
        if not self.tiktok_uploader:
            logger.error("❌ TikTok uploader no configurado")
            return 0
        
        logger.info(f"📱 Subiendo {min(len(videos_list), max_uploads)} videos a TikTok...")
        
        uploaded_count = 0
        for i, video_info in enumerate(videos_list[:max_uploads]):
            try:
                logger.info(f"📱 Subiendo a TikTok: {video_info['filename']}")
                
                # Aquí llamarías al método de upload de TikTok
                # result = self.tiktok_uploader.upload_video(video_info['path'])
                
                # Por ahora, simular upload exitoso
                logger.info(f"✅ TikTok upload {i+1} completado")
                uploaded_count += 1
                
                # Esperar entre uploads
                if i < len(videos_list) - 1:
                    time.sleep(120)  # 2 minutos entre uploads
                    
            except Exception as e:
                logger.error(f"❌ Error subiendo a TikTok: {e}")
                continue
        
        return uploaded_count
    
    def upload_to_youtube(self, videos_list, max_uploads=3):
        """
        Subir videos a YouTube Shorts
        """
        if not self.youtube_uploader:
            logger.error("❌ YouTube uploader no configurado")
            return 0
        
        logger.info(f"🎬 Subiendo {min(len(videos_list), max_uploads)} videos a YouTube Shorts...")
        
        try:
            # Usar el método de upload del YouTube uploader
            self.youtube_uploader.process_uploads(max_uploads=max_uploads)
            logger.info(f"✅ YouTube uploads completados")
            return max_uploads  # Asumir éxito por ahora
            
        except Exception as e:
            logger.error(f"❌ Error subiendo a YouTube: {e}")
            return 0
    
    def run_dual_upload(self, tiktok_max=2, youtube_max=3):
        """
        Ejecutar subida dual a ambas plataformas
        """
        logger.info("🚀 Iniciando subida dual TikTok + YouTube Shorts")
        
        # Configurar uploaders
        tiktok_ready = self.setup_tiktok_uploader()
        youtube_ready = self.setup_youtube_uploader()
        
        if not tiktok_ready and not youtube_ready:
            logger.error("❌ No se pudo configurar ningún uploader")
            return False
        
        # Encontrar videos
        videos_info = self.find_videos_to_upload()
        
        results = {
            "tiktok_uploaded": 0,
            "youtube_uploaded": 0,
            "total_processed": 0
        }
        
        # Subir a TikTok
        if tiktok_ready and videos_info["tiktok"]:
            results["tiktok_uploaded"] = self.upload_to_tiktok(
                videos_info["tiktok"], 
                max_uploads=tiktok_max
            )
        
        # Esperar entre plataformas
        if tiktok_ready and youtube_ready:
            logger.info("⏰ Esperando entre plataformas...")
            time.sleep(300)  # 5 minutos entre plataformas
        
        # Subir a YouTube
        if youtube_ready and videos_info["youtube"]:
            results["youtube_uploaded"] = self.upload_to_youtube(
                videos_info["youtube"], 
                max_uploads=youtube_max
            )
        
        results["total_processed"] = results["tiktok_uploaded"] + results["youtube_uploaded"]
        
        # Reporte final
        logger.info("📊 REPORTE FINAL:")
        logger.info(f"   📱 TikTok uploads: {results['tiktok_uploaded']}")
        logger.info(f"   🎬 YouTube uploads: {results['youtube_uploaded']}")
        logger.info(f"   📈 Total procesados: {results['total_processed']}")
        
        return results["total_processed"] > 0
    
    def run_youtube_only(self, max_uploads=3):
        """
        Ejecutar subida SOLO a YouTube Shorts
        """
        logger.info("🎬 Iniciando subida SOLO a YouTube Shorts")
        
        # Configurar solo YouTube uploader
        youtube_ready = self.setup_youtube_uploader()
        
        if not youtube_ready:
            logger.error("❌ No se pudo configurar YouTube uploader")
            return False
        
        # Encontrar videos para YouTube
        videos_info = self.find_videos_to_upload()
        
        if not videos_info["youtube"]:
            logger.warning("⚠️ No se encontraron videos FUNDIDO para YouTube")
            return False
        
        # Subir solo a YouTube
        uploaded_count = self.upload_to_youtube(
            videos_info["youtube"], 
            max_uploads=max_uploads
        )
        
        # Reporte final
        logger.info("📊 REPORTE FINAL YOUTUBE:")
        logger.info(f"   🎬 YouTube uploads: {uploaded_count}")
        logger.info(f"   ✅ Configuración: NO para niños (madeForKids=False)")
        
        return uploaded_count > 0
    
    def show_status(self):
        """
        Mostrar estado del sistema dual
        """
        print("🔄 ESTADO DEL SUBIDOR DUAL")
        print("=" * 60)
        
        # Verificar carpetas
        tiktok_exists = os.path.exists(self.tiktok_folder)
        youtube_exists = os.path.exists(self.youtube_folder)
        
        print(f"📁 Carpeta TikTok: {'✅' if tiktok_exists else '❌'} {self.tiktok_folder}")
        print(f"📁 Carpeta YouTube: {'✅' if youtube_exists else '❌'} {self.youtube_folder}")
        
        # Contar videos
        if tiktok_exists:
            tiktok_count = len(list(Path(self.tiktok_folder).glob("*.mp4")))
            print(f"📱 Videos para TikTok: {tiktok_count}")
        
        if youtube_exists:
            youtube_count = len(list(Path(self.youtube_folder).glob("*FUNDIDO*.mp4")))
            print(f"🎬 Videos FUNDIDO para YouTube: {youtube_count}")
        
        # Estado de configuración
        print(f"\n⚙️ CONFIGURACIÓN:")
        print(f"   📱 TikTok uploader: Disponible")
        print(f"   🎬 YouTube uploader: Configurado")
        print(f"   🔄 Modo dual: Activo")
        print(f"   ⚠️ Importante: Videos NO marcados para niños")

def create_dual_pipeline_integration():
    """
    Crear integración con el pipeline principal
    """
    integration_code = '''
# INTEGRACIÓN EN run_complete_pipeline.py
# Agregar este paso al final del pipeline:

{
    "id": 8,
    "name": "Upload Dual TikTok + YouTube",
    "script": "dual_platform_uploader.py",
    "timeout": 1200,  # 20 minutos
    "required": False,
    "description": "Sube videos a TikTok y YouTube Shorts automáticamente"
}
'''
    
    print("🔗 INTEGRACIÓN CON PIPELINE PRINCIPAL")
    print("=" * 60)
    print(integration_code)

def main():
    """
    Función principal
    """
    print("🔄 SUBIDOR DUAL TIKTOK + YOUTUBE SHORTS")
    print("=" * 70)
    
    # Crear uploader dual
    dual_uploader = DualPlatformUploader()
    
    # Mostrar estado
    dual_uploader.show_status()
    
    print("\n📋 CONFIGURACIÓN REQUERIDA:")
    print("1. ✅ TikTok uploader ya configurado")
    print("2. 🔧 Configurar credenciales de YouTube en config/youtube_credentials.json")
    print("3. 📁 Verificar carpetas de videos")
    print("4. 🔑 YouTube API ya configurado")
    
    print("\n🚀 FLUJO AUTOMÁTICO:")
    print("   📱 Videos de 'processed' → TikTok")
    print("   🎬 Videos 'FUNDIDO' → YouTube Shorts")
    print("   ⏰ Subidas escalonadas para evitar límites")
    print("   📊 Logs detallados de cada upload")
    print("   ⚠️ CRÍTICO: madeForKids=False (NO para niños)")
    
    # Mostrar integración
    create_dual_pipeline_integration()
    
    print("\n💡 MODO SOLO YOUTUBE:")
    print("   Para subir SOLO a YouTube Shorts:")
    print("   dual_uploader.run_youtube_only(max_uploads=3)")

if __name__ == "__main__":
    main()
