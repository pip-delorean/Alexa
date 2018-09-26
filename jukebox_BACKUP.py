from __future__ import unicode_literals
import string, os, math, time, random, sys, re, vlc, pafy, queue, asyncio
from os import listdir
from vlcPlayer import Media_Player
from mediaRetriever import Media_Retriever

async def command_handler():
    while True:
        try:
            command = input('Command: ')
            if command[0] == '!':
                command = command[1:].lower().split()
                args = command[1:]
                await command_dict[command[0]](args)
                
        except KeyboardInterrupt as e:
            print(e)

async def play(args):

    if len(args) == 1:

        if args[0].lower() == 'random':

            media_dict = retriever.getRandomMedia('../Music')
            player.addMediaToQueue(media_dict)

        else:
            
            local = False
            song = args[0]
            media_dict = retriever.getMedia(song, local)
            
            if media_dict == None:
                print('No match to search query "' + song + '"')
            else:
                player.addMediaToQueue(media_dict)
        
    elif len(args) > 1:

        local = args[0].lower()
        
        if local in ['local','music','media','library']:
            local = True
            song = ' '.join(args[1:])
            
        else:
            local = False
            song = ' '.join(args)

        media_dict = retriever.getMedia(song, local)
        
        if media_dict == None:
            print('No match to search query "' + song + '"/Search cancelled')

        else:
            player.addMediaToQueue(media_dict)
        
    else:
        print('Too few arguments')

async def skip(args):
    if len(args) == 0:
        player.skip()

    elif len(args) == 1:
        player.skip(int(args[0]))

    else:
        print('Too many/few arguments')

async def queue(args):
    if len(args) == 0:
        player.queue()
    else:
        print('Too many arguments!')

        
command_dict = {'play':play, 'skip':skip, 'queue':queue}

retriever = Media_Retriever()
player = Media_Player()

loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(command_handler())
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
