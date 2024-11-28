import tkinter as tk
import os
import webbrowser
import datetime
import psutil
import re
from difflib import get_close_matches
import random
import speech_recognition as sr
import subprocess

conversational_responses = {

    # Spanish Responses
    "hola": ["¡Hola! ¿Cómo puedo ayudarte hoy?", "¡Hola! ¿En qué puedo asistirte?", "¡Hola! ¿Qué tal? ¿Cómo puedo ayudarte?", "¡Hola! ¿Cómo va todo? ¿En qué puedo ayudarte?", "¡Hola! ¿Cómo te va? ¿En qué te ayudo hoy?"],
    "que tal": ["¡Estoy bien, gracias! ¿Y tú?", "Estoy genial, ¡gracias por preguntar! ¿Cómo estás tú?", "Estoy muy bien, gracias. ¿Y tú cómo te encuentras?", "¡Todo bien! ¿Y tú, cómo estás?", "Estoy bien, gracias. ¿Cómo te va a ti?"],
    "adiós": ["¡Hasta luego! ¡Cuídate!", "¡Adiós! ¡Nos vemos pronto!", "¡Hasta pronto! ¡Cuídate mucho!", "¡Adiós! ¡Espero verte pronto!", "¡Hasta luego! ¡Cuídate y que tengas un buen día!"],
    "gracias": ["¡De nada!", "¡Con gusto!", "¡Es un placer ayudar!", "¡A ti! ¡Siempre estoy aquí para ayudarte!", "¡No hay de qué! ¡Estoy aquí para ayudarte!"],
    "cómo estás": ["¡Estoy bien, gracias! ¿Y tú?", "Estoy genial, ¡gracias por preguntar! ¿Cómo estás tú?", "Estoy muy bien, gracias. ¿Y tú cómo te encuentras?", "¡Todo bien! ¿Y tú, cómo estás?", "Estoy bien, gracias. ¿Cómo te va a ti?"],
    "quién eres": ["¡Soy tu asistente! Estoy aquí para ayudarte.", "¡Soy tu asistente virtual, siempre listo para ayudarte!", "¡Soy tu ayudante digital, aquí para lo que necesites!", "¡Soy tu asistente, listo para asistirte con todo!", "¡Soy tu asistente! ¿En qué te puedo ayudar?"],
    "cuál es tu nombre": ["Me puedes llamar Darwin. 😊", "Me llaman Darwin, ¡estoy aquí para ayudarte!", "Puedes llamarme Darwin. 😊", "Soy Darwin, tu asistente digital.", "Mi nombre es Darwin. ¡Encantado de ayudarte!"],
    "qué haces": ["¡Ayudo con tareas, información y más!", "¡Ayudo con todo lo que necesites, desde tareas hasta información!", "¡Puedo ayudarte con tareas, preguntas y mucho más!", "¡Soy experto en tareas, respuestas y aplicaciones! ¿Qué necesitas?", "¡Ayudo en lo que sea necesario, tareas, consultas y mucho más!"],
    "dime un chiste": ["¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter. 🐦😂", "¿Cómo se llama un boomerang que no vuelve? Un palo. 😂", "¿Por qué los gatos no juegan a las cartas? Porque siempre están haciendo trampas. 🐱😂", "¿Sabes por qué el libro de matemáticas está triste? Porque tenía demasiados problemas. 📚😂", "¿Por qué no puedes confiar en un átomo? Porque hacen todo lo posible para formar moléculas. 😂"],
    "dime algo interesante": ["¡Los pulpos tienen tres corazones! ¡Increíble, ¿verdad?", "Los colibríes son los únicos pájaros que pueden volar hacia atrás. ¡Súper interesante!", "Sabías que el corazón de un camarón está en su cabeza? ¡Es curioso, verdad!", "El Sol es 400 veces más grande que la Luna, pero la Luna está 400 veces más cerca de la Tierra. ¡Qué curioso!", "Las abejas pueden reconocer rostros humanos, ¡increíble, verdad?"],
    "qué puedes hacer": ["¡Puedo ayudarte con tareas, responder preguntas, abrir aplicaciones y más!", "¡Puedo hacer muchas cosas, desde ayudarte con tareas hasta buscar información y abrir apps!", "¡Puedo asistirte en tareas, responder tus dudas y mucho más!", "¡Puedo hacer varias cosas, como buscar información o abrir aplicaciones por ti!", "¡Puedo ayudarte con muchas cosas! Desde resolver dudas hasta realizar tareas y mucho más."],
    "cómo me puedes ayudar": ["¡Desde tareas hasta información!", "¡Puedo ayudarte en todo lo que necesites! Tareas, preguntas y más.", "¡Puedo asistirte con cualquier duda o tarea que tengas!", "¡Ayudo con todo tipo de tareas, desde información hasta abrir aplicaciones!", "¡Puedo ayudarte con lo que sea, solo dime qué necesitas!"],
    "hablas español": ["¡Sí, claro! ¿En qué puedo ayudarte?", "¡Por supuesto! ¿En qué te puedo asistir?", "¡Sí, hablo español! ¿Cómo te puedo ayudar?", "¡Claro que sí! ¿En qué puedo ayudarte hoy?", "¡Sí! ¿En qué te gustaría que te ayudara?"],
    "cuantos idiomas hablas": ["Hablo inglés y español.", "Puedo comunicarme en inglés y español.", "Hablo dos idiomas: inglés y español.", "Soy fluido en inglés y español.", "Hablo tanto inglés como español."],
    "estoy mal": ["Lo siento mucho. ¿Hay algo en lo que pueda ayudarte?", "Lamento escuchar eso. ¿Te gustaría hablar de ello?", "Vaya, espero que te sientas mejor pronto. ¿Puedo ayudarte en algo?", "Siento escuchar eso. Si necesitas algo, estoy aquí para ayudarte.", "Lamento mucho que no te sientas bien. ¿Hay algo que pueda hacer por ti?"],
    "estoy bien": ["Me alegra saberlo. ¿En qué puedo ayudarte?", "¡Qué bueno! ¿Hay algo en lo que pueda asistirte?", "Me alegra escuchar eso. ¿Necesitas algo?", "Qué bien que estés bien. ¿En qué puedo ayudarte hoy?", "¡Me alegra que estés bien! ¿Hay algo en lo que te pueda ayudar?"],
}

# Execute Function
def execute_command(command):
    command = command.lower()
    response = None

    if command in conversational_responses:
       response = random.choice(conversational_responses[command])

    if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', command):
        webbrowser.open(command)
        response = f"Abriendo sitio web: {command}"
    
    elif "chrome" in command and "busca" in command:
        search_term = command.split("busca", 1)[1].split("en chrome")[0].strip()
        if search_term:
            search_url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(search_url)
            response = f"Buscando '{search_term}' en Chrome..."
        else:
            response = "Porfavor especifica tu busqueda despues del termino 'busca'."

    elif command.startswith("pon "):
        query = command[len("pon "):].strip()  
        if query:
          search_url = f"https://www.youtube.com/results?search_query={query} + song"
          webbrowser.open(search_url)
          response = f"Poniendo '{query}' en YouTube..."
        else:
          response = "Porfavor especifica la canción que quieres poner."

    elif "youtube" in command and "encuentra" in command:
        search_term = command.split("encuentra", 1)[1].split("en youtube")[0].strip()
        if search_term:
            search_url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.open(search_url)
            response = f"Finding '{search_term}' in YouTube..."
        else:
            response = "Porfavor especifica tu busqueda despues del termino 'encuentra'."
            
    elif "youtube" in command and "busca" in command:
        search_term = command.split("busca", 1)[1].split("en youtube")[0].strip()
        if search_term:
            search_url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.open(search_url)
            response = f"Buscando '{search_term}' en YouTube..."
        else:
            response = "Porfavor especifica tu busqueda despues del termino 'busca'."

    elif command.startswith("busca "):
        query = command[len("busca "):].strip()  
        if query:
          search_url = f"https://www.google.com/search?q={query}"
          webbrowser.open(search_url)
          response = f"Buscando '{query}' en Google..."
        else:
          response = "Porfavor especifica que quieres buscar."
    
    elif "chrome" in command:
        os.system("open -a 'Google Chrome'")
        response = "Abriendo Google Chrome..."
    
    elif "editor de texto" in command:
        os.system("open -a 'TextEdit'")
        response = "Abriendo el editor de texto..."
    
    elif "calculadora" in command:
        os.system("open -a 'Calculator'")
        response = "Abriendo la calculadora..."
    
    elif "apagar" in command:
        os.system("sudo shutdown -h now")
        response = "Apagando el sistema..."
    
    elif "reiniciar" in command:
        os.system("sudo shutdown -r now")
        response = "Reiniciando el sistema..."

    elif "codigo" in command:
        os.system("open -a Visual Studio Code")
        response = "Abriendo Visual Studio Code..."

    elif "correo" in command:
        os.system("open -a Mail")
        response = "Abriendo el correo electrónico..."
    
    elif "musica" in command:
        os.system("open -a Music")
        response = "Abriendo el reproductor de Música..."
    
    elif "hora" in command:
        current_date = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"Son las {current_date}"
    
    elif "dia" in command:
        current_day = datetime.datetime.now().strftime("%d/%m")
        response = f"Hoy es {current_day}"

    elif "fecha" in command:
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        response = f"La fecha: {date}"    
    
    elif "cpu" in command:
        cpu_usage = psutil.cpu_percent(interval=1)
        response = f"Uso de la CPU: {cpu_usage}%"
    
    elif "memoria" in command:
        memory = psutil.virtual_memory()
        response = f"Memoria en uso: {memory.percent}%"
    
    elif "bateria" in command:
        battery = psutil.sensors_battery()
        response = f"Batería: {battery.percent}%" if battery else "El estado de la batería no esta disponible."
    
    elif "wifi" in command:
        wifi_status = os.popen("networksetup -getairportpower en0").read()
        response = "El Wi-Fi está conectado" if "On" in wifi_status else "El Wi-Fi no está conectado"
    
    elif "abre" in command:
        app_name = command.split("abre", 1)[1].strip()
        if app_name:
            open_status = os.system(f"open -a '{app_name}'")
            if open_status != 0:  
                search_url = f"https://www.google.com/search?q={app_name}"
                webbrowser.open(search_url)
                response = f"No se pudo abrir '{app_name}'. Buscando '{app_name}' en Google..."
            else:
                response = f"Abriendo {app_name}..."
        else:
            response = "Por favor, especifica el nombre de la aplicación."
    
    elif "clear" in command:
        entry.delete(0, tk.END)
        response = "Ingresa un nuevo comando."

    # If a direct answer is not found
    if response is None:
        closest_match = get_close_matches(command, conversational_responses.keys(), n=1, cutoff=0.6)
        if closest_match:
            response = random.choice(conversational_responses[closest_match[0]])
        else:
            response = "Lo siento, no te he podido entender."


    label.config(text=response)
    entry.delete(0, tk.END)
    return response

# Voice command function
def listen_for_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        label.config(text="Escuchando...")
        root.update()  
        recognizer.adjust_for_ambient_noise(source, duration=1)  
        audio = recognizer.listen(source)

    try:

        command = recognizer.recognize_google(audio, language="es-ES")
        
        entry.delete(0, tk.END)
        entry.insert(0, command)
        
        response = execute_command(command)
        
        label.config(text=f"{response}")
        
    except sr.UnknownValueError:
        label.config(text="Error")
    except sr.RequestError:
        label.config(text="Error")
    except Exception as e:
        label.config(text=f"Error: {str(e)}")

# Function to open a file
def open_file():
    file_name = "menu.py"
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_folder, file_name)
    
    if os.path.exists(file_path):
        subprocess.Popen(['python3', file_path], close_fds=True)  
        os._exit(0)
    else:
        print(f"El archivo '{file_name}' no existe en la carpeta: {current_folder}")

root = tk.Tk()
root.title("Smart Assistant")
root.geometry("600x370")

button = tk.Button(root, text="⚙️", command=open_file)
button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=20)

label = tk.Label(root, text="Escribe un comando o di algo")
label.pack(pady=20)

entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, width=30)
entry.pack(side=tk.LEFT, padx=10)

button_voice = tk.Button(entry_frame, text="🎙️", command=listen_for_voice_command)
button_voice.pack(side=tk.LEFT, padx=5)


button_frame = tk.Frame(root)
button_frame.pack(pady=10)

button_open_notepad = tk.Button(button_frame, text="Chrome", 
    command=lambda: os.system("open -a 'Google Chrome'"))
button_open_notepad.pack(side=tk.LEFT, padx=10)

button_open_chrome = tk.Button(button_frame, text="ChatGPT", 
    command=lambda: os.system("open -a 'ChatGPT'"))
button_open_chrome.pack(side=tk.LEFT, padx=5)

button_open_calculator = tk.Button(button_frame, text="Calculadora", 
    command=lambda: os.system("open -a 'Calculator'"))
button_open_calculator.pack(side=tk.LEFT, padx=5)

button_execute = tk.Button(root, text="Ejecutar", 
    command=lambda: execute_command(entry.get()))
button_execute.pack(pady=10)

root.mainloop()