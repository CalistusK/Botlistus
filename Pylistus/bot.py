import asyncio
import discord
from discord.ext import commands
import configparser
import feedparser
import re
import time
from threading import Timer

client = discord.Client()
config = configparser.ConfigParser()

class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
	    self._timer = None
	    self.interval = interval
	    self.function = function
	    self.args = args
	    self.kwargs = kwargs
	    self.is_running = False
	    self.next_call = time.time()
	    self.start()

	def _run(self):
	    self.is_running = False
	    self.start()
	    self.function(*self.args, **self.kwargs)

	def start(self):
	    if not self.is_running:
	      self.next_call += self.interval
	      self._timer = threading.Timer(self.next_call - time.time(), self._run)
	      self._timer.start()
	      self.is_running = True

	def stop(self):
	    self._timer.cancel()
	    self.is_running = False

class RSS():

	@client.event
	async def on_message(message):
		url = 'http://feeds.feedburner.com/DustforceMaps'
		d = feedparser.parse(url)

		# if message.content.startswith('-last3maps'):
		# 	for entrynum in list(range(3)[::-1]):
		# 		mapauthor = re.search('(?<=user/).*(?=\">)', d['items'][entrynum].description)
		# 		thumb = re.search('(?<=img src=\").*(?=\"/>)', d['items'][entrynum].description)
		# 		embed=discord.Embed(title=d['items'][entrynum].title, url=d['items'][entrynum].link)
		# 		embed.set_author(name=mapauthor.group(0), url='http://atlas.dustforce.com/user/'+mapauthor.group(0))
		# 		embed.set_thumbnail(url=thumb.group(0))
		# 		await client.send_message(message.channel, embed=embed)
				
		if message.author.id = '71525265808826368':
			if message.content.startswith('-rss'):
				baseetag = d.etag
				baseID = re.search('(?<=m\/).*(?=\/)', d['items'][0].link)

				async def checkfeed(checketag):
					if baseetag != checketag:
						newcount = 0
						for entrynum in list(range(3)[::-1]):
							currID = re.search('(?<=m\/).*(?=\/)', d['items'][entrynum].link)
							if baseID.group(0) < currID.group(0):
								newcount = newcount+1
								mapauthor = re.search('(?<=user/).*(?=\">)', d['items'][entrynum].description)
								thumb = re.search('(?<=img src=\").*(?=\"/>)', d['items'][entrynum].description)
								embed=discord.Embed(title=d['items'][entrynum].title, url=d['items'][entrynum].link)
								embed.set_author(name=mapauthor.group(0), url='http://atlas.dustforce.com/user/'+mapauthor.group(0))
								embed.set_thumbnail(url=thumb.group(0))
								await client.send_message(message.channel, embed=embed)
						if newcount == 3:
							newcount == 0
							for entrynum in list(range(4,21)):
								currID = re.search('(?<=m\/).*(?=\/)', d['items'][entrynum].link)
								if baseID.group(0) < currID.group(0):
									newcount = newcount+1
							if newcount > 0:
								await client.send_message(message.channel, '...and '+newcount+' more. (Checked last 20 maps)')

				rt = RepeatedTimer(1, checkfeed, d.etag)
				try:
					sleep(600)
				finally:
					rt.stop()

config.read('config.ini')
client.run (config['DiscordAPI']['Key'], bot=True)