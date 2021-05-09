import pyttsx3 
import datetime
import random
import speech_recognition as sr
import smtplib
import pyaudio
import pyautogui
import webbrowser as wb
from time import sleep
from email.message import EmailMessage
from settings import sendermail, senderpassword, to, emailtext

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id) 
    
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommandMic():
    mic = sr.Microphone(device_index=1)
    r = sr.Recognizer()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
        said = ""
    try:
       said = r.recognize_google(audio)
       print("you said: " + said)
    except sr.UnknownValueError:
        print("i did not understand that")
    except sr.RequestError as e:
        print("Request error; {0}".format(e))
    return said


def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        tgreeting = [" good morning sir "]
    elif hour == 12 and hour < 18:
        tgreeting = [" good afternoon sir "]
    elif hour <=18 and hour == 23:
        tgreeting = [" good evening sir "]
    else:
        tgreeting = [" i see you are working late into the night again ", " burning the midnight oil again I see ",
                    " i couldn't sleep either sir "] 
    speak("I am haaro ")
    speak(random.choice(tgreeting))
    speak("how may I help you")
    

def time():
    time = datetime.datetime.now().strftime("%I %M %p")
    miltime = datetime.datetime.now().strftime("%H %M")
    speak("The time is " + time)
    speak("or " + miltime + " if you perfer")

    
def date():
    date = datetime.datetime.now().strftime("%A, %B, %d, %Y")
    speak("Today is " + date)
    
    
def sendEmail():
    email_list = {
        'Steve':'steve@sawatson.net', 'Adam':'steve@sawatson.net'
    }
    try:
        speak('who do you want to send the email to?')
        name = str(takeCommandMic())
        reciever = email_list[name]
        speak('what wouold you like the subject of the email to be')
        subject = str(takeCommandMic())   
        speak("what would you like the email to say")
        content = str(takeCommandMic())
        speak("would you like me to read back the message")
        answer = str(takeCommandMic())
        if "yes" in answer:
            speak(content)
            speak("are you happy with the contents on the email and would like me to send it?")
            answer = str(takeCommandMic())
            if "yes" in answer:
                trysendemail(reciever, subject, content)
            else:
                speak("would you like to rerecord your message?")
                answer = str(takeCommandMic())
                if "yes" in answer:
                    sendEmail()
                else:
                    speak("I'll be here if you need me")
        else:
            speak("would you like to try this again?")
            answer = str(takeCommandMic())
            if "yes" in answer:
                sendEmail()
            else:
                speak("that's fine")
    except Exception as e:
        print(e)
        speak("unable to send email")
    
    
def trysendemail(reciever, subject, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sendermail, senderpassword)
        email = EmailMessage()
        email['From'] = sendermail
        email['To'] = reciever
        email['Subject'] = subject
        email.set_content(content)
        server.send_message(email)
        server.close()
        speak("your email has been sent")
    except Exception as e:
        speak('something went wong witht the email')
        speak("would you like me me to display the error?")
        answer = str(takeCommandMic())
        if "yes" in answer:
            print(e)
        else:
            speak("that's ok")
        
        
def firstrun():
    initial = 0
    hour = datetime.datetime.now().hour
    print (hour)
    while initial == 0:
        if hour >= 6 and hour < 12:
            tgreeting = ["good morning sir"]
        elif hour >= 12 and hour < 18:
            tgreeting = ["good afternoon sir"]
        elif hour >= 18 and hour < 24:
            tgreeting = ["good evening sir "]
        else:
            tgreeting = ["i see you are working late into the night again", "burning the midnight oil again I see",
                    "i couldn't sleep either sir"] 
        speak("I am haaro ")
        speak(random.choice(tgreeting))
        speak("would you like me to tell you the forcast for today?")
        initial = initial + 1


def sendwhatsmsg(phone_no, message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(10)
    pyautogui.press('enter')
    
if __name__ =="__main__":
    firstrun()
    while True:
        query = str(takeCommandMic())
        if "time"  in query:
            time()
        elif "date" in query:
           date()
        elif "email" in query:
           sendEmail()     
        elif 'message' in query:
            user_name= {'Haro':'3523217980'}
            try:
                speak("who do you want to send the message to?")
                name = str(takeCommandMic())
                phone_no = user_name[name]
                speak("what should I send?")
                message=str(takeCommandMic())
                sendwhatsmsg(phone_no, message)
                speak("message has been sent")
            except Exception as e:
                print(e)
                speak("unable to send message")
        elif "exit program" in query:
            listening = False
            print ("Exiting program")
            exit()