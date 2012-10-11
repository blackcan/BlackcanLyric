#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import urllib2
import HTMLParser  

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class MainHandler(webapp.RequestHandler):
    def get(self):
    	
    	song = self.request.get('song')
    	song = song.encode('utf-8')
    	song = urllib2.quote(song)
    	singer = self.request.get('singer')
    	singer = singer.encode('utf-8')
    	singer = urllib2.quote(singer)
    	url = "http://lyrics.oiktv.com/search.php?sn=" + singer + "&an=&ln=" + song + "&lrc=&sx=all"
    	url = url.encode('utf-8')

        lyricWeb = urllib2.urlopen(url)
        lyricContent = lyricWeb.read()
        lyricWeb.close()
        
        lyricContent = lyricContent.replace("\" + \"", '')
        lyricContent = lyricContent.replace("\"+\"", '')
        Parser = LyricHTMLURLParser()
        
        #self.response.out.write(lyricContent)
        
        try:
            Parser.feed(lyricContent)
            #Parser.close()
            minimum = 99
            lyricURLIndex = 0
            i = 0
            while i < len(Parser.songName):
            	if len(Parser.songName[i]) < minimum:
            		minimum = len(Parser.songName[i])
            		lyricURLIndex = i
                i = i + 1
            lyricURL = Parser.lyricURL[lyricURLIndex]
        except:
        	self.response.out.write('')
        	
        
        if len(Parser.lyricURL) == 0:
        	url = "http://lyrics.oiktv.com/search.php?sn=&an=&ln=" + song + "&lrc=&sx=all"
        	url = url.encode('utf-8')
        	lyricWeb = urllib2.urlopen(url)
        	lyricContent = lyricWeb.read()
        	lyricWeb.close()
        	lyricContent = lyricContent.replace("\" + \"", '')
        	lyricContent = lyricContent.replace("\"+\"", '')
        	Parser = LyricHTMLURLParser()
        	#self.response.out.write(lyricContent)
        	try:
        		Parser.feed(lyricContent)
        		#Parser.close()
        		minimum = 99
        		lyricURLIndex = 0
        		i = 0
        		while i < len(Parser.songName):
        			if len(Parser.songName[i]) < minimum:
        				minimum = len(Parser.songName[i])
        				lyricURLIndex = i
        			i = i + 1
        			lyricURL = Parser.lyricURL[lyricURLIndex]
        	except:
        		self.response.out.write('')
        		
        
        if len(Parser.lyricURL) > 0:
        	# self.response.out.write(lyricURL)
			url = "http://lyrics.oiktv.com/" + lyricURL
			
			lyricWeb = urllib2.urlopen(url)
			lyricContent = lyricWeb.read()
			lyricWeb.close()
			
			lyricContent = lyricContent[lyricContent.index("<h2 class=\"lrc_g6\">"):-1]
			
			# self.response.out.write(lyricContent)
			Parser = LyricHTMLParser()
			
			
			lyricContent = lyricContent.replace("\" + \"", '')
			lyricContent = lyricContent.replace("\"+\"", '')
			
			try:
				Parser.feed(lyricContent)
			except:
				self.response.out.write('')
			
			
			
			resultLyric = ''
			for line in Parser.lyrics:
				resultLyric += line
			
			self.response.out.write(resultLyric)
		
class LyricHTMLURLParser(HTMLParser.HTMLParser):
	
	lyricURL = []
	songName = []
	find = False
	
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.lyricURL = []
		self.songName = []
		self.find = False
		
	def handle_starttag(self, tag, attrs):
		if tag == 'a' and attrs[0][1].count('&lid=') != 0 and not self.find:
			self.lyricURL.append(attrs[0][1])
			self.find = True
			
	def handle_data(self, data):
		if self.find:
			self.songName.append(data)
			self.find = False
	
	
		
		
class LyricHTMLParser(HTMLParser.HTMLParser):
	
	lyrics = []
	
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.lyrics = []
	
	def handle_data(self, data):
		
		data = data.strip()
		if data and not hasattr(self, 'stop'):
			self.lyrics.append(data)
		
	def handle_starttag(self, tag, attrs):
		if tag == 'br':
			self.lyrics.append('\n')
			
	def handle_endtag(self, tag):
		if tag == 'br':
			self.lyrics.append('\n')
		if tag == 'div':
			self.stop = True
		if tag == 'h2':
			self.lyrics.append('\n\n')
			
	
		
def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
