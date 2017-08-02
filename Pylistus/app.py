import asyncio
import discord
import configparser

client = discord.Client()
config = configparser.ConfigParser()

config.read('config.ini')

client.run (config['DiscordAPI']['Key'], bot=True)

# For RSS: 1. Check and store system time on startup, and when pulling latest n items.
#		   2. On next check, post all items older than stored system time.