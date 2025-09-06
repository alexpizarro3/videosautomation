import os, time, pathlib, requests, mimetypes
from google import genai
from google.genai import types
# from IPython.display import Video # This is for Colab, not needed for local execution
# from google.colab import userdata # This is for Colab, not needed for local execution

# API key desde Colab Userdata
# GEMINI_API_KEY = userdata.get('apikey')  # asegúrate de haberla guardado antes
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') # Use environment variable for local execution
assert GEMINI_API_KEY, "Falta tu GEMINI_API_KEY en Colab userdata"

# Modelos válidos según tu cuenta:
#  - "veo-3.0-generate-preview"   (Veo 3 con audio; si tienes acceso)
#  - "veo-3.0-fast-generate-preview"
#  - "veo-2.0-generate-001"       (Veo 2, sin audio)
#VEO_MODEL = "veo-2.0-generate-001"   # puedes cambiarlo si tienes Veo 3 habilitado
VEO_MODEL = "models/veo-3.0-generate-preview"   # calidad alta con audio
#VEO_MODEL = "models/veo-3.0-fast-generate-preview"   # puedes cambiarlo si tienes Veo 3 habilitado

IMAGE_PATH = r"data/images/gemini_image_1.png"  # Cambia por tu imagen (.png/.jpg/.jpeg)
PROMPT = ("ultra HD ASMR loop. Genera una imagen digital hiperrealista de Playa surrealista de frutas vibrantes estilo hiperrealista. Fresas, arándanos, frambuesas forman olas suaves. Sonido ASMR de olas de fruta y crujidos suaves al tacto. Ambiente onírico, relajante. #FoodTok #ASMR")
OUT_MP4 = "veo_out.mp4"

client = genai.Client(api_key=GEMINI_API_KEY)

# Leer la imagen como bytes y detectar MIME
mime, _ = mimetypes.guess_type(IMAGE_PATH)
if not mime:
    mime = "image/png"

if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"No se encontró la imagen en: {IMAGE_PATH}")

with open(IMAGE_PATH, "rb") as f:
    img_bytes = f.read()

# Construir objeto de imagen compatible
image = types.Image(image_bytes=img_bytes, mime_type=mime)

def download(url, dest):
    pathlib.Path(pathlib.Path(dest).parent).mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    open(dest, "wb").write(r.content)
    return dest

# 1) Crear la operación
operation = client.models.generate_videos(
    model=VEO_MODEL,
    prompt=PROMPT,
    image=image,
    config=types.GenerateVideosConfig(
        #duration_seconds=8,      # usa duration_seconds
        # number_of_videos=1,     # opcional
        # negative_prompt="cartoon, low quality",  # opcional
    )
)

# 2) Polling hasta que termine (NO existe .wait)
while not operation.done:
    print("Esperando que termine la generacin...")
    time.sleep(10)
    operation = client.operations.get(operation)

# 3) Obtener el video y descargarlo
generated = operation.response.generated_videos[0]

# Dependiendo de la versin: usa el cliente para descargar el 'file' del video
client.files.download(file=generated.video)
generated.video.save(OUT_MP4)

print("Guardado:", OUT_MP4)
# Video(OUT_MP4, embed=True) # This is for Colab, not needed for local execution
