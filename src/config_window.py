import tkinter as tk
from tkinter import filedialog, StringVar
import configparser

def config_window(user_type, on_complete):
    def save_config():
        postgres_bin_path = postgres_bin_var.get()
        
        if not postgres_bin_path.endswith("/bin") and not postgres_bin_path.endswith("\\bin"):
            tk.messagebox.showerror("Erro", "Caminho da pasta bin inválido. Acesse a pasta PostgreSQL, e depois selecione a versão do seu Postgres (Normalmente é 14 ou 16). Feito isso, clique na pasta bin.")
            return
        
        config['Paths']['PostgresBinPath'] = postgres_bin_var.get()
        config['Paths']['defaultdatabasepath'] = default_path_var.get()
        config['Database']['User'] = user_var.get()
        config['Database']['Password'] = password_var.get()

        if user_type == 2:
            config['Paths']['QuestorIniPath'] = questor_ini_var.get()

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        app.destroy()
        on_complete()

    config = configparser.ConfigParser()
    config.read('config.ini')

    questor_ini_default = 'D:/Workspace/QuestorTributarioTrunk/outputD26/Win32/Questor.Conexao.ini'
    questor_ini_value = config['Paths'].get('QuestorIniPath', questor_ini_default)
    postgres_bin_value = config['Paths'].get('PostgresBinPath', '')
    default_path_value = config['Paths'].get('defaultdatabasepath', '')
    user_value = config['Database'].get('User', '')
    password_value = config['Database'].get('Password', '')

    app = tk.Tk()
    app.title("Configure Corretamente")
    app.configure(bg="#333")
    app.resizable(False, False)

    questor_ini_var = StringVar(app, value=questor_ini_value)
    postgres_bin_var = StringVar(app, value=postgres_bin_value)
    default_path_var = StringVar(app, value=default_path_value)
    user_var = StringVar(app, value=user_value)
    password_var = StringVar(app, value=password_value)

    if user_type == 2:
        tk.Label(app, text="Caminho do Questor.Conexao.ini:", bg="#333", fg="white").pack(anchor="w", padx=10, pady=2)
        tk.Entry(app, textvariable=questor_ini_var, bg="#444", fg="white").pack(fill="x", padx=10)
        tk.Button(app, text="Escolher Arquivo", command=lambda: questor_ini_var.set(filedialog.askopenfilename(initialdir="D:/Workspace/QuestorTributarioTrunk/outputD26/Win32")), bg="#555", fg="white").pack(fill="x", padx=10, pady=2)

    tk.Label(app, text="Pasta bin na instalação do Postgres:", bg="#333", fg="white").pack(anchor="w", padx=10, pady=2)
    tk.Entry(app, textvariable=postgres_bin_var, bg="#444", fg="white").pack(fill="x", padx=10)
    tk.Button(app, text="Escolher Pasta", command=lambda: postgres_bin_var.set(filedialog.askdirectory(initialdir="C:/Program Files/PostgreSQL")), bg="#555", fg="white").pack(fill="x", padx=10, pady=2)

    tk.Label(app, text="Pasta onde você coloca suas bases:", bg="#333", fg="white").pack(anchor="w", padx=10, pady=2)
    tk.Entry(app, textvariable=default_path_var, bg="#444", fg="white").pack(fill="x", padx=10)
    tk.Button(app, text="Escolher Pasta", command=lambda: default_path_var.set(filedialog.askdirectory(initialdir="D:/")), bg="#555", fg="white").pack(fill="x", padx=10, pady=2)

    tk.Label(app, text="Usuário (Somente postgres):", bg="#333", fg="white").pack(anchor="w", padx=10, pady=2)
    tk.Entry(app, textvariable=user_var, bg="#444", fg="white").pack(fill="x", padx=10)

    tk.Label(app, text="Senha (Somente postgres):", bg="#333", fg="white").pack(anchor="w", padx=10, pady=2)
    tk.Entry(app, textvariable=password_var, show='*', bg="#444", fg="white").pack(fill="x", padx=10)

    tk.Button(app, text="Salvar Configurações", command=save_config, bg="#007BFF", fg="white").pack(fill="x", padx=10, pady=10)
    
    app.update_idletasks()
    width = 500
    height = 400
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    app.geometry(f'{width}x{height}+{x}+{y}')

    return app
