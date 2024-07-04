import tkinter as tk
from tkinter import filedialog, StringVar, messagebox
from PIL import Image
from pystray import Icon as trayIcon, MenuItem as item
import os
import threading
import configparser

from .firebird import configurar_firebird, load_config as load_config_firebird
from .postgres import configurar_postgres, load_config as load_postgres_config
from .config_window import config_window
from .compacteds import processar_arquivo_compactado

def create_window():
    app = tk.Tk()
    app.title("Configurador de Bases")
    app.configure(bg="#333")
    app.resizable(False, False)
    app.overrideredirect(True)
    app.attributes('-topmost', 1)

    nome_base_var = StringVar(app)
    arquivo_var = StringVar(app)
    config_in_progress = False  

    tk.Label(app, text="Nome da Base:", bg="#333", fg="white").pack(anchor="w", padx=10, pady=2)
    tk.Entry(app, textvariable=nome_base_var, bg="#444", fg="white").pack(fill="x", padx=10)
    tk.Label(app, text="Arquivo do Banco de Dados:", bg="#333", fg="white").pack(anchor="w", padx=18, pady=2)
    tk.Entry(app, textvariable=arquivo_var, bg="#444", fg="white").pack(fill="x", padx=10)
    tk.Button(app, text="Escolher Arquivo", command=lambda: arquivo_var.set(filedialog.askopenfilename()), bg="#555", fg="white").pack(fill="x", padx=10, pady=2)
    tk.Button(app, text="Configurar Base", command=lambda: configurar_base(nome_base_var.get(), arquivo_var.get()), bg="#007BFF", fg="white").pack(fill="x", padx=10, pady=10)
    tk.Button(app, text="Minimizar", command=app.withdraw, bg="#555", fg="white").pack(fill="x", padx=10, pady=5)

    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = screen_width - width - 10
    y = screen_height - height - 50
    app.geometry(f'{width}x{height}+{x}+{y}')

    def clear_fields(success):
        nonlocal config_in_progress
        if success:
            nome_base_var.set("")
            arquivo_var.set("")
        config_in_progress = False  

    def configurar_base(nome_base, caminho_arquivo):
        nonlocal config_in_progress
        if nome_base == '' or caminho_arquivo == '':
            messagebox.showerror("Erro", "Informe o nome e o caminho da base.")
            return
        config_in_progress = True  
        if caminho_arquivo.endswith('.zip') or caminho_arquivo.endswith('.tar.gz') or caminho_arquivo.endswith('.tgz') or caminho_arquivo.endswith('.tar') or caminho_arquivo.endswith('.rar'):
            processar_arquivo_compactado(nome_base, caminho_arquivo, clear_fields)
            app.withdraw()
        else:
            _, ext = os.path.splitext(caminho_arquivo)
            if ext.lower() == '.fdb':
                configurar_firebird(nome_base, caminho_arquivo, load_config_firebird(), clear_fields)
                app.withdraw()
            elif ext.lower() in ('.dump', '.backup'):
                configurar_postgres(nome_base, caminho_arquivo, load_postgres_config(), lambda success: (clear_fields(success), enable_tray_menu()))
                app.withdraw()
            else:
                messagebox.showerror("Erro", "Tipo de arquivo inválido.")
                config_in_progress = False

    def quit_application(icon, app):
        icon.stop()
        app.quit()

    def show_hide_window(icon, app):
        if config_in_progress:
            messagebox.showinfo("Informação", "Configuração da base em andamento. Por favor, aguarde a conclusão.")
        elif app.state() == 'withdrawn':
            app.deiconify()
        else:
            app.withdraw()

    def open_config_window():
        if config_in_progress:
            messagebox.showinfo("Informação", "Configuração da base em andamento. Por favor, aguarde a conclusão.")
            return
        app.withdraw()
        def on_complete():
            app.deiconify()
        config_app = config_window(2, on_complete)
        config_app.attributes('-topmost', 1)
        config_app.mainloop()

    def enable_tray_menu():
        icon.update_menu(menu)

    icon_image = Image.open("icon.png")
    menu = (
        item('Abrir', lambda: show_hide_window(icon, app)),
        item('Configurações', open_config_window),
        item('Fechar tudo', lambda: quit_application(icon, app))
    )
    icon = trayIcon("Configurador de Bases", icon_image, menu=menu)
    
    def setup(icon):
        icon.visible = True
    
    threading.Thread(target=lambda: icon.run(setup)).start()
    
    return app
