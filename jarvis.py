import pyttsx3 # used to convert text to speech : pip install pyttsx3
import datetime # to get date and time
import speech_recognition as sr # pip install SpeechRecognition
import wikipedia # to search on wikipedia : pip install wikipedia
import webbrowser # to open any website
import smtplib #to send email : pip install smtplib
import pyautogui # to take screenshots : pip install pyautogui
import psutil # for CPU usage and Battery updates : pip install psutil
import pyjokes # pip install pyjokes
from GoogleNews import GoogleNews # pip install GoogleNews
import random
import os

engine = pyttsx3.init('sapi5') #windows driver for audio 

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%H:%M:%S") 
    #%I - hours with zero padded decimal number (12 hour clock)
    #%M - minute with zero padded decimal number
    #%S - seconds with zero padded decimal number
    return Time

def date():
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    date = str(datetime.datetime.now().day)
    speak("Today's date is:"+ date +"/" + month +"/"+ year)   

def wishme():
    hour  = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18 :
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Jarvis, your assistant")
    speak("How can I help you?")

def takeCommand():
    #it takes microphone input from the user and returns str output
    r = sr.Recognizer()
    with sr.Microphone() as source: # making use of the microphone
        print("Listening...")
        r.pause_threshold = 1 # wait for  1 sec  and then listen to audio
        audio = r.listen(source)
        
        try:
            print("Recogninsing...")
            query = r.recognize_google(audio, language='en-in') # speech recognision using Google Speech Recognision API
            print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            speak("Please say that again, I didn't get that")
            return "None"

        return query

def sendEmail(to,content):
    From = "pqr@abc.com"
    password ="abcdef"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(From,password)
    server.sendmail(From,to,content)
    server.close()

def screenshot():
    image = pyautogui.screenshot()
    image.save("C:\\Users\\Hitesh\\Desktop\\Jarvis\\ss.jpg")

def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at " + usage)
    battery = psutil.sensors_battery()
    speak("Battery is at ")
    speak(battery.percent)

def joke():
    speak(pyjokes.get_joke())

def news():
    speak("What kind of news would you like to hear ?")
    type = takeCommand()
    googleNews = GoogleNews()
    googleNews = GoogleNews(lang = 'en')
    googleNews.search(type) # will search the kind we want to hear
    googleNews.getpage(1) # page number of news 
    googleNews.result()
    list = googleNews.gettext()
    #print(list)
    if len(list) > 0:
       speak(random.choice(list))
    else:
       speak("No news related to this topic.") 

if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()

        #logic for executing tasks based on query
        if 'wikipedia' in query:
            query = query.replace('wikipedia','')
            results = wikipedia.summary(query,sentences =  2)
            speak("According to wikipedia")
            speak(results)

        elif 'open youtube' in query:
            chromePath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
            webbrowser.get(chromePath).open_new_tab("youtube.com")

        elif 'open google' in query:
            chromePath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
            webbrowser.get(chromePath).open_new_tab("google.com")

        elif 'time' in query:
            speak("Currently the time is :" + time() )

        elif 'date' in query:
            date()

        elif 'email to hitesh' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "abcd@xyz.com"
                sendEmail(to,content)
                speak('Email has been sent successfully!')
            except Exception as e:
                print(e)
                speak('Sorry! I am not able to send this mail.')

        elif 'search in chrome' in query:
            speak("What should I search?")
            chromePath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
            search = takeCommand().lower()
            webbrowser.get(chromePath).open_new_tab(search)   

        elif 'remember something for me' in query:
            speak("What should I remember")
            data = takeCommand()
            speak("You told me to remember that "+ data)
            remember = open("data.txt","w")
            remember.write(data)
            remember.close()

        elif 'do you remember anything' in query :
            remeber = open('data.txt','r')
            speak('You told me to remember that ' + remeber.read())

        elif 'screenshot' in query:
            screenshot()
            speak("Screenshot successfully taken.")

        elif 'cpu' in query or 'battery' in query:
            cpu()

        elif 'joke' in query:
            joke()

        elif 'news' in query:
            news()

        elif 'logout' in query:
            os.system("shutdown -l")

        elif 'shutdown' in query: # shutsdown without saving any changed unsaved files
            os.system("shutdown /s /t l")

        elif 'restart' in query:
            os.system("shutdown /r /t l") 

        elif 'offline' in query:
            speak('See you later, bye!')
            quit()