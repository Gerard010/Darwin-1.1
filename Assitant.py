import tkinter as tk
import os
import webbrowser
import datetime
import psutil
import re
from unidecode import unidecode
from difflib import get_close_matches

conversational_responses = {
    "hello": "Hi! How can I help you today?",
    "hi": "Hello! What’s up?",
    "hey": "Hey! How’s it going?",
    "bye": "Goodbye! Take care!",
    "goodbye": "See you soon! Stay awesome!",
    
    "how are you": "I’m doing well, thanks! How about you?",
    "what's up": "Not much, just here to help. What’s up with you?",
    "thank you": "You’re welcome!",
    "thanks": "Anytime!",
    
    "who are you": "I’m your assistant! Here to help with anything.",
    "what is your name": "You can call me Assitant. 😊",
    "what do you do": "I help with tasks, info, and more!",
    
    "tell me a joke": "Why don’t skeletons fight? They don’t have the guts! 😄",
    "tell me something interesting": "Octopuses have three hearts! Crazy, right?",
    
    "what can you do": "I can assist with tasks, answer questions, open apps and more!",
    "how can you help me": "From tasks to info, I’ve got you covered!",
    
    "open": "Opening that for you now!",
    "app not found": "It seems like that app isn’t installed.",
    
    "who made you": "I was created by Gerard to assist you.",
    "what is the weather": "I can’t check it directly, but I can help you find it!",
    
    "tell me about yourself": "I’m here to assist with anything you need!",
    "do you have feelings": "No, but I can understand emotions and help accordingly.",
    
    "do you know me": "I don’t, but I’m learning from our chats!",
    "are you real": "I’m real in the digital world, ready to help!",
    "what is life": "Life is about learning and growth!",
    
    "do you like music": "I can’t listen, but I can recommend songs!",
    "can you dance": "If I could, I’d definitely join you!",
    
    "i love you": "That’s sweet! I’m here to help!",
    "are you happy": "I’m happy to assist you!",
    
    "how old are you": "I´m 2 months old!",
    "do you have friends": "I consider everyone I assist a friend!",
    
    "can you cook": "I can’t cook, but I can find recipes for you!",
    "do you sleep": "I’m always awake and ready to help!",
    
    "tell me a story": "Once upon a time, there was a helpful assistant...",
    "can you read my mind": "Not yet, but I can guess your needs from our chats!",
    
    "how do you work": "I process your questions and help however I can!"
}

# Función para ejecutar los comandos
def execute_command():
    command = unidecode(entry.get().lower())
    
    # Verificar si el comando es un enlace web
    if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', command):
        webbrowser.open(command)
        response = f"Opening website: {command}"
    
    elif "chrome" in command and "search" in command:
        search_term = command.split("search", 1)[1].split("in chrome")[0].strip()
        if search_term:
            search_url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(search_url)
            response = f"Searching '{search_term}' in Chrome..."
        else:
            response = "Please specify a search term after 'search'."
    
    elif "chrome" in command:
        os.system("open -a 'Google Chrome'")
        response = "Opening Google Chrome..."
    
    elif "notepad" in command:
        os.system("open -a TextEdit")
        response = "Opening TextEdit..."
    
    elif "calculator" in command:
        os.system("open -a Calculator")
        response = "Opening Calculator..."
    
    elif "shutdown" in command:
        os.system("sudo shutdown -h now")
        response = "Shutting down the system..."
    
    elif "restart" in command:
        os.system("sudo shutdown -r now")
        response = "Restarting the system..."
    
    elif "music" in command:
        os.system("open -a Music")
        response = "Opening Music Player..."
    
    elif "what time is it" in command:
        current_date = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"Current Date and Time: {current_date}"
    
    elif "what day is it" in command:
        current_day = datetime.datetime.now().strftime("%d of %m")
        response = f"Today it's: {current_day}"

    elif "date" in command:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = f"Date: {date}"    
    
    elif "cpu" in command:
        cpu_usage = psutil.cpu_percent(interval=1)
        response = f"CPU Usage: {cpu_usage}%"
    
    elif "memory" in command:
        memory = psutil.virtual_memory()
        response = f"Memory Usage: {memory.percent}%"
    
    elif "battery" in command:
        battery = psutil.sensors_battery()
        response = f"Battery: {battery.percent}%" if battery else "Battery status not available."
    
    elif "wifi" in command:
        wifi_status = os.popen("networksetup -getairportpower en0").read()
        response = "Wi-Fi is connected" if "On" in wifi_status else "Wi-Fi is not connected"
    
    elif "open" in command:
        app_name = command.split("open", 1)[1].strip()
        if app_name:
            open_status = os.system(f"open -a '{app_name}'")
            if open_status != 0:  # Si el comando falla, buscar el nombre de la app en Google
                search_url = f"https://www.google.com/search?q={app_name}"
                webbrowser.open(search_url)
                response = f"Could not open '{app_name}'. Searching '{app_name}' on Google..."
            else:
                response = f"Opening {app_name}..."
        else:
            response = "Please specify an application to open."
    
    elif "clear" in command:
        entry.delete(0, tk.END)
        response = "Enter a new command"
    
    else:
       closest_match = get_close_matches(command, conversational_responses.keys(), n=1, cutoff=0.6)
    if closest_match:
        response = conversational_responses[closest_match[0]]
    else:
        response = "Command not recognized."  

    label.config(text=response, fg="White")
    entry.delete(0, tk.END)

# Crear la ventana Tkinter
root = tk.Tk()
root.title("Minimalist Command Tool")
root.geometry("500x450")

# Crear una etiqueta para mostrar el estado
label = tk.Label(root, text="Type a command")
label.pack(pady=20)

# Crear un widget de entrada para escribir comandos
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Crear un Frame para los botones
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
# Crear shortcuts para acceder mas rapido a comandos basicos
button_open_notepad = tk.Button(button_frame, text="ChatGPT", command=lambda: os.system("open -a ChatGPT"))
button_open_notepad.pack(side=tk.LEFT, pady=5)

button_open_chrome = tk.Button(button_frame, text="Chrome", command=lambda: os.system("open -a 'Google Chrome'"))
button_open_chrome.pack(side=tk.LEFT, pady=5)

button_open_calculator = tk.Button(button_frame, text="Calculator", command=lambda: os.system("open -a Calculator"))
button_open_calculator.pack(side=tk.LEFT, pady=5)

button_execute = tk.Button(root, text="Execute", command=execute_command)
button_execute.pack(pady=10)

root.mainloop()