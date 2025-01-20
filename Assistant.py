import tkinter as tk
import os
import webbrowser
import datetime
import psutil
import re
import random
import speech_recognition as sr
import subprocess

def process_command_ai(command):
    try:
        result = subprocess.run(
            ["ollama", "run", "llava:13b"],
            input=command,
            text=True,
            capture_output=True
        )
        return result.stdout.strip()
    except Exception:
        return "Error using the IA."

root = tk.Tk()
root.title("DarwinIA")
root.geometry("555x333")

def execute_command(command):
    response = ""
    if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', command):
        webbrowser.open(command)
        response = f"Opening website: {command}"
    elif "chrome" in command and "search" in command:
        search_term = command.split("search", 1)[1].split("in chrome")[0].strip()
        if search_term:
            search_url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(search_url)
            response = f"Searching '{search_term}' on Chrome..."
        else:
            response = "Please specify your search after 'search'."
    elif command.startswith("play "):
        query = command[len("play "):].strip()
        if query:
            search_url = f"https://www.youtube.com/results?search_query={query}+song"
            webbrowser.open(search_url)
            response = f"Playing '{query}' on YouTube..."
        else:
            response = "Please specify the song you want to play."
    elif "youtube" in command and "find" in command:
        search_term = command.split("find", 1)[1].split("on youtube")[0].strip()
        if search_term:
            search_url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.open(search_url)
            response = f"Finding '{search_term}' on YouTube..."
        else:
            response = "Please specify your search after 'find'."
    elif "youtube" in command and "search" in command:
        search_term = command.split("search", 1)[1].split("on youtube")[0].strip()
        if search_term:
            search_url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.open(search_url)
            response = f"Searching '{search_term}' on YouTube..."
        else:
            response = "Please specify your search after 'search'."
    elif command.startswith("search "):
        query = command[len("search "):].strip()
        if query:
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
            response = f"Searching '{query}' on Google..."
        else:
            response = "Please specify what you want to search."
    elif "chrome" in command:
        os.system("open -a 'Google Chrome'")
        response = "Opening Google Chrome..."
    elif "text editor" in command:
        os.system("open -a 'TextEdit'")
        response = "Opening the text editor..."
    elif "calculator" in command:
        os.system("open -a 'Calculator'")
        response = "Opening the calculator..."
    elif "shutdown" in command:
        os.system("sudo shutdown -h now")
        response = "Shutting down the system..."
    elif "restart" in command:
        os.system("sudo shutdown -r now")
        response = "Restarting the system..."
    elif "cod" in command:
        os.system("open -a 'Visual Studio Code'")
        response = "Opening Visual Studio Code..."
    elif "mail" in command:
        os.system("open -a Mail")
        response = "Opening the email client..."
    elif "music" in command:
        os.system("open -a Music")
        response = "Opening the Music player..."
    elif "time" in command:
        current_date = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"It is {current_date}"
    elif "day" in command:
        current_day = datetime.datetime.now().strftime("%d/%m")
        response = f"Today is {current_day}"
    elif "date" in command:
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        response = f"The date is: {date}"
    elif "cpu" in command:
        cpu_usage = psutil.cpu_percent(interval=1)
        response = f"CPU usage: {cpu_usage}%"
    elif "memory" in command:
        memory = psutil.virtual_memory()
        response = f"Memory usage: {memory.percent}%"
    elif "battery" in command:
        battery = psutil.sensors_battery()
        response = f"Battery: {battery.percent}%" if battery else "Battery status is not available."
    elif "wifi" in command:
        wifi_status = os.popen("networksetup -getairportpower en0").read()
        response = "Wi-Fi is connected" if "On" in wifi_status else "Wi-Fi is not connected"
    elif "open" in command:
        app_name = command.split("open", 1)[1].strip()
        if app_name:
            open_status = os.system(f"open -a '{app_name}'")
            if open_status != 0:
                search_url = f"https://www.google.com/search?q={app_name}"
                webbrowser.open(search_url)
                response = f"Could not open '{app_name}'. Searching '{app_name}' on Google..."
            else:
                response = f"Opening {app_name}..."
        else:
            response = "Please specify the name of the application."
    elif "clear" in command:
        entry.delete(0, tk.END)
        response = "Enter a new command."
    else:
        # Usa la IA si no se reconoce el comando
        response = process_command_ai(command)

    label.config(text=response)
    entry.delete(0, tk.END)
    return response

def listen_for_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        label.config(text="Listening...")
        root.update()
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="en-US")
        entry.delete(0, tk.END)
        entry.insert(0, command)
        response = execute_command(command)
        label.config(text=response)
    except:
        label.config(text="Error")

label = tk.Label(root, text="Write a command")
label.pack(pady=20)

entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, width=30)
entry.pack(side=tk.LEFT, padx=10)

button_voice = tk.Button(entry_frame, text="🎙️", command=listen_for_voice_command)
button_voice.pack(side=tk.LEFT, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

button_chrome = tk.Button(button_frame, text="Chrome",
                          command=lambda: os.system("open -a 'Google Chrome'"))
button_chrome.pack(side=tk.LEFT, padx=10)

button_calculator = tk.Button(button_frame, text="Calculator",
                              command=lambda: os.system("open -a 'Calculator'"))
button_calculator.pack(side=tk.LEFT, padx=5)

button_calculator = tk.Button(button_frame, text="ChatGPT",
                              command=lambda: os.system("open -a 'ChatGPT'"))
button_calculator.pack(side=tk.LEFT, padx=0)

button_execute = tk.Button(root, text="Execute",
                           command=lambda: execute_command(entry.get()))
button_execute.pack(pady=10)

root.mainloop()