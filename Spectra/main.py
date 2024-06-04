from __future__ import with_statement
import keyboard
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import pywhatkit as kit
import sys
import pyautogui
import time
import operator
import requests
from googletrans import Translator
import drawing

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
    return query


def get_random_trivia():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    data = response.json()

    if data["response_code"] == 0:
        question = data["results"][0]["question"]
        correct_answer = data["results"][0]["correct_answer"]
        incorrect_answers = data["results"][0]["incorrect_answers"]

        answers = incorrect_answers + [correct_answer]
        answers = "\n".join(answers)

        print(f"Question: {question}\n\n{answers}")
        speak(f"Question: {question}\n\n{answers}")
        time.sleep(10)
        speak(f"The correct answer is: {correct_answer}")
        print(f"The correct answer is: {correct_answer}")
    else:
        print("Sorry, I couldn't retrieve a trivia question at the moment.")
        speak("Sorry, I couldn't retrieve a trivia question at the moment.")


def play_rock_paper_scissors():
    speak("Let's play Rock, Paper, Scissors!")
    speak("Please choose: rock, paper, or scissors.")
    computer_choice = random.choice(['rock', 'paper', 'scissors'])
    user_choice = takeCommand().lower()
    speak(f"You chose {user_choice}.")
    if user_choice == 'rock':
        print(drawing.rock)
    elif user_choice == 'paper':
        print(drawing.paper)
    else:
        print(drawing.scissors)
    speak(f"Computer chose {computer_choice}.")
    if computer_choice == 'rock':
        print(drawing.rock)
    elif computer_choice == 'paper':
        print(drawing.paper)
    else:
        print(drawing.scissors)

    if user_choice == computer_choice:
        speak("It's a tie!")
        print("It's a tie!")
    elif user_choice == 'rock':
        if computer_choice == 'paper':
            speak("Computer wins!")
            print("Computer wins!")
        else:
            speak("You win!")
    elif user_choice == 'paper':
        if computer_choice == 'scissors':
            speak("Computer wins!")
            print("Computer wins!")

        else:
            speak("You win!")
            print("You win!")

    elif user_choice == 'scissors':
        if computer_choice == 'rock':
            speak("Computer wins!")
            print("Computer wins!")
        else:
            speak("You win!")
            print("You win!")


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
        print("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
        print("Good Afternoon")
    else:
        speak("Good Evening!")

    speak("Ready To Comply. What can I do for you ?")


def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'translate' in query:
            speak("What do you want to translate?")
            text_to_translate = takeCommand().lower()
            speak("Which language do you want to translate into?")
            target_language = takeCommand().lower()
            translated_text = translate_text(text_to_translate, target_language)
            speak(f"The translation is here")
            print(f"The translation is: {translated_text}")
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'search on youtube' in query:
            query = query.replace("search on youtube", "")
            webbrowser.open(f"www.youtube.com/results?search_query={query}")
        elif 'open youtube' in query:
            speak("what you will like to watch ?")
            qrry = takeCommand().lower()
            kit.playonyt(f"{qrry}")
        elif 'close chrome' in query:
            os.system("taskkill /f /im chrome.exe")
        elif 'close youtube' in query:
            os.system("taskkill /f /im sedge.exe")
        elif 'open google' in query:
            speak("what should I search ?")
            qry = takeCommand().lower()
            webbrowser.open(f"{qry}")
            results = wikipedia.summary(qry, sentences=2)
            speak(results)
        elif 'close google' in query:
            os.system("taskkill /f /im msedge.exe")
        elif 'play music' in query:
            music_dir = 'E:\Musics'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, random.choice(songs)))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")
        elif "restart the system" in query:
            os.system("shutdown /r /t 5")
        elif "lock the system" in query:
            os.system("rundll32.exe user32.dll, LockWorkStation")
        elif "close notepad" in query:
            os.system("taskkill /f /im notepad.exe")
        elif "open command prompt" in query:
            os.system("start cmd")
        elif "close command prompt" in query:
            os.system("taskkill /f /im cmd.exe")
        elif "go to sleep" in query:
            speak(' alright then, I am switching off')
            sys.exit()
        elif "take screenshot" in query:
            speak('tell me a name for the file')
            name = takeCommand().lower()
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("screenshot saved")
        elif "calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("ready")
                print("Listning...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)


            def get_operator_fn(op):
                return {
                    '+': operator.add,
                    '-': operator.sub,
                    'x': operator.mul,
                    'divided': operator.__truediv__,
                }[op]


            def eval_bianary_expr(op1, oper, op2):
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)


            speak("your result is")
            speak(eval_bianary_expr(*(my_string.split())))
        elif "what is my ip address" in query:
            speak("Checking")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                speak("your ip adress is")
                speak(ipAdd)
            except Exception as e:
                speak("network is weak, please try again some time later")
        elif "volume up" in query:
            for _ in range(5):
                pyautogui.press("volumeup")
        elif "volume down" in query:
            pyautogui.press("volumedown")
        elif "mute" in query:
            pyautogui.press("volumemute")
        elif "refresh" in query:
            pyautogui.moveTo(1551, 551, 2)
            pyautogui.click(x=1551, y=551, clicks=1, interval=0, button='right')
            pyautogui.moveTo(1620, 667, 1)
            pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left')
        elif "scroll down" in query:
            pyautogui.scroll(1000)
        elif "ms" in query:
            pyautogui.hotkey('winleft', 'r')  # Press Win+R to open Run
            time.sleep(0.5)
            pyautogui.typewrite("winword")  # Type "winword" for Word
            pyautogui.press('enter')
        elif 'type' in query:
            query = query.replace("type", "")
            pyautogui.write(f"{query}", 0.5)
        elif 'backspace' in query:
            pyautogui.hotkey('ctrl', 'backspace')
        if 'open chrome' in query:
            os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe')
        elif 'maximize this window' in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('x')
        elif 'google search' in query:
            query = query.replace("google search", "")
            pyautogui.hotkey('alt', 'd')
            pyautogui.write(f"{query}", 0.1)
            pyautogui.press('enter')
        elif 'youtube search' in query:
            query = query.replace("youtube search", "")
            # Press Alt + D to focus on the address bar
            pyautogui.hotkey('alt', 'd')
            time.sleep(1)

            # Press Tab multiple times to navigate to the search bar
            for _ in range(6):  # Adjust the range as needed
                pyautogui.press('tab')
                time.sleep(0.5)

            # Type the search query
            pyautogui.write(query, interval=0.1)
            time.sleep(1)

            # Press Enter to submit the search
            pyautogui.press('enter')

        elif 'open new window' in query:
            pyautogui.hotkey('ctrl', 'n')
        elif 'open incognito window' in query:
            pyautogui.hotkey('ctrl', 'shift', 'n')
        elif 'minimise this window' in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('n')
        elif 'open history' in query:
            pyautogui.hotkey('ctrl', 'h')
        elif 'open downloads' in query:
            pyautogui.hotkey('ctrl', 'j')
        elif 'previous tab' in query:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
        elif 'next tab' in query:
            pyautogui.hotkey('ctrl', 'tab')
        elif 'close tab' in query:
            pyautogui.hotkey('ctrl', 'w')
        elif 'close window' in query:
            pyautogui.hotkey('ctrl', 'shift', 'w')
        elif 'clear history' in query:
            keyboard.press_and_release('ctrl+shift+delete')
            time.sleep(1)
            keyboard.press_and_release('enter')
        elif 'close chrome' in query:
            os.system("taskkill /f /im chrome.exe")
        elif 'games' in query:
            play_rock_paper_scissors()
        elif "trivia" in query:
            get_random_trivia()