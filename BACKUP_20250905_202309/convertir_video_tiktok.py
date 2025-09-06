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
        # Horizontal: calcular crop basado en altura para mantener 9:16
        crop_w = int(height * 9 / 16)
        # Asegurar que el crop no exceda las dimensiones originales
        if crop_w > width:
            crop_w = width
            crop_h = int(width * 16 / 9)
            if crop_h > height:
                crop_h = height
        else:
            crop_h = height
        filtro = f"crop={crop_w}:{crop_h},scale=1080:1920"
        print("Filtro aplicado (horizontal):", filtro)
    else:
        # Vertical: escalar manteniendo proporción y crop si es necesario
        if width / height > 9 / 16:
            # Más ancho que 9:16, crop al ancho
            crop_w = int(height * 9 / 16)
            filtro = f"crop={crop_w}:{height},scale=1080:1920"
        else:
            # Más alto que 9:16 o ya es 9:16, solo escalar
            filtro = "scale=1080:1920"
        print("Filtro aplicado (vertical):", filtro)
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
