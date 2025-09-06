# 🗺️ MAPA COMPLETO DE DEPENDENCIAS - VIDEOSAUTOMATION

## 📋 DEPENDENCIAS LOCALES CRÍTICAS

### 🔥 **ARCHIVOS PRINCIPALES CON DEPENDENCIAS LOCALES**

#### `generate_veo_video_from_image.py` (CRÍTICO)
```python
from viral_video_prompt_generator import ViralVideoPromptGenerator, enhance_existing_prompts
from image_metadata_analyzer import ImageMetadataAnalyzer  
from viral_image_selector import ViralImageSelector
```
**DEPENDENCIAS:**
- `viral_video_prompt_generator.py` ✅
- `image_metadata_analyzer.py` ✅ 
- `viral_image_selector.py` ✅

#### `subir_tiktok_selenium_final_v5.py` (SISTEMA PRINCIPAL)
```python
from dynamic_description_generator import DynamicDescriptionGenerator
```
**DEPENDENCIAS:**
- `dynamic_description_generator.py` ✅

#### `subir_multiples_videos_dinamicos.py`
```python
from subir_tiktok_selenium_final_v5 import (
    setup_selenium_driver,
    load_video_mapping,
    upload_single_video
)
from dynamic_description_generator import DynamicDescriptionGenerator
```
**DEPENDENCIAS:**
- `subir_tiktok_selenium_final_v5.py` ✅
- `dynamic_description_generator.py` ✅

#### `subir_multiples_videos_ultra_dinamicos.py`
```python
from dynamic_description_generator import DynamicDescriptionGenerator
```
**DEPENDENCIAS:**
- `dynamic_description_generator.py` ✅

#### `prepare_viral_pipeline.py`
```python
from image_metadata_analyzer import ImageMetadataAnalyzer, analyze_existing_images, save_image_analysis_report
from viral_video_prompt_generator import ViralVideoPromptGenerator
```
**DEPENDENCIAS:**
- `image_metadata_analyzer.py` ✅
- `viral_video_prompt_generator.py` ✅

---

## 🏗️ **ARCHIVOS CORE COPIADOS (CON DEPENDENCIAS ORIGINALES)**

### `core/04_generate_videos.py` (copia de `generate_veo_video_from_image.py`)
**PROBLEMA:** Mantiene imports de archivos raíz que se moverán
```python
# ESTOS IMPORTS FALLARÁN después del refactoring
from viral_video_prompt_generator import ViralVideoPromptGenerator
from image_metadata_analyzer import ImageMetadataAnalyzer
from viral_image_selector import ViralImageSelector
```

---

## 🎯 **ARCHIVOS QUE NO TIENEN DEPENDENCIAS LOCALES (SEGUROS)**

### Scripts Principales Independientes:
- `test_tiktok_scraping.py` ✅
- `generate_prompts_from_scrap.py` ✅ 
- `gen_images_from_prompts.py` ✅
- `procesar_final_tiktok.py` ✅
- `unir_videos_simple.py` ✅
- `gemini_utils.py` ✅
- `verify_image_paths.py` ✅

### Upload Scripts Independientes:
- `subir_tiktok_optimized.py` ✅
- `subir_tiktok_playwright.py` ✅
- Todos los scripts `subir_tiktok_*` (excepto los que usan dynamic_description_generator)

---

## 🔧 **ARCHIVOS DE UTILIDADES**

### Utilidades Independientes:
- `gemini_utils.py` ✅
- `setup.py` ✅
- `refactor.py` ✅

---

## 📦 **ARCHIVOS DE TESTING (SEGUROS PARA ARCHIVAR)**

### Scripts de Test (Sin dependencias críticas):
- `test_*.py` (30+ archivos) ✅
- `*_test.py` ✅
- `*_debug.py` ✅
- `diagnostic_*.py` ✅

---

## 🚨 **PLAN DE REFACTORING SEGURO**

### FASE 1: CONSERVAR ARCHIVOS CRÍTICOS EN RAÍZ
**Mantener en raíz durante refactoring:**
- `dynamic_description_generator.py` 🔒
- `viral_video_prompt_generator.py` 🔒
- `image_metadata_analyzer.py` 🔒
- `viral_image_selector.py` 🔒
- `subir_tiktok_selenium_final_v5.py` 🔒

### FASE 2: ACTUALIZAR IMPORTS EN CORE/
**Archivos que necesitan actualización de imports:**
- `core/04_generate_videos.py` 
  - Cambiar: `from viral_video_prompt_generator import` 
  - Por: `from ..viral_video_prompt_generator import`

### FASE 3: ARCHIVAR SCRIPTS SEGUROS
**Scripts sin dependencias locales:**
- `test_*.py` → `archive/testing/`
- Scripts experimentales → `archive/experiments/`
- Scripts duplicados de upload → `archive/upload_variants/`

### FASE 4: REORGANIZAR ESTRUCTURA
**Solo después de verificar que todo funciona:**
- Mover utilidades a `utils/`
- Reorganizar core scripts
- Actualizar imports finales

---

## 🔍 **VERIFICACIÓN DE RUTAS**

### Rutas de Archivos Críticos:
```
data/images/gemini_image_*.png  # Ya migrado ✅
video_prompt_map.json           # Raíz ✅  
config/upload_cookies_playwright.json  # Config ✅
chrome_profile_selenium_final/  # Raíz ✅
```

### Scripts que Referencian Rutas:
- `generate_veo_video_from_image.py` → `data/images/` ✅
- `gen_images_from_prompts.py` → `data/images/` ✅
- `subir_tiktok_selenium_final_v5.py` → `video_prompt_map.json` ✅

---

## ✅ **ESTRATEGIA ULTRA-SEGURA**

1. **CREAR BACKUP COMPLETO** antes de cualquier cambio
2. **MANTENER DEPENDENCIAS EN RAÍZ** durante refactoring inicial
3. **ARCHIVAR SOLO ARCHIVOS SIN DEPENDENCIAS** primero
4. **VERIFICAR FUNCIONAMIENTO** después de cada paso
5. **ACTUALIZAR IMPORTS** solo al final y uno por uno
6. **TESTING CONTINUO** en cada fase

---

## 🎯 **ARCHIVOS QUE PUEDEN ELIMINARSE INMEDIATAMENTE**

### Debug/Temporal Files:
- `debug_*.png` (50+ archivos)
- `dragdrop_*.png` (30+ archivos)
- `*.html` (archivos debug)
- `__pycache__/` ✅
- Videos temporales antiguos

### Scripts Duplicados/Experimentales:
- `advanced_visual_analyzer.py`
- `authentic_viral_fusion.py`
- `create_visual_concept.py`
- `definitive_viral_generator.py`
- Scripts `subir_tiktok_` duplicados (excepto `final_v5`)

---

## 🔒 **ARCHIVOS INTOCABLES DURANTE REFACTORING**

1. `subir_tiktok_selenium_final_v5.py` 🔒
2. `dynamic_description_generator.py` 🔒
3. `video_prompt_map.json` 🔒
4. `chrome_profile_selenium_final/` 🔒
5. `config/upload_cookies_playwright.json` 🔒
6. `data/images/gemini_image_*.png` 🔒
