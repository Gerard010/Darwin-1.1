import os
import subprocess
import tkinter as tk
from tkinter import font
import webbrowser

def open_english():
    file_name = "Assistant.py"
    
    # Obtener la carpeta actual del script
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta completa del archivo
    file_path = os.path.join(current_folder, file_name)
    
    if os.path.exists(file_path):
        # Abrir el nuevo archivo en un proceso independiente
        subprocess.Popen(['python3', file_path], close_fds=True)  # Cambia a 'python' si usas Python 2.x o en Windows
        os._exit(0)  # Cierra la ventana actual
    else:
        print(f"Error")

def open_espanol():
    file_name = "Asistente.py"
    
    # Obtener la carpeta actual del script
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta completa del archivo
    file_path = os.path.join(current_folder, file_name)
    
    if os.path.exists(file_path):
        # Abrir el nuevo archivo en un proceso independiente
        subprocess.Popen(['python3', file_path], close_fds=True)  # Cambia a 'python' si usas Python 2.x o en Windows
        os._exit(0)  # Cierra la ventana actual
    else:
        print(f"Error")

def open_manual_instrucciones(event=None):
    file_name = "manual_instrucciones.html"
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_folder, file_name)
    
    if os.path.exists(file_path):
        webbrowser.open(f'file://{file_path}')
    else:
        print("Error: El archivo no existe.")

root = tk.Tk()
root.title("Smart Assistant")
root.geometry("500x300")

# Etiqueta para el título
title_label = tk.Label(root, text="¡Hi! Welcome to Darwin", font=("Helvetica", 16, "bold"))
title_label.pack(pady=(30, 10))  # Margen superior e inferior

# Descripción
description_label = tk.Label(root, text="The best IA assistant fully developed in Python.", font=("Helvetica", 14))
description_label.pack(pady=(0, 20))  # Margen inferior

# Etiqueta para elegir idioma
language_label = tk.Label(root, text="Choose the lenguage:", font=("Helvetica", 14))
language_label.pack(pady=(0, 10))  # Margen inferior

# Botones para seleccionar idioma
button_frame = tk.Frame(root)
button_frame.pack(pady=(0, 20))  # Margen inferior

boton_espanol = tk.Button(button_frame, text="Español", command=open_espanol, width=20)
boton_espanol.pack(side=tk.LEFT, padx=10)  # Margen lateral

boton_ingles = tk.Button(button_frame, text="English", command=open_english, width=20)
boton_ingles.pack(side=tk.LEFT, padx=10)  # Margen lateral

underline_font = font.Font(family="Helvetica", size=13, underline=True)

# Instrucciones
instructions_label = tk.Label(root, text="Click here to see the instruction manual", fg="blue", cursor="hand1", font=underline_font)
instructions_label.pack(pady=(20, 0))  # Margen superior

# Vincular el clic en la etiqueta a la función de abrir el manual
instructions_label.bind("<Button-1>", open_manual_instrucciones)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()