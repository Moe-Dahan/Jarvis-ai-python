import pyaudio
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import subprocess
import os
import requests
from bs4 import BeautifulSoup
from numpy import nan, printoptions
import yahoo_fin.stock_info as si
import pandas as pd


#set pyttsx3 to init
engine = pyttsx3.init()
#Set jarvis speaking to you set the "voices[1].id" to have a females voice
def speak(audio):
    engine.setProperty('rate', 170)  # setting up new voice rate you can adjust i find 170 most human like
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[0].id)  # changing index, changes voices. 1 for female 0 for male
    volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume', 1.0)  # setting up volume level  between 0 and 1
    engine.say(audio)
    engine.runAndWait()
#search the internet for websites that you like
def internet_commands():
    spoken = f'{understand}'.replace('open '.lstrip(), '')
    if " " in understand:
        speak(f'ok opening {spoken} now')
        '''i got .com.au as im in australia you can go ahead and swap it with your country extension for your
        homeland sites, most sites like facebook redirect straight to .com even with the extension on the end '''
        webbrowser.open(f'www.{spoken}.com.au'.lstrip())
#added google search still needs a bit of cleaning but works good
def search():
    if " " in understand:
        headers = {'User-Agent': 'google my user-agent and put browser here eg: Mozilla/etc'}
        url = requests.get(f'https://www.google.com/search?q={understand}', headers=headers)
        soup = BeautifulSoup(url.content, 'html.parser')
        name = soup.find("div", {'class': "ifM9O"})
        speak("searching web now for your answers")
        speak(name)
#tells you the time and date
def time_date():
    time = datetime.datetime.now().strftime("%I %M %p")
    date = datetime.date.today().strftime("%A %d %m %y")
    if 'time' in understand:
        speak("the time today is {0}".format(time))
    if 'date' in understand:
        speak('the date today is {0}'.format(date))
#opens applications that are installed on your PC
def applications():
    if 'spotify' in understand:
        subprocess.call('Change to your C drive')
        #example
    if 'notepad' in understand:
        subprocess.call('C:\\Windows\\Notepad.exe')
    if 'pycharm' in understand:
        subprocess.call('Change to your C drive')
#Media asking jarvis to tell you what is in the playlist and play movie
def entertain():
    if 'movies' in understand:
        movies = os.listdir('C:\\Users\\yourUser\\Videos\\movies')
        for movie in movies:
             speak(movie.replace('.mp4', ''.lstrip()))
    if 'tv' in understand:
        tv = os.listdir('C:\\Users\\yourUser\\Videos\\tv shows')
        for show in tv:
             speak(show.replace('.mp4', ''.lstrip()))
#under Valued stock valuation starts here
def under_valued():
    user_choice = f'{understand}'.replace('check '.lstrip(), '')
    pay_to_earn = si.get_quote_table(user_choice)
    pull_pay_to_earn = pay_to_earn["PE Ratio (TTM)"]
    if pull_pay_to_earn in pay_to_earn:
        speak(f'The pay to Earn Ratio for {user_choice} is {pull_pay_to_earn}')
        if pay_to_earn not in pull_pay_to_earn:
            val = si.get_stats_valuation(user_choice)
            val = val.iloc[:,:2]
            val.columns = ["Attribute", "Recent"]
            pulled_pay = float(val[val.Attribute.str.contains("Trailing P/E")].iloc[0,1])
            speak(f'[+] The pay to Earn Ratio for {user_choice} is {pulled_pay}')
    else:
        speak(f'The P/E ratio for {user_choice} is unavailable')
    val = si.get_stats_valuation(user_choice)
    val = val.iloc[:,:2]
    val.columns = ["Attribute", "Recent"]
    price_to_sale = float(val[val.Attribute.str.contains("Price/Sales")].iloc[0,1])
    speak(f'The Price to Sale for stock {user_choice} is {price_to_sale}')
    print(f'The Price to Sale for stock {user_choice} is {price_to_sale}')
    see = float(val[val.Attribute.str.contains("Price/Book")].iloc[0,1])
    speak(f'The Price to book for {user_choice} is {see}')
    print(f'The Price to book for {user_choice} is {see}')
    live_price = si.get_live_price(user_choice)
    speak(f'This is the live price for {user_choice} {live_price}')
    print(f'This is the live price for {user_choice} {live_price}')
#get the top gainers
def gainers_lossers():
    if 'win' in understand:
        gainers = si.get_day_gainers()
        #speak(f'These are the top gainers of today {gainers}')
        print(f'These are the top gainers of today {gainers}')
    elif 'loss' in understand:
        lossers = si.get_day_losers()
        #speak(f'These are the top lossers of the day {lossers}')
        print(f'These are the top lossers of the day {lossers}')
#from here jarvis will take all your commands and turn them into text
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("waiting......")
        r.adjust_for_ambient_noise(source, 1)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
        audio = r.listen(source)
    try:
        print("Recognizing...")
        understand = r.recognize_google(audio)
        print(f"User said: {understand}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return understand
#main jarvis loop
while True:
    understand = take_command().lower()
    #Opens webbrowser windows like facebook, ebay etc.... just say 'open' plus the site you like eg open facebook 
    if 'open' in understand:
        internet_commands()
        #tells you the time or date just say tell me the 'time' or 'data'
    if 'tell' in understand:
        time_date()
        # Opens up programs installed on your PC just say start program name
    if 'start' in understand:
        applications()
        '''Tells you your Playlist in movies and TV Shows Movies and TVshows must be stored 
        in your videos folder under seperate folders named movies and tv shows'''
    if 'playlist' in understand:
        entertain()
        # searches the Google and gives you the first search result answers inside of Google Search if available
    if 'search' in understand:
        search()
    if 'check' in understand:
        under_valued()
    if 'who' in understand:
        gainers_lossers()