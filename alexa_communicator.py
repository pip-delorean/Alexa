from flask import Flask
from flask_ask import Ask, statement, question, session
from jukebox import Jukebox_Handler as jb

app = Flask(__name__)
ask = Ask(app, '/jukebox')

jukebox = jb()

class Alexa_Communicator():
    
    def __init__(self):
        pass

    @app.route('/')
    def homepage(self):
        return 'It IS working.'
    
    def run(self):
        app.run(debug=True)

    @ask.launch
    def startSkill():
        
        welcome_message = 'Jukebox opened, say a command'
        
        return question(welcome_message)
    
    @ask.intent('AMAZON.FallbackIntent')
    def fallbackIntent():
        return statement('No sir')

    @ask.intent('PlayIntent')
    def playIntent(media):

        status = jukebox.play(media)
        print(status)

        return statement(status)

    @ask.intent('PlayLocalIntent')
    def playLocalIntent(media):

        status = jukebox.play(media, True)

        return statement(status)

    @ask.intent('PlayRandomIntent')
    def playRandomIntent():

        status = jukebox.playRandom()

        return statement(status)

    @ask.intent("SkipIntent")
    def skipIntent(skipCount):
        
        if skipCount == None:
            skipCount = 1
            
        status = jukebox.skip(skipCount)
        print(status)
        
        return statement(status)

    @ask.intent("QueueIntent")
    def queueIntent():

        status = jukebox.queue()

        return statement(status)
    
    @ask.intent("ClearQueueIntent")
    def clearQueueIntent():
        
        status = jukebox.clearQueue()

        return statement(status)
    
    @ask.intent("ResumeIntent")
    def resumeIntent():
        
        status = jukebox.resume()

        return statement(status)
    
    @ask.intent("PauseIntent")
    def pauseIntent():
        
        status = jukebox.pause()

        return statement(status)
    
    @ask.intent("StopIntent")
    def stopIntent():
        
        status = jukebox.stop()

        return statement(status)
    
    @ask.intent('CurrentlyPlayingIntent')
    def currentlyPlayingIntent():
        
        status = jukebox.currentlyPlaying()
        
        return statement(status)