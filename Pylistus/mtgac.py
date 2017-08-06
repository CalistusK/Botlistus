import asyncio
import configparser
import discord
import requests
import json
from discord.ext import commands

client = discord.Client()
config = configparser.ConfigParser()
bot = commands.Bot(command_prefix='.')

@bot.command()
async def c(*, cardname: str):

	card = {"name": cardname}
	response = requests.get("https://api.magicthegathering.io/v1/cards", params=card)
	cardinfo = json.loads(response.text)
	carddata = cardinfo['cards'][0]

	name = carddata['name'] + ' '
	cost = carddata['manaCost'] + '\n'
	rarity = carddata['rarity'] + ' ('
	fromset = carddata['set'] + ')\n'
	cardtype = carddata['type'] + '\n'
	cardtext = carddata['text']
	if carddata['types'] == "Creature":
		pt = '\n' + carddata['power'] + '/' + carddata['toughness']
	else:
		pt = ''

	match = name + cost + rarity + fromset + cardtype + cardtext + pt

	await bot.say(match)

config.read('config.ini')
bot.run(config['DiscordAPI']['Key'])