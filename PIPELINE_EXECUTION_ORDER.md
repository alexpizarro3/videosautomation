# Orden de Ejecución del Pipeline de Automatización de Videos

Este documento describe el orden secuencial para ejecutar los scripts que componen el pipeline de generación de videos para TikTok.

---

### 1. Extracción de Datos y Análisis de Tendencias

- **Script:** `test_tiktok_scraping.py`
- **Propósito:** Extrae datos y métricas de una cuenta de TikTok para identificar tendencias, conceptos de video y analizar el rendimiento de contenido existente.

### 2. Generación de Prompts para Imágenes

- **Script:** `generate_prompts_from_scrap.py`
- **Propósito:** Utiliza los datos extraídos del scraping para generar, mediante IA, prompts creativos y optimizados para la creación de imágenes virales.

### 3. Generación de Imágenes

- **Script:** `gen_images_from_prompts.py`
- **Propósito:** Toma los prompts generados en el paso anterior y los utiliza para crear imágenes visualmente impactantes con un modelo de generación de imágenes de IA.

### 4. Generación de Videos a partir de Imágenes

- **Script:** `generate_veo_video_from_image.py`
- **Propósito:** Convierte las imágenes generadas en videos cortos y dinámicos. El script selecciona las mejores imágenes, adapta los prompts para un formato de video y utiliza la API de Veo para la generación.

### 5. Optimización y Procesamiento Final de Videos

- **Script:** `procesar_final_tiktok.py`
- **Propósito:** Aplica optimizaciones finales a los videos generados, incluyendo crop centrado y zoom, para asegurar la configuración óptima para plataformas como TikTok.

### 6. Unión de Videos

- **Script:** `unir_videos_simple.py`
- **Propósito:** Combina múltiples videos optimizados en un solo video final, listo para su publicación.
