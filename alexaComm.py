from __future__ import unicode_literals
import string, os, math, time, random, sys, re, vlc, pafy, queue, asyncio
from os import listdir
from vlcPlayer import Media_Player
from mediaRetriever import Media_Retriever
from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, '/jukebox')

class Alexa_Communicator():
    
    def __init__(self):
        pass

    @app.route('/')
    def homepage(self):
        return 'It IS working.'

    @ask.launch
    def startSkill():
        welcome_message = 'Jukebox opened, say a command'
        return question(welcome_message)

    @ask.intent('PlayIntent')
    def playIntent(song):
        song = play(song)
        return statement('Playing ' + song)

    @ask.intent('PlayLocalIntent')
    def playIntent(song):
        song = play(song, True)
        return statement('Playing ' + song)

    @ask.intent('AMAZON.FallbackIntent')
    def fallbackIntent():
        return statement('No sir')

    @ask.intent('PlayRandomIntent')
    def playIntent():
        song = play('random', True)
        return statement('Playing a random song')

    @ask.intent("SkipIntent")
    def skipIntent(skipCount):
        print('FUCK: ', skipCount)
        if skipCount==None:
            skipCount = 1
        skip(skipCount)
        return statement('Skipped ' + str(skipCount) + ' tracks')

    @ask.intent("QueueIntent")
    def queueIntent():
        print('I SHOULD NOT EXIST')
        queue_string = queue_status()
        return statement(queue_string)

    def runApp(self):
        app.run(debug=True)

def play(song, local = False):

    if song.lower() == 'random':

        media_dict = retriever.getRandomMedia('../Music')
        player.addMediaToQueue(media_dict)

    else:
        
        media_dict = retriever.getMedia(song, local)
        
        if media_dict == None:
            print('No match to search query "' + song + '"')
        else:
            player.addMediaToQueue(media_dict)
            song = list(media_dict.keys())[0]

    return song

def skip(tracks_to_skip = 1):
    if int(tracks_to_skip) == 1:
        player.skip()

    else:
        player.skip(int(tracks_to_skip))

def queue_status():
    queue_string = player.queue()
    return queue_string

retriever = Media_Retriever()
player = Media_Player()
alexa = Alexa_Communicator()


loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(alexa.runApp())
    loop.run_forever()

except KeyboardInterrupt:
    pass

finally:
    print('Loop complete')
    loop.close()



### FEATURES ###

#VLC:
    #Play Pause Stop Skip Repeat Shuffle Seek volume queue now_playing
#Media Retriever:
    #Put song length next to name
    #imply youtube
    #imply first result
#Jukebox:
    #Implement user commands (i.e. !play, !skip, etc.)
    #Implement async event loop

