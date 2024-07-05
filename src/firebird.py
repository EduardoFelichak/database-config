import configparser
from tkinter import messagebox
from plyer import notification
import os

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def criar_arquivo_ini_se_analista(config):
    user_type = int(config['User']['Type'])
    ini_file_path = config['Paths']['QuestorIniPath']
    if user_type == 1 and not os.path.exists(ini_file_path):
        with open(ini_file_path, "w") as file:
            file.write("[Settings]\n")

def configurar_firebird(nome_base, caminho_arquivo, config, clear_fields):
    criar_arquivo_ini_se_analista(config)
    
    ini_file_path = config['Paths']['QuestorIniPath']
    try:
        with open(ini_file_path, "a") as file:
            file.write(f"\n[{nome_base}]\nTipoBancoDados=FireBird\nServidor=localhost\nPortaConexao=3050\nArqBancoDados={caminho_arquivo}\nUsuarioBancoDados=SYSDBA\nUsuarioBancoSistema=0\nSenhaUsuarioBancoDados=uFH3KVnlRqx1\nLibraryName=dbxfb.dll\nVendorLib=fbclient.dll\nPerfCadNaoTrazNada=0\nPerfCadNaoTrazNadaCon=0\nPerfConNaoAtualizarDCLookup=0\nUsarZebedee=0\nPortaZebedee=3059\nMaisOpcoesZebedee=\nMemDestruirDMCadastro=1\nMemLiberarCacheMemoria=1\nPadronizaTamanhoControles=1\n")
        notification.notify(title="Configuração de Bases", message=f"Base Firebird '{nome_base}' configurada com sucesso!", timeout=10)
        clear_fields(True)
    except Exception as e:
        notification.notify(title="Erro na Configuração", message=f"Erro ao configurar a base Firebird '{nome_base}': {str(e)}", timeout=10)
        clear_fields(False)
