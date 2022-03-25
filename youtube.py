import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia

listener=sr.Recognizer()
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()
def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice=listener.listen(source)
            command=listener.recognize_google(voice)
            #command='alfred play'
            command=command.lower()
            if 'alfred' in command:
                command=command.replace('alfred','')
                print(command)
    except:
        pass
    return command
def run_alfred():
    command=take_command()
    print(command)
    if 'play' in command:
        song=command.replace('play',"")
        talk('playing'+song)
        pywhatkit.playonyt(song)
    else:
        talk('please say the command again')
while True:
    run_alfred()