# 🔐 GUÍA PASO A PASO: CONFIGURAR GITHUB SECRETS

## 🎯 ¿Qué vamos a hacer?

Configurar los **GitHub Secrets** para que tu sistema funcione automáticamente sin exponer información sensible.

## 📋 PASO 1: Ir a tu repositorio

1. Abre tu navegador y ve a: https://github.com/alexpizarro3/videosautomation
2. Asegúrate de estar logueado en tu cuenta de GitHub

## ⚙️ PASO 2: Acceder a la configuración

1. En tu repositorio, haz click en la pestaña **"Settings"** (⚙️)
2. En el menú lateral izquierdo, busca y haz click en:
   - **"Secrets and variables"** 
   - Luego **"Actions"**

## 🔑 PASO 3: Agregar los secrets

Haz click en **"New repository secret"** para cada uno de estos:

### Secret 1: GEMINI_API_KEY
```
Name: GEMINI_API_KEY
Secret: [tu API key de Gemini aquí]
```

### Secret 2: VEO3_API_KEY  
```
Name: VEO3_API_KEY
Secret: [tu API key de Veo3 aquí]
```

### Secret 3: TIKTOK_USERNAME
```
Name: TIKTOK_USERNAME
Secret: chakakitafreakyvideos
```

### Secret 4: TIKTOK_EMAIL
```
Name: TIKTOK_EMAIL
Secret: alexpizarro3@gmail.com
```

### Secret 5: TIKTOK_COOKIES
```
Name: TIKTOK_COOKIES
Secret: [contenido completo del archivo data/tiktok_cookies.json]
```

## 📄 PASO 4: Obtener el contenido de cookies

Para el secret `TIKTOK_COOKIES`, necesitas copiar TODO el contenido del archivo:

1. Abre el archivo: `data/tiktok_cookies.json`
2. Selecciona todo el contenido (Ctrl+A)
3. Copia todo (Ctrl+C)
4. Pega en el campo "Secret" de GitHub

El contenido debe verse algo así:
```json
{
  "sessionid": "valor_largo_aqui",
  "csrftoken": "otro_valor_aqui",
  "tt_webid": "otro_valor",
  ...más cookies...
}
```

## ✅ PASO 5: Verificar configuración

Una vez agregados todos los secrets, deberías ver:

```
✅ GEMINI_API_KEY
✅ VEO3_API_KEY  
✅ TIKTOK_USERNAME
✅ TIKTOK_EMAIL
✅ TIKTOK_COOKIES
```

## 🚀 PASO 6: Activar GitHub Actions

1. Ve a la pestaña **"Actions"** en tu repositorio
2. Si aparece un mensaje para habilitar Actions, haz click en **"I understand, enable Actions"**
3. Busca el workflow **"🎬 TikTok Video Automation"**
4. Haz click en **"Enable workflow"** si está deshabilitado

## 🧪 PASO 7: Probar manualmente

Para probar que todo funciona:

1. En la pestaña **"Actions"**
2. Selecciona **"🎬 TikTok Video Automation"**
3. Haz click en **"Run workflow"**
4. Selecciona branch **"main"**
5. Haz click en **"Run workflow"**

## ⏰ PASO 8: Verificar horarios automáticos

El sistema se ejecutará automáticamente en estos horarios:

- **09:00 UTC** = 04:00 México / 10:00 España
- **15:00 UTC** = 10:00 México / 16:00 España  
- **21:00 UTC** = 16:00 México / 22:00 España

## 📊 PASO 9: Monitorear resultados

- Cada ejecución aparecerá en la pestaña **"Actions"**
- Puedes ver logs detallados haciendo click en cada ejecución
- Los artifacts (contenido generado) se guardan por 7 días

## 🔧 Solución de problemas

### "Secret no encontrado"
- Verifica que el nombre esté exactamente como se especifica
- Revisa que no haya espacios extra

### "Error de autenticación"
- Verifica que las API keys sean correctas
- Para TikTok: actualiza las cookies (pueden expirar)

### "Workflow no se ejecuta"
- Verifica que GitHub Actions esté habilitado
- Revisa que el archivo `.github/workflows/automation.yml` esté presente

## ✨ ¡Listo!

Una vez completados estos pasos, tu sistema de automatización estará funcionando 24/7 sin necesidad de tu computadora encendida.

El sistema analizará tus 109 videos, creará contenido optimizado y lo subirá automáticamente 3 veces al día con el objetivo de superar las 1,270 views por video.
