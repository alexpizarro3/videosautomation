#!/usr/bin/env python3
"""
Script de configuración inicial para el sistema de automatización de TikTok
Configura el entorno, instala dependencias y prepara el sistema para funcionar.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_header():
    """Mostrar header del script"""
    print("=" * 60)
    print("🚀 CONFIGURACIÓN INICIAL - TIKTOK AUTOMATION")
    print("=" * 60)
    print()

def check_python_version():
    """Verificar versión de Python"""
    print("📋 Verificando versión de Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def create_directories():
    """Crear directorios necesarios"""
    print("\n📁 Creando directorios...")
    
    directories = [
        "data/analytics",
        "data/images", 
        "data/videos",
        "data/uploads",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")

def setup_env_file():
    """Configurar archivo .env"""
    print("\n🔧 Configurando archivo .env...")
    
    env_file = Path(".env")
    template_file = Path(".env.template")
    
    if not env_file.exists():
        if template_file.exists():
            shutil.copy(template_file, env_file)
            print("   ✅ Archivo .env creado desde plantilla")
        else:
            # Crear .env básico
            env_content = """# API Keys para Google Generative AI
GEMINI_API_KEY=your_gemini_api_key_here
VEO3_API_KEY=your_veo3_api_key_here

# Configuración de TikTok
TIKTOK_USERNAME=your_tiktok_username
TIKTOK_PASSWORD=your_tiktok_password

# Configuración del sistema
TREND_ANALYSIS_ENABLED=true
MAX_VIDEOS_PER_DAY=3
LOG_LEVEL=INFO
"""
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            print("   ✅ Archivo .env creado")
    else:
        print("   ⚠️  Archivo .env ya existe")
    
    print("\n💡 IMPORTANTE: Edita el archivo .env con tus API keys:")
    print(f"   📝 {env_file.absolute()}")

def install_dependencies():
    """Instalar dependencias de Python"""
    print("\n📦 Instalando dependencias...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("   ⚠️  requirements.txt no encontrado")
        return False
    
    try:
        # Actualizar pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Instalar dependencias
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        print("   ✅ Dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error instalando dependencias: {e}")
        return False

def check_chrome():
    """Verificar que Chrome esté instalado"""
    print("\n🌐 Verificando Google Chrome...")
    
    chrome_paths = [
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        "/usr/bin/google-chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("   ✅ Google Chrome encontrado")
            return True
    
    print("   ⚠️  Google Chrome no encontrado")
    print("   💡 Instala Chrome para usar el sistema de scraping")
    return False

def test_imports():
    """Probar importaciones críticas"""
    print("\n🧪 Probando importaciones...")
    
    critical_imports = [
        "selenium",
        "requests", 
        "google.genai",
        "PIL",
        "cv2",
        "numpy"
    ]
    
    all_good = True
    for module in critical_imports:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - No instalado")
            all_good = False
    
    return all_good

def create_gitignore():
    """Crear archivo .gitignore"""
    print("\n📄 Configurando .gitignore...")
    
    gitignore_content = """# Archivos de configuración sensibles
.env
data/tiktok_cookies.json

# Datos generados
data/analytics/*.json
data/images/*.jpg
data/images/*.png
data/videos/*.mp4
data/uploads/*.json

# Logs
logs/*.log

# Cache de Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Entorno virtual
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Archivos temporales
*.tmp
*.bak
.DS_Store
Thumbs.db
"""
    
    gitignore_file = Path(".gitignore")
    if not gitignore_file.exists():
        with open(gitignore_file, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("   ✅ .gitignore creado")
    else:
        print("   ⚠️  .gitignore ya existe")

def show_next_steps():
    """Mostrar próximos pasos"""
    print("\n" + "=" * 60)
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASOS:")
    print()
    print("1. 🔑 Configurar API Keys:")
    print("   - Edita el archivo .env")
    print("   - Añade tu GEMINI_API_KEY (https://makersuite.google.com/app/apikey)")
    print("   - Añade tu VEO3_API_KEY (cuenta de estudiante)")
    print()
    print("2. 🧪 Probar generadores:")
    print("   python test_generators.py")
    print()
    print("3. 🚀 Ejecutar sistema completo:")
    print("   python src/main.py")
    print()
    print("4. 🤖 Configurar automatización:")
    print("   - GitHub: Configura Secrets en tu repositorio")
    print("   - Local: Usa cron (Linux/Mac) o Task Scheduler (Windows)")
    print()
    print("💡 Para soporte: Revisa README.md o abre un issue en GitHub")

def main():
    """Función principal"""
    print_header()
    
    # Verificaciones y configuración
    steps = [
        ("Verificar Python", check_python_version),
        ("Crear directorios", create_directories),
        ("Configurar .env", setup_env_file),
        ("Instalar dependencias", install_dependencies),
        ("Verificar Chrome", check_chrome),
        ("Probar importaciones", test_imports),
        ("Configurar .gitignore", create_gitignore)
    ]
    
    all_success = True
    for step_name, step_func in steps:
        try:
            if hasattr(step_func, '__call__'):
                if step_func() is False:
                    all_success = False
            else:
                step_func()
        except Exception as e:
            print(f"   ❌ Error en {step_name}: {e}")
            all_success = False
    
    # Mostrar resultado final
    if all_success:
        show_next_steps()
    else:
        print("\n⚠️  Configuración completada con advertencias")
        print("💡 Revisa los errores arriba y soluciónalos antes de continuar")

if __name__ == "__main__":
    main()
