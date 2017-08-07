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

	card = {"name": cardname, "orderBy": 'name'}
	response = requests.get("https://api.magicthegathering.io/v1/cards", params=card)
	cardinfo = json.loads(response.text)
	carddata = cardinfo['cards'][0]

	name = carddata['name'] + ' '
	if "manaCost" in carddata:
		cost = carddata['manaCost'] + '\n'
	else:
		cost = '\n'
	rarity = carddata['rarity'] + ' ('
	fromset = carddata['set'] + ')\n'
	cardtype = carddata['type'] + '\n'
	cardtext = carddata['text']
	if "power" in carddata:
		pt = '\n' + carddata['power'] + '/' + carddata['toughness']
	else:
		pt = ''

	match = name + cost + rarity + fromset + cardtype + cardtext + pt

	await bot.say(match)

# @bot.command()

# There are no provisions for sending messages <2000 characters long
# in the following code. Need to fix before re-enabling.

# async def r(*, cardname: str):

# 	card = {"name": cardname, "orderBy": 'name'}
# 	response = requests.get("https://api.magicthegathering.io/v1/cards", params=card)
# 	cardinfo = json.loads(response.text)
# 	carddata = cardinfo['cards'][0]

# 	if "rulings" in carddata:
# 		rulecount = len(carddata['rulings'])
# 		ruletar = carddata['rulings']
# 		arules = ''

# 		for rn in list(range(rulecount)):
# 			arules = arules + ruletar[rn]['date'] + ' - ' + ruletar[rn]['text'] + '\n'

# 	else:
# 		arules = 'No rulings found for ' + carddata['name']

# 	await bot.say(arules)

config.read('config.ini')
bot.run(config['DiscordAPI']['Key'])
