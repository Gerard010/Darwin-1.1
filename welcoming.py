import os
import subprocess
import tkinter as tk
from tkinter import font
import webbrowser

# Function to open the English Assistant
def open_english():
    file_name = "Assistant.py"
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_folder, file_name)
    
    if os.path.exists(file_path):
        subprocess.Popen(['python3', file_path], close_fds=True)
        os._exit(0) 
    else:
        print(f"Error")

# Function to open the Spanish Assistant
def open_spanish():
    file_name = "Asistente.py"
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_folder, file_name)
    
    if os.path.exists(file_path):
        subprocess.Popen(['python3', file_path], close_fds=True)
        os._exit(0) 
    else:
        print(f"Error")

# Function to open the 
def open_instruction_manual(event=None):
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

title_label = tk.Label(root, text="Hi! Welcome to Darwin", font=("Helvetica", 16, "bold"))
title_label.pack(pady=(30, 10))

description_label = tk.Label(root, text="The best IA assistant fully developed in Python.", font=("Helvetica", 14))
description_label.pack(pady=(0, 20))  

language_label = tk.Label(root, text="Choose the lenguage:", font=("Helvetica", 14))
language_label.pack(pady=(0, 10))  

button_frame = tk.Frame(root)
button_frame.pack(pady=(0, 20))

boton_espanol = tk.Button(button_frame, text="Español", command=open_spanish, width=20)
boton_espanol.pack(side=tk.LEFT, padx=10)

boton_ingles = tk.Button(button_frame, text="English", command=open_english, width=20)
boton_ingles.pack(side=tk.LEFT, padx=10)  

underline_font = font.Font(family="Helvetica", size=13, underline=True)


instructions_label = tk.Label(root, text="Click here to see the instruction manual", fg="blue", cursor="hand1", font=underline_font)
instructions_label.pack(pady=(20, 0))  

# Vincular el clic en la etiqueta a la función de abrir el manual
instructions_label.bind("<Button-1>", open_instruction_manual)

root.mainloop()