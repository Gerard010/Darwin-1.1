import tkinter as tk
import os
import webbrowser
import datetime
import psutil
import re
import random
import speech_recognition as sr
import subprocess

# Función para procesar el comando con IA
def procesar_comando_ia(comando):
    try:
        resultado = subprocess.run(
            ["ollama", "run", "llava:13b"],
            input=comando,
            text=True,
            capture_output=True
        )
        return resultado.stdout.strip()
    except Exception:
        return "Error al usar la IA."

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("DarwinIA")
ventana.geometry("555x333")

# Función que ejecuta el comando introducido
def ejecutar_comando(comando):
    respuesta = ""
    # Verifica si el comando es una URL
    if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', comando):
        webbrowser.open(comando)
        respuesta = f"Abriendo sitio web: {comando}"
    elif "chrome" in comando and "busca" in comando:
        termino_busqueda = comando.split("busca", 1)[1].split("en chrome")[0].strip()
        if termino_busqueda:
            url_busqueda = f"https://www.google.com/search?q={termino_busqueda}"
            webbrowser.open(url_busqueda)
            respuesta = f"Buscando '{termino_busqueda}' en Chrome..."
        else:
            respuesta = "Por favor, especifica tu búsqueda después de 'search'."
    elif comando.startswith("pon "):
        query = comando[len("pon "):].strip()
        if query:
            url_busqueda = f"https://www.youtube.com/results?search_query={query}+song"
            webbrowser.open(url_busqueda)
            respuesta = f"Reproduciendo '{query}' en YouTube..."
        else:
            respuesta = "Por favor, especifica la canción que deseas reproducir."
    elif "youtube" in comando and "encuentra" in comando:
        termino_busqueda = comando.split("encuentra", 1)[1].split("en youtube")[0].strip()
        if termino_busqueda:
            url_busqueda = f"https://www.youtube.com/results?search_query={termino_busqueda}"
            webbrowser.open(url_busqueda)
            respuesta = f"Buscando '{termino_busqueda}' en YouTube..."
        else:
            respuesta = "Por favor, especifica tu búsqueda después de 'find'."
    elif "youtube" in comando and "busca" in comando:
        termino_busqueda = comando.split("busca", 1)[1].split("en youtube")[0].strip()
        if termino_busqueda:
            url_busqueda = f"https://www.youtube.com/results?search_query={termino_busqueda}"
            webbrowser.open(url_busqueda)
            respuesta = f"Buscando '{termino_busqueda}' en YouTube..."
        else:
            respuesta = "Por favor, especifica tu búsqueda después de 'search'."
    elif comando.startswith("busca "):
        query = comando[len("busca "):].strip()
        if query:
            url_busqueda = f"https://www.google.com/search?q={query}"
            webbrowser.open(url_busqueda)
            respuesta = f"Buscando '{query}' en Google..."
        else:
            respuesta = "Por favor, especifica lo que deseas buscar."
    elif "chrome" in comando:
        os.system("open -a 'Google Chrome'")
        respuesta = "Abriendo Google Chrome..."
    elif "editor de texto" in comando:
        os.system("open -a 'TextEdit'")
        respuesta = "Abriendo el editor de texto..."
    elif "calculadora" in comando:
        os.system("open -a 'Calculator'")
        respuesta = "Abriendo la calculadora..."
    elif "apaga" in comando:
        os.system("sudo shutdown -h now")
        respuesta = "Apagando el sistema..."
    elif "reinicia" in comando:
        os.system("sudo shutdown -r now")
        respuesta = "Reiniciando el sistema..."
    elif "cod" in comando:
        os.system("open -a 'Visual Studio Code'")
        respuesta = "Abriendo Visual Studio Code..."
    elif "mail" in comando:
        os.system("open -a Mail")
        respuesta = "Abriendo el cliente de correo..."
    elif "musica" in comando:
        os.system("open -a Music")
        respuesta = "Abriendo el reproductor de música..."
    elif "hora" in comando:
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        respuesta = f"La hora es {hora_actual}"
    elif "dia" in comando:
        dia_actual = datetime.datetime.now().strftime("%d/%m")
        respuesta = f"Hoy es {dia_actual}"
    elif "fecha" in comando:
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        respuesta = f"La fecha es: {fecha_actual}"
    elif "cpu" in comando:
        uso_cpu = psutil.cpu_percent(interval=1)
        respuesta = f"Uso de CPU: {uso_cpu}%"
    elif "memoria" in comando:
        memoria = psutil.virtual_memory()
        respuesta = f"Uso de memoria: {memoria.percent}%"
    elif "bateria" in comando:
        bateria = psutil.sensors_battery()
        respuesta = f"Batería: {bateria.percent}%" if bateria else "Estado de la batería no disponible."
    elif "wifi" in comando:
        estado_wifi = os.popen("networksetup -getairportpower en0").read()
        respuesta = "Wi-Fi está encendido" if "On" in estado_wifi else "Wi-Fi está apagado"
    elif "abre" in comando:
        nombre_app = comando.split("abre", 1)[1].strip()
        if nombre_app:
            estado_apertura = os.system(f"open -a '{nombre_app}'")
            if estado_apertura != 0:
                url_busqueda = f"https://www.google.com/search?q={nombre_app}"
                webbrowser.open(url_busqueda)
                respuesta = f"No se pudo abrir '{nombre_app}'. Buscando '{nombre_app}' en Google..."
            else:
                respuesta = f"Abriendo {nombre_app}..."
        else:
            respuesta = "Porfavor, especifica la app."
    elif "clear" in comando:
        entrada.delete(0, tk.END)
        respuesta = "Introduce un nuevo comando."
    else:
        # Usa la IA si no se reconoce el comando
        respuesta = procesar_comando_ia(comando)

    etiqueta.config(text=respuesta)
    entrada.delete(0, tk.END)
    return respuesta

# Función para reconocer el comando por voz
def escuchar_comando_voz():
    reconocedor = sr.Recognizer()
    with sr.Microphone() as fuente:
        etiqueta.config(text="Escuchando...")
        ventana.update()
        reconocedor.adjust_for_ambient_noise(fuente, duration=1)
        audio = reconocedor.listen(fuente)
    try:
        comando = reconocedor.recognize_google(audio, language="es-ES")
        entrada.delete(0, tk.END)
        entrada.insert(0, comando)
        respuesta = ejecutar_comando(comando)
        etiqueta.config(text=respuesta)
    except:
        etiqueta.config(text="Error")

# Etiqueta principal
etiqueta = tk.Label(ventana, text="Escribe un comando")
etiqueta.pack(pady=20)

# Marco para la entrada de texto
marco_entrada = tk.Frame(ventana)
marco_entrada.pack(pady=10)

entrada = tk.Entry(marco_entrada, width=30)
entrada.pack(side=tk.LEFT, padx=10)

boton_voz = tk.Button(marco_entrada, text="🎙️", command=escuchar_comando_voz)
boton_voz.pack(side=tk.LEFT, padx=5)

# Marco para botones
marco_botones = tk.Frame(ventana)
marco_botones.pack(pady=10)

boton_chrome = tk.Button(marco_botones, text="Chrome",
                         command=lambda: os.system("open -a 'Google Chrome'"))
boton_chrome.pack(side=tk.LEFT, padx=10)

boton_calculadora = tk.Button(marco_botones, text="Calculadora",
                              command=lambda: os.system("open -a 'Calculator'"))
boton_calculadora.pack(side=tk.LEFT, padx=5)

boton_chatgpt = tk.Button(marco_botones, text="ChatGPT",
                          command=lambda: os.system("open -a 'ChatGPT'"))
boton_chatgpt.pack(side=tk.LEFT, padx=0)

boton_ejecutar = tk.Button(ventana, text="Ejecutar",
                           command=lambda: ejecutar_comando(entrada.get()))
boton_ejecutar.pack(pady=10)

ventana.mainloop()