# Orden de Ejecución del Pipeline de Automatización de Videos

Este documento describe el orden secuencial para ejecutar los scripts que componen el pipeline de generación de videos virales para TikTok con sistema profesional de prompts.

---

### 1. Extracción de Datos y Análisis de Tendencias

- **Script:** `test_tiktok_scraping.py`
- **Propósito:** Extrae datos y métricas de una cuenta de TikTok para identificar tendencias, conceptos de video y analizar el rendimiento de contenido existente.
- **Output:** Análisis de 75 videos con métricas de engagement y tendencias detectadas.

### 2. Generación de Prompts para Imágenes

- **Script:** `generate_prompts_from_scrap.py`
- **Propósito:** Utiliza los datos extraídos del scraping para generar, mediante IA, prompts creativos y optimizados para la creación de imágenes virales.
- **Output:** `data/analytics/fusion_prompts_auto.json` con prompts base optimizados.

### 3. Generación de Imágenes

- **Script:** `gen_images_from_prompts.py`
- **Propósito:** Toma los prompts generados en el paso anterior y los utiliza para crear imágenes visualmente impactantes con un modelo de generación de imágenes de IA.
- **Output:** Imágenes `data/images/gemini_image_1.png` a `data/images/gemini_image_6.png` listas para video.

### 4. **[NUEVO]** Preparación del Pipeline Viral Profesional

- **Script:** `prepare_viral_pipeline.py`
- **Propósito:** Analiza las imágenes generadas para extraer metadatos (temática, colores, mood) y genera prompts de video profesionales optimizados para viralización.
- **Características:**
  - Análisis automático de imágenes con Gemini Vision
  - Detección de temas, colores dominantes y elementos virales
  - Generación de prompts profesionales con hooks virales
  - Sistema de scoring de engagement (0-100)
  - Verificación completa del pipeline
- **Output:** 
  - `data/image_analysis/image_analysis_report_*.json` - Análisis de imágenes
  - `data/analytics/fusion_prompts_auto_enhanced.json` - Prompts profesionales

### 5. Generación de Videos a partir de Imágenes **[MEJORADO]**

- **Script:** `generate_veo_video_from_image.py`
- **Propósito:** Convierte las imágenes generadas en videos cortos y dinámicos utilizando prompts profesionales optimizados para máximo engagement viral.
- **Mejoras Implementadas:**
  - Sistema de prompts virales profesionales con 5 categorías
  - Análisis de metadatos de imagen en tiempo real
  - Integración inteligente de contexto visual
  - Fallback a sistema legacy mejorado
  - Scoring automático de potencial viral
- **Output:** Videos MP4 optimizados con metadatos profesionales y scoring viral.

### 6. Optimización y Procesamiento Final de Videos

- **Script:** `procesar_final_tiktok.py`
- **Propósito:** Aplica optimizaciones finales a los videos generados, incluyendo crop centrado y zoom, para asegurar la configuración óptima para plataformas como TikTok.

### 7. Unión de Videos

- **Script:** `unir_videos_simple.py`
- **Propósito:** Combina múltiples videos optimizados en un solo video final, listo para su publicación.

---

## 🎬 FLUJO OPTIMIZADO RECOMENDADO

### Opción A: Pipeline Completo Tradicional
```bash
1. python test_tiktok_scraping.py
2. python generate_prompts_from_scrap.py  
3. python gen_images_from_prompts.py
4. python prepare_viral_pipeline.py
5. python generate_veo_video_from_image.py
6. python procesar_final_tiktok.py
7. python unir_videos_simple.py
```

### Opción B: Pipeline Rápido (con imágenes existentes)
```bash
1. python prepare_viral_pipeline.py      # Analiza imágenes + genera prompts profesionales
2. python generate_veo_video_from_image.py   # Genera videos virales optimizados
3. python procesar_final_tiktok.py       # Optimiza para TikTok
4. python unir_videos_simple.py          # Une videos finales
```

---

## 🚀 NUEVAS CARACTERÍSTICAS DEL SISTEMA

### Sistema de Prompts Virales Profesionales
- **5 Categorías Virales:** ASMR, Satisfying, Aesthetic, Educational, Entertainment
- **25+ Hooks Virales** por categoría optimizados para engagement
- **8 Paletas de Colores** específicamente diseñadas para viral content
- **Scoring Algorítmico** de predicción de engagement (0-100)
- **Metadatos Profesionales** con timing óptimo y strategy hashtags

### Análisis Inteligente de Imágenes
- **Detección Automática** de temática principal con Gemini Vision
- **Extracción de Colores** dominantes para optimización de video
- **Análisis de Mood** para alineación emocional perfecta
- **Elementos de Movimiento** identificados para animación viral
- **Hooks Visuales** detectados para captar atención inmediata

### Integración Contextual
- **Prompts Adaptativos** que se ajustan al contenido visual de cada imagen
- **Enriquecimiento Dinámico** con información extraída automáticamente
- **Fallback Inteligente** a sistema legacy mejorado si es necesario
- **Verificación Automática** de archivos y dependencias del pipeline
