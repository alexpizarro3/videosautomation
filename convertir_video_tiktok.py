import subprocess
import os
import cv2

def convertir_a_9_16_zoom(input_path, output_path):
    """
    Convierte un video horizontal (16:9) a vertical (9:16) con zoom, o escala si ya es vertical.
    """
    # Detecta dimensiones del video
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    print(f"Dimensiones detectadas: {width}x{height}")
    if width > height:
        # Horizontal: crop y scale
        crop_h = int(width * 16 / 9)
        filtro = f"crop={width}:{crop_h},scale=1080:1920"
        print("Filtro aplicado (horizontal):", filtro)
    else:
        # Vertical: más zoom (escalar a altura aún mayor y recortar centro)
        # Escala a 1800x3200, luego crop al centro 1080x1920
        filtro = "scale=1800:3200,crop=1080:1920"
        print("Filtro aplicado (vertical con más zoom):", filtro)
    comando = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-vf", filtro,
        "-c:a", "copy",
        output_path
    ]
    print("Ejecutando:", " ".join(comando))
    subprocess.run(comando, check=True)

if __name__ == "__main__":
    input_video = "Fruta.mp4"
    output_video = "Fruta_tiktok.mp4"
    if not os.path.exists(input_video):
        print(f"No se encontró el archivo {input_video}")
    else:
        convertir_a_9_16_zoom(input_video, output_video)
        print(f"Video convertido y guardado como {output_video}")
