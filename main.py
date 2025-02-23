import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import requests

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I didn't get that. Can you repeat?")
        return "None"
    return command.lower()

def get_weather(city):
    api_key = "your_openweathermap_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] != 200:
        return "City not found."
    weather = response["weather"][0]["description"]
    temperature = response["main"]["temp"]
    return f"The weather in {city} is {weather} with a temperature of {temperature}°C."

def execute_command(command):
    if 'time' in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {now}")
    elif 'open' in command:
        site = command.replace('open ', '').strip()
        url = f"https://{site}"
        webbrowser.open(url)
        speak(f"Opening {site}")
    elif 'search' in command:
        query = command.replace('search ', '').strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Searching Google for {query}")
    elif 'weather' in command:
        city = command.replace('weather in ', '').strip()
        weather_info = get_weather(city)
        speak(weather_info)
    elif 'shutdown' in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif 'restart' in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif 'exit' in command or 'quit' in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I don't understand that command.")

def run_bot():
    speak("Hello, I am your advanced Python bot. How can I assist you today?")
    while True:
        command = listen_command()
        if command != "None":
            execute_command(command)

run_bot()