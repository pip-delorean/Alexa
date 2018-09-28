from __future__ import unicode_literals
import string, os, math, time, vlc, unidecode
from os import listdir

class Media_Player():

    def __init__(self):
        
        self.Instance = vlc.Instance(["--network-caching=5000"])
        self.player = None
        self.queue = []
        self.playing = [1,2,3,4]
        
    def addToQueue(self, media): # adds given list formatted ['song name', 'song location'] to queue
        
        self.queue.append(media)
        
        if self.player == None:
            status = self.playNextMedia()
            
        else:
            status = 'Added ' + media[0] + ' to queue!'
        
        return status
            
    def playNextMedia(self):
        
        if self.queue:
            
            media = self.queue[0]
            title = media[0]
            location = media[1]
            
            self.player = self.Instance.media_player_new()
            events = self.player.event_manager()
            events.event_attach(vlc.EventType.MediaPlayerEndReached, self.onFinish)
            
            media = self.Instance.media_new(location)
            media.get_mrl()
            
            self.player.set_media(media)
            self.player.play()
            
            status = 'Now playing ' + title
            
        else:
            status = 'Queue empty'
            self.player = None
            
        return status
    
    def onFinish(self, event):
        self.queue.pop(0)
        self.playNextMedia()
        
    def playbackTime(self):
        
        if self.player != None:
            
            sec = self.player.get_time() / 1000
            m, s = divmod(sec, 60)
            status = "%02d:%02d" % (m,s)
            
        else:
            status = "Nothing playing currently"
            
        return status
    
    def skip(self, skipCount = 1):
        
        counter = 0
        
        if self.queue:
            
            if skipCount == 1:
                plural = ''
                
            else:
                plural = 's'
            
            while self.queue and skipCount > 0:
                self.queue.pop(0)
                skipCount -= 1
                counter += 1
                
            self.player.stop()
            self.playNextMedia()
            status = 'Skipped ' + str(counter) + ' track' + plural
                
        else:
            status = 'The queue is empty!'
        
        return status
            
    def listQueue(self):
        
        if len(self.queue) > 1:
            
            status = 'There are ' + str(len(self.queue)-1) + 'tracks in the queue: '
            for i in range(1, len(self.queue)):
                status += self.queue[i][0] + ', '
            
        else:
            status = 'The queue is empty!'
        
        return status
    
    def clearQueue(self):
        
        if self.player != None:
            while len(self.queue) > 1:
                self.queue.pop(-1)
                
        else:
            self.queue = []
            
        status = "Queue cleared"
        
        return status
    
    def currentlyPlaying(self):
        
        if self.queue:
            
            status = 'Currently playing ' + self.queue[0][0]
            
        else:
            status = 'Nothing currently playing'
        
        return status
    
    def resume(self):
        
        if self.player != None:
            
            self.player.resume()
            
            status = "Resumed player"
            
        else:
            status = "Nothing to resume"
        
        return status
    
    def pause(self):
        
        if self.player != None:
            
            self.player.pause()
            
            status = "Paused player"
            
        else:
            status = "Nothing to pause"
        
        return status
    
    def stop(self):
        
        if self.player != None:
            
            self.player.stop()
            self.queue.pop(0)
            self.player = None
            
            status = "Stopped player"
            
        else:
            status = "Nothing to stop"
        
        return status
            
