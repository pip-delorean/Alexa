import string, os, pafy, math, time, random, sys, urllib, urllib.parse, urllib.request, re, requests, html
from os import listdir
import unidecode

RESULT_LIMIT = 3 # Default number of results listed in selection
MEDIA_DIR = '../Music'

class Media_Retriever():
    
    def __init__(self):
        pass
    
    def searchMedia(self, query, local = False): # returns a list of search results, ["media", "media location"] based on query
                
        limit = RESULT_LIMIT
        media_dir = MEDIA_DIR
                
        if local:
            
            strict = True # Is the file search strict, match query exactly vs by keywords
            
            media_results = self.searchLocalFiles(query, media_dir, strict)
            media_list = self.mediaListGenerator(media_results, limit)
            
        else:
            
            media_results = self.searchYoutube(query)
            media_list = self.mediaListGenerator(media_results, limit)
            
        return media_list
            
    def searchYoutube(self, query):
        
        media_results = []
        
        query_string = urllib.parse.urlencode({"search_query": query})
        html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        
        htmlDecoded = html_content.read().decode()
        htmlDecoded = html.unescape(htmlDecoded)
        htmlDecoded = unidecode.unidecode(htmlDecoded)
        
        titles = re.findall(r'class="yt-lockup-title ">.*?href=\"\/watch\?v=.*?>(.*?)</a>.*?Duration', htmlDecoded)  # Returns video titles
        search_results = re.findall(r'class="yt-lockup-title ">.*?href=\"\/watch\?v=(.{11}).*?Duration', htmlDecoded)  # Returns the ?v="<this>" part of the video links
        
        for i in range(len(titles)):
            media_results.append([titles[i], 'https://www.youtube.com/watch?v=' + search_results[i]])
        
        return media_results
        
    def getStreamURL(self, url):
        
        video = pafy.new(url)
        audio = video.getbestaudio()
        streamURL = audio.url
        
        return streamURL
        
    def mediaListGenerator(self, media_list, limit = RESULT_LIMIT):
        
        temp_list = []
        
        if len(media_list) < limit:
            limit = len(media_list)
            
        for i in range(limit):
            temp_list.append(media_list[i])
            
        media_list = temp_list
        
        return media_list
        
    
    def searchLocalFiles(self, query, search_dir = MEDIA_DIR, strict = False):
        
        media_results = []
        
        if strict:
            query = [query.lower()]
            
        else:
            query = query.lower().split()
        
        for path, subdirs, files in os.walk(search_dir):
            
            for name in files:
                duplicate = False

                for term in query:
                    
                    if term in name.lower() and '.mp3' in name.lower():
                        
                        for i in range(len(media_results)):
                            
                            if name == media_results[i][0]:
                                
                                duplicate = True
                                break
                            
                        if not duplicate:
                            media_results.append([name, os.path.join(path, name)])

        return media_results
        
            