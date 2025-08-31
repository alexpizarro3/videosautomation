import asyncio
import random
import time
from playwright.async_api import async_playwright
import os
import json
from dotenv import load_dotenv

def human_delay(min_s=0.7, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))

async def cargar_cookies(context, cookies_path):
    with open(cookies_path, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    # Playwright espera cookies en formato dict, sin campos extra
    for cookie in cookies:
        # Elimina campos no soportados
        for k in ["hostOnly", "storeId"]:
            cookie.pop(k, None)
        # Playwright espera expires, no expirationDate
        if "expirationDate" in cookie:
            cookie["expires"] = int(cookie["expirationDate"])
            del cookie["expirationDate"]
        # Corregir el campo sameSite
        if "sameSite" in cookie:
            val = cookie["sameSite"]
            if val in [None, "null", "no_restriction"]:
                cookie["sameSite"] = "None"
            elif val in ["Strict", "Lax", "None"]:
                pass
            else:
                cookie["sameSite"] = "None"
    await context.add_cookies(cookies)
    print(f"✅ Cookies cargadas desde {cookies_path}")
    human_delay(2, 4)

async def subir_video_tiktok(page, video_path, descripcion, hashtags):
    await page.goto("https://www.tiktok.com/upload", timeout=60000)
    await page.wait_for_selector('input[type="file"]', timeout=60000)
    # Simula hover y scroll antes de interactuar
    await page.hover('input[type="file"]')
    await page.evaluate('window.scrollBy(0, 100)')
    human_delay()
    await page.set_input_files('input[type="file"]', video_path)
    print(f"✅ Video seleccionado: {video_path}")
    # Espera a que aparezca el editor de descripción
    await page.wait_for_selector('.caption-editor [contenteditable="true"]', timeout=120000)
    await page.hover('.caption-editor [contenteditable="true"]')
    await page.click('.caption-editor [contenteditable="true"]')
    human_delay()
    texto = f"{descripcion}\n{' '.join(hashtags)}"
    await page.fill('.caption-editor [contenteditable="true"]', texto)
    print("✅ Descripción y hashtags ingresados")
    human_delay()
    # Scroll y hover al botón Post
    await page.evaluate('window.scrollBy(0, 200)')
    await page.hover('button[data-e2e="post_video_button"]')
    human_delay(1, 3)
    await page.click('button[data-e2e="post_video_button"]')
    print("✅ Botón Post clickeado")
    human_delay(3, 6)

async def main():
    load_dotenv()
    cookies_path = "config/upload_cookies_playwright.json"
    with open("video_prompt_map.json", "r", encoding="utf-8") as f:
        video_prompt_map = json.load(f)
    async with async_playwright() as p:
        # Ruta de Brave en Windows
        brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        if not os.path.exists(brave_path):
            print(f"❌ No se encontró Brave en {brave_path}. Usando Chromium por defecto.")
            browser = await p.chromium.launch(headless=False, slow_mo=150)
        else:
            browser = await p.chromium.launch(headless=False, slow_mo=150, executable_path=brave_path)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 900, "height": 1600}
        )
        await cargar_cookies(context, cookies_path)
        page = await context.new_page()
        await page.goto("https://www.tiktok.com/", timeout=60000)
        human_delay(2, 4)
        # Verifica si la sesión está activa
        try:
            await page.wait_for_selector('[data-e2e="profile-icon"], .avatar, a[href*="/@"]', timeout=15000)
            print("✅ Sesión activa detectada con cookies")
        except Exception:
            print("⚠️  No se detectó sesión activa con cookies. Debes actualizar las cookies manualmente.")
            await browser.close()
            return
        for item in video_prompt_map:
            video_path = item.get("video", "")
            prompt = item.get("prompt", "")
            if not os.path.exists(video_path):
                print(f"❌ Archivo no encontrado, saltando: {video_path}")
                continue
            descripcion = f"{prompt}\n\nDisfruta este video viral con sonido envolvente y efectos ASMR. ¡No olvides seguirme para más contenido único!"
            hashtags = [f"#{w.capitalize()}" for w in prompt.split() if w.isalpha()][:5]
            hashtags += ['#Viral', '#ASMR', '#FYP', '#TikTokViral']
            hashtags = list(dict.fromkeys(hashtags))[:5]
            await subir_video_tiktok(page, video_path, descripcion, hashtags)
            human_delay(5, 10)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
