import string, os, pafy, math, time, random, sys, urllib, urllib.parse, urllib.request, re, requests, html
from os import listdir

RESULT_LIMIT = 5 # Maximum number of results listed in selection

class Media_Retriever():
    
    def __init__(self):
        pass

    def getMedia(self, song, local = False):
        
        song = song.lower()
        media_titles = []
        
        if local == True:
            media = self.findAllFiles(song, '../Music', True)
            
            if len(media) == 0:
                media_dict = None
                
            elif len(media) == 1:
                media_dict = media[0]
                
            else:
                
                for song_dict in media:
                    media_titles.append(list(song_dict.keys())[0])

                selection = self.selectMedia(media_titles)

                if selection == 0:
                    media_dict = None

                else:
                    for song_dict in media:
                        if media_titles[selection-1] in song_dict:
                            media_dict = song_dict
                            break
                
                    
                    

                
        else:
            media_dict = self.getYoutubeURL(song)
            
            if list(media_dict.keys())[0] == None:
                media_dict = None

        return media_dict

    def getRandomMedia(self, mediaDir):
        file_paths = []
        count = 0
        for path, subdirs, files in os.walk(mediaDir):
            for name in files:
                if '.mp3' in name:
                    file_paths.append({name: os.path.join(path, name)})

        return random.choice(file_paths)
    
        
    def getYoutubeURL(self, search_terms): # When passed a search term, will get youtube links and ask for a selection, then return selected link

        titles, search_results = self.searchYoutube(search_terms)
        selection = self.selectMedia(titles)

        if selection != 0:
            url = 'https://www.youtube.com/watch?v=' + search_results[selection-1]
            url = self.getStreamURL(url)
            title = titles[selection-1]
            
        else:
            url = None
            title = None

            
        return {title: url}

    def searchYoutube(self, search_terms):
        query_string = urllib.parse.urlencode({"search_query": search_terms})
        html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        htmlDecoded = html_content.read().decode()
        htmlDecoded = html.unescape(htmlDecoded)
        titles = re.findall(r'class="yt-lockup-title ">.*?href=\"\/watch\?v=.*?>(.*?)</a>.*?Duration', htmlDecoded)  # Returns video titles
        search_results = re.findall(r'class="yt-lockup-title ">.*?href=\"\/watch\?v=(.{11}).*?Duration', htmlDecoded)  # Returns the ?v="<this>" part of the video links
        return titles, search_results

    def getStreamURL(self, url): # Passed a youtube url, generates an audio streaming url and returns
        video = pafy.new(url)
        audio = video.getbestaudio()
        streamURL = audio.url
        return streamURL

    def selectMedia(self, media): # Passed a list of video titles, returns a selection (int)
        count = 1
        selection_str = '\n'
        selection = ''
        for item in media:
        
            selection_str += str(count) + '. ' + item + '\n'
            count += 1
            
            if count > RESULT_LIMIT:
                break
            
        print(selection_str)
        selection = input('Make your selection: ')
        
        if selection.isdigit() and int(selection) <= RESULT_LIMIT:
            selection = int(selection)
        else:
            selection = 0
        return selection
    
    def findFile(self, keyword, search_dir):
        for file in os.listdir(search_dir):
            for word in keyword.split():
                if word in file.lower().split():
                    return file

    def findFiles(self, keyword, search_dir):
        files = []
        for file in os.listdir(search_dir):
            for word in keyword.split():
                if word in file.lower().split():
                    if '.mp3' in file:
                        files.append(file)
        return files

    def findAllFiles(self, keyword, search_dir, strict=False): # Find all files with a keyword in their name in current directory and all  subdirectories
        file_paths = []
        for path, subdirs, files in os.walk(search_dir):
            for name in files:
                if not strict: # Strict will only match file names that match the keyword exactly
                    for word in keyword.split():
                        if word in name.lower().split():
                            if '.mp3' in name:
                                if name not in (list(d.keys()) for d in file_paths):
                                    file_paths.append({name: os.path.join(path, name)})
                
                else:
                        if keyword in name.lower():
                            if '.mp3' in name:
                                if name not in (list(d.keys()) for d in file_paths):
                                    file_paths.append({name: os.path.join(path, name)})
                                    

        return file_paths


                                        



