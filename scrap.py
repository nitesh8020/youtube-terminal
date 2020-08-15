from bs4 import BeautifulSoup
import requests
import pafy
import pyglet
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import io

headers= {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

def get_lyrics(title):
    title.replace(' ','+')
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options,executable_path=r'/home/nitesh/chromedriver')
    link = "https://google.com/search?q=" + title
    driver.get(link)
    elem = driver.find_element_by_xpath("//*")
    content = elem.get_attribute("innerHTML")
    
    content = BeautifulSoup(content, "lxml")

    text = content.find_all('span',attrs={'jsname':'YS01Ge'})
        
    lyrics = ""
    for span in text:   
        lyrics = lyrics + span.text + '\n'
    
    driver.close()

    return lyrics


def get_yt_link(title):
    title.replace(' ','+')
    link = "https://www.youtube.com/results?search_query=" + title
    response = requests.get(link, headers = headers, timeout = 10)
    content = BeautifulSoup(response.content, "html.parser")
    
    vid_link=[]
    for i in range(20):
        vid = content.findAll('a',attrs={'class':'yt-uix-tile-link'})[i]
        vid_link.append(vid)
        
    for l in vid_link:
        video = 'https://www.youtube.com' + l['href']
        title = l['title']
        print("Do you want to download the video with title \n",title)
        c = input("Enter Y/N")
        if(c == 'Y' or c == 'y'):
            return video
        else:
            continue
    print("\n No song Selected thus playing default song\n ")
    return vid_link[0]

def menu():
    print("Select one of following choice")
    print("1. Download song and play it")
    print("2. Play song online ")
    ch = int(input("Enter your choice 1 or 2"))
    title = input("Enter song title ")
    return ch,title


def play(audio,length):
    try:
        os.remove('music.m4a')
    except:
        pass
    audio.download('music.m4a' , quiet = True)
    
    player= pyglet.media.Player()
    music = pyglet.media.load('music.m4a')
    player.queue(music)
    player.play()
    overall = time.time() + length
    try:
        while time.time()<overall:
            player.play()
    
    except KeyboardInterrupt:
        player.pause()
    try:
        os.remove('music.m4a')
    except:
        pass

def player():
    ch,title = menu()
    url = get_yt_link(title)
    video = pafy.new(url) 
    s = video.title
    length = (float)(video.length)
    bestaudio = video.getbestaudio(preftype = "m4a")
    c = input("Do yo wanna get lyrics y/n")
    if(c=='y'):
        print("\n \n Lyrics \n")
        print(get_lyrics(title))
    if(ch == 2):
        play(bestaudio,length)
    else :
        name = s + '.m4a'
        bestaudio.download(name)
        player= pyglet.media.Player()
        music = pyglet.media.load(name)
        player.queue(music)
        player.play()
        overall = time.time() + length
        try:
            while time.time()<overall:
                player.play()
        
        except:
            player.pause()
        
    
player()
