# 🧹 PLAN DE REFACTORIZACIÓN VIDEOSAUTOMATION

## 📊 ANÁLISIS ACTUAL
- **Total archivos**: 100+ archivos en root
- **Archivos Python**: 50+ scripts
- **Archivos debug**: 30+ imágenes/HTML
- **Videos generados**: 10+ archivos MP4
- **Estado**: Muy desorganizado, muchos duplicados

## 🎯 OBJETIVOS DE REFACTORIZACIÓN
1. **Reducir archivos**: De 100+ a menos de 30 archivos importantes
2. **Organizar estructura**: Mover todo a carpetas apropiadas
3. **Consolidar scripts**: Unir funcionalidades similares
4. **Limpiar debug**: Eliminar archivos temporales
5. **Crear pipeline claro**: Scripts principales bien definidos

## 📁 NUEVA ESTRUCTURA PROPUESTA

```
videosautomation/
├── 📁 core/                          # Scripts principales del pipeline
│   ├── 01_scrape_analytics.py        # Análisis TikTok (era test_tiktok_scraping.py)
│   ├── 02_generate_prompts.py        # Generación prompts (era generate_prompts_from_scrap.py)
│   ├── 03_generate_images.py         # Generación imágenes (era gen_images_from_prompts.py)
│   ├── 04_generate_videos.py         # Generación videos (era generate_veo_video_from_image.py)
│   ├── 05_optimize_videos.py         # Optimización TikTok (era procesar_final_tiktok.py)
│   ├── 06_unite_videos.py            # Unir con transiciones (era unir_videos_simple.py)
│   └── 07_upload_tiktok.py           # Subida TikTok (era subir_tiktok_playwright.py)
├── 📁 utils/                         # Utilidades comunes
│   ├── gemini_utils.py               # Funciones Gemini
│   ├── video_utils.py                # Funciones video (FFmpeg)
│   ├── tiktok_utils.py               # Funciones TikTok
│   └── config_utils.py               # Configuración
├── 📁 data/                          # Datos del proyecto
│   ├── analytics/                    # Métricas y análisis
│   ├── images/                       # Imágenes generadas
│   ├── videos/                       # Videos (original, procesados, finales)
│   └── logs/                         # Logs del sistema
├── 📁 config/                        # Configuración
│   ├── tiktok_cookies.json
│   └── settings.json
├── 📁 archive/                       # Archivos históricos/backup
│   └── old_scripts/                  # Scripts antiguos por si acaso
├── 📱 run_pipeline.py                # Script principal que ejecuta todo
├── 🔧 setup.py                       # Configuración inicial
├── 📋 requirements.txt               # Dependencias
├── 📖 README.md                      # Documentación
└── 🔐 .env                          # Variables de entorno
```

## 🗂️ CLASIFICACIÓN DE ARCHIVOS ACTUALES

### ✅ **MANTENER Y CONSOLIDAR** (Scripts principales)
- `test_tiktok_scraping.py` → `core/01_scrape_analytics.py`
- `generate_prompts_from_scrap.py` → `core/02_generate_prompts.py` 
- `gen_images_from_prompts.py` → `core/03_generate_images.py`
- `generate_veo_video_from_image.py` → `core/04_generate_videos.py`
- `procesar_final_tiktok.py` → `core/05_optimize_videos.py`
- `unir_videos_simple.py` → `core/06_unite_videos.py`
- `subir_tiktok_playwright.py` → `core/07_upload_tiktok.py`

### 🔧 **CONSOLIDAR EN UTILS**
- `gemini_utils.py` → `utils/gemini_utils.py`
- Funciones de video → `utils/video_utils.py`
- Funciones TikTok → `utils/tiktok_utils.py`

### 📦 **ARCHIVAR** (Scripts de desarrollo/testing)
- `test_*.py` (30+ archivos) → `archive/testing/`
- `*_test.py`, `*_debug.py` → `archive/testing/`
- Scripts experimentales → `archive/experiments/`

### 🗑️ **ELIMINAR** (Archivos temporales/duplicados)
- `debug_*.png` (50+ archivos)
- `dragdrop_*.png` (30+ archivos)  
- `gemini_image_*.png` (archivos temporales)
- `*.html` (archivos debug)
- Videos de prueba antiguos
- `__pycache__/`

### 📁 **ORGANIZAR** (Mover a carpetas)
- Videos finales → `data/videos/final/`
- Videos originales → `data/videos/original/`
- Videos procesados → `data/videos/processed/`

## 🚀 PLAN DE EJECUCIÓN

### **FASE 1: Preparación**
1. Crear nueva estructura de carpetas
2. Backup de archivos importantes
3. Crear script de migración

### **FASE 2: Consolidación**
1. Unir scripts similares
2. Crear pipeline principal
3. Mover utilidades a utils/

### **FASE 3: Limpieza**
1. Archivar archivos de testing
2. Eliminar archivos temporales
3. Organizar videos por categorías

### **FASE 4: Documentación**
1. Actualizar README.md
2. Crear documentación de cada script
3. Crear guía de uso simple

## 📈 BENEFICIOS ESPERADOS
- ✅ **90% menos archivos** en directorio root
- ✅ **Pipeline claro** de 7 pasos numerados
- ✅ **Fácil mantenimiento** con utils organizadas
- ✅ **Documentación clara** para nuevos usuarios
- ✅ **Ejecución simple** con `python run_pipeline.py`

## ⚡ COMANDOS DE EJECUCIÓN SIMPLIFICADOS

**Antes** (complicado):
```bash
python test_tiktok_scraping.py
python generate_prompts_from_scrap.py  
python gen_images_from_prompts.py
python generate_veo_video_from_image.py
python procesar_final_tiktok.py
python unir_videos_simple.py
python subir_tiktok_playwright.py
```

**Después** (simple):
```bash
python run_pipeline.py --all              # Pipeline completo
python run_pipeline.py --steps 1-4        # Solo generación
python run_pipeline.py --step 5           # Solo optimización
python core/05_optimize_videos.py         # Script individual
```

¿Procedemos con la refactorización? ¿Hay algún aspecto específico que quieras modificar del plan?
