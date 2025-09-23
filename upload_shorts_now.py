import re
def upload_single_video(uploader, video_path, prompt_original=""):
    """
    Sube un solo video a YouTube Shorts usando el uploader real.
    Retorna True si la subida fue exitosa, False si falló.
    """
    try:
        # Generar metadatos dinámicos
        metadata = generar_metadata_youtube(video_path, prompt_original)
        
        # Subir el video
        result = uploader.upload(
            video_path,
            title=metadata["title"],
            description=metadata["description"],
            tags=metadata["tags"],
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
from dynamic_description_generator import DynamicDescriptionGenerator

# Agregar el directorio raíz al path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def generar_titulo_viral(video_path, prompt_original=""):
    """Genera títulos virales para YouTube Shorts usando el generador dinámico"""
    
    if not prompt_original:
        # Fallback a títulos genéricos si no hay prompt
        plantillas = [
            "🔥 ESTO SE ESTÁ VOLVIENDO VIRAL EN TIKTOK",
            "😱 NO VAS A CREER LO QUE ACABAS DE VER",
            "🤯 ESTO ESTÁ ROMPIENDO INTERNET AHORA MISMO",
        ]
        return random.choice(plantillas) + " #Shorts #Viral #Trending"

    generator = DynamicDescriptionGenerator()
    elements = generator.extract_key_elements(prompt_original)
    
    # Usar el "hook" del generador dinámico como base para el título
    hook = random.choice(generator.viral_hooks.get(elements["category"], generator.viral_hooks["general"]))
    
    # Capitalizar y limpiar para formato de título
    titulo = hook.upper()
    
    # Agregar hashtags clave
    titulo += " #Shorts #Viral #" + elements["category"].capitalize()

    return titulo

def generar_descripcion(video_path, prompt_original=""):
    """Genera descripción optimizada para YouTube Shorts usando el generador dinámico"""
    
    try:
        generator = DynamicDescriptionGenerator()
        # Usar el mismo generador que TikTok para consistencia
        descripcion = generator.generate_dynamic_description(video_path, prompt_original)
        
        # Asegurarse de que los hashtags de YouTube estén presentes
        if "#Shorts" not in descripcion:
            descripcion += " #Shorts"
        if "#YouTubeShorts" not in descripcion:
            descripcion += " #YouTubeShorts"
            
        return descripcion
        
    except Exception as e:
        print(f"⚠️ Error en generador de descripción dinámica para YouTube: {e}")
        # Fallback a descripción simple si falla el generador dinámico
        return "🔥 ¡Este contenido está EXPLOTANDO en todas las redes sociales!\n\n¿Qué opinas? ¡Déjanos tu comentario! 👇\n\n#Shorts #Viral #Trending #ContentCreator #Entertainment"

def generar_metadata_youtube(video_path, prompt_original=""):
    """Genera metadata completa para YouTube Shorts"""
    
    titulo = generar_titulo_viral(video_path, prompt_original)
    descripcion = generar_descripcion(video_path, prompt_original)
    
    # Extraer hashtags de la descripción para usarlos como tags
    tags = re.findall(r"#(\w+)", descripcion)
    tags.extend(["Shorts", "Viral", "Trending", "YouTubeShorts"])
    tags = list(set(tags)) # Eliminar duplicados

    metadata = {
        "title": titulo,
        "description": descripcion,
        "tags": tags,
        "categoryId": "24",  # Entertainment
        "defaultLanguage": "es",
        "defaultAudioLanguage": "es",
        "privacyStatus": "public",
        "madeForKids": False,  # ⭐ IMPORTANTE: NO es contenido para niños
        "selfDeclaredMadeForKids": False,  # ⭐ Declaración explícita
        "notifySubscribers": True,
        "snippet": {
            "title": titulo,
            "description": descripcion,
            "tags": tags,
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
