#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 SETUP YOUTUBE OAUTH - AUTENTICACIÓN INICIAL
Configura la autenticación OAuth para YouTube Data API v3
"""

import os
import json
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes requeridos para YouTube Data API
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly'
]

def setup_oauth():
    """
    Configurar OAuth para YouTube API
    """
    print("🔐 CONFIGURACIÓN OAUTH YOUTUBE")
    print("=" * 50)
    
    credentials_file = "config/youtube_credentials.json"
    token_file = "config/youtube_token.json"
    
    # Verificar que exista el archivo de credenciales
    if not os.path.exists(credentials_file):
        print(f"❌ Archivo de credenciales no encontrado: {credentials_file}")
        print("\n📝 PASOS PARA CONFIGURAR:")
        print("1. Ir a Google Cloud Console")
        print("2. Crear proyecto o seleccionar existente")
        print("3. Habilitar YouTube Data API v3")
        print("4. Crear credenciales OAuth 2.0")
        print("5. Descargar JSON y guardar como config/youtube_credentials.json")
        return False
    
    # Cargar credenciales
    with open(credentials_file, 'r') as f:
        creds_data = json.load(f)
    
    # Extraer datos OAuth del archivo
    if 'youtube_api' in creds_data:
        oauth_data = creds_data['youtube_api']
        client_id = oauth_data['client_id']
        client_secret = oauth_data['client_secret']
    else:
        print("❌ Formato de credenciales incorrecto")
        return False
    
    print(f"✅ Credenciales cargadas")
    print(f"📧 Client ID: {client_id[:20]}...")
    
    creds = None
    
    # Verificar si ya existe token
    if os.path.exists(token_file):
        print("🔍 Token existente encontrado, verificando...")
        try:
            with open(token_file, 'r') as f:
                token_data = json.load(f)
            
            creds = Credentials(
                token=token_data['token'],
                refresh_token=token_data['refresh_token'],
                client_id=token_data['client_id'],
                client_secret=token_data['client_secret'],
                scopes=token_data['scopes']
            )
            
            # Verificar si necesita refresh
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refrescando token...")
                creds.refresh(Request())
                
                # Guardar token actualizado
                save_token(creds, token_file)
                print("✅ Token refrescado")
            
        except Exception as e:
            print(f"⚠️ Error con token existente: {e}")
            creds = None
    
    # Si no hay credenciales válidas, hacer flow OAuth
    if not creds or not creds.valid:
        print("🔐 Iniciando proceso OAuth...")
        
        # Crear configuración OAuth temporal
        oauth_config = {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:8080/callback"]
            }
        }
        
        # Guardar temporalmente para el flow
        temp_file = "temp_oauth.json"
        with open(temp_file, 'w') as f:
            json.dump(oauth_config, f)
        
        try:
            # Ejecutar flow OAuth
            flow = InstalledAppFlow.from_client_secrets_file(
                temp_file, SCOPES)
            
            print("\n🌐 INSTRUCCIONES:")
            print("1. Se abrirá tu navegador")
            print("2. Inicia sesión en Google")
            print("3. Autoriza la aplicación")
            print("4. Copia el código de autorización")
            
            creds = flow.run_local_server(port=8080)
            
            # Guardar token
            save_token(creds, token_file)
            
            print("✅ ¡Autenticación exitosa!")
            
        except Exception as e:
            print(f"❌ Error en OAuth: {e}")
            return False
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    # Probar conexión
    print("🧪 Probando conexión...")
    try:
        service = build('youtube', 'v3', credentials=creds)
        
        # Probar con una llamada simple
        request = service.channels().list(part="snippet", mine=True)
        response = request.execute()
        
        if response['items']:
            channel = response['items'][0]['snippet']
            print(f"✅ Conexión exitosa!")
            print(f"📺 Canal: {channel['title']}")
            print(f"📧 Email: {channel.get('description', 'No disponible')}")
        else:
            print("⚠️ Conexión exitosa pero no se encontró canal")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        return False

def save_token(creds, token_file):
    """
    Guardar token OAuth
    """
    token_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': 'https://oauth2.googleapis.com/token',
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': list(creds.scopes) if creds.scopes else SCOPES
    }
    
    os.makedirs(os.path.dirname(token_file), exist_ok=True)
    with open(token_file, 'w') as f:
        json.dump(token_data, f, indent=2)

def main():
    """
    Función principal
    """
    print("🎬 SETUP YOUTUBE AUTHENTICATION")
    print("=" * 60)
    
    success = setup_oauth()
    
    if success:
        print(f"\n✅ ¡CONFIGURACIÓN COMPLETA!")
        print(f"🎯 Ya puedes usar youtube_shorts_uploader.py")
        print(f"\n🚀 SIGUIENTE PASO:")
        print(f"python youtube_shorts_uploader.py")
    else:
        print(f"\n❌ Error en la configuración")
        print(f"🔧 Revisa las credenciales y vuelve a intentar")

if __name__ == "__main__":
    main()
