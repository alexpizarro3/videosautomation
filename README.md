# 🤖 TikTok Video Automation System

Sistema 100% automático y gratuito para crear y subir videos a TikTok usando IA.

## 🚀 Características

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
