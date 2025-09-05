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

### 8. **[NUEVO]** Generación de Descripciones Dinámicas y Upload Automatizado

- **Scripts:** 
  - `subir_tiktok_selenium_final_v5.py` - Upload individual con descripción dinámica
  - `subir_multiples_videos_dinamicos.py` - Sistema de upload masivo
- **Propósito:** Automatiza completamente la subida de videos a TikTok con descripciones únicas y virales generadas automáticamente para cada video basándose en su contenido específico.
- **Características:**
  - **Descripciones Dinámicas:** Genera automáticamente descripciones únicas para cada video
  - **Análisis de Contenido:** Identifica el tipo de contenido (ASMR, Food, General) automáticamente
  - **Plantillas Virales:** 9 plantillas optimizadas con hooks probados para engagement máximo
  - **Mapeo Inteligente:** Utiliza `video_prompt_map.json` para personalizar descripciones
  - **Upload Selenium:** Sistema anti-detección avanzado con XPaths específicos
  - **Modal Handling:** Manejo inteligente de modales sin publicación prematura
  - **Upload Masivo:** Procesamiento automático de múltiples videos con pausas estratégicas
- **Output:** Videos publicados en TikTok con descripciones optimizadas para viralización

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
8. python subir_tiktok_selenium_final_v5.py          # Upload individual
```

### Opción B: Pipeline Rápido (con imágenes existentes)
```bash
1. python prepare_viral_pipeline.py                  # Analiza imágenes + genera prompts profesionales
2. python generate_veo_video_from_image.py          # Genera videos virales optimizados
3. python procesar_final_tiktok.py                  # Optimiza para TikTok
4. python unir_videos_simple.py                     # Une videos finales
5. python subir_tiktok_selenium_final_v5.py         # Upload individual con descripción dinámica
```

### Opción C: **[NUEVO]** Upload Masivo Automatizado
```bash
1. python subir_multiples_videos_dinamicos.py       # Upload masivo de todos los videos mapeados
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

### Sistema de Descripciones Dinámicas **[NUEVO]**
- **Análisis Automático** del contenido de cada video desde `video_prompt_map.json`
- **3 Categorías Inteligentes:** ASMR, FoodTok, General Viral
- **9 Plantillas Virales** con hooks probados para engagement máximo
- **Personalización Contextual** usando elementos específicos del prompt original
- **Optimización de Hashtags** automática según el tipo de contenido
- **Sistema Anti-Spam** con variaciones únicas para cada video

### Sistema de Upload Automatizado **[NUEVO]**
- **Selenium Anti-Detección** con configuración stealth avanzada
- **XPaths Específicos** validados para todos los elementos de TikTok
- **Modal Handling Inteligente** que previene publicación prematura
- **Upload Individual** con confirmación y preview de descripción
- **Upload Masivo** con pausas estratégicas y resumen de resultados
- **Chrome Profile Persistence** para mantener sesión entre uploads

---

## 🎯 SISTEMA COMPLETO DE DESCRIPCIONES DINÁMICAS

### Funcionamiento del Sistema

1. **Carga del Mapeo:** El sistema lee `video_prompt_map.json` que contiene:
   ```json
   {
     "video": "path/to/video.mp4",
     "prompt": "Prompt original usado para generar el video",
     "imagen": "imagen_source.png"
   }
   ```

2. **Análisis de Contenido:** Identifica automáticamente el tipo de contenido:
   - **ASMR:** Detecta palabras como "asmr", "relajante", "sonidos", "crujientes"
   - **FoodTok:** Identifica "food", "comida", "chef", "cocina", "vegetales"
   - **General Viral:** Todo el demás contenido con efectos visuales

3. **Generación de Descripciones:** Usa plantillas específicas para cada categoría:

   **ASMR Templates:**
   - "🔥 ASMR VIRAL que te va a HIPNOTIZAR! {contenido}..."
   - "😱 NO PUEDES PARAR DE VER ESTO! {contenido}..."
   - "✨ ASMR que te va a hacer DORMIR en 30 segundos {contenido}..."

   **FoodTok Templates:**
   - "🍽️ FOODTOK VIRAL! {contenido}..."
   - "😍 COMIDA que se ve IRREAL! {contenido}..."
   - "🔥 RECETA VIRAL de TikTok! {contenido}..."

   **General Templates:**
   - "🤯 ESTO es lo más VIRAL de TikTok! {contenido}..."
   - "😱 NO VAS A CREER lo que acabas de ver! {contenido}..."
   - "✨ CONTENIDO que está ROMPIENDO Internet! {contenido}..."

4. **Personalización:** Extrae elementos específicos del prompt para personalizar el `{contenido}`:
   - "Capibara chef cortando vegetales de cristal" para videos de capibara
   - "Cortes de lima con efectos neón increíbles" para contenido de lima
   - "Efectos cyberpunk ÉPICOS" para contenido cyberpunk

### Opciones de Upload

#### Upload Individual (`subir_tiktok_selenium_final_v5.py`)
- Sube un video específico con descripción dinámica generada
- Muestra preview de la descripción antes de subir
- Ideal para testing y uploads puntuales

#### Upload Masivo (`subir_multiples_videos_dinamicos.py`)
- Procesa automáticamente todos los videos del mapeo
- Genera descripción única para cada video
- Incluye confirmación por video y pausas estratégicas
- Resumen completo del proceso con estadísticas

---

## 🔧 CONFIGURACIÓN Y REQUISITOS

### Archivos Necesarios
- `config/upload_cookies_playwright.json` - Cookies de sesión de TikTok
- `video_prompt_map.json` - Mapeo de videos y prompts
- `chrome_profile_selenium_final/` - Perfil persistente de Chrome

### Dependencias Adicionales
```bash
pip install selenium
```

### Configuración Inicial
1. Configurar cookies de TikTok en `config/upload_cookies_playwright.json`
2. Verificar que `video_prompt_map.json` esté actualizado
3. Ejecutar login manual la primera vez para establecer el perfil de Chrome

---

## 📊 MÉTRICAS Y OPTIMIZACIÓN

### Descripciones Optimizadas Para:
- **Engagement Máximo:** Hooks probados y llamadas a la acción específicas
- **Algoritmo de TikTok:** Hashtags estratégicos y palabras clave virales
- **Interacción:** Preguntas directas y elementos de sorpresa
- **Retención:** Elementos de curiosidad y promesas de valor

### Elementos Virales Incluidos:
- ✅ Emojis estratégicos para mayor visibilidad
- ✅ Preguntas directas para engagement
- ✅ Llamadas a la acción específicas (like, comment, share)
- ✅ Hashtags optimizados por categoría
- ✅ Elementos de sorpresa y curiosidad
- ✅ Lenguaje adaptado a la audiencia de TikTok
