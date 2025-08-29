# 🚀 Guía de Configuración - TikTok Video Automation

Esta guía te llevará paso a paso para configurar el sistema de automatización de videos de TikTok.

## 📋 Prerequisitos

### Cuentas y APIs necesarias:
1. **Cuenta de TikTok** activa
2. **API Key de Gemini** (Google AI Studio)
3. **API Key de Veo3** (cuenta educativa)
4. **Cuenta de GitHub** para automatización

### Software requerido:
- Python 3.11+
- Google Chrome
- Git

## 🛠️ Instalación

### 1. Clonar o descargar el proyecto
```bash
git clone https://github.com/tu-usuario/videosautomation.git
cd videosautomation
```

### 2. Instalar Python y dependencias
```bash
# Instalar Python 3.11+ desde python.org
# Verificar instalación
python --version

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus datos reales:
```

**Archivo `.env`:**
```env
GEMINI_API_KEY=tu_api_key_de_gemini
VEO3_API_KEY=tu_api_key_de_veo3
TIKTOK_USERNAME=tu_usuario_tiktok
TIKTOK_PASSWORD=tu_password_tiktok

SCRAPING_DELAY=2
MAX_VIDEOS_TO_ANALYZE=50
MAX_IMAGES_PER_DAY=10
MAX_VIDEOS_PER_DAY=3
IMAGE_QUALITY=high
VIDEO_DURATION=15
UPLOAD_DELAY=30
MAX_HASHTAGS=10
LOG_LEVEL=INFO
```

## 🔑 Obtener API Keys

### Gemini API Key
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Crea una nueva API key
4. Copia la key y pégala en tu archivo `.env`

### Veo3 API Key
1. Accede a tu cuenta educativa de Veo3
2. Ve a la sección de API/Developers
3. Genera una nueva API key
4. Copia la key y pégala en tu archivo `.env`

**Nota:** Veo3 tiene límite de 3 videos gratis por día en cuenta educativa.

## 🍪 Configurar Cookies de TikTok

### Método 1: Exportar desde navegador
1. Abre TikTok en Chrome e inicia sesión
2. Presiona F12 para abrir Developer Tools
3. Ve a la pestaña "Application" > "Storage" > "Cookies" > "https://www.tiktok.com"
4. Busca las cookies importantes:
   - `sessionid`
   - `csrf_token`
   - `tt_csrf_token`
   - `tt_chain_token`

### Método 2: Usar extensión de Chrome
1. Instala "Cookie Editor" desde Chrome Web Store
2. Ve a TikTok logueado
3. Exporta las cookies en formato JSON
4. Guarda en `config/tiktok_cookies.json`

**Formato del archivo `config/tiktok_cookies.json`:**
```json
{
  "cookies": [
    {
      "name": "sessionid",
      "value": "tu_session_id_real",
      "domain": ".tiktok.com",
      "path": "/",
      "secure": true,
      "httpOnly": true
    },
    {
      "name": "csrf_token", 
      "value": "tu_csrf_token_real",
      "domain": ".tiktok.com",
      "path": "/",
      "secure": true,
      "httpOnly": false
    }
  ]
}
```

## 🧪 Prueba Local

### Ejecutar en modo de prueba
```bash
cd src
python main.py --username tu_usuario --max-videos 10 --create-videos 1 --dry-run
```

### Parámetros disponibles:
- `--username` / `-u`: Usuario de TikTok a analizar
- `--max-videos` / `-m`: Máximo de videos a analizar (default: 50)
- `--create-videos` / `-c`: Cantidad de videos a crear (default: 3)
- `--dry-run` / `-d`: Ejecutar sin subir videos (solo testing)

### Verificar funcionamiento:
1. ✅ Scraping de métricas
2. ✅ Análisis de tendencias  
3. ✅ Generación de prompts
4. ✅ Generación de imágenes
5. ✅ Generación de videos
6. ✅ (Opcional) Subida a TikTok

## 🤖 Configurar Automatización con GitHub Actions

### 1. Subir código a GitHub
```bash
# Crear repositorio en GitHub
# Subir código (sin archivos sensibles)
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/videosautomation.git
git push -u origin main
```

### 2. Configurar Secrets en GitHub
Ve a tu repositorio > Settings > Secrets and variables > Actions

**Crear estos secrets:**
- `GEMINI_API_KEY`: Tu API key de Gemini
- `VEO3_API_KEY`: Tu API key de Veo3
- `TIKTOK_USERNAME`: Tu usuario de TikTok
- `TIKTOK_PASSWORD`: Tu contraseña de TikTok (opcional)
- `TIKTOK_COOKIES`: Contenido completo del archivo tiktok_cookies.json
- `SLACK_WEBHOOK_URL`: (Opcional) Para notificaciones

### 3. Activar GitHub Actions
1. Ve a la pestaña "Actions" en tu repositorio
2. Habilita GitHub Actions si está deshabilitado
3. El workflow se ejecutará automáticamente según el horario configurado

### 4. Horarios de ejecución (configurables en .github/workflows/video_automation.yml)
- **9:00 AM UTC** (9:00 AM UTC = 4:00 AM EST / 1:00 AM PST)
- **3:00 PM UTC** (3:00 PM UTC = 10:00 AM EST / 7:00 AM PST)  
- **9:00 PM UTC** (9:00 PM UTC = 4:00 PM EST / 1:00 PM PST)

## 📁 Estructura de Archivos Generados

```
data/
├── metrics/          # Datos de análisis de TikTok
├── images/           # Imágenes generadas por IA
├── videos/           # Videos generados por IA
├── prompts/          # Planes de contenido
└── sessions/         # Logs de cada ejecución

logs/                 # Logs de la aplicación
```

## 🚨 Solución de Problemas

### Error: "No se pudieron cargar las cookies"
- Verifica que el archivo `config/tiktok_cookies.json` existe
- Asegúrate de que las cookies están en el formato correcto
- Las cookies pueden expirar, regenera cada 30 días

### Error: "API key inválida"
- Verifica que las API keys están correctas en `.env`
- Asegúrate de que las APIs tienen cuotas disponibles
- Para Gemini: verifica que la API está habilitada en tu proyecto

### Error en scraping de TikTok
- TikTok puede cambiar su estructura, el scraper necesitaría actualizarse
- Usa VPN si hay restricciones geográficas
- Reduce la frecuencia de scraping

### Videos no se suben
- Verifica que las cookies de TikTok están actualizadas
- Asegúrate de que el formato de video es correcto (vertical, MP4)
- TikTok puede tener restricciones de automatización

## 📊 Monitoreo

### Logs locales
```bash
# Ver logs en tiempo real
tail -f logs/automation_YYYYMMDD.log
```

### GitHub Actions
1. Ve a la pestaña "Actions" en tu repositorio
2. Selecciona la ejecución que quieres revisar
3. Revisa los logs de cada paso

### Archivos generados
Los archivos se guardan en `data/` y se pueden descargar como artifacts desde GitHub Actions.

## 🔧 Personalización

### Modificar frecuencia
Edita `.github/workflows/video_automation.yml` para cambiar los horarios:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Cada 6 horas
```

### Cambiar tipos de contenido
Modifica `src/generation/prompt_generator.py` para personalizar:
- Estilos de imagen
- Tipos de videos
- Templates de títulos
- Hashtags preferidos

### Ajustar límites
Modifica `config/config.yml` para cambiar:
- Límites diarios
- Configuraciones de APIs
- Parámetros de análisis

## 🆘 Soporte

Si encuentras problemas:

1. **Revisa los logs** para errores específicos
2. **Verifica la configuración** de API keys y cookies
3. **Consulta la documentación** de las APIs utilizadas
4. **Abre un issue** en GitHub con detalles del error

## ⚖️ Consideraciones Legales

- ✅ Usa solo tu propia cuenta de TikTok
- ✅ Respeta los términos de servicio de TikTok
- ✅ No hagas spam ni contenido inapropiado
- ✅ Mantén las API keys seguras
- ⚠️ La automatización puede estar contra los ToS de TikTok
- ⚠️ Usa bajo tu propio riesgo

## 🎯 Próximos Pasos

Una vez configurado:

1. **Ejecuta en modo dry-run** para probar
2. **Revisa los videos generados** antes de subir
3. **Ajusta los prompts** según los resultados
4. **Monitorea el rendimiento** de los videos subidos
5. **Optimiza basado en métricas** obtenidas

¡Tu sistema de automatización está listo! 🚀
