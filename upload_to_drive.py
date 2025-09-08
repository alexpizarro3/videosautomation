import os
import glob
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# --- CONFIGURAR ESTOS IDS DE CARPETA CON LOS DE TU DRIVE ---
DRIVE_FOLDER_IDS = {
    'imagenes': '1I4uS6zYcIglZm6OMDgxQzBQ6SfAk7e12',
    'procesados': '1uLNzGobCU_kH28qPosKOolidpZuVwCEa',
    'fundidos': '18toSvjqiwim2U_g0IoHO8_pxEk4DUTef',
}

"""
El archivo de credenciales debe llamarse 'client_secret.json' y estar en la raíz del proyecto.
Agrega 'client_secret.json' a tu .gitignore para evitar subirlo al repositorio.
"""
CREDENTIALS_FILE = 'client_secret.json'
TOKEN_FILE = 'token.json'


def authenticate_drive():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service


def upload_file(service, file_path, folder_id):
    file_name = os.path.basename(file_path)
    media = MediaFileUpload(file_path, resumable=True)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Subido: {file_name} a carpeta {folder_id}")
    return file.get('id')


def upload_images(service):
    image_files = glob.glob('data/images/*.png')
    for img in image_files:
        upload_file(service, img, DRIVE_FOLDER_IDS['imagenes'])

def upload_processed_videos(service):
    video_files = glob.glob('data/videos/processed/*.mp4')
    for vid in video_files:
        upload_file(service, vid, DRIVE_FOLDER_IDS['procesados'])

def upload_fundido_video(service):
    fundido_files = glob.glob('data/videos/final/*FUNDIDO_TIKTOK*.mp4')
    for vid in fundido_files:
        upload_file(service, vid, DRIVE_FOLDER_IDS['fundidos'])


def main():
    service = authenticate_drive()
    upload_images(service)
    upload_processed_videos(service)
    upload_fundido_video(service)

if __name__ == '__main__':
    main()
