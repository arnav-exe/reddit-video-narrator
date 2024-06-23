import requests
from modifiedcipher import decrypt
import praw

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import pyscreenshot
import cv2
import numpy as np

import os
import time

from gtts import gTTS

from moviepy.editor import *

from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import http.client
import socket



f1 = open("cred.txt", "r")

client_id = decrypt(f1.readline().rstrip())
client_secret = decrypt(f1.readline().rstrip())
username = decrypt(f1.readline().rstrip())
password = decrypt(f1.readline().rstrip())
f1.close()

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
data = {
    'grant_type' : 'password',
    'username' : username,
    'password' : password
}

headers = {'User-Agent' : 'MyAPI/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
token = res.json()['access_token']
headers['Authorization'] = f'bearer {token}'

print(requests.get('https://oath.reddit.com/api/v1/me', headers=headers)) #response [200] here equals good ✓



#----------PRAW----------#

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=headers,
    username=username
)

num_lines = sum(1 for line in open('URLS.txt'))

loop1 = 0
while loop1 < num_lines and loop1 < 6:
    with open('URLS.txt', 'r+') as f2:
        url = f2.readline().rstrip()
        data = f2.read().splitlines(True)

    with open('URLS.txt', 'w') as f2:
        f2.writelines(data[0:])
    f2.close()

    post = reddit.submission(url=url)

    comments_list1 = []
    comments_list2 = []

    for top_level_comment in post.comments[:6]: #number inside square brackets denotes how many comments to get. will be taking 3 extra comments as backups
        comments_list1.append(top_level_comment.body)
        comments_list2.append(top_level_comment.body)

    count = 0
    while count < len(comments_list1):
        comments_list1[count] = comments_list1[count].replace("*", "").replace("#", "").replace("^", "")
        comments_list2[count] = comments_list2[count].replace("*", "").replace("#", "").replace("^", "").replace("\n\n", ".\n")
        head, sep, tail = comments_list1[count].partition("\n")
        comments_list1[count] = head.lstrip().rstrip()[1:-1]
        count += 1



    #----------pyscreenshot----------#
    #getting screenshot of post title
    subreddit = str(post.subreddit)
    title = post.title

    if len(title) > 42*7:
        y2 = 435

    elif len(title) > 42*6:
        y2 = 435-19

    elif len(title) > 42*5:
        y2 = 435-19-19

    elif len(title) > 42*4:
        y2 = 435-19-19-19

    elif len(title) > 42*3:
        y2 = 435-19-19-19-19

    elif len(title) > 42*2:
        y2 = 435-19-19-19-19-19

    elif len(title) > 42:
        y2 = 435-19-19-19-19-19-19

    else: #base condition (for when post title is 1 line long)
        y2 = 435-19-19-19-19-19-19-19



    #----------SELENIUM----------#

    path = str(os.getcwd()) + "\chromedriver.exe"

    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    options.add_extension("abp.crx") #adding adblockplus extension

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(path, options=options)

    driver.get("chrome://extensions/?id=cfhdojbkjhnklbpkdaibdccddilifddb") #ALLOWS EXTENSION TO RUN IN INCOGNITO
    driver.execute_script("return document.querySelector('extensions-manager').shadowRoot.querySelector('#viewManager > extensions-detail-view.active').shadowRoot.querySelector('div#container.page-container > div.page-content > div#options-section extensions-toggle-row#allow-incognito').shadowRoot.querySelector('label#label input').click()");

    driver.get(url)

    time.sleep(1)

    img = pyscreenshot.grab(bbox=(740, 199, 1480, y2)) #X1, Y1, X2, Y2
    img.save(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\imgs\vid{}\title.png".format(loop1+1))

    body = driver.find_element_by_css_selector('body')
    for i in range(10):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.05)

    time.sleep(1)
    body.send_keys(Keys.HOME)
    time.sleep(1)

    count = 0
    xval = 1448
    comments_list_new = []

    while count < (len(comments_list1)-3):
        try:
            if comments_list1[count].find('"') != -1:
                element = driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(comments_list1[count])) #for comments that end with speech quote
                comments_list_new.append(comments_list2[count])
            else:
                element = driver.find_element_by_xpath('//*[contains(text(), "{}")]'.format(comments_list1[count])) #for comments that dont end in speech quote
                comments_list_new.append(comments_list2[count])

        except:
            count += 1
            pass
        
        else:

            driver.execute_script("arguments[0].scrollIntoView();", element) #always results in comment to be too high (off screen), meaning using sendkeys i can press up arrow key 4 times
            driver.execute_script("window.scrollBy(0, -150);")

            print(comments_list_new)



            #----------pyscreenshot---------#

            img = pyscreenshot.grab(bbox=(0, 0, 2560, 1440)) #X1, Y1, X2, Y2
            img.save(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\imgs\vid{}\temp.png".format(loop1+1))



            #----------OPENCV2----------#

            img = cv2.imread(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\imgs\vid{}\temp.png".format(loop1+1)) #NOTE: IMAGE IS USING BGR COLOURSPACE
            y, x, channels = img.shape

            length = 167

            while length < y: #loop to detect and deal with any comments that have a glowing red ring around them
                if list(img[length, 783]) != [255, 255, 255]:
                    if (list(img[length+9, 783]) == [138, 138, 255]) or (list(img[length+9, 783]) == [234, 234, 255]):
                        length += 10
                        xval = 1453

                    else:
                        break

                length += 1

            cropped = img[167:(length-15), 740:xval] #img[Y1:Y2, X1:X2]     #(741, 167, 1448, ???) #X1, Y1, X2, Y2
            
            #if (length-182) > 45: #if screenshot height is greater than 45 pixels, then we can assume it is NOT a deleted comment
            xval = 1479
            cv2.imwrite(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\imgs\vid{}\comment{}.png".format(loop1+1, str(count+1)), cropped)
            
            count += 1

    driver.quit()



#----------gtts----------#

    count = 0

    while count < len(comments_list_new):
        tts = gTTS(comments_list_new[count], tld="as", lang="en")
        tts.save(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\audio\audio{}\comment{}.mp3".format(loop1+1, count+1))

        count += 1

    tts = gTTS(title, tld="as", lang="en")
    tts.save(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\audio\audio{}\title.mp3".format(loop1+1))

    loop1 += 1




vidNames = []
loop2 = 0
while loop2 < 1:



    #----------moviepy---------#

    clips = []

    introNarration = AudioFileClip(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\audio\audio{}\title.mp3".format(loop2+1))
    introImg = ImageClip(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\imgs\vid{}\title.png".format(loop2+1)).set_duration(introNarration.duration).resize(2.0)
    longTransition = VideoFileClip(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\TESTING\moviepy testing\[1s] TV Color Bars - Distorted with Static and Timecode.mp4").volumex(0.5).resize(width=1920)

    introClip = introImg.set_audio(introNarration) #final intro clip built
    clips.append(introClip) #intro clip appended to list
    clips.append(longTransition) #1s transition appended to list

    x = 1
    while x <= 6: #change this to 23 when producing proper yt videos (will produce 20 clips since last 3 are failsafes)
        try:
            narration = AudioFileClip(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\audio\audio{}\comment{}.mp3".format(loop2+1, x))
            img = ImageClip(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\imgs\vid{}\comment{}.png".format(loop2+1, x)).set_duration(narration.duration).resize(2.0)
            shortTransition = VideoFileClip(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\TESTING\moviepy testing\[0.5s] TV Color Bars - Distorted with Static and Timecode.mp4").volumex(0.5).resize(width=1920)
            
            clip = img.set_audio(narration) #final comment clip built

            clips.append(clip) #comment clip appended to list
            clips.append(shortTransition) #0.5s transition appended to list

            x += 1

        except:
            x += 1

    clips.pop() #removing last 0.5s transition (will be replaced with 1s transition)

    outro = VideoFileClip(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\TESTING\moviepy testing\like subscribe outro.mp4")

    clips.append(longTransition) #1s transition appended to list
    clips.append(outro) #outro appended to list

    final = concatenate_videoclips(clips) #combining clips list into 1 object

    bg = VideoFileClip(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\TESTING\moviepy testing\galaxy background.mp4").fx(vfx.loop, duration=final.duration) #importing looped version of background video
    final = CompositeVideoClip([bg, final.set_position("center")]) #placing background underneath all content

    bgmusic = AudioFileClip(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\TESTING\moviepy testing\tranquility-bgmusic.mp3").volumex(0.025).fx(afx.audio_loop, duration=final.duration) #importing looped version of background music
    finalAudio = CompositeAudioClip([bgmusic, final.audio]) 
    final.audio = finalAudio #compositing and adding background music to final video

    vidName = "[{}] ".format(subreddit) + str(loop2+1).zfill(2) + ".mp4" #example name: [Askreddit] 04.mp4
    vidNames.append(vidName)

    final.write_videofile(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\Output\{}.mp4".format(vidNames[loop2]), threads=8, fps=30, codec="libx264")

    introNarration.close()
    introImg.close()
    longTransition.close()
    narration.close()
    img.close() #error here. Ima be honest this shit so broken. Its pulling narration from second video and using it on first video, telling me ImageClip is now a numpy array and can't be closed. Might have to restructure entire program to OOPS <-- 19/02/2022 update: LOL
    shortTransition.close()
    outro.close()
    bg.close()
    bgmusic.close()



    #----------YouTube API----------#

    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    socket.setdefaulttimeout(30000)

    ttl = "[AskReddit] " + post.title
    if(ttl[97] == " "):
        ttl = ttl[:96] + "..."

    else:
        ttl = ttl[:97] + "..."

    dsc = """I would love to hear your own stories in the comments section below! 👇

    Here at Reddit Uncovered, we endeavour to bring high quality content from the hottest and juiciest reddit threads! Stay tuned for more posts and don't forget to

    𝕊𝕌𝔹𝕊ℂℝ𝕀𝔹𝔼❕"""

    # request_body = {
    #     'snippet': {
    #         'categoryId': 24,
    #         'title': ttl,
    #         'description': dsc,
    #         'tags': ['reddit', 'stories', 'reddit stories']
    #     },
    #     'status': {
    #         'privacyStatus': "private",
    #         'selfDeclaredMadeForKids': False, 
    #     },
    #     'notifySubscribers': True
    # }

    # mediaFile = MediaFileUpload(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\Output\{}.mp4".format(vidNames[loop2]), chunksize=-1, resumable=True)

    # response_upload = service.videos().insert(
    #     part='snippet,status',
    #     body=request_body,
    #     media_body=mediaFile
    #     ).execute()

    # service.thumbnails().set(
    #     videoId=response_upload.get('id'),
    #     media_body=MediaFileUpload(r"C:\Users\avij4\Desktop\Python\Projects\reddit video creator\thumbnails\default.png") #putting default thumbnail img for now. Will be replaceed once proper img has been created
    #     ).execute()

    print("Video and thumbnail '{}' uploaded to youtube!".format(loop2+1))

    loop2 += 1


#CONFIRMED everything reddit related done,
#CONFIRMED everything selenium related done,
#CONFIRMED everything tts related done,
#CONFIRMED everything moviepy related is done,
#CONFIRMED everything youtube API related is done

#16/02/2022 - Need to implement deleted comment detection - FIXED
#rn im thinking of checking the height of the screenshot. If it's less than 45 pixels, then it is safe to assume that the screenshot is of a deleted comment, and so it can be discarded

#19/02/2022 - YT titles are broken, since ttl runs on loop2, whenever post.title is pulled, it just keeps getting the title of the last reddit link, since praw is no longer active - 
#planning to move ttl code to loop1 and then store the titles in a list called postTitles and then use the loop2 as the index to access the correct YT title in loop2
#idk if any of that made sense it is currently 3am so fuck you if it doesnt