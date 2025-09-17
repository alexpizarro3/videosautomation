def upload_single_video(uploader, video_path):
    """
    Sube un solo video a YouTube Shorts usando el uploader real.
    Retorna True si la subida fue exitosa, False si falló.
    """
    try:
        # Generar título y descripción virales
        titulo = generar_titulo_viral(video_path)
        descripcion = generar_descripcion(video_path)
        # Subir el video
        result = uploader.upload(
            video_path,
            title=titulo,
            description=descripcion,
            madeForKids=False,
            audience="general"
        )
        if result:
            print(f"[YouTube] Video subido correctamente: {video_path}")
            return True
        else:
            print(f"[YouTube] Falló la subida del video: {video_path}")
            return False
    except Exception as e:
        print(f"[YouTube] Error subiendo video: {video_path} -> {e}")
        return False

#!/usr/bin/env python3
"""
🎬 YOUTUBE SHORTS UPLOADER - UPLOAD DIRECTO
Sistema simplificado para subir videos a YouTube Shorts

⭐ CONFIGURACIÓN IMPORTANTE:
- Contenido configurado como NO para niños (madeForKids=False)
- Declaración explícita de contenido para audiencia general
- Optimizado para máximo alcance viral en YouTube Shorts
"""

import os
import sys
import json
import random
from datetime import datetime
from pathlib import Path
from youtube_uploader_real import YouTubeShortsUploaderReal as Uploader

# Agregar el directorio raíz al path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def generar_titulo_viral(video_path):
    """Genera títulos virales para YouTube Shorts"""
    
    plantillas = [
        "🔥 ESTO SE ESTÁ VOLVIENDO VIRAL EN TIKTOK",
        "😱 NO VAS A CREER LO QUE ACABAS DE VER",
        "🤯 ESTO ESTÁ ROMPIENDO INTERNET AHORA MISMO",
        "✨ EL VIDEO QUE TODOS ESTÁN COMPARTIENDO",
        "🎯 CONTENIDO VIRAL QUE NECESITAS VER",
        "🚀 ESTO VA A SER TENDENCIA EN 24 HORAS",
        "💎 VIRAL GOLD: EL VIDEO DEL MOMENTO",
        "🌟 ESTO ES LO MÁS VIRAL DE HOY",
        "🔥 BREAKING: NUEVO VIRAL HIT",
        "⚡ CONTENIDO QUE ESTÁ EXPLOTANDO EN REDES"
    ]
    
    # Seleccionar plantilla aleatoria
    titulo = random.choice(plantillas)
    
    # Agregar elementos del archivo si es posible
    video_name = Path(video_path).stem.upper()
    if "FUNDIDO" in video_name:
        titulo += " | EFECTOS ÉPICOS"
    elif "SIMPLE" in video_name:
        titulo += " | CONTENIDO PURO"
    
    # Hashtags para YouTube
    titulo += " #Shorts #Viral #Trending"
    
    return titulo

def generar_descripcion(video_path):
    """Genera descripción optimizada para YouTube Shorts"""
    
    descripciones = [
        "🔥 ¡Este contenido está EXPLOTANDO en todas las redes sociales!\n\n¿Qué opinas? ¡Déjanos tu comentario! 👇\n\n#Shorts #Viral #Trending #ContentCreator #Entertainment",
        
        "😱 ¡NO PUEDES PERDERTE este video viral!\n\nSi te gustó, ¡dale LIKE y SUSCRÍBETE para más contenido épico! 🚀\n\n#ViralVideo #Shorts #Trending #Entertainment #Viral",
        
        "🤯 ¡CONTENIDO que está rompiendo Internet!\n\n¿Ya lo compartiste? ¡Dale LIKE si quieres más videos como este! ✨\n\n#Trending #Viral #Shorts #ContentCreator #Entertainment",
        
        "✨ ¡El VIDEO del momento que todos están viendo!\n\nCOMENTA qué te pareció y SUSCRÍBETE para no perderte nada 🎯\n\n#Viral #Shorts #Trending #Entertainment #ContentCreator",
        
        "🚀 ¡VIRAL ALERT! Este es el contenido que necesitabas ver hoy\n\n¿Te gustó? ¡LIKE, COMENTA y COMPARTE! 💎\n\n#ViralContent #Shorts #Trending #Entertainment #Viral"
    ]
    
    return random.choice(descripciones)

def generar_metadata_youtube(video_path):
    """Genera metadata completa para YouTube Shorts"""
    
    metadata = {
        "title": generar_titulo_viral(video_path),
        "description": generar_descripcion(video_path),
        "tags": ["Shorts", "Viral", "Trending", "Entertainment", "ContentCreator", "TikTok", "ViralVideo"],
        "categoryId": "24",  # Entertainment
        "defaultLanguage": "es",
        "defaultAudioLanguage": "es",
        "privacyStatus": "public",
        "madeForKids": False,  # ⭐ IMPORTANTE: NO es contenido para niños
        "selfDeclaredMadeForKids": False,  # ⭐ Declaración explícita
        "notifySubscribers": True,
        "snippet": {
            "title": generar_titulo_viral(video_path),
            "description": generar_descripcion(video_path),
            "tags": ["Shorts", "Viral", "Trending", "Entertainment", "ContentCreator", "TikTok", "ViralVideo"],
            "categoryId": "24",  # Entertainment
            "defaultLanguage": "es",
            "defaultAudioLanguage": "es"
        },
        "status": {
            "privacyStatus": "public",
            "madeForKids": False,  # ⭐ CONFIGURACIÓN CRÍTICA
            "selfDeclaredMadeForKids": False,  # ⭐ Doble confirmación
            "notifySubscribers": True,
            "publishAt": None  # Publicar inmediatamente
        }
    }
    
    return metadata

def encontrar_videos_para_shorts():
    """Encuentra videos listos para YouTube Shorts"""
    
    videos_finales = Path("data/videos/final")
    videos_encontrados = []
    
    if videos_finales.exists():
        for video in videos_finales.glob("*.mp4"):
            # Priorizar videos FUNDIDO para YouTube Shorts
            if "FUNDIDO" in video.name.upper():
                videos_encontrados.append(str(video))
    
    # Si no hay videos FUNDIDO, usar cualquier MP4 disponible
    if not videos_encontrados:
        for video in videos_finales.glob("*.mp4"):
            videos_encontrados.append(str(video))
    
    return videos_encontrados

def mostrar_menu_videos(videos):
    """Muestra menú de selección de videos"""
    
    print("\n" + "="*60)
    print("🎬 YOUTUBE SHORTS UPLOADER")
    print("="*60)
    print(f"📁 Videos disponibles: {len(videos)}")
    print()
    
    for i, video in enumerate(videos, 1):
        video_name = Path(video).name
        file_size = os.path.getsize(video) / (1024*1024)  # MB
        print(f"   {i}. {video_name} ({file_size:.1f} MB)")
    
    print(f"   {len(videos)+1}. 🚀 SUBIR TODOS LOS VIDEOS")
    print(f"   0. ❌ Salir")
    print()
    
    while True:
        try:
            opcion = input("📝 Selecciona una opción: ").strip()
            
            if opcion == "0":
                return None
            elif opcion == str(len(videos)+1):
                return "ALL"
            else:
                idx = int(opcion) - 1
                if 0 <= idx < len(videos):
                    return videos[idx]
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
        except ValueError:
            print("❌ Por favor ingresa un número válido.")

def simular_upload_youtube(video_path):
    """Simula el upload a YouTube Shorts (para desarrollo)"""
    
    print(f"\n🎬 PROCESANDO: {Path(video_path).name}")
    print("-" * 50)
    
    # Generar metadatos completos
    metadata = generar_metadata_youtube(video_path)
    
    print(f"📝 TÍTULO: {metadata['title']}")
    print(f"📄 DESCRIPCIÓN: {metadata['description'][:100]}...")
    print(f"📂 ARCHIVO: {video_path}")
    print(f"📊 TAMAÑO: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    
    # ⭐ CONFIGURACIÓN CRÍTICA PARA NIÑOS
    print(f"👶 CONTENIDO PARA NIÑOS: {"❌ NO" if not metadata['madeForKids'] else "✅ SÍ"}")
    print(f"🔒 DECLARACIÓN EXPLÍCITA: {"❌ NO es para niños" if not metadata['selfDeclaredMadeForKids'] else "✅ Es para niños"}")
    
    # Verificaciones
    if os.path.getsize(video_path) > 100 * 1024 * 1024:  # 100MB
        print("⚠️  ADVERTENCIA: Video muy grande para YouTube Shorts")
    
    print("\n🔄 SIMULANDO UPLOAD A YOUTUBE SHORTS...")
    print("   ✅ Archivo validado")
    print("   ✅ Metadatos generados")
    print("   ✅ Configuración Shorts aplicada")
    print("   ⭐ Configuración 'NO para niños' aplicada")
    print("   ✅ Video procesado por YouTube")
    
    # Simular ID de video
    video_id = f"YSHT_{random.randint(100000, 999999)}"
    print(f"\n🎉 ¡VIDEO SUBIDO EXITOSAMENTE!")
    print(f"🔗 ID del Video: {video_id}")
    print(f"🌐 URL: https://youtube.com/shorts/{video_id}")
    print(f"👶 CONFIRMACIÓN: Configurado como contenido NO para niños ✅")
    
    return video_id

def upload_multiple_videos(uploader, videos):
    """Sube múltiples videos a YouTube Shorts"""
    
    print(f"\n🚀 INICIANDO UPLOAD MASIVO DE {len(videos)} VIDEOS")
    print("=" * 60)
    
    resultados = []
    
    for i, video in enumerate(videos, 1):
        print(f"\n📹 PROCESANDO VIDEO {i}/{len(videos)}")
        
        try:
            success = upload_single_video(uploader, video)
            if success:
                resultados.append({
                    "video": Path(video).name,
                    "status": "SUCCESS",
                    "timestamp": datetime.now().isoformat()
                })
            else:
                resultados.append({
                    "video": Path(video).name,
                    "status": "FAILED",
                    "timestamp": datetime.now().isoformat()
                })
            
            print("✅ Upload completado")
            
            # Pausa entre uploads
            if i < len(videos):
                print("⏳ Esperando 30 segundos antes del siguiente upload...")
                import time
                time.sleep(2)  # Reducido para demo
                
        except Exception as e:
            print(f"❌ Error en upload: {e}")
            resultados.append({
                "video": Path(video).name,
                "status": "ERROR", 
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DEL UPLOAD MASIVO")
    print("="*60)
    
    exitosos = len([r for r in resultados if r["status"] == "SUCCESS"])
    errores = len([r for r in resultados if r["status"] == "ERROR"])
    
    print(f"✅ Videos subidos exitosamente: {exitosos}")
    print(f"❌ Videos con errores: {errores}")
    print(f"📊 Total procesados: {len(resultados)}")
    
    # Guardar reporte
    reporte_path = f"logs/youtube_upload_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs("logs", exist_ok=True)
    
    with open(reporte_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Reporte guardado en: {reporte_path}")
    
    return resultados

def main():
    """Función principal del uploader"""
    
    # Verificar directorio de videos
    if not os.path.exists("data/videos/final"):
        print("❌ No se encontró el directorio data/videos/final")
        print("💡 Ejecuta primero el pipeline completo para generar videos")
        return
    
    # Buscar videos disponibles
    videos = encontrar_videos_para_shorts()
    
    if not videos:
        print("❌ No se encontraron videos para subir a YouTube Shorts")
        print("💡 Asegúrate de tener videos en data/videos/final/")
        return
    
    # Mostrar menú
    seleccion = mostrar_menu_videos(videos)
    
    if seleccion is None:
        print("👋 Upload cancelado por el usuario")
        return
    
    # Inicializar uploader
    uploader = Uploader()
    if not getattr(uploader, 'auth_ok', True):
        print("[!] Error autenticando YouTube")
        sys.exit(1)
    
    # Procesar selección
    if seleccion == "ALL":
        upload_multiple_videos(uploader, videos)
    else:
        # Upload individual
        success = upload_single_video(uploader, seleccion)
        if success:
            print(f"\n🎉 ¡Video subido a YouTube Shorts!")
        else:
            print(f"\n❌ Falló la subida del video {seleccion}")
    
    print("\n✨ ¡Proceso completado! Revisa YouTube Studio para confirmar.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Upload interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()