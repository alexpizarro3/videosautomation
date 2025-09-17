
import os
import glob
import time
from selenium import webdriver
from drive_uploader_selenium import setup_stealth_chrome_drive, upload_file_to_drive

# --- CONFIGURAR ESTOS IDS DE CARPETA CON LOS DE TU DRIVE ---
DRIVE_FOLDER_IDS = {
    'imagenes': '1I4uS6zYcIglZm6OMDgxQzBQ6SfAk7e12',
    'procesados': '1uLNzGobCU_kH28qPosKOolidpZuVwCEa',
    'fundidos': '18toSvjqiwim2U_g0IoHO8_pxEk4DUTef',
}

def main():
    """Sube todos los archivos necesarios a Google Drive usando Selenium."""
    print("🚗 Iniciando subida de archivos a Google Drive con Selenium...")
    
    options = setup_stealth_chrome_drive()
    driver = webdriver.Chrome(options=options)

    try:
        # Navegar a Google Drive y esperar a que el usuario inicie sesión si es necesario
        driver.get("https://drive.google.com")
        print("Por favor, inicia sesión en Google si es necesario. El script continuará en 15 segundos...")
        time.sleep(15)

        # Subir imágenes
        print("\n--- Subiendo imágenes ---")
        image_files = glob.glob('data/images/*.png')
        for img in image_files:
            upload_file_to_drive(driver, img, DRIVE_FOLDER_IDS['imagenes'])

        # Subir videos procesados
        print("\n--- Subiendo videos procesados ---")
        video_files = glob.glob('data/videos/processed/*.mp4')
        for vid in video_files:
            upload_file_to_drive(driver, vid, DRIVE_FOLDER_IDS['procesados'])

        # Subir video final (fundido)
        print("\n--- Subiendo video final ---")
        fundido_files = glob.glob('data/videos/final/*FUNDIDO_TIKTOK*.mp4')
        for vid in fundido_files:
            upload_file_to_drive(driver, vid, DRIVE_FOLDER_IDS['fundidos'])

        print("\n🎉 Todas las subidas a Google Drive se han completado.")

    finally:
        print("🔒 Cerrando el navegador.")
        driver.quit()

if __name__ == '__main__':
    main()
