#!/usr/bin/env python3
"""
🚀 DUAL UPLOADER AUTOMÁTICO SIN INTERACCIÓN
Sube automáticamente videos narrativos a TikTok y YouTube Shorts
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

def upload_remaining_tiktok_videos():
    """
    Subir videos narrativos restantes a TikTok automáticamente
    """
    print("📱 SUBIENDO VIDEOS NARRATIVOS RESTANTES A TIKTOK")
    print("=" * 60)
    
    # Importar funciones de TikTok
    try:
        sys.path.append(str(Path(__file__).parent))
        import subir_tiktok_selenium_final_v5 as tiktok_uploader
        
        # Buscar videos narrativos processed
        processed_folder = Path("data/videos/processed")
        narrative_videos = list(processed_folder.glob("narrative_video_*_tiktok_FINAL.mp4"))
        
        if not narrative_videos:
            print("⚠️ No se encontraron videos narrativos para TikTok")
            return 0
        
        print(f"📁 Videos encontrados: {len(narrative_videos)}")
        
        uploaded_count = 0
        for i, video_path in enumerate(narrative_videos, 1):
            try:
                print(f"\n📱 SUBIENDO {i}/{len(narrative_videos)}: {video_path.name}")
                
                # Generar descripción ASMR específica
                if "narrative_video_1" in video_path.name:
                    descripcion = "🔥 HISTORIA ASMR VIRAL - PARTE 1 | Biblioteca dorada susurrante 😱\n\n¿Te relajó? 🔥\nSigue la historia completa ✨\n\n#ASMR #Historia #Viral #Parte1 #Trending #fyp"
                elif "narrative_video_2" in video_path.name:
                    descripcion = "😱 HISTORIA ASMR VIRAL - PARTE 2 | Pasadizo azul místico 🌀\n\n¡Continúa la aventura! 💎\n¿Qué crees que pase? 🤔\n\n#ASMR #Historia #Viral #Parte2 #Misterio #fyp"
                elif "narrative_video_3" in video_path.name:
                    descripcion = "✨ HISTORIA ASMR VIRAL - FINAL | Reloj de arena prismático 🌈\n\n¡FINAL ÉPICO! 🎉\n¿Te gustó la historia? ❤️\n\n#ASMR #Historia #Viral #Final #Épico #fyp"
                else:
                    descripcion = "🔥 ASMR NARRATIVO ULTRA VIRAL 😱\n\n¿Te hipnotizó? ✨\nDoble TAP si te gustó 💎\n\n#ASMR #Narrativo #Viral #Trending #fyp"
                
                # Subir usando la función principal de TikTok
                result = tiktok_uploader.subir_video_selenium_xpaths_definitivos(
                    video_path=str(video_path),
                    descripcion=descripcion
                )
                
                if result:
                    print(f"✅ TikTok upload {i} completado")
                    uploaded_count += 1
                else:
                    print(f"❌ Falló TikTok upload {i}")
                
                # Esperar entre uploads (2-3 minutos)
                if i < len(narrative_videos):
                    wait_time = 150  # 2.5 minutos
                    print(f"⏰ Esperando {wait_time} segundos...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f"❌ Error subiendo {video_path.name}: {e}")
                continue
        
        print(f"\n📊 RESUMEN TIKTOK: {uploaded_count}/{len(narrative_videos)} videos subidos")
        return uploaded_count
        
    except ImportError as e:
        print(f"❌ Error importando TikTok uploader: {e}")
        return 0
    except Exception as e:
        print(f"❌ Error general TikTok: {e}")
        return 0

def upload_all_youtube_videos():
    """
    Subir todos los videos FUNDIDO a YouTube Shorts automáticamente
    """
    print("\n🎬 SUBIENDO VIDEOS A YOUTUBE SHORTS")
    print("=" * 60)
    
    try:
        from youtube_uploader_real import YouTubeShortsUploaderReal
        
        uploader = YouTubeShortsUploaderReal()
        
        if not uploader.authenticate():
            print("❌ Error autenticando YouTube")
            return 0
        
        # Buscar videos FUNDIDO
        final_folder = Path("data/videos/final")
        fundido_videos = list(final_folder.glob("*FUNDIDO*.mp4"))
        
        if not fundido_videos:
            print("⚠️ No se encontraron videos FUNDIDO para YouTube")
            return 0
        
        print(f"📁 Videos FUNDIDO encontrados: {len(fundido_videos)}")
        
        uploaded_count = 0
        for i, video_path in enumerate(fundido_videos, 1):
            try:
                print(f"\n🎬 SUBIENDO {i}/{len(fundido_videos)}: {video_path.name}")
                
                # Títulos específicos para videos narrativos
                if "unidos" in video_path.name.lower():
                    titulo = "🔥 HISTORIA ASMR COMPLETA | 3 Partes ÉPICAS #Shorts #ASMR #Historia"
                    descripcion = "✨ ¡La HISTORIA ASMR COMPLETA que está ROMPIENDO Internet!\n\n🎭 3 partes épicas en un solo video\n🔥 Efectos ultra-coloridos hipnóticos\n😱 Narrativa que te va a ATRAPAR\n\nCOMENTA qué parte te gustó más y SUSCRÍBETE para más historias ÉPICAS!\n\n#ASMR #Historia #Viral #Shorts #Trending #Narrativa #Épico"
                else:
                    titulo = uploader.generar_titulo_viral(str(video_path))
                    descripcion = uploader.generar_descripcion(str(video_path))
                
                result = uploader.upload_video(
                    video_path=str(video_path),
                    title=titulo,
                    description=descripcion
                )
                
                if result:
                    print(f"✅ YouTube upload {i} completado")
                    print(f"🔗 URL: {result['url']}")
                    uploaded_count += 1
                else:
                    print(f"❌ Falló YouTube upload {i}")
                
                # Esperar entre uploads (1 minuto)
                if i < len(fundido_videos):
                    wait_time = 60
                    print(f"⏰ Esperando {wait_time} segundos...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f"❌ Error subiendo {video_path.name}: {e}")
                continue
        
        print(f"\n📊 RESUMEN YOUTUBE: {uploaded_count}/{len(fundido_videos)} videos subidos")
        return uploaded_count
        
    except ImportError as e:
        print(f"❌ Error importando YouTube uploader: {e}")
        return 0
    except Exception as e:
        print(f"❌ Error general YouTube: {e}")
        return 0

def run_dual_upload_automatic():
    """
    Ejecutar upload dual completamente automático
    """
    print("🚀 DUAL UPLOADER AUTOMÁTICO")
    print("=" * 70)
    print(f"🕐 Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "tiktok_uploaded": 0,
        "youtube_uploaded": 0,
        "total_processed": 0,
        "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Subir a TikTok primero
    print("\n🎯 FASE 1: TIKTOK UPLOADS")
    results["tiktok_uploaded"] = upload_remaining_tiktok_videos()
    
    # Esperar entre plataformas
    if results["tiktok_uploaded"] > 0:
        print("\n⏰ PAUSA ENTRE PLATAFORMAS (1 minuto)...")
        time.sleep(60)  # 1 minuto
    
    # Subir a YouTube
    print("\n🎯 FASE 2: YOUTUBE UPLOADS")  
    results["youtube_uploaded"] = upload_all_youtube_videos()
    
    # Calcular totales
    results["total_processed"] = results["tiktok_uploaded"] + results["youtube_uploaded"]
    results["end_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Reporte final
    print("\n" + "="*70)
    print("📊 REPORTE FINAL DUAL UPLOAD")
    print("="*70)
    print(f"🕐 Iniciado: {results['start_time']}")
    print(f"🕐 Finalizado: {results['end_time']}")
    print(f"📱 TikTok uploads: {results['tiktok_uploaded']}")
    print(f"🎬 YouTube uploads: {results['youtube_uploaded']}")
    print(f"📈 Total procesados: {results['total_processed']}")
    
    if results["total_processed"] > 0:
        print("🎉 ¡UPLOAD DUAL COMPLETADO EXITOSAMENTE!")
    else:
        print("⚠️ No se procesaron videos")
    
    # Guardar reporte
    try:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"logs/dual_upload_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Reporte guardado: {report_file}")
        
    except Exception as e:
        print(f"⚠️ Error guardando reporte: {e}")
    
    return results["total_processed"] > 0

def main():
    """
    Función principal automática
    """
    try:
        success = run_dual_upload_automatic()
        if success:
            print("\n✅ Proceso completado exitosamente")
        else:
            print("\n❌ No se procesaron videos")
            
    except KeyboardInterrupt:
        print("\n⚠️ Proceso cancelado por usuario")
    except Exception as e:
        print(f"\n❌ Error general: {e}")

if __name__ == "__main__":
    main()
