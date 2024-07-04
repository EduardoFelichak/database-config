import requests
import os
import zipfile
import io

GITHUB_REPO = "EduardoFelichak/database-config"
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def get_latest_release():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def download_and_extract_asset(asset_url, asset_name):
    response = requests.get(asset_url, stream=True)
    response.raise_for_status()
    with open(asset_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    if asset_name.endswith(".zip"):
        with zipfile.ZipFile(asset_name, 'r') as zip_ref:
            zip_ref.extractall()

def update_application():
    try:
        release = get_latest_release()
        for asset in release['assets']:
            if asset['name'] == "database-config.zip": 
                asset_url = asset['browser_download_url']
                download_and_extract_asset(asset_url, asset['name'])
                print("Atualização concluída com sucesso.")
                return
        print("Nenhuma atualização disponível.")
    except Exception as e:
        print(f"Falha ao verificar atualizações: {str(e)}")
        raise

if __name__ == "__main__":
    update_application()
