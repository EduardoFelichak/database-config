import tkinter as tk
from tkinter import ttk, messagebox
import configparser
from .config_window import config_window

def initial_setup():
    def save_user_type():
        user_type = user_type_var.get()
        if user_type not in ['1', '2']:
            messagebox.showerror("Erro", "Selecione uma categoria de usuário.")
            return
        
        config = configparser.ConfigParser()
        config.read('config.ini')
        config['User']['Type'] = user_type
        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        
        app.destroy()

        def on_complete():
            if user_type == '1':
                from src.main_window_anl import create_window as create_window_analyst
                app_analyst = create_window_analyst()
                app_analyst.mainloop()
            else:
                from src.main_window_dev import create_window as create_window_dev
                app_dev = create_window_dev()
                app_dev.mainloop()

        next_window = config_window(int(user_type), on_complete)
        next_window.mainloop()
    
    app = tk.Tk()
    app.title("Configuração Inicial")
    app.configure(bg="#333")
    app.resizable(False, False)
    app.overrideredirect(True)
    app.attributes('-topmost', 1)
    
    user_type_var = tk.StringVar()
    
    tk.Label(app, text="Selecione a categoria de usuário:", bg="#333", fg="white").pack(anchor="w", padx=10, pady=2)
    combobox = ttk.Combobox(app, textvariable=user_type_var, values=["1 - Pessoa Normal", "2 - Desenvolvedor"], state="readonly")
    combobox.pack(fill="x", padx=10)
    combobox.bind("<<ComboboxSelected>>", lambda event: user_type_var.set(combobox.get().split(' ')[0]))
    
    tk.Button(app, text="OK", command=save_user_type, bg="#007BFF", fg="white").pack(fill="x", padx=10, pady=10)
    
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = screen_width - width - 10
    y = screen_height - height - 50
    app.geometry(f'{width}x{height}+{x}+{y}')
    
    return app
