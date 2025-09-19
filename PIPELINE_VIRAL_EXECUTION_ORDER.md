# Orden de Ejecución del Pipeline de Automatización de Videos

Este documento describe el orden secuencial para ejecutar los scripts que componen el pipeline de generación de videos virales para TikTok con sistema de descripciones dinámicas.

---

### 1. Extracción de Datos y Análisis de Tendencias

- **Script:** `test_tiktok_scraping.py`
- **Propósito:** Extrae datos y métricas de una cuenta de TikTok para identificar tendencias, conceptos de video y analizar el rendimiento de contenido existente.
- **Output:** Análisis de 75 videos con métricas de engagement y tendencias detectadas.

### 2. Generación de Prompts para Imágenes (Selenium)

- **Script:** `generate_prompts_from_scrap.py`
- **Propósito:** Utiliza los datos extraídos del scraping para generar, mediante la UI de Gemini (Selenium), prompts creativos y optimizados para la creación de imágenes virales. Tiene un fallback a prompts pre-definidos en caso de fallo.
- **Output:** `data/analytics/fusion_prompts_auto.json` con prompts base optimizados.

### 3. Generación de Imágenes (Selenium)

- **Script:** `gen_images_from_prompts.py`
- **Propósito:** Toma los prompts generados y los utiliza para crear imágenes visualmente impactantes usando la UI de Gemini (Selenium). Si falla, utiliza Pollinations y HuggingFace como fallbacks.
- **Output:** Imágenes `data/images/viral_image_1.png` a `data/images/viral_image_6.png` listas para video.

### 4. Generación de Videos a partir de Imágenes

- **Script:** `generate_veo_video_from_image.py`
- **Propósito:** Convierte las imágenes generadas en videos cortos y dinámicos utilizando la API de Veo3 con prompts optimizados.
- **Output:** Videos MP4 optimizados para TikTok.

### 5. Optimización y Procesamiento Final de Videos

- **Script:** `procesar_final_tiktok.py`
- **Propósito:** Aplica optimizaciones finales a los videos generados, incluyendo crop centrado y zoom, para asegurar la configuración óptima para plataformas como TikTok.

### 6. Unión de Videos

- **Script:** `unir_videos_simple.py`
- **Propósito:** Combina múltiples videos optimizados en un solo video final, listo para su publicación.

### 7. **[SISTEMA DUAL COMPLETO]** Upload Automatizado TikTok + YouTube Shorts

- **Scripts Principales:** 
  - `dual_platform_uploader.py` - **[NUEVO]** Sistema dual completo TikTok + YouTube Shorts
  - `subir_tiktok_selenium_final_v5.py` - Upload TikTok individual con descripción dinámica
  - `youtube_shorts_uploader.py` - **[NUEVO]** Upload YouTube Shorts con API v3
  - `test_tiktok_upload.py` - **[NUEVO]** Test de funcionamiento TikTok
  - `upload_shorts_now.py` - **[NUEVO]** Upload directo YouTube Shorts
- **Propósito:** Sistema dual automatizado que sube videos a ambas plataformas principales de videos cortos con optimizaciones específicas para cada una.
- **Características Avanzadas:**
  - **🔄 Dual Platform:** Upload simultáneo o independiente a TikTok y YouTube Shorts
  - **📱 TikTok Optimizado:** Descripciones dinámicas, anti-detección, XPaths específicos
  - **🎬 YouTube Shorts API:** Integración completa con YouTube Data API v3 y OAuth 2.0
  - **🎯 Títulos Virales:** 10 plantillas optimizadas para YouTube Shorts
  - **🔐 Seguridad:** Sistema de credenciales seguro con archivos template
  - **📊 Analytics:** Tracking y logs detallados de uploads en ambas plataformas
  - **⚡ Smart Routing:** Videos 'processed' → TikTok, Videos 'FUNDIDO' → YouTube Shorts
- **Output:** Videos publicados simultáneamente en TikTok y YouTube Shorts con optimizaciones específicas

---

## 🎬 FLUJO OPTIMIZADO RECOMENDADO

### **🤖 Opción AUTOMÁTICA: Pipeline Completo Dual Platform**
```bash
python run_complete_pipeline.py                     # Ejecuta TODO automáticamente (45-60 min)
python dual_platform_uploader.py                   # [NUEVO] Upload dual TikTok + YouTube Shorts
```
**Características:**
- ✅ Ejecuta los 7 pasos automáticamente
- ✅ Upload dual a TikTok + YouTube Shorts
- ✅ Manejo de timeouts inteligente
- ✅ Logging detallado de cada paso
- ✅ Continúa aunque fallen pasos opcionales
- ✅ Reporte JSON completo al final
- ✅ No requiere intervención humana

### Opción A: Pipeline Completo Manual con Dual Upload
```bash
1. python test_tiktok_scraping.py
2. python generate_prompts_from_scrap.py  
3. python gen_images_from_prompts.py
4. python generate_veo_video_from_image.py
5. python procesar_final_tiktok.py
6. python unir_videos_simple.py
7. python dual_platform_uploader.py
8. python upload_to_drive.py               # [NUEVO] Upload to drive
```

### Opción B: Pipeline Rápido con Dual Upload
```bash
1. python generate_veo_video_from_image.py          # Genera videos desde imágenes existentes
2. python procesar_final_tiktok.py                  # Optimiza para TikTok
3. python unir_videos_simple.py                     # Une videos finales
4. python dual_platform_uploader.py                 # [NUEVO] Upload dual TikTok + YouTube
```

### Opción C: Uploads Individuales por Plataforma
```bash
# Solo TikTok
python test_tiktok_upload.py                        # [NUEVO] Test TikTok
python subir_tiktok_selenium_final_v5.py           # Upload individual TikTok

# Solo YouTube Shorts  
python upload_shorts_now.py                         # [NUEVO] Upload YouTube Shorts

# Upload Masivo TikTok
python subir_multiples_videos_dinamicos.py         # Upload masivo TikTok
```

### Opción D: **[RECOMENDADA]** Sistema Dual Completo
```bash
python dual_platform_uploader.py                    # [NUEVO] Sistema dual automático
```
**Características del Sistema Dual:**
- 🔄 **Routing Inteligente:** Videos 'processed' → TikTok, Videos 'FUNDIDO' → YouTube
- 📱 **TikTok Optimizado:** Descripciones dinámicas + anti-detección
- 🎬 **YouTube API:** Títulos virales + OAuth 2.0 + metadata optimizada
- ⏰ **Upload Escalonado:** Tiempos de espera para evitar rate limits
- 📊 **Tracking Completo:** Logs y seguimiento de ambas plataformas

---

## 🤖 ORQUESTADOR COMPLETO AUTOMATIZADO

### Características del Orquestador (`run_complete_pipeline.py`)

- **Ejecución Automática:** No requiere intervención humana durante todo el proceso
- **Manejo de Timeouts:** Cada paso tiene timeout específico (3-15 minutos según complejidad)
- **Logging Inteligente:** Registra cada paso con timestamps y duración
- **Continuidad:** Si un paso opcional falla, continúa con el siguiente
- **Detención Inteligente:** Se detiene solo si fallan pasos críticos requeridos
- **Reporte Completo:** Genera reporte JSON detallado al final
- **Verificación de Prerequisites:** Verifica archivos y directorios necesarios

### Timeouts por Paso:
1. **Scraping TikTok:** 5 minutos
2. **Generación de Prompts:** 4 minutos  
3. **Generación de Imágenes:** 10 minutos
4. **Generación de Videos:** 15 minutos
5. **Procesamiento Final:** 5 minutos
6. **Unión de Videos:** 3 minutos (opcional)
7. **Upload Dual TikTok + YouTube:** 20 minutos **[ACTUALIZADO]**

### Uso Recomendado:
```bash
# Ejecución completa automática con dual upload
python run_complete_pipeline.py

# Solo sistema dual upload
python dual_platform_uploader.py

# Test individual de plataformas
python test_tiktok_upload.py          # Test TikTok
python upload_shorts_now.py           # Test YouTube Shorts

# El script mostrará:
# - Verificación de prerequisites
# - Progreso de cada paso en tiempo real
# - Uploads a ambas plataformas
# - Resumen final con estadísticas
# - Reporte JSON guardado automáticamente
```

---

## � SISTEMA DUAL PLATFORM COMPLETO

### Arquitectura del Sistema Dual

El sistema dual permite publicar contenido simultáneamente en **TikTok** y **YouTube Shorts**, maximizando el alcance y engagement del contenido viral generado.

#### **📱 TikTok Pipeline:**
- **Input:** Videos de `data/videos/processed/`
- **Características:** 
  - Selenium automatizado con anti-detección
  - Descripciones dinámicas generadas por IA
  - Sistema de XPaths específicos validados
  - Manejo inteligente de modales
- **Output:** Videos publicados en TikTok con descripciones optimizadas

#### **🎬 YouTube Shorts Pipeline:**
- **Input:** Videos de `data/videos/final/` (archivos con "FUNDIDO")
- **Características:**
  - YouTube Data API v3 con OAuth 2.0
  - Títulos virales optimizados (10 plantillas)
  - Metadata automática (categoría, tags, descripción)
  - Configuración automática como NO contenido para niños
- **Output:** Videos publicados en YouTube Shorts con optimización viral

### Scripts del Sistema Dual

#### **Configuración y Setup:**
```bash
# Configuración inicial YouTube
python test_youtube_direct.py                       # Setup OAuth YouTube
python configure_video_settings.py                  # Configurar metadata

# Test de funcionamiento
python test_tiktok_upload.py                        # Test TikTok
python upload_shorts_now.py                         # Test YouTube Shorts
```

#### **Upload Dual Automático:**
```bash
python dual_platform_uploader.py                    # Sistema dual completo
```

#### **Uploads Individuales:**
```bash
# Solo TikTok
python subir_tiktok_selenium_final_v5.py

# Solo YouTube Shorts
python upload_shorts_now.py
python force_youtube_upload.py                      # Force upload si hay errores
```

### Configuración de Credenciales

#### **YouTube (OAuth 2.0):**
```bash
# Archivos requeridos:
config/youtube_credentials.json                     # Credenciales OAuth (template provided)
config/youtube_token.json                          # Token generado automáticamente

# Setup:
1. Completar youtube_credentials.json con client_id y client_secret
2. Ejecutar python test_youtube_direct.py
3. Autorizar en navegador (una sola vez)
4. Sistema guarda token automáticamente
```

#### **TikTok (Selenium):**
```bash
# Sistema automático:
- Chrome profile persistente en chrome_profile_selenium_final/
- Login manual en primera ejecución
- Cookies guardadas automáticamente
- Anti-detección configurado
```

### Ventajas del Sistema Dual

✅ **Maximización de Alcance:** Presencia en ambas plataformas principales
✅ **Optimización Específica:** Cada plataforma con sus mejores prácticas  
✅ **Automation Completa:** Upload simultáneo sin intervención manual
✅ **Tracking Unificado:** Logs y seguimiento de ambas plataformas
✅ **Fallback Systems:** Si una plataforma falla, la otra continúa
✅ **Rate Limit Management:** Tiempos de espera inteligentes
✅ **Content Routing:** Videos optimizados para cada plataforma automáticamente

---

## �🚀 SISTEMA DE DESCRIPCIONES DINÁMICAS

### Características Principales
- **Análisis Automático** del contenido de cada video desde `video_prompt_map.json`
- **3 Categorías Inteligentes:** ASMR, FoodTok, General Viral
- **9 Plantillas Virales** con hooks probados para engagement máximo
- **Personalización Contextual** usando elementos específicos del prompt original
- **Optimización de Hashtags** automática según el tipo de contenido
- **Sistema Anti-Spam** con variaciones únicas para cada video

### Sistema de Upload Automatizado
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
- `config/youtube_credentials.json` - **[NUEVO]** Credenciales OAuth YouTube (template provided)
- `config/youtube_token.json` - **[NUEVO]** Token OAuth generado automáticamente
- `video_prompt_map.json` - Mapeo de videos y prompts
- `chrome_profile_selenium_final/` - Perfil persistente de Chrome
- `data/videos/processed/` - **[NUEVO]** Videos para TikTok
- `data/videos/final/` - **[NUEVO]** Videos FUNDIDO para YouTube Shorts

### Dependencias Adicionales
```bash
# Dependencias base
pip install selenium webdriver-manager

# Dependencias YouTube API
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install google-api-python-client

# Dependencias completas
pip install -r requirements.txt
```

### Configuración Inicial Dual Platform

#### **Setup TikTok:**
1. Configurar cookies de TikTok en `config/upload_cookies_playwright.json`
2. Verificar que `video_prompt_map.json` esté actualizado
3. Ejecutar login manual la primera vez para establecer el perfil de Chrome

#### **Setup YouTube Shorts:** **[NUEVO]**
1. Crear proyecto en Google Cloud Console
2. Habilitar YouTube Data API v3
3. Configurar OAuth Consent Screen (Testing mode)
4. Crear credenciales OAuth 2.0
5. Completar `config/youtube_credentials.json` con client_id y client_secret
6. Ejecutar `python test_youtube_direct.py` para autorizar y generar token
7. Sistema guarda automáticamente en `config/youtube_token.json`

#### **Verificación del Sistema:**
```bash
# Test completo del sistema dual
python test_tiktok_upload.py                        # Verificar TikTok
python upload_shorts_now.py                         # Verificar YouTube Shorts
python dual_platform_uploader.py                    # Test sistema dual completo
```

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

---

## 📋 RESUMEN DE COMANDOS PRINCIPALES

### **🚀 Comandos Más Usados (Sistema Dual)**

```bash
# Pipeline completo automático con dual upload
python run_complete_pipeline.py && python dual_platform_uploader.py

# Solo sistema dual upload (videos ya generados)
python dual_platform_uploader.py

# Tests individuales
python test_tiktok_upload.py                        # Test TikTok
python upload_shorts_now.py                         # Test YouTube Shorts

# Setup inicial
python test_youtube_direct.py                       # Configurar YouTube OAuth
python configure_video_settings.py                  # Configurar metadata videos
```

### **📱 Solo TikTok**
```bash
python subir_tiktok_selenium_final_v5.py           # Upload individual
python subir_multiples_videos_dinamicos.py         # Upload masivo
python test_tiktok_upload.py                       # Test funcionamiento
```

### **🎬 Solo YouTube Shorts**
```bash
python upload_shorts_now.py                        # Upload directo
python force_youtube_upload.py                     # Force upload
python configure_video_settings.py                 # Configurar metadata
```

### **⚙️ Configuración y Diagnóstico**
```bash
python SYSTEM_READY.py                             # Estado del sistema
python test_youtube_direct.py                      # Setup YouTube OAuth
python diagnose_token.py                           # Diagnosticar tokens
```

---

## 🎯 RECOMENDACIONES FINALES

### **Para Máximo Rendimiento:**
1. **Usar Sistema Dual:** `python dual_platform_uploader.py` - Maximiza alcance
2. **Pipeline Automático:** `python run_complete_pipeline.py` - Proceso completo sin intervención
3. **Monitoreo:** Revisar logs en `logs/` para optimización continua
4. **Backup:** Mantener copias de `config/` y `data/` regularmente

### **Flujo Recomendado Diario:**
```bash
# Generación completa automática (1 vez al día)
python run_complete_pipeline.py

# Upload dual automático (2-3 veces al día)
python dual_platform_uploader.py

# Monitoreo y ajustes
python SYSTEM_READY.py
```

**🎉 ¡Sistema Dual Platform completamente funcional!**
