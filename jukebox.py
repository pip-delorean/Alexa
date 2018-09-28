from media_retriever import Media_Retriever as mr
from media_player import Media_Player as mp
import random

class Jukebox_Handler():
    
    def __init__(self):
        self.retriever = mr()
        self.player = mp()
    
    def play(self, media, local = False):
            
        media_list = self.retriever.searchMedia(media, local)
        media = media_list[0]
        media[1] = self.retriever.getStreamURL(media[1])
        status = self.player.addToQueue(media)
            
        return status
    
    def playRandom(self):
        
        local = True
        
        media_list = self.retriever.searchMedia('all', local)
        media = random.choice(media_list)
        status = self.player.addToQueue(media)
        
        return status
    
    def skip(self, skipCount = 1):
        
        status = self.player.skip(int(skipCount))
        
        return status
    
    def pause(self):
        
        status = self.player.pause()
        
        return status
    
    def resume(self):
        
        status = self.player.resume()
        
        return status
    
    def stop(self):
        
        status = self.player.stop()
        
        return status
    
    def clearQueue(self):
        
        status = self.player.clearQueue()
        
        return status
    
    def queue(self):
        
        status = self.player.listQueue()
        
        return status
    
    def currentlyPlaying(self):
        
        status = self.player.currentlyPlaying()
        
        return status
    
    def playbackTime(self):
        
        status = self.player.playbackTime()
        
        return playbackTime
    