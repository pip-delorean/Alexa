from media_retriever import Media_Retriever as mr
from media_player import Media_Player as mp

class Jukebox_Handler():
    
    def __init__(self):
        self.retriever = mr()
        self.player = mp()
    
    def play(self, media, local = False):
            
        media_list = self.retriever.searchMedia(media, local)
        media = media_list[0]
        media[1] = self.retriever.getStreamURL(media[1])
        print(media[1])
        status = self.player.addToQueue(media)
            
        return status
    
    def skip(self, skipCount = 1):
        
        status = self.player.skip(int(skipCount))
        
        return status
    