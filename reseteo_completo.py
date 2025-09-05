#!/usr/bin/env python3
"""
🔄 RESETEO COMPLETO DEL SISTEMA TIKTOK
Elimina todas las huellas de detección y prepara un entorno limpio
"""

import os
import shutil
import json
import time

def reseteo_completo():
    """Reseteo completo del sistema"""
    print("🔄 INICIANDO RESETEO COMPLETO DEL SISTEMA")
    print("=" * 50)
    
    # 1. Eliminar perfil del browser
    print("1️⃣ Eliminando perfil del browser...")
    browser_profile = "browser_profile"
    if os.path.exists(browser_profile):
        try:
            shutil.rmtree(browser_profile)
            print(f"✅ Perfil eliminado: {browser_profile}")
        except Exception as e:
            print(f"⚠️ Error eliminando perfil: {e}")
            print("   💡 Cierra Chrome manualmente y vuelve a ejecutar")
    else:
        print("ℹ️ No había perfil previo")
    
    # 2. Limpiar archivos temporales
    print("\n2️⃣ Limpiando archivos temporales...")
    temp_files = [
        "test_video.mp4",
        "debug_upload_page_*.png",
        "ultra_stealth_v4_mod_*.png",
        "debug_pre_emergency_*.png",
        "debug_final_emergency_*.png",
        "diagnostic_final_*.png"
    ]
    
    import glob
    for pattern in temp_files:
        files = glob.glob(pattern)
        for file in files:
            try:
                os.remove(file)
                print(f"✅ Eliminado: {file}")
            except:
                continue
    
    # 3. Verificar cookies
    print("\n3️⃣ Verificando cookies...")
    cookies_path = "config/upload_cookies_playwright.json"
    if os.path.exists(cookies_path):
        try:
            with open(cookies_path, 'r') as f:
                cookies = json.load(f)
            print(f"✅ Cookies encontradas: {len(cookies)} cookies")
            
            # Verificar si las cookies son recientes (menos de 7 días)
            file_time = os.path.getmtime(cookies_path)
            current_time = time.time()
            days_old = (current_time - file_time) / (24 * 3600)
            
            if days_old > 7:
                print(f"⚠️ Cookies tienen {days_old:.1f} días - Considera renovarlas")
                print("   💡 Ejecuta: python setup_tiktok_cookies.py")
            else:
                print(f"✅ Cookies recientes ({days_old:.1f} días)")
        except Exception as e:
            print(f"❌ Error verificando cookies: {e}")
            print("   💡 Ejecuta: python setup_tiktok_cookies.py")
    else:
        print("❌ No se encontraron cookies")
        print("   💡 Ejecuta: python setup_tiktok_cookies.py")
    
    # 4. Crear directorio limpio para el nuevo perfil
    print("\n4️⃣ Preparando entorno limpio...")
    os.makedirs(browser_profile, exist_ok=True)
    print(f"✅ Directorio de perfil creado: {browser_profile}")
    
    # 5. Verificar archivos necesarios
    print("\n5️⃣ Verificando archivos necesarios...")
    required_files = [
        "data/videos/final/videos_unidos_FUNDIDO_TIKTOK.mp4",
        "subir_tiktok_ultra_stealth_v5_extremo.py"
    ]
    
    all_ready = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ Falta: {file}")
            all_ready = False
    
    print("\n" + "=" * 50)
    if all_ready:
        print("🎉 RESETEO COMPLETADO - SISTEMA LISTO")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Si las cookies son viejas: python setup_tiktok_cookies.py")
        print("2. Ejecutar versión V5: python subir_tiktok_ultra_stealth_v5_extremo.py")
        print("3. O probar diagnóstico: python diagnostic_tiktok_blocker.py")
    else:
        print("⚠️ RESETEO COMPLETADO PERO FALTAN ARCHIVOS")
        print("   Revisa los archivos faltantes antes de continuar")
    
    return all_ready

if __name__ == "__main__":
    reseteo_completo()
