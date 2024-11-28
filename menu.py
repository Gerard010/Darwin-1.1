import tkinter as tk
import subprocess
import os

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

root = tk.Tk()
root.title("Smart Assistant")
root.geometry("500x300")

boton_espanol = tk.Button(text="Español", command=open_espanol, width=20, height=5)
boton_espanol.pack(pady=40)  # Margen lateral

boton_ingles = tk.Button(text="English", command=open_english, width=20, height=5)
boton_ingles.pack() 

root.mainloop()