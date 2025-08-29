# 🔐 CONFIGURACIÓN DE GITHUB SECRETS
# Para automatización 100% en la nube

## ¿QUÉ SON LOS GITHUB SECRETS?
Los GitHub Secrets son variables de entorno encriptadas que permiten almacenar información sensible (API keys, passwords, etc.) de forma segura en GitHub. Se ejecutan en servidores de GitHub, NO en tu computadora.

## 🔧 CÓMO CONFIGURAR LOS SECRETS

### 1. Ve a tu repositorio en GitHub
- Abre tu repositorio: https://github.com/tu-usuario/videosautomation
- Click en "Settings" (⚙️)
- En el menú izquierdo, click en "Secrets and variables" → "Actions"

### 2. Agregar estos SECRETS (click "New repository secret"):

#### 🤖 API KEYS:
```
Nombre: GEMINI_API_KEY
Valor: tu_api_key_de_gemini_aqui

Nombre: VEO3_API_KEY  
Valor: tu_api_key_de_veo3_aqui
```

#### 👤 DATOS DE TIKTOK:
```
Nombre: TIKTOK_USERNAME
Valor: chakakitafreakyvideos

Nombre: TIKTOK_EMAIL
Valor: alexpizarro3@gmail.com
```

#### 🍪 COOKIES DE TIKTOK:
```
Nombre: TIKTOK_COOKIES
Valor: (contenido completo del archivo data/tiktok_cookies.json)
```

## 🚀 VENTAJAS DE GITHUB ACTIONS

### ✅ VENTAJAS:
1. **100% Gratis**: GitHub Actions da 2,000 minutos gratis/mes
2. **Sin computadora**: Funciona 24/7 en servidores de GitHub
3. **Confiable**: Infraestructura de Microsoft/GitHub
4. **Escalable**: Puede manejar múltiples cuentas
5. **Logs completos**: Puedes ver qué pasó en cada ejecución
6. **Notificaciones**: Te avisa si algo falla

### ⚠️ CONSIDERACIONES:
1. **Límite de tiempo**: Máximo 6 horas por job (más que suficiente)
2. **Límite de almacenamiento**: 500MB de artifacts (suficiente para videos)
3. **IP diferente**: GitHub Actions usa IPs diferentes cada vez
4. **Sin persistencia**: Los archivos se borran entre ejecuciones

## 🔄 CÓMO FUNCIONA LA AUTOMATIZACIÓN

### Horarios programados (UTC):
- **09:00 UTC** = 04:00 México / 10:00 España
- **15:00 UTC** = 10:00 México / 16:00 España  
- **21:00 UTC** = 16:00 México / 22:00 España

### Proceso automático:
1. 🔍 **Extraer métricas** de tus videos existentes
2. 📊 **Analizar tendencias** y rendimiento
3. 🧠 **Generar prompt** optimizado basado en datos
4. 🎨 **Crear imagen** con Gemini API
5. 🎬 **Generar video** con Veo3 API
6. 📱 **Subir a TikTok** usando tus cookies
7. 📊 **Guardar logs** y métricas

### Monitoreo:
- Ve a tu repo → "Actions" para ver todas las ejecuciones
- Cada ejecución muestra logs detallados
- Si algo falla, recibes notificación por email

## 🛡️ SEGURIDAD

### Datos protegidos:
- ✅ API Keys encriptadas en GitHub
- ✅ Cookies seguras en Secrets
- ✅ Logs no muestran información sensible
- ✅ Artifacts se borran automáticamente en 7 días

### Acceso:
- ❌ Nadie más puede ver tus secrets
- ❌ GitHub no puede acceder a tus secrets
- ❌ Los logs públicos no muestran secrets

## 📊 CONFIGURACIÓN AVANZADA

### Variables adicionales que puedes configurar:
```
# Personalización de contenido
CONTENT_THEMES: "comedia,viral,trending"
MAX_VIDEOS_PER_DAY: "3"
PREFERRED_HASHTAGS: "#viral #fyp #comedia"

# Configuración de calidad
IMAGE_QUALITY: "high"
VIDEO_DURATION: "15-30"
UPLOAD_QUALITY: "1080p"

# Notificaciones
DISCORD_WEBHOOK: "tu_webhook_de_discord"
EMAIL_NOTIFICATIONS: "true"
```

## 🚀 PASOS PARA ACTIVAR:

### 1. Configura los secrets en GitHub (explicado arriba)

### 2. Haz push de tu código:
```bash
git add .
git commit -m "🤖 Automatización completa configurada"
git push origin main
```

### 3. Ve a "Actions" en tu repo y verifica que el workflow aparezca

### 4. Prueba manual:
- Click en "Actions"
- Click en "🎬 TikTok Video Automation"
- Click en "Run workflow" → "Run workflow"

### 5. ¡Listo! 🎉
El sistema se ejecutará automáticamente 3 veces al día

## 💡 TIPS IMPORTANTES:

1. **Tus cookies de TikTok**: Pueden expirar, actualízalas cada 2-3 semanas
2. **APIs de Google**: Vigila tus límites de uso
3. **Monitoreo**: Revisa los logs semanalmente
4. **Backup**: GitHub guarda tu código, pero los datos generados se borran
5. **Optimización**: El sistema aprende de tus videos anteriores

## 🆘 SOLUCIÓN DE PROBLEMAS:

### Si falla la extracción de TikTok:
- Actualiza cookies en GitHub Secrets
- TikTok puede haber cambiado su estructura

### Si falla la generación de imágenes:
- Verifica GEMINI_API_KEY en Secrets
- Revisa límites de tu cuenta de Google

### Si falla la generación de videos:
- Verifica VEO3_API_KEY en Secrets  
- Recuerda: solo 3 videos gratis por día

### Si falla la subida:
- Actualiza cookies de TikTok
- Verifica que el video cumple políticas de TikTok

¡Tu sistema será 100% automático y gratuito! 🚀
