import zipfile
import tarfile
import rarfile
import os
from tkinter import messagebox
from .postgres import configurar_postgres, load_config
from .firebird import configurar_firebird

def substituir_caminho_mapeado(caminho):
    if caminho.startswith('P:'):
        return caminho.replace('P:', '\\\\COLUMBIA\\DADOS')
    return caminho

def descompactar_arquivo(arquivo, pasta_destino):
    try:
        if zipfile.is_zipfile(arquivo):
            with zipfile.ZipFile(arquivo, 'r') as zip_ref:
                zip_ref.extractall(pasta_destino)
        elif tarfile.is_tarfile(arquivo):
            with tarfile.open(arquivo, 'r:*') as tar_ref:
                tar_ref.extractall(pasta_destino)
        elif rarfile.is_rarfile(arquivo):
            with rarfile.RarFile(arquivo, 'r') as rar_ref:
                rar_ref.extractall(pasta_destino)
        else:
            raise ValueError("Formato de arquivo compactado não suportado.")
    except Exception as e:
        messagebox.showerror("Erro na Descompactação", f"Erro ao descompactar o arquivo: {str(e)}")
        return False
    return True

def processar_arquivo_compactado(nome_base, caminho_arquivo, clear_fields):
    config = load_config()
    pasta_default = config['Paths'].get('DefaultDatabasePath', 'D:/Dados')
    pasta_destino = os.path.join(pasta_default, nome_base)

    caminho_arquivo = substituir_caminho_mapeado(caminho_arquivo)  # Substitui o caminho se necessário

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    if not descompactar_arquivo(caminho_arquivo, pasta_destino):
        clear_fields(False)
        return

    arquivos_descompactados = os.listdir(pasta_destino)
    if not arquivos_descompactados:
        messagebox.showerror("Erro na Descompactação", "Nenhum arquivo encontrado após a descompactação.")
        clear_fields(False)
        return

    caminho_banco = None
    for arquivo in arquivos_descompactados:
        if arquivo.lower().endswith(('.fdb', '.dump', '.backup')):
            caminho_banco = os.path.join(pasta_destino, arquivo)
            break

    if not caminho_banco:
        messagebox.showerror("Erro na Descompactação", "Arquivo do banco de dados não encontrado após a descompactação.")
        clear_fields(False)
        return

    if caminho_banco.lower().endswith('.fdb'):
        configurar_firebird(nome_base, caminho_banco, config, clear_fields)
    else:
        configurar_postgres(nome_base, caminho_banco, config, clear_fields)
