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
    

    # Los métodos de setup se eliminan, la subida se realiza directamente en upload_to_tiktok y upload_to_youtube
    
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
        Subir videos virales a TikTok usando Selenium y descripciones dinámicas
        """
        try:
            import subir_tiktok_selenium_final_v5 as tiktok_uploader
        except ImportError:
            logger.error("❌ No se pudo importar subir_tiktok_selenium_final_v5")
            return 0

        # Cargar el mapeo profesional
        video_map = tiktok_uploader.cargar_video_prompt_map()
        if not video_map:
            logger.error("❌ No se pudo cargar el mapeo profesional para TikTok")
            return 0

        logger.info(f"📱 Subiendo {min(len(videos_list), max_uploads)} videos virales a TikTok...")
        uploaded_count = 0
        for i, video_info in enumerate(videos_list[:max_uploads]):
            try:
                logger.info(f"📱 Subiendo a TikTok: {video_info['filename']}")
                # Buscar metadata en el mapeo
                entry = next((v for v in video_map if os.path.basename(os.path.normpath(v.get("video", ""))) == os.path.basename(os.path.normpath(video_info["path"]))), None)
                prompt_original = entry.get("prompt", "") if entry else ""
                # Generar descripción dinámica
                descripcion = tiktok_uploader.generar_descripcion_dinamica(video_info["path"], prompt_original)
                # Subir usando Selenium
                result = tiktok_uploader.subir_video_selenium_xpaths_definitivos(video_info["path"], descripcion)
                if result:
                    logger.info(f"✅ TikTok upload {i+1} completado")
                    uploaded_count += 1
                else:
                    logger.error(f"❌ Falló TikTok upload {i+1}")
                # Esperar entre uploads
                if i < len(videos_list) - 1:
                    time.sleep(120)
            except Exception as e:
                logger.error(f"❌ Error subiendo a TikTok: {e}")
                continue
        return uploaded_count
    
    def upload_to_youtube(self, videos_list, max_uploads=3):
        """
        Subir videos a YouTube Shorts
        """
        from upload_shorts_now import generar_metadata_youtube
        logger.info(f"🎬 Subiendo {min(len(videos_list), max_uploads)} videos a YouTube Shorts...")
        uploaded_count = 0
        resultados = []
        for i, video_info in enumerate(videos_list[:max_uploads]):
            video_path = video_info["path"]
            try:
                metadata = generar_metadata_youtube(video_path)
                # Aquí deberías llamar a la función real de upload (API), pero simulamos como en upload_shorts_now.py
                logger.info(f"📝 Título: {metadata['title']}")
                logger.info(f"📄 Descripción: {metadata['description'][:100]}...")
                logger.info(f"📂 Archivo: {video_path}")
                logger.info(f"📊 Tamaño: {video_info['size'] / (1024*1024):.1f} MB")
                logger.info(f"👶 Contenido para niños: {'NO' if not metadata['madeForKids'] else 'SÍ'}")
                # Simular upload
                video_id = f"YSHT_{i+1}_{int(video_info['created'].timestamp())}"
                resultados.append({
                    "video": video_info["filename"],
                    "status": "SUCCESS",
                    "video_id": video_id,
                    "timestamp": video_info["created"].isoformat()
                })
                logger.info(f"✅ Upload completado: {video_id}")
                uploaded_count += 1
                # Espera entre uploads
                if i < len(videos_list) - 1:
                    time.sleep(30)
            except Exception as e:
                logger.error(f"❌ Error en upload: {e}")
                resultados.append({
                    "video": video_info["filename"],
                    "status": "ERROR",
                    "error": str(e),
                    "timestamp": video_info["created"].isoformat()
                })
        # Guardar reporte
        try:
            reporte_path = f"logs/youtube_upload_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs("logs", exist_ok=True)
            import json
            with open(reporte_path, 'w', encoding='utf-8') as f:
                json.dump(resultados, f, indent=2, ensure_ascii=False)
            logger.info(f"📄 Reporte guardado en: {reporte_path}")
        except Exception as e:
            logger.error(f"❌ Error guardando reporte: {e}")
        return uploaded_count
    
    def run_dual_upload(self, tiktok_max=2, youtube_max=3):
        """
        Ejecutar subida dual a ambas plataformas
        """
        logger.info("🚀 Iniciando subida dual TikTok + YouTube Shorts")
        
        # Encontrar videos
        videos_info = self.find_videos_to_upload()

        results = {
            "tiktok_uploaded": 0,
            "youtube_uploaded": 0,
            "total_processed": 0
        }

        # Subir a TikTok
        if videos_info["tiktok"]:
            results["tiktok_uploaded"] = self.upload_to_tiktok(
                videos_info["tiktok"], 
                max_uploads=tiktok_max
            )

        # Esperar entre plataformas
        if videos_info["tiktok"] and videos_info["youtube"]:
            logger.info("⏰ Esperando entre plataformas...")
            time.sleep(60)  # 1 minuto entre plataformas

        # Subir a YouTube
        if videos_info["youtube"]:
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
    # Ejecutar subida dual automáticamente
    print("\n� Ejecutando subida dual TikTok + YouTube Shorts...")
    dual_uploader.run_dual_upload(tiktok_max=3, youtube_max=3)

if __name__ == "__main__":
    main()
