import requests
import os
import subprocess
from tkinter import messagebox
import tkinter as tk

GITHUB_REPO = "EduardoFelichak/database-config"
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
CURRENT_VERSION = "v1.0.2"  

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

def download_and_run_installer(asset_url, asset_name):
    try:
        response = requests.get(asset_url, stream=True)
        response.raise_for_status()
        with open(asset_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        subprocess.run([asset_name], check=True)
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro de Atualização", f"Erro ao baixar ou executar a atualização: {e}")
        root.destroy()
        raise

def update_application():
    try:
        release = get_latest_release()
        latest_version = release['tag_name']
        if latest_version > CURRENT_VERSION:
            for asset in release['assets']:
                if asset['name'].endswith(".exe"):
                    asset_url = asset['browser_download_url']
                    download_and_run_installer(asset_url, asset['name'])
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo("Atualização", "Atualização concluída com sucesso!")
                    root.destroy()
                    break
            else:
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Atualização", "Nenhuma atualização disponível.")
                root.destroy()
        else:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Atualização", "Você já está usando a versão mais recente.")
            root.destroy()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro de Atualização", f"Erro ao atualizar: {e}")
        root.destroy()
        raise

if __name__ == "__main__":
    update_application()
