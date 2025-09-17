# Pipeline Narrativo ASMR - Orden de Ejecución

Este documento describe el orden secuencial para ejecutar los scripts que componen el **Pipeline Narrativo ASMR**, un sistema paralelo que genera historias envolventes basadas en análisis de TikTok viral.

---

## 🎭 PIPELINE NARRATIVO ASMR

### 1. Extracción de Datos y Análisis de Tendencias

- **Script:** `test_tiktok_scraping.py` ✅ *Reutilizado*
- **Propósito:** Extrae datos y métricas de una cuenta de TikTok para identificar tendencias, conceptos de video y analizar el rendimiento de contenido existente.
- **Output:** Análisis de 75 videos con métricas de engagement y tendencias detectadas.

### 2. Generación de Historias Narrativas ASMR

- **Script:** `generate_story_prompts_from_scrap.py` 🆕 *Nuevo*
- **Propósito:** Analiza los datos del scraping para crear 2 historias ASMR envolventes y narrativas basadas en los contenidos más virales detectados.
- **Output:** `data/analytics/story_prompts_narrative.json` con 2 historias completas.
- **Características:**
  - Análisis de patrones virales de TikTok
  - Generación de 2 historias ASMR competitivas
  - Enfoque en sonido envolvente y adictivo
  - Narrativa secuencial coherente

### 3. Generación de Imágenes por Historia

- **Script:** `generate_story_images.py` 🆕 *Nuevo*
- **Propósito:** Genera 6 imágenes (3 por cada historia) que representen visualmente las narrativas ASMR creadas.
- **Output:** 6 imágenes en `data/images/` (story1_image_1-3.png, story2_image_1-3.png)
- **Características:**
  - 3 imágenes secuenciales por historia
  - Elementos visuales ASMR sin efectos de ecualizador
  - Coherencia visual en cada narrativa

### 4. Selección de la Mejor Historia

- **Script:** `select_best_story.py` 🆕 *Nuevo*
- **Propósito:** Evalúa ambas historias y selecciona la más prometedora basándose en criterios de viralidad y potencial ASMR.
- **Output:** 3 imágenes finales de la historia ganadora (renombradas a `gemini_image_1-3.png`)
- **Criterios de Evaluación:**
  - Potencial viral basado en análisis de TikTok
  - Coherencia narrativa ASMR
  - Calidad y consistencia visual
  - Potencial de engagement

### 5. Generación de Videos Narrativos Secuenciales

- **Script:** `generate_narrative_videos.py` 🆕 *Nuevo*
- **Propósito:** Crea 3 videos que narran la historia seleccionada de forma secuencial, cada uno basado en una imagen específica.
- **Output:** Videos MP4 que cuentan la historia completa con sonido ASMR envolvente.
- **Características ASMR:**
  - Sonido envolvente de principio a fin
  - Audio adictivo sin efectos visuales de ecualizador
  - Transiciones suaves entre secuencias
  - Narrativa coherente a través de los 3 videos

### 6. Optimización y Procesamiento Final de Videos

- **Script:** `procesar_final_tiktok.py` ✅ *Reutilizado*
- **Propósito:** Aplica optimizaciones finales a los videos generados, incluyendo crop centrado y zoom, para asegurar la configuración óptima para plataformas como TikTok.

### 7. Unión de Videos

- **Script:** `unir_videos_simple.py` ✅ *Reutilizado*
- **Propósito:** Combina los 3 videos narrativos en un solo video final que cuenta la historia completa ASMR.

### 8. Upload Automatizado TikTok + YouTube Shorts

- **Script:** `dual_platform_uploader.py` ✅ *Reutilizado*
- **Propósito:** Sistema dual automatizado que sube el video narrativo a ambas plataformas principales de videos cortos.

### 9. Subida automática de archivos generados a Google Drive

- **Script:** `upload_to_drive.py` ✅ *Reutilizado*
- **Propósito:** Sube automáticamente las imágenes generadas y los videos procesados/fundidos a las carpetas correspondientes en Google Drive para análisis y respaldo.

---

## 🎬 FLUJO NARRATIVO RECOMENDADO

### **🎭 Pipeline Narrativo ASMR Completo**
```bash
1. python test_tiktok_scraping.py                   # ✅ Análisis de tendencias virales
2. python generate_story_prompts_from_scrap.py      # 🆕 Crea 2 historias ASMR
3. python generate_story_images.py                  # 🆕 6 imágenes (3 por historia)
4. python select_best_story.py                      # 🆕 Selecciona mejor historia
5. python generate_narrative_videos_veo3.py              # 🆕 Videos secuenciales narrativos
6. python procesar_final_tiktok.py                  # ✅ Optimización para TikTok
7. python unir_videos_simple.py                     # ✅ Une la historia completa
8. python dual_uploader_automatic.py                # ✅ Upload dual automático
9. python upload_to_drive.py                        # ✅ Backup en la nube
```

### **Características del Pipeline Narrativo:**
- ✅ **Historias Coherentes:** Narrativa ASMR envolvente de principio a fin
- ✅ **Análisis Viral:** Basado en datos reales de TikTok trending
- ✅ **Competencia de Historias:** 2 historias compiten, se selecciona la mejor
- ✅ **Sonido Inmersivo:** Audio ASMR adictivo sin efectos visuales
- ✅ **Secuencia Visual:** 3 imágenes que narran la historia completa
- ✅ **Output Idéntico:** Mismo resultado final (3 videos) que el pipeline original
- ✅ **Reutilización:** Aprovecha scripts existentes optimizados

---

## 🆚 COMPARACIÓN DE PIPELINES

### **Pipeline Original (Viral Básico)**
- Enfoque: Contenido viral individual
- Imágenes: 6 imágenes independientes
- Videos: 3 videos sin narrativa conectada
- Tiempo: 45-60 minutos

### **Pipeline Narrativo ASMR**
- Enfoque: Historia narrativa ASMR coherente
- Imágenes: 6 imágenes (2 historias de 3 cada una)
- Videos: 3 videos que narran una historia completa
- Tiempo: 50-70 minutos (incluye selección de historia)

---

## 🎯 VENTAJAS DEL PIPELINE NARRATIVO

### **📚 Storytelling Avanzado:**
- Narrativas coherentes que mantienen la atención
- Historias basadas en análisis de contenido viral real
- ASMR envolvente que genera adicción auditiva

### **🧠 Inteligencia Competitiva:**
- Sistema de evaluación automática de historias
- Selección basada en métricas de viralidad
- Optimización continua del contenido

### **🎵 Experiencia ASMR Superior:**
- Sonido diseñado para ser adictivo
- Sin distracciones visuales (ecualizadores)
- Inmersión auditiva de principio a fin

### **📈 Mayor Engagement Potencial:**
- Narrativas que conectan emocionalmente
- Contenido secuencial que genera expectativa
- Historias memorables y compartibles

---

## 🔧 CONFIGURACIÓN ESPECÍFICA NARRATIVA

### **Archivos Adicionales Generados:**
- `data/analytics/story_prompts_narrative.json` - Historias ASMR generadas
- `data/analytics/story_evaluation.json` - Evaluación y selección de historias
- `data/images/story1_image_*.png` - Imágenes de la primera historia
- `data/images/story2_image_*.png` - Imágenes de la segunda historia
- `data/videos/narrative_*.mp4` - Videos narrativos secuenciales

### **Dependencias Adicionales:**
```bash
# Todas las dependencias del pipeline original +
pip install nltk                    # Para análisis de texto narrativo
pip install textstat               # Para evaluación de legibilidad
pip install transformers           # Para generación de historias avanzada
```

---

## 📋 COMANDOS DE EJECUCIÓN

### **🎭 Pipeline Narrativo Completo:**
```bash
# Ejecución manual paso a paso
python test_tiktok_scraping.py
python generate_story_prompts_from_scrap.py
python generate_story_images.py
python select_best_story.py
python generate_narrative_videos_veo3.py
python procesar_final_tiktok.py
python unir_videos_simple.py
python dual_uploader_automatic.py
python upload_to_drive.py
```

### **🎬 Comparación Rápida:**
```bash
# Pipeline Original
python run_complete_pipeline.py

# Pipeline Narrativo (cuando esté implementado)
python run_narrative_pipeline.py
```

---

## 🎯 PRÓXIMOS PASOS DE IMPLEMENTACIÓN

### **Orden de Desarrollo:**
1. 🆕 `generate_story_prompts_from_scrap.py` - Base del sistema narrativo
2. 🆕 `generate_story_images.py` - Generación visual de historias
3. 🆕 `select_best_story.py` - Sistema de evaluación inteligente
4. 🆕 `generate_narrative_videos.py` - Videos secuenciales ASMR
5. 🆕 `run_narrative_pipeline.py` - Orquestador completo

---

**🎉 ¡Pipeline Narrativo ASMR - El futuro del contenido viral envolvente!**
