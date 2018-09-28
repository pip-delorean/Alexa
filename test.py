from media_retriever import Media_Retriever as mr
from media_player import Media_Player as mp
from alexa_communicator import Alexa_Communicator as ac
from jukebox import Jukebox_Handler as jb
import time

retrvr = mr()
player = mp()
alexa = ac()
jukebox = jb()

#alexa.run()

local = False

results = retrvr.searchMedia('viva la vida', local)
for i in range(len(results)):
    print(results[1][1])
    
if not local:
    results[1][1] = retrvr.getStreamURL(results[1][1])
    
print(results[1][1])
    
print(player.addToQueue(results[1]))

while player.player != None:
    time.sleep(5)
    player.playbackTime()