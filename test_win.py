import pygetwindow as gw
import time

import pygetwindow as gw
from pywinauto import Application
import time


def get_windows_titles():
    windows = gw.getAllTitles()
    return [w for w in windows if w]

# Obtener la lista inicial de ventanas
initial_windows = set(get_windows_titles())

def bring_window_to_front(window_title):
    app = Application().connect(title=window_title)
    window = app[window_title]
    window.set_focus()

while True:
    time.sleep(2)  # Esperar 1 segundo entre comprobaciones
    current_windows = set(get_windows_titles())
    # Detectar nuevas ventanas
    new_windows = current_windows - initial_windows
    if new_windows:


        print(f"Nueva ventana detectada: {new_windows}",str(new_windows))
        # Aquí puedes agregar el código para manejar la nueva ventana

        if 'Profilogram' in str(new_windows):
            time.sleep(4)
            for win in new_windows:
                bring_window_to_front(win)
    # Actualizar la lista de ventanas iniciales
    initial_windows = current_windows
    