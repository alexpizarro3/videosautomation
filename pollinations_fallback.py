#!/usr/bin/env python3
"""
Fallback Pollinations IA para generación de videos cuando Veo3 falla.
"""
import os
import requests
import time

def pollinations_generate_video(imagen_path, prompt, out_dir="data/videos/original"):
    """
    Genera un video usando Pollinations IA a partir de una imagen y prompt.
    Devuelve la ruta del video generado o None si falla.
    """
    print(f"[Pollinations] Generando video con fallback IA...")
    try:
        # Simulación de upload de imagen y prompt a Pollinations
        # (Reemplaza por la API real si tienes endpoint)
        url = "https://api.pollinations.ai/v1/video"
        files = {"image": open(imagen_path, "rb")}
        data = {"prompt": prompt}
        response = requests.post(url, files=files, data=data, timeout=120)
        if response.status_code == 200:
            # Guardar el video en disco
            ts = time.strftime("%Y%m%d_%H%M%S")
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, f"pollinations_video_{ts}.mp4")
            with open(out_path, "wb") as f:
                f.write(response.content)
            print(f"[Pollinations] Video guardado: {out_path}")
            return out_path
        else:
            print(f"[Pollinations] Error en la API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[Pollinations] Error generando video: {e}")
        return None
