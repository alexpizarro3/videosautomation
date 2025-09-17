from dotenv import load_dotenv
load_dotenv()

import os
from youtube_uploader_selenium import subir_video_youtube_selenium
from upload_shorts_now import generar_metadata_youtube

# --- Configuración de la prueba ---
# Usamos un video de prueba existente
video_de_prueba = "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4"
# --- Fin de la configuración ---

def run_test():
    """Ejecuta la prueba de subida a YouTube."""
    print("Iniciando prueba de subida a YouTube...")

    # Verificar si el video de prueba existe
    if not os.path.exists(video_de_prueba):
        print(f"Error: El video de prueba no se encontró en: {video_de_prueba}")
        print("Por favor, asegúrate de que el archivo exista o actualiza la ruta en el script de prueba.")
        return

    print(f"Video de prueba seleccionado: {video_de_prueba}")

    # Generar metadata para el video
    print("Generando metadata para el video...")
    try:
        metadata = generar_metadata_youtube(video_de_prueba)
        print("Metadata generada exitosamente.")
        # Imprimir metadata para verificación
        # print(f"   Título: {metadata['title']}")
        # print(f"   Descripción: {metadata['description']}")
    except Exception as e:
        print(f"Error al generar la metadata: {e}")
        return

    # Ejecutar el proceso de subida
    print("Intentando subir el video con Selenium...")
    try:
        success = subir_video_youtube_selenium(video_de_prueba, metadata)
        if success:
            print("Prueba finalizada: ¡El video se subió exitosamente!")
        else:
            print("Prueba finalizada: La subida del video falló. Revisa los logs para más detalles.")
    except Exception as e:
        print(f"Error catastrófico durante la ejecución de la prueba: {e}")

if __name__ == "__main__":
    run_test()
