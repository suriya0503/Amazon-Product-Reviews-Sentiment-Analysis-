from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from selenium import webdriver
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import time
import pyttsx3
import speech_recognition as sr
#from selenium.webdriver.chrome.options import Options
driver=webdriver.Chrome('/home/sreeraj/Downloads/chromedriver')
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
MONTHS=["january","february","march","april","may","june","july","august","september","october","october","november","december"]
DAY_EXTENSIONS=["rd","th","st","nd"]

def speak(text):
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source)
        said=""

        try:
            said=r.recognize_google(audio)
            print(said)
            if(said=='August 15'):speak('happy independence day')

        except Exception as e:
           print("Exception"+str(e))
    return said

#authenticating google account
def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(n,service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
import datetime
def get_date(text):
    text=text.lower()
    today=datetime.date.today()

    if text.count("today") > 0:
        return today
    day=-1
    day_of_week=-1
    month=-1
    year=today.year

    for word in text.split():
        if word in MONTHS:
            month=MONTHS.index(word)+1
        elif word in DAYS:
            day_of_week=DAYS.index(word)
        elif word.isdigit():
            day=int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found=word.find(ext)
                if found>0:
                    try:day=int(word[:found])    
                    except:pass

    if month<today.month and month!=-1:
        year=year+1
    if day<today.day and month==-1 and day!=-1:
        month=month+1
    if month==-1 and day==-1 and day_of_week !=-1:
        current_day_of_week=today.weekday()
        dif=day_of_week-current_day_of_week
        if dif<0:
            dif+=7
            if text.count("next")>=1:
                dif+=7
        return today+datetime.timedelta(dif)
    return datetime.date(month=month,day=day,year=year)

def gmeetjoiner(text):
    print(text)
    driver.get('https://www.geeksforgeeks.com')
#text=get_audio().lower()
text=input()
if 'join' in text:
    gmeetjoiner(text)
print(get_date(text))