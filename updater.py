import requests
import zipfile
import io
import os
from tkinter import messagebox
import tkinter as tk

GITHUB_REPO = "EduardoFelichak/database-config"
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def get_latest_release():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro de Atualização", f"Não foi possível obter a última versão: {e}")
        root.destroy()
        raise

def download_and_extract_asset(asset_url, asset_name):
    try:
        response = requests.get(asset_url, stream=True)
        response.raise_for_status()
        with open(asset_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        if asset_name.endswith(".zip"):
            with zipfile.ZipFile(asset_name, 'r') as zip_ref:
                zip_ref.extractall()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro de Atualização", f"Erro ao baixar ou extrair a atualização: {e}")
        root.destroy()
        raise

def update_application():
    try:
        release = get_latest_release()
        for asset in release['assets']:
            if asset['name'].endswith(".zip"): 
                asset_url = asset['browser_download_url']
                download_and_extract_asset(asset_url, asset['name'])
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Atualização", "Atualização concluída com sucesso!")
                root.destroy()
                break
    except Exception as e:
        pass 

if __name__ == "__main__":
    update_application()
