# -*- coding: utf-8 -*-
"""
Genera videos con Gemini/Veo 3 a partir de imágenes y guarda los MP4 localmente.
Requisitos:
  pip install google-genai python-dotenv
ENV:
  GEMINI_API_KEY=tu_api_key   (o VEO3_API_KEY como fallback)
  VEO3_MODEL=models/veo-3.0-generate-preview  (opcional)
"""

import os
import re
import json
import time
import mimetypes
import random
from typing import List, Dict, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

# ------------------------
# Utilidades
# ------------------------

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def backoff_sleep(attempt: int):
    """Exponential backoff con jitter, máx 60s."""
    delay = min(60, (2 ** attempt) + random.uniform(0, 1))
    time.sleep(delay)

# ------------------------
# Selección de prompts
# ------------------------

def seleccionar_mejores_imagenes_y_prompts() -> List[Dict[str, str]]:
    """Lee prompts de data/analytics/fusion_prompts_auto.json y devuelve top 3 con ajustes para video."""
    with open("data/analytics/fusion_prompts_auto.json", "r", encoding="utf-8") as f:
        prompts_data = json.load(f)
    prompts = prompts_data["prompts"]

    imagenes = [f"gemini_image_{i+1}.png" for i in range(6)]
    keywords_virales = [
        'asmr', 'kawaii', 'capibara', 'explosión', 'colores vibrantes', 'pastel', 'fruta',
        'atardecer', 'gaviotas', 'gelatina', 'acuario', 'pecera', 'playero', 'relajante',
        'adictivo', 'macro', 'neon', 'viral', 'miniatura', 'crujiente', 'sonido', 'burbuja',
        'crema', 'rosa', 'turquesa', 'summer', 'foodart'
    ]

    def score_prompt(p: str) -> int:
        s = 0
        low = p.lower()
        for kw in keywords_virales:
            if kw in low:
                s += 1
        s += low.count('asmr') + low.count('adictivo') + low.count('viral')
        return s

    scored = [(score_prompt(p), i, p) for i, p in enumerate(prompts)]
    top3 = sorted(scored, reverse=True)[:3]

    mejores = []
    for _, idx, prompt_original in top3:
        prompt_video = prompt_original
        # Pasar de imagen a video + reforzar ASMR
        prompt_video = re.sub(r'Genera una imagen digital hiperrealista de', 'Genera un video ASMR viral de', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'Genera una imagen digital hiperrealista', 'Genera un video ASMR viral', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'Genera una imagen', 'Genera un video', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'\bimagen(es)?\b', 'video', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'\bImagen(es)?\b', 'Video', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'Formato PNG\.?', '', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'Responde solo con imagen PNG\.?', '', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'\bPNG\b', '', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'estilo hiperrealista', 'estilo visual viral', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'estilo visual hiperrealista', 'estilo visual viral', prompt_video, flags=re.IGNORECASE)
        prompt_video = re.sub(r'estilo diorama hiperrealista', 'estilo diorama viral', prompt_video, flags=re.IGNORECASE)
        prompt_video += "\n\nHaz que el video sea super adictivo, con sonidos ASMR envolventes y efectos visuales virales."

        # Imagen por índice; si no existe, usar la primera disponible
        imagen = imagenes[idx] if os.path.exists(imagenes[idx]) else next((im for im in imagenes if os.path.exists(im)), None)
        if not imagen:
            continue
        mejores.append({"prompt": prompt_video.strip(), "imagen": imagen})

    return mejores

# ------------------------
# Cliente Veo
# ------------------------

class VeoClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("VEO3_API_KEY")
        assert api_key, "❌ Falta GEMINI_API_KEY (o VEO3_API_KEY) en el entorno"
        self.model_name = os.getenv("VEO3_MODEL", "models/veo-3.0-generate-preview")
        self.client = genai.Client(api_key=api_key)

    def _open_image(self, image_path: str) -> types.Image:
        mime, _ = mimetypes.guess_type(image_path)
        if not mime:
            mime = "image/png"
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        return types.Image(image_bytes=img_bytes, mime_type=mime)

    def generate_video_from_image(
        self,
        image_path: str,
        prompt: str,
        out_dir: str = "data/videos",
        max_attempts_poll: int = 60,
        retry_on_429: int = 3
    ) -> Optional[str]:
        """Genera un video y lo guarda como mp4. Devuelve la ruta o None."""
        ensure_dir(out_dir)

        # --- Envío con reintentos por 429/quotas ---
        send_attempt = 0
        operation = None
        while send_attempt <= retry_on_429:
            try:
                image_obj = self._open_image(image_path)
                print(f"🤖 Modelo: {self.model_name}")
                print("📝 Enviando solicitud de generación...")
                operation = self.client.models.generate_videos(
                    model=self.model_name,
                    prompt=prompt,
                    image=image_obj,
                    config=types.GenerateVideosConfig()
                )
                break
            except Exception as e:
                msg = str(e).lower()
                if "429" in msg or "resource_exhausted" in msg or "quota" in msg or "rate" in msg:
                    print(f"⚠️  Límite alcanzado (intento {send_attempt+1}/{retry_on_429+1}). Backoff...")
                    backoff_sleep(send_attempt)
                    send_attempt += 1
                    continue
                print(f"❌ Error al iniciar generación: {e}")
                return None

        if operation is None:
            print("❌ No se pudo iniciar la operación (posible límite de API).")
            return None

        # --- Poll hasta done ---
        attempt = 0
        while attempt < max_attempts_poll:
            if getattr(operation, "done", False):
                break
            time.sleep(10)
            try:
                operation = self.client.operations.get(operation)
            except Exception as e:
                print(f"⚠️  Error al consultar estado: {e}")
                backoff_sleep(min(attempt, 5))
            attempt += 1

        if not getattr(operation, "done", False):
            print("⏰ Timeout esperando la generación.")
            return None

        # --- Descargar usando files.download(...) y save(...) ---
        try:
            videos = getattr(getattr(operation, "response", None), "generated_videos", None)
            if not videos:
                err = getattr(operation, "error", None)
                print(f"❌ Respuesta sin videos. Error: {err}")
                return None

            gv = videos[0]  # primer resultado
            # 1) descargar al file store del SDK
            self.client.files.download(file=gv.video)

            # 2) guardar en disco
            ts = time.strftime("%Y%m%d_%H%M%S")
            outfile = os.path.join(out_dir, f"veo_video_{ts}.mp4")
            gv.video.save(outfile)

            if os.path.exists(outfile) and os.path.getsize(outfile) > 1024:
                print(f"✅ Guardado: {outfile}")
                return outfile

            print("⚠️  Descarga realizada pero archivo es muy pequeño.")
            return None

        except Exception as e:
            print(f"❌ Error descargando el video: {e}")
            return None

# ------------------------
# Main
# ------------------------

def main():
    # 1) Seleccionar top 3 y mostrar en consola
    mejores = seleccionar_mejores_imagenes_y_prompts()
    if not mejores:
        print("❌ No hay imágenes disponibles (gemini_image_*.png).")
        return

    print("Las 3 mejores opciones seleccionadas automáticamente:")
    for i, it in enumerate(mejores, 1):
        print(f"Opción {i}: Imagen={it['imagen']}")
        print(f"Prompt: {it['prompt'][:120]}...")

    vc = VeoClient()
    video_prompt_map = []

    # 2) Generar hasta 3 videos
    for i, item in enumerate(mejores[:3], 1):
        print(f"\nGenerando video {i} para imagen: {item['imagen']}")
        out = vc.generate_video_from_image(item["imagen"], item["prompt"])
        if out:
            video_prompt_map.append({"video": out, "prompt": item["prompt"], "imagen": item["imagen"]})
        else:
            print("💡 Video generado pero requiere descarga manual o hubo límite de API.")

    # 3) Guardar mapeo
    ensure_dir("data")
    with open("video_prompt_map.json", "w", encoding="utf-8") as f:
        json.dump(video_prompt_map, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
