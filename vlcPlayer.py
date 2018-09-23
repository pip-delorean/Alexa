from __future__ import unicode_literals
import string, os, math, time, vlc
from os import listdir

class Media_Player():

    def __init__(self):
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.onFinish)
        self.q = []
        self.playing = [1,2,3,4]
        
    def onFinish(self, event):
        time.sleep(1)
        self.q.pop(0)
        self.playNextMedia()
        
    def addMediaToQueue(self, media_dict):
        self.q.append(media_dict)
        if self.player.get_state().value not in self.playing:
            self.playNextMedia()

    def playNextMedia(self):
        if self.q:
            media_dict = self.q[0]
            title = list(media_dict.keys())[0]
            url = media_dict[title]
            self.player = self.Instance.media_player_new()
            self.events = self.player.event_manager()
            self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.onFinish)
            media = self.Instance.media_new(url)
            media.get_mrl()
            self.player.set_media(media)
            self.player.play()
            print('Now playing: ' + title)
        else:
            print('Playlist empty!')
            

    def playbackTime(self):
        sec = self.player.get_time() / 1000
        m, s = divmod(sec, 60)
        print ("%02d:%02d" % (m,s))

    def skip(self, tracksToSkip = 1):
        if tracksToSkip != 1:
            for i in range(tracksToSkip-1):
                if self.q:
                    self.q.pop(0)
                else:
                    break

        self.q.pop(0)
        self.player.stop()
        self.playNextMedia()

    def queue(self):
        count = 1
        if self.q:
            print('\nCurrently playing: ' + list(self.q[0].keys())[0])
            print('\nQueue:')
            if len(self.q) > 1:
                for i in range(len(self.q)-1):
                    print(str(count) + '. ' + list(self.q[count].keys())[0])
                    count += 1
                print()
                
            else:
                print('No songs in queue.\n')

        else:
            print('No songs in queue.\n')
        



