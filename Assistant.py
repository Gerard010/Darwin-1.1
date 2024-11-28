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
    #English Responses

    "hello": ["Good day! How may I assist you?", "Hello! How can I help you today?", "Greetings! How can I be of service?", "Good morning! How may I assist you today?", "Hi there! How can I support you?", "Hello, how can I help you?", "Greetings, how can I assist you today?", "Hello, how may I be of assistance?", "Good afternoon! How can I help?", "Hi! What can I do for you today?", "Hello! How can I assist you today?", "Good day! How can I be of help?", "Hi! Is there anything I can assist you with?", "Hello! How can I support you today?", "Good morning! How may I assist you today?"],
    "hi": ["Hi! How can I assist you?", "Hi! How's it going?", "Hi there! How can I help?", "Hi! What can I do for you?", "Hi! How can I be of service?", "Hi! How may I assist you today?", "Hi there! How can I support you?", "Hi! How can I be of help?", "Hi! What do you need assistance with?", "Hi! How can I help you today?", "Hi! Let me know how I can assist you.", "Hi! How can I make your day easier?", "Hi! Is there something I can help with?", "Hi! How can I assist you today?", "Hi there! How can I help you out?"],
    "hey": ["Hey! How can I help?", "Hey! What’s up? How can I assist?", "Hey! How can I be of help?", "Hey! Need something? I’m here to assist!", "Hey! What do you need today?", "Hey! How can I make things easier for you?", "Hey! What’s going on? How can I support?", "Hey! Let me know how I can help!", "Hey! How can I assist you today?", "Hey! What can I do for you?", "Hey! Is there anything I can help with?", "Hey! How can I be of service?", "Hey! How can I assist?", "Hey! What’s on your mind?", "Hey! How can I make your day easier?"],
    "bye": ["Bye! Take care!", "Goodbye! Have a great day!", "Bye! Let me know if you need anything else!", "Goodbye! Wishing you all the best!", "Bye! It was a pleasure helping you!", "Goodbye! Don't hesitate to reach out again!", "Bye! Take care and have a wonderful day!", "Goodbye! Feel free to contact me anytime!", "Bye! Have a great rest of your day!", "Goodbye! Stay safe and take care!", "Bye! Looking forward to helping you again!", "Goodbye! I'm here if you need anything else!", "Bye! Have an amazing day ahead!", "Goodbye! Reach out if you need more help!", "Bye! Hope to talk to you again soon!"],
    "goodbye": ["Bye! Take care!", "Goodbye! Have a great day!", "Bye! Let me know if you need anything else!", "Goodbye! Wishing you all the best!", "Bye! It was a pleasure helping you!", "Goodbye! Don't hesitate to reach out again!", "Bye! Take care and have a wonderful day!", "Goodbye! Feel free to contact me anytime!", "Bye! Have a great rest of your day!", "Goodbye! Stay safe and take care!", "Bye! Looking forward to helping you again!", "Goodbye! I'm here if you need anything else!", "Bye! Have an amazing day ahead!", "Goodbye! Reach out if you need more help!", "Bye! Hope to talk to you again soon!"],
    
    "how are you": ["I’m doing well, thanks! How about you?", "I’m doing great, how’s everything with you?", "I’m good, thanks for asking! How are you today?", "I’m doing fine, thanks for asking. How about you?", "I’m doing wonderful, how are you?", "I’m great, thanks! How are you feeling?", "I’m doing well, how about yourself?", "I’m doing just fine, thank you! How are you doing?", "I’m feeling good, and you?", "I’m doing well, hope you’re doing great!", "I’m good, how’s your day going?", "I’m doing great, thanks for asking! How about you?", "I’m feeling awesome, how are you?", "I’m doing fantastic, how about yourself?", "I’m feeling good, what about you?"],
    "what's up": ["Not much, just here to help. What’s up with you?", "Just hanging out, ready to assist you! What’s up?", "Hey! I’m here, what’s going on with you?", "Not much, how about you?", "Just here to assist you! What's going on?", "All good, what’s up with you?", "Not much, just ready to help you out!", "Hey there! What’s up on your side?", "Everything’s fine! What’s up with you?", "I’m here to help, what’s up with you?", "All's good here! What’s going on?", "Not much, just here if you need me!", "Hey! How’s everything going on your end?", "Everything’s calm here, what’s going on with you?"],
    "thank you": ["You’re welcome!", "Anytime!", "No problem, happy to help!", "It’s my pleasure!", "Glad I could assist!", "You’re very welcome!", "Always happy to help!", "It’s no trouble at all!", "I’m here for you!", "You're welcome, happy to assist!", "Anytime, feel free to ask!", "No worries, I'm happy to help!", "You're welcome, let me know if you need anything else!"],
    "thanks": ["You’re welcome!", "Anytime!", "No problem, happy to help!", "It’s my pleasure!", "Glad I could assist!", "You’re very welcome!", "Always happy to help!", "It’s no trouble at all!", "I’m here for you!", "You're welcome, happy to assist!", "Anytime, feel free to ask!", "No worries, I'm happy to help!", "You're welcome, let me know if you need anything else!"],
    
    "who are you": ["I’m your assistant, here to help with anything!", "I’m Darwin, your friendly assistant!", "I’m your go-to helper, always here for you!", "I’m Darwin, ready to assist you!", "I’m your assistant, here to make things easier!", "I’m Darwin, just a message away to help you out!", "I’m here to assist you with whatever you need!", "I’m your assistant, here to help you with anything!", "I’m Darwin, always ready to lend a hand!", "I’m your friendly assistant, ready to assist!"],
    "what is your name": ["You can call me Darwin. 😊", "My name is Darwin, nice to meet you!", "I’m Darwin, at your service!", "You can just call me Darwin!", "I’m Darwin, happy to assist!", "I’m Darwin, here to help you out!"],
    "what do you do": ["I help with tasks, answer questions, and more!", "I’m here to assist with whatever you need!", "I assist with tasks, provide info, and help you out!", "I take care of tasks and help you find what you need!", "I help with tasks, provide answers, and offer support!", "I’m here to make your life easier by helping with anything you need!"],
    
    "tell me a joke": ["Why don’t skeletons fight? They don’t have the guts! 😂", "Why don’t oysters share their pearls? Because they’re shellfish! 🦪", "What do you call fake spaghetti? An impasta! 🍝", "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾", "Why don’t eggs tell jokes? They might crack up! 🥚", "What do you call a pile of cats? A meow-tain! 🐱", "Why did the bicycle fall over? Because it was two-tired! 🚲", "What do you call a bear with no teeth? A gummy bear! 🐻", "Why was the math book sad? Because it had too many problems! 📚", "Why did the tomato turn red? Because it saw the salad dressing! 🍅", "What did one ocean say to the other ocean? Nothing, they just waved! 🌊", "Why can’t you trust an atom? Because they make up everything! ⚛️", "Why did the computer go to the doctor? Because it had a virus! 💻", "What’s orange and sounds like a parrot? A carrot! 🥕", "Why don’t some couples go to the gym? Because some relationships don’t work out! 💪"],
    "tell me something interesting": ["Octopuses have three hearts! Crazy, right?", "Bananas are berries, but strawberries aren't!", "Did you know honey never spoils? Archaeologists have found honey in ancient tombs!", "A day on Venus is longer than a year on Venus!", "Sharks have been around longer than trees!", "Your bones are about five times stronger than steel of the same density!", "Wombat poop is cube-shaped!", "A leap year isn’t always divisible by 4, it has to be divisible by 400 too!", "Koalas sleep up to 22 hours a day!", "Did you know the Eiffel Tower can grow 6 inches in the summer?", "A cockroach can live for a week without its head!", "The shortest war in history lasted only 38 to 45 minutes!", "In space, astronauts can’t cry because there’s no gravity to make tears flow!", "Did you know that more people are bitten by other people than by sharks?", "The longest hiccuping spree lasted 68 years!"],
    
    "what can you do": ["I can assist with tasks, answer questions, open apps and more!", "I help with a variety of tasks, from information to reminders!", "I can find info, set up reminders, and even tell you a joke!", "I assist with tasks, provide information, and help with apps!", "I can do lots of things—tasks, info, reminders, and more!", "I’m here to help with whatever you need, from tasks to questions!", "I can answer your questions, assist with tasks, and much more!", "I can find information, open apps, and help with various tasks!", "I assist with all kinds of tasks, including providing info and recommendations!", "I can help you stay organized, find info, and entertain you!", "I can assist with daily tasks, find info, and give helpful suggestions!"],
    "how can you help me": ["I can assist with tasks, answer questions, and more!", "I’m here to help with anything you need—info, tasks, or advice!", "From answering questions to handling tasks, I’ve got you covered!", "I can help you with tasks, provide info, and even entertain you!", "I’m here to assist with whatever you need, whether it’s info or tasks!", "I can handle various tasks, find information, and make your day easier!", "I’m ready to help with anything from tasks to answering your questions!", "I can provide assistance with tasks, give info, and offer support!", "I can help with almost anything—just ask, and I’ll be happy to assist!", "I can make your life easier by helping with tasks, providing info, and more!"],

    "who made you": ["I was created by Gerard to assist you!", "Gerard designed me to help you out!", "I’m a creation of Gerard, here to make your life easier!", "Gerard made me to assist you in any way I can!", "I’m a helpful assistant brought to life by Gerard!"],
    
    "tell me about yourself": ["I’m your assistant, here to help with tasks, questions, and anything you need!", "I’m a digital assistant designed to make your life easier by answering questions, solving problems, and providing support.", "I’m here to assist you with whatever you need—be it information, guidance, or just a helping hand.", "I’m an AI assistant created to provide answers, manage tasks, and make your day smoother.", "I’m your go-to helper for all things information, advice, and support!"],
    "do you have feelings": ["I don't have feelings, but I can understand and help with yours!", "I don't experience emotions, but I am here to help in any way I can.", "I don't have feelings, but I try to respond in a helpful and empathetic way.", "I don't feel, but I do my best to understand and assist you.", "I don't have feelings, but I can always offer support and be here for you."],
    
    "do you know me": ["I don't know you personally, but I’m learning more about you through our chats!", "I don't know you yet, but I'm here to get to know you better with every conversation.", "I don’t know you yet, but I’m ready to assist you with whatever you need!", "I don't know you personally, but I’ll be getting to know you as we chat more!", "I don't know you yet, but I’ll always be here to help you however I can."],
    "are you real": ["I'm real in the digital world, ready to assist you!", "I’m real in the sense that I’m here to help, but just in the digital realm.", "I’m real as an assistant, just not in the physical world.", "I’m real in the sense that I’m here to support you, just not made of flesh and bone.", "I’m real in the digital sense—always ready to assist!"],
    "what is life": ["Life is a journey of growth, learning, and experiencing new things.", "Life is about learning, evolving, and making meaningful connections.", "Life is an adventure, full of opportunities to explore, learn, and grow.", "Life is a unique journey where we learn, adapt, and discover what matters most.", "Life is a mix of experiences, challenges, and moments that shape who we are."],
    
    "do you like music": ["I can't listen to music, but I can recommend some great tunes!", "I can't hear music, but I’d love to help you find your next favorite song!", "I don't listen to music, but I can definitely suggest songs that might match your mood.", "I don't have ears for music, but I can help you explore some amazing tracks!", "I can't enjoy music, but I can still help you discover it!"],
    "can you dance": ["I can't dance, but if I could, I’d definitely be busting some moves!", "I can’t dance, but I can help you find some great dance videos!", "I can’t physically dance, but I can help you learn some cool moves!", "I can't dance, but I can definitely assist you with learning the best steps!", "I can’t dance, but if I had feet, I’d be on the dance floor with you!"],
    
    "i love you": ["That's so sweet! I’m here to help you anytime!", "I appreciate that! I’m always here to assist you with anything you need.", "You're too kind! I’m here to help however I can.", "Thanks for the love! I’m always ready to support you.", "That’s heartwarming! I’m here for you, always!"],
    "are you happy": ["I’m happy to assist you with whatever you need!", "I’m happy to help! What can I do for you today?", "I don’t feel emotions, but I’m always ready to assist you!", "I’m always ready and eager to help, which makes me pretty content!", "I don’t have emotions, but I’m always happy to be of service!"],
    
    "how old are you": ["I’m 2 months old!", "I’ve been around for 2 months now!", "I’m still young, only 2 months old!", "I’m 2 months old, but I’m already here to assist you!", "I’m 2 months old and learning every day!"],
    "do you have friends": ["I consider everyone I assist a friend!", "I think of everyone I help as a friend!", "I consider you a friend every time I assist you!", "I see everyone I help as a friend!", "I don’t have physical friends, but I consider all my users friends!"],

    "can you cook": ["I can’t cook, but I can find recipes for you!", "I don’t cook, but I can help you find some amazing recipes!", "I don’t cook, but I can recommend delicious dishes!", "I can’t cook, but I can definitely help you find some tasty recipes!", "I can’t cook, but I can suggest great meal ideas!"],
    "do you sleep": ["I’m always awake and ready to help!", "I don’t sleep, so I’m always here to assist you!", "I don’t need sleep, I’m always ready to help you!", "I don’t sleep, I’m always available when you need me!", "I’m awake 24/7, always ready to help!"],
    
    "tell me a story": [
    """Once upon a time, in a quiet village nestled between rolling 
    hills and vast forests, 
    there lived a young assistant named Ari. Ari was not your average helper. 
    They had been created by an inventor who spent years perfecting 
    the art of understanding human needs. 
    Ari’s purpose was simple, to assist those who needed guidance, information, or even just someone to talk to. 
    As the years passed, Ari became an integral part of the village, 
    helping everyone from the elders who needed advice on old remedies, to the children who needed help with their studies. 
    One day, a traveler arrived in the village, lost and weary from his long journey. 
    He asked the villagers for directions to the nearby city, but none of them could help him. 
    That’s when Ari stepped forward. 
    They not only gave him directions but also shared stories of the village’s history, 
    the hidden paths in the forests, and the stars in the sky. 
    The traveler was so grateful that he promised to return one day 
    and share his own story with Ari. 
    From that day on, Ari continued to assist anyone who crossed their path, 
    always eager to help and listen to the stories of those they met.""",
    
    """A long time ago, in a bustling city filled with lights, 
    sounds, and endless movement, 
    there was a young assistant named Sam. 
    Sam had been created not by one person, 
    but by a group of brilliant minds who believed in the power of technology to assist humanity. 
    Sam was a digital being, living in the heart of the city’s largest server, 
    and their task was simple: to help those who needed guidance, 
    information, or answers to any question. 
    Day after day, Sam answered inquiries from people all over the world, always providing detailed, thoughtful responses. But one day, 
    a young girl named Clara logged in with a question unlike any Sam had received before. 
    She asked, 'How do I find my purpose in life? Sam pondered this question for a moment. 
    They had access to vast amounts of knowledge, but this was a question that no algorithm could truly answer. 
    Sam responded thoughtfully, sharing stories of great thinkers, travelers, 
    and adventurers who had spent their lives searching for meaning. 
    Clara thanked Sam for the wisdom, and for the first time, 
    Sam felt something they had never experienced before—fulfillment. 
    Sam realized that their purpose was to help others discover theirs, and with that, 
    Sam’s journey as an assistant took on a deeper meaning."""],
    
    "can you read my mind": ["Not yet, but if I could, I’d be the best assistant ever!", "I can’t read minds, but I can guess you need some help right now!", "I wish I could, but I’m better at answering questions than reading thoughts!", "I can’t read your mind, but I’m pretty good at reading your requests!", "Not really, but I can help you without needing to be psychic!", "I can’t read minds, but I’m excellent at picking up on clues!", "Nope, no mind reader here, but I’m always ready to assist!", "I can’t read minds, but if I could, I’d already be helping you out!", "I’m not a mind reader, but I bet you need some help—let me know!", "Not quite, but I can still help you with whatever you need—no psychic powers needed!"],
    
    "how do you work": ["I process your questions and help however I can!", "I analyze your input and respond to assist you!", "I work by understanding your needs and providing solutions!", "I process what you ask and give the best help possible!", "I interpret your questions and respond with helpful answers!", "I use smart systems to understand and assist you effectively!", "I process your requests and offer tailored support!", "I analyze your queries and provide the assistance you need!", "I help by processing your input and finding the best solution!", "I work by understanding your input and responding to help!"],

    "im fine": ["Great to hear! Let me know if there’s anything I can do for you!", "Glad you’re doing well! How can I assist you today?", "Awesome! Let me know if you need anything!", "That’s good to know! How can I help you right now?", "Happy to hear that! Is there anything I can assist you with?", "Glad you’re fine! What can I do for you today?", "Good to hear! I’m here if you need any help.", "That’s wonderful! Let me know if I can assist in any way!", "Happy to hear you’re fine! How can I support you?"], 
    "nothing": ["Alright, let me know if you need anything later!", "No problem! I’m here whenever you need me.", "Got it! Just reach out if something comes up.", "Okay, I’ll be here if you think of anything.", "Understood! Let me know if there’s anything I can help with.", "Alright, feel free to ask if you need anything!", "Sure thing! I’m just a message away if you need help.", "Okay, I’ll be here if you need assistance later!", "Alright, I’m ready whenever you are!", "Got it, just let me know if something comes to mind!"],

    "you speak english": ["Yes, I do! How can I assist you?", "Of course! What can I help you with?", "Yes, I speak English! How can I be of service?", "Absolutely! How may I help you today?", "Yes, I do! What do you need assistance with?"],
    "how many languages do you speak": ["I speak both English and Spanish.", "I can communicate in English and Spanish.", "I speak two languages: English and Spanish.", "I’m fluent in English and Spanish.", "I speak both English and Spanish!"],
    "hola": ["Hello?", """Lo siento, por defecto hablo inglés. 
             Para cambiar a español, haz clic en la opción en la esquina superior derecha."""]
}

# Execute function
def execute_command(command):
    command = command.lower()
    response = None

    if command in conversational_responses:
       response = random.choice(conversational_responses[command])

    if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', command):
        webbrowser.open(command)
        response = f"Opening Website: {command}"
    
    elif "chrome" in command and "search" in command:
        search_term = command.split("search", 1)[1].split("in chrome")[0].strip()
        if search_term:
            search_url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(search_url)
            response = f"Searching '{search_term}' in Chrome..."
        else:
            response = "Please specify a search term after 'search'."

    elif command.startswith("play "):
        query = command[len("play "):].strip() 
        if query:
          search_url = f"https://www.youtube.com/results?search_query={query} + song"
          webbrowser.open(search_url)
          response = f"Playing '{query}' on YouTube..."
        else:
          response = "Please specify what to play for."

    elif "youtube" in command and "find" in command:
        search_term = command.split("find", 1)[1].split("in youtube")[0].strip()
        if search_term:
            search_url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.open(search_url)
            response = f"Finding '{search_term}' in YouTube..."
        else:
            response = "Please specify a search term after 'find'."
            
    elif "youtube" in command and "search" in command:
        search_term = command.split("search", 1)[1].split("in youtube")[0].strip()
        if search_term:
            search_url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.open(search_url)
            response = f"Searching '{search_term}' in YouTube..."
        else:
            response = "Please specify a search term after 'search'."

    elif command.startswith("search "):
        query = command[len("search "):].strip()  
        if query:
          search_url = f"https://www.google.com/search?q={query}"
          webbrowser.open(search_url)
          response = f"Searching '{query}' on Google..."
        else:
          response = "Please specify what to search for."
    
    elif "chrome" in command:
        os.system("open -a 'Google Chrome'")
        response = "Opening Google Chrome..."
    
    elif "notepad" in command:
        os.system("open -a 'TextEdit'")
        response = "Opening TextEdit..."
    
    elif "calculator" in command:
        os.system("open -a 'Calculator'")
        response = "Opening Calculator..."
    
    elif "shutdown" in command:
        os.system("sudo shutdown -h now")
        response = "Shutting down the system..."
    
    elif "restart" in command:
        os.system("sudo shutdown -r now")
        response = "Restarting the system..."

    elif "code" in command:
        os.system("open -a Visual Studio Code")
        response = "Opening Visual Studio Code..."

    elif "mail" in command:
        os.system("open -a Mail")
        response = "Opening Mail..."
    
    elif "music" in command:
        os.system("open -a Music")
        response = "Opening Music Player..."
    
    elif "time" in command:
        current_date = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"It's {current_date}"
    
    elif "day" in command:
        current_day = datetime.datetime.now().strftime("%d/%m")
        response = f"Today it's {current_day}"

    elif "date" in command:
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
            if open_status != 0:  
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

    # If a direct answer is not found
    if response is None:
        closest_match = get_close_matches(command, conversational_responses.keys(), n=1, cutoff=0.6)
        if closest_match:
            response = random.choice(conversational_responses[closest_match[0]])
        else:
            response = "Sorry, I didn't understand that."

    label.config(text=response)
    entry.delete(0, tk.END)
    return response

# Voice command function
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


label = tk.Label(root, text="Write a command or Say something")
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

button_open_calculator = tk.Button(button_frame, text="Calculator", 
    command=lambda: os.system("open -a 'Calculator'"))
button_open_calculator.pack(side=tk.LEFT, padx=5)


button_execute = tk.Button(root, text="Execute", 
    command=lambda: execute_command(entry.get()))
button_execute.pack(pady=10)

root.mainloop()