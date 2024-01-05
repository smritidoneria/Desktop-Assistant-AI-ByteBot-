import os
import speech_recognition as sr
import webbrowser
import datetime
from openai import OpenAI
from config import apikey
import random
import requests, json
import subprocess
from translate import Translator
import shlex
import pyautogui
import time

chatStr = ""


def say(text):
    try:

        os.system(f'say {shlex.quote(text)}')

    except Exception as e:
        print(f"Error in say function: {e}")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print(sr.Microphone)
        r.pause_threshold = 1
        print("Listening...")

        # print(audio)
        try:
            audio = r.listen(source)
        except sr.UnknownValueError as e:
            print(f"Error: {e}")
        except sr.RequestError as e:
            print(f"Error: {e}")

        try:

            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            #  query=input()
            print(f"User: {query}")
            return query
        except Exception as e:
            print(e)
            print("Sorry, I didn't get that. Can you please repeat?")
            return ""


def translator():
    languages = ['fr', 'it', 'es', 'ru', 'de', 'nl']
    languages_full = ['french', 'italian', 'spanisch', 'russian', 'german', 'dutch']
    say("say the text you want to translate")
    text = takecommand()
    say("In which language do you want to translate your text")

    for language in languages:
        translator = Translator(to_lang=language)
        translation = translator.translate(text)
        say(f'Translation to {languages_full}: {translation}')


def open_app(application_name):
    try:
        subprocess.run(["open", "-a", application_name])
        return f"Opening {application_name}..."
    except Exception as e:
        return f"Error opening {application_name}: {str(e)}"


def check_app_exists(application_name, app_list):
    lower_app_name = application_name.lower()
    lower_app_list = [app.lower() for app in app_list]

    return lower_app_name in lower_app_list


def open_apps():
    app_names = ["Calendar", "Chess", "Clock", "Contacts", "Dictionary", "FaceTime", "Find My", "Font Book", "Freeform",
                 "GarageBand", "Home", "Image Capture", "iMovie", "JetBrains Toolbox", "Keynote", "Launchpad", "Mail",
                 "Maps", "Messages", "Mission Control", "Music", "Notes", "Numbers", "Pages", "Photo Booth", "Photos",
                 "Podcasts", "Postman", "Preview", "PyCharm CE", "QuickTime Player", "Reminders", "Safari", "Shortcuts",
                 "Siri", "Stickies", "Stocks", "System Settings", "TextEdit", "Time Machine", "TV", "Utilities",
                 "Voice Memos", "Weather"]

    say(f"enter the app to open ")
    desired_app_name = takecommand()


    if check_app_exists(desired_app_name, app_names):
        result = open_app(desired_app_name)
        print(result)
    else:
        print(f"{desired_app_name} is not in the list of known applications.")


def shutdown():
    if platform.system.lower() == "darwin":
        subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])


def restart():
    if platform.system().lower() == "darwin":
        subprocess.run(["osascript", "-e", 'tell app "System Events" to restart'])


def adjust_volume(volume_level):
    if platform.system().lower() == "darwin":
        subprocess.run(["osascript", "-e", f'set volume output volume {volume_level}'])


def news():
    api_key = "81dd3376a78c4facb67670830488474b"
    main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=" + api_key
    news1 = requests.get(main_url).json()

    for article in news1['articles']:
        title = article['title']
        description = article['description']
        source_name = article['source']['name']
        author = article['author'] if 'author' in article else None

        # Print or process the extracted information
        say(f'Title: {title}')
        say(f'Description: {description}')
        say(f'Source Name: {source_name}')
        say(f'Author: {author}')


def weather():
    api_key = "d1d77e7561da6e6422487df20d44d34f"
    say("enter the city")
    city_name = input("enter city")
    baseURL = "https://api.openweathermap.org/data/2.5/weather?q="

    complete_URL = baseURL + city_name + "&appid=" + api_key
    response = requests.get(complete_URL)
    data = response.json()
    temp_max = data['main']['temp_max']
    temp_min = data['main']['temp_min']
    say(f"the max temperature in {city_name} is {temp_max}")
    say(f"the min temperature in {city_name} is {temp_min}")


def set_alarm():
    try:
        pyautogui.hotkey('command', 'space')
        time.sleep(10)
        pyautogui.write('Clock')
        pyautogui.press('return')
        time.sleep(20)

        print("Clicking on Alarm section")
        pyautogui.click(x=692, y=95)
        time.sleep(2)

        print("Clicking on plus button")
        pyautogui.click(x=1223, y=96)
        time.sleep(2)

        print("Setting the alarm time")
        pyautogui.click(x=713, y=340)  # Click on the hour setting
        pyautogui.write('8')
        time.sleep(1)
        pyautogui.click(x=762, y=338)  # Click on the minute setting
        pyautogui.write('00')

        pyautogui.press('return')
        print("Alarm set successfully.")
        say("Smriti Alarm set successfully")

    except Exception as e:
        print(f"Error setting alarm: {e}")
        say("Sorry, but can you please try again")


def chat(query):
    global chatStr
    print(chatStr)

    chatStr += f"Smriti: {query}\n AI: "
    client = OpenAI(api_key=apikey)

    response = client.completions.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # todo: Wrap this inside of a  try catch block
    print(response.choices[0].text)
    say(response.choices[0].text)
    chatStr += f"{response.choices[0].text}\n"
    return response.choices[0].text


def ai(prompt):
    text1 = f"Openai response for Prompt: {prompt}"
    client = OpenAI(api_key=apikey)

    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response.choices[0].text)
    text1 += response.choices[0].text
    print(text1)

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    filename = f"Openai/prompt-{random.randint(1, 121212)}"
    print(f"Creating file: {filename}")

    try:
        with open(filename, "w") as f:
            f.write(text1)
        print("File created successfully.")
    except Exception as e:
        print(f"Error creating file: {e}")


if __name__ == '__main__':
    print("Pycharm")
    say("I am my ai")
    while True:
        text = takecommand()
        sites = [["youtube", "https:youtube.com"], ["wikipedia", "https:wikipedia.com"]]
        # say(text)
        for site in sites:
            if f"open {site[0]}".lower() in text.lower():
                say(f"Opining {site[0]} smriti")
                webbrowser.open(site[1])
        if "the time" in text:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f" Smriti the time is {strfTime}")
        elif "open facetime".lower() in text.lower():
            os.system(f"open /System/Applications/FaceTime.app")
        elif "using artificial intelligence".lower() in text.lower():
            ai(prompt=text)
        elif "weather".lower() in text.lower():
            weather()
        elif "news".lower() in text.lower():
            news()
        elif "open app".lower() in text.lower():
            open_apps()
        elif "translate".lower() in text.lower():
            translator()

        elif "set alarm".lower() in text.lower():
            set_alarm()
        elif "shutdown".lower() in text.lower():
            shutdown()
        elif "restart".lower() in text.lower():
            restart()
        elif "volume".lower() in text.lower():
            adjust_volume()
        else:
            chat(text)

'''
import pyautogui
import time


def get_coordinates():
    print("Move the mouse cursor to the desired location...")
    time.sleep(10)  
    x, y = pyautogui.position()
    print(f"Coordinates: x={x}, y={y}")


if __name__ == "__main__":
    get_coordinates()
    '''

