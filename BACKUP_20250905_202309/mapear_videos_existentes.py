import os
import json

# Cargar prompts
with open("data/analytics/fusion_prompts_auto.json", "r", encoding="utf-8") as f:
    prompts_data = json.load(f)
prompts = prompts_data["prompts"]

# Buscar todos los videos generados
video_files = [f for f in os.listdir('.') if f.startswith('veo_video_') and f.endswith('.mp4')]
video_files.sort()  # Ordenar por nombre

video_prompt_map = []
for idx, video in enumerate(video_files):
    prompt = prompts[idx] if idx < len(prompts) else ""
    video_prompt_map.append({
        "video": video,
        "prompt": prompt
    })

with open("video_prompt_map.json", "w", encoding="utf-8") as f:
    json.dump(video_prompt_map, f, ensure_ascii=False, indent=2)

print(f"Se generó video_prompt_map.json con {len(video_prompt_map)} videos mapeados.")
