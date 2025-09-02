# 🤖## 📋 Orden del Pipeline Completo

### 🎯 **Pipeline Principal de Análisis y Generación**
1. Ejecuta `test_tiktok_scraping.py` para analizar tu perfil y generar `data/analytics/tiktok_metrics_xxxxxxxxxx.json`.
2. Ejecuta `generate_prompts_from_scrap.py` para crear prompts virales fusionados en `data/analytics/fusion_prompts_auto.json` usando el JSON anterior.
3. Ejecuta `gen_images_from_prompts.py` para generar imágenes virales a partir de los prompts.
4. Ejecuta `generate_veo_video_from_image.py` para crear videos virales desde las imágenes y generar `video_prompt_map.json`.

### 🎬 **Pipeline de Optimización para TikTok** 
5. Ejecuta `procesar_final_tiktok.py` para optimizar los videos de Veo 3 con:
   - ✅ Zoom 1.2x óptimo para captura perfecta
   - ✅ Crop centrado para formato TikTok (720x1280)
   - ✅ Configuración perfecta para boca completa del pez
   - **Salida**: 3 videos individuales `*_tiktok_FINAL.mp4`

6. Ejecuta `unir_videos_simple.py` para crear versiones unificadas con transiciones:
   - ✅ Versión Simple: concatenación directa (`videos_unidos_SIMPLE_TIKTOK.mp4`)
   - ✅ Versión Fundido: transiciones suaves (`videos_unidos_FUNDIDO_TIKTOK.mp4`)
   - **Salida**: Videos listos para TikTok con efectos profesionales

### 📱 **Pipeline de Subida**
7. Ejecuta `subir_tiktok_playwright.py` (o `subir_tiktok_auto.py`) para subir los videos optimizados a TikTok usando el mapeo y agregando descripción/hashtags virales.

**🚀 Ejecución Rápida Completa:**
```powershell
# Después de tener videos de Veo 3 en data/videos/
python procesar_final_tiktok.py    # Optimizar individualmente  
python unir_videos_simple.py       # Unir con transiciones
python subir_tiktok_playwright.py  # Subir a TikTok
```

Así tienes el orden exacto para automatizar todo el proceso de análisis, generación, optimización y subida.ideo Automation System

Sistema 100% automático y gratuito para crear y subir videos a TikTok usando IA.

## � Orden del Pipeline Completo

1. Ejecuta `test_tiktok_scraping.py` para analizar tu perfil y generar `data/analytics/tiktok_metrics_xxxxxxxxxx.json`.
2. Ejecuta `generate_prompts_from_scrap.py` para crear prompts virales fusionados en `data/analytics/fusion_prompts_auto.json` usando el JSON anterior.
3. Ejecuta `gen_images_from_prompts.py` para generar imágenes virales a partir de los prompts.
4. Ejecuta `generate_veo_video_from_image.py` para crear videos virales desde las imágenes y generar `video_prompt_map.json`.
5. Ejecuta `subir_tiktok_playwright.py` (o `subir_tiktok_auto.py`) para subir los videos generados a TikTok usando el mapeo y agregando descripción/hashtags virales.

Así tienes el orden exacto para automatizar todo el proceso de análisis, generación y subida.

## �🚀 Características

- ✅ **100% Gratuito**: Usa APIs gratuitas y GitHub Actions
- ✅ **100% Automático**: Funciona sin tu computadora encendida
- ✅ **Análisis Inteligente**: Analiza tus videos existentes para optimizar
- ✅ **Generación IA**: Crea imágenes con Gemini y videos con Veo3
- ✅ **Auto-Upload**: Sube automáticamente a TikTok
- ✅ **3 videos/día**: Ejecuta 3 veces al día automáticamente

## 📊 Estadísticas del Sistema

- **Videos analizados**: 109+ videos de tu cuenta
- **Tasa de éxito**: 19.3% videos high-performance
- **Objetivo actual**: 1,270+ views por video
- **Estrategia**: Comedia relatable optimizada

## Estructura del Proyecto

```
videosautomation/
├── src/
│   ├── analytics/
│   │   ├── tiktok_scraper.py      # Scraping de métricas TikTok
│   │   ├── trend_analyzer.py      # Análisis de tendencias
│   │   └── metrics_processor.py   # Procesamiento de métricas
│   ├── generation/
│   │   ├── image_generator.py     # Generación de imágenes con Gemini
│   │   ├── video_generator.py     # Generación de videos con Veo3
│   │   └── prompt_generator.py    # Generación de prompts
│   ├── upload/
│   │   ├── tiktok_uploader.py     # Subida a TikTok
│   │   └── content_formatter.py   # Formateo de contenido
│   ├── utils/
│   │   ├── config.py              # Configuración
│   │   ├── logger.py              # Sistema de logs
│   │   └── helpers.py             # Funciones auxiliares
│   └── main.py                    # Script principal
├── data/
│   ├── metrics/                   # Datos de métricas
│   ├── images/                    # Imágenes generadas
│   ├── videos/                    # Videos generados
│   └── prompts/                   # Prompts guardados
├── config/
│   ├── tiktok_cookies.json        # Cookies de TikTok
│   └── config.yml                 # Configuración general
├── requirements.txt
├── .env.example
├── .gitignore
└── automation/
    └── .github/
        └── workflows/
            └── video_automation.yml  # GitHub Actions
```

## Configuración

1. Copiar `.env.example` a `.env` y completar las variables
2. Colocar las cookies de TikTok en `config/tiktok_cookies.json`
3. Instalar dependencias: `pip install -r requirements.txt`

## Uso

### Ejecución manual
```bash
python src/main.py
```

### Automatización con GitHub Actions
El sistema se ejecuta automáticamente 1-3 veces al día usando GitHub Actions.

## APIs Utilizadas

- **Gemini API**: Generación de imágenes
- **Veo3 API**: Generación de videos (cuenta educativa)
- **TikTok**: Subida de contenido (cookies)

## Frecuencia

- Mínimo: 1 vez al día
- Máximo: 3 veces al día
- Límite Veo3: 3 videos gratis por día
