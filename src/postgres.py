import configparser
import subprocess
import threading
from tkinter import messagebox
from plyer import notification
import psycopg2
import os

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def run_command_powershell(cmd, nome_base, success_message, error_message, after_func, config):
    try:
        process = subprocess.Popen(["powershell", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        stdout_str = stdout.decode('utf-8')
        stderr_str = stderr.decode('utf-8')

        if process.returncode == 0 or "already exists" in stderr_str or "errors ignored on restore" in stderr_str:
            add_to_ini_file(nome_base, config) 
            notification.notify(title="Pronto!!!", message=success_message.format(nome_base), timeout=10)
            after_func(True)
        else:
            notification.notify(title="Erro na Configuração", message=error_message.format(nome_base, stderr_str), timeout=10)
            after_func(False)
    except Exception as e:
        notification.notify(title="Erro na Configuração", message=f"Erro ao executar o comando: {str(e)}", timeout=10)
        after_func(False)

def add_to_ini_file(nome_base, config):
    ini_file_path = config['Paths']['QuestorIniPath']
    with open(ini_file_path, "a") as file:
        file.write(f"\n[{nome_base}]\nTipoBancoDados=PostgreSQL\nServidor=127.0.0.1\nPortaConexao=5432\nArqBancoDados={nome_base}\nUsuarioBancoDados=postgres\nUsuarioBancoSistema=0\nSenhaUsuarioBancoDados=uFH3KVnlRqx1\nLibraryName=dbxopg.dll\nVendorLib=libpq.dll\nPerfCadNaoTrazNada=0\nPerfCadNaoTrazNadaCon=0\nPerfConNaoAtualizarDCLookup=0\nUsarZebedee=0\nPortaZebedee=3059\nMaisOpcoesZebedee=\nMemDestruirDMCadastro=1\nMemLiberarCacheMemoria=1\nPadronizaTamanhoControles=1\n")

def configurar_postgres(nome_base, caminho_arquivo, config, clear_fields):
    notification.notify(title="Configurando a base", message="Iniciei a configuração, te informo quando tudo terminar.", timeout=10)
    db_user = config['Database']['User']
    db_password = config['Database']['Password']
    db_host = config['Database']['Host']

    conn = psycopg2.connect(dbname="postgres", user=db_user, password=db_password, host=db_host)
    conn.autocommit = True
    if base_existe(conn, nome_base):
        conn.close()
        notification.notify(title="Erro na Configuração", message=f"A base de dados '{nome_base}' já existe.", timeout=10)
        return
    cur = conn.cursor()
    try:
        cur.execute(f'CREATE DATABASE "{nome_base}" WITH OWNER = {db_user} ENCODING = "UTF8" LC_COLLATE = "portuguese_brazil.1252" LC_CTYPE = "portuguese_brazil.1252" TABLESPACE = pg_default CONNECTION LIMIT = -1 TEMPLATE template0;')
    except Exception as e:
        notification.notify(title="Erro na Configuração", message=f"Erro ao criar a base de dados {nome_base}: {str(e)}", timeout=10)
        return
    finally:
        cur.close()

    pg_restore_path = os.path.join(config['Paths']['PostgresBinPath'], 'pg_restore.exe')
    if not os.path.exists(pg_restore_path):
        notification.notify(title="Erro na Configuração", message="O caminho para pg_restore não foi encontrado. Verifique sua configuração.", timeout=10)
        return

    cmd = f'$env:PGPASSWORD="{db_password}"; & "{pg_restore_path}" -h {db_host} -U {db_user} -d "{nome_base}" -v "{caminho_arquivo}"'
    
    threading.Thread(target=run_command_powershell, args=(cmd, nome_base, f"Base Postgres '{nome_base}' configurada com sucesso!", f"Falha ao restaurar a base {nome_base}.\nErro: {{}}", clear_fields, config)).start()

def base_existe(conn, nome_base):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (nome_base,))
    existe = cur.fetchone()
    cur.close()
    return existe is not None
