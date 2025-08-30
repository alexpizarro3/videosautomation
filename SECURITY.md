# 🔐 GUÍA DE SEGURIDAD - AUTOMATIZACIÓN TIKTOK

## ⚠️ ARCHIVOS SENSIBLES - NUNCA SUBIR A GITHUB

### 🚨 CRÍTICO - Mantener SIEMPRE en local:
```
.env                     # ❌ NUNCA subir - Contiene API keys reales
data/tiktok_cookies.json # ❌ NUNCA subir - Datos de sesión TikTok
logs/                    # ❌ NUNCA subir - Pueden contener info sensible
data/analytics/          # ❌ NUNCA subir - Métricas privadas
data/generated/          # ❌ NUNCA subir - Contenido generado
```

### ✅ SEGUROS - Pueden estar en GitHub:
```
.env.example            # ✅ Plantilla sin datos reales
.env.template           # ✅ Plantilla sin datos reales
.gitignore              # ✅ Configuración de seguridad
README.md               # ✅ Documentación pública
src/                    # ✅ Código fuente (sin secrets)
requirements.txt        # ✅ Lista de dependencias
```

## 🛡️ CONFIGURACIÓN DE SEGURIDAD APLICADA

### 1. Variables de entorno protegidas:
- `.env` está en `.gitignore` - **NO se sube a GitHub**
- Solo las plantillas (.env.example, .env.template) están en GitHub
- API keys y datos personales están **solo en tu computadora**

### 2. GitHub Secrets (para automatización):
- Las API keys se almacenan **encriptadas** en GitHub Secrets
- Solo tu repositorio puede acceder a ellas
- No aparecen en logs públicos
- Se usan automáticamente en GitHub Actions

### 3. Datos de TikTok protegidos:
- Cookies en archivo local (no en GitHub)
- Username/email solo en GitHub Secrets
- Sesiones seguras para automatización

## 🔧 CÓMO CONFIGURAR CORRECTAMENTE

### Paso 1: Configuración local
```bash
# Copiar plantilla
cp .env.example .env

# Editar con tus datos reales
nano .env  # o abrir con tu editor
```

### Paso 2: GitHub Secrets (para automatización)
```
Repository Settings → Secrets → Actions → New repository secret
```

### Paso 3: Verificar seguridad
```bash
# Verificar que .env NO está en git
git status  # .env no debe aparecer

# Verificar .gitignore
cat .gitignore | grep .env  # debe incluir .env
```

## 🚨 QUÉ HACER SI EXPONES DATOS

### Si subiste accidentalmente .env:
```bash
# 1. Remover del repositorio
git rm --cached .env
git commit -m "Remove sensitive .env file"
git push

# 2. Cambiar API keys inmediatamente
# - Generar nuevas API keys en Google AI Studio
# - Actualizar .env local
# - Actualizar GitHub Secrets

# 3. Verificar historial
git log --all -- .env  # Ver si .env aparece en historial
```

### Si las API keys fueron comprometidas:
1. **Revocar inmediatamente** en Google AI Studio
2. **Generar nuevas** API keys
3. **Actualizar** .env local y GitHub Secrets
4. **Monitorear** uso no autorizado

## 🔐 MEJORES PRÁCTICAS

### ✅ HACER:
- Usar GitHub Secrets para automatización
- Mantener .env solo en local
- Verificar .gitignore regularmente
- Usar plantillas (.env.example) para documentación
- Rotar API keys periódicamente

### ❌ NO HACER:
- Subir .env a GitHub
- Compartir API keys en mensajes
- Hardcodear secrets en código
- Usar mismas API keys en múltiples proyectos
- Ignorar warnings de seguridad

## 📊 VERIFICACIÓN DE SEGURIDAD

### Comando de verificación:
```bash
# Verificar que archivos sensibles NO están en GitHub
git ls-files | grep -E "\.(env|key|secret|cookie)" || echo "✅ Sin archivos sensibles"

# Verificar .gitignore
grep -E "\.(env|key|secret|cookie)" .gitignore && echo "✅ Archivos protegidos"
```

## 🚀 AUTOMATIZACIÓN SEGURA

Una vez configurados los GitHub Secrets:
- El sistema usa **encriptación** de GitHub
- Las API keys **nunca** aparecen en logs
- La automatización funciona **sin exponer datos**
- Todo el contenido sensible permanece **protegido**

---

## ✨ SISTEMA 100% SEGURO Y AUTOMÁTICO

Con esta configuración, tu sistema de automatización TikTok:
- 🔒 **Protege** toda tu información sensible
- 🤖 **Funciona** automáticamente en GitHub Actions  
- 📱 **Genera** contenido 24/7 sin riesgos
- 🛡️ **Cumple** mejores prácticas de seguridad
