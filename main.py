from src.initial_setup import initial_setup
from src.main_window_dev import create_window as create_window_dev
from src.main_window_anl import create_window as create_window_analyst
import configparser

def check_user_type():
    config = configparser.ConfigParser()
    config.read('config.ini')
    user_type = int(config['User']['Type'])
    return user_type

if __name__ == "__main__":
    user_type = check_user_type()
    if user_type == 0:
        app = initial_setup()
    elif user_type == 1:
        app = create_window_analyst()
    else:
        app = create_window_dev()
    app.mainloop()
