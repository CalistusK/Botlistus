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
async def mtg():
	helplist = """ The following commands are available:\n
	.c <cardname> - Search for the Oracle text of a card\n
	.ce <cardname> - Search for the Oracle text of a card by exact name\n
	.cf <cardname> - Search for the Oracle text of a card by approximate name\n
	.cn <nickname> - Search for the Oracle text of a card by nickname\n 
	.p <cardname> - Search for the price (USD) of a card\n
	.ps <set> <cardname> - Search for the price (USD) of a card by set\n
	.pe <cardname> - Search for the price (USD) of a card by exact name\n
	.pf <cardname> - Search for the price (USD) of a card by approximate name
	"""
	await bot.say(helplist)

@bot.command()
async def c(*, cardname: str):

	card = {"q": cardname}
	response = requests.get("https://api.scryfall.com/cards/search", params=card)
	cardinfo = json.loads(response.text)
	carddata = cardinfo['data'][0]

	name = carddata['name'] + ' '
	if "mana_cost" in carddata:
		cost = carddata['mana_cost'] + '\n'
	else:
		cost = '\n'
	rarity = carddata['rarity'] + ' ('
	fromset = carddata['set'] + ')\n'
	cardtype = carddata['type_line'] + '\n'
	cardtext = carddata['oracle_text']
	if "power" in carddata:
		pt = '\n' + carddata['power'] + '/' + carddata['toughness']
	else:
		pt = ''

	match = name + cost + rarity.title() + fromset.upper() + cardtype.replace("â€”","—") + cardtext + pt

	await bot.say(match)

@bot.command()
async def ce(*, cardname: str):

	card = {"exact": cardname}
	response = requests.get("https://api.scryfall.com/cards/named", params=card)
	cardinfo = json.loads(response.text)

	name = cardinfo['name'] + ' '
	if "mana_cost" in cardinfo:
		cost = cardinfo['mana_cost'] + '\n'
	else:
		cost = '\n'
	rarity = cardinfo['rarity'] + ' ('
	fromset = cardinfo['set'] + ')\n'
	cardtype = cardinfo['type_line'] + '\n'
	cardtext = cardinfo['oracle_text']
	if "power" in cardinfo:
		pt = '\n' + cardinfo['power'] + '/' + cardinfo['toughness']
	else:
		pt = ''

	match = name + cost + rarity.title() + fromset.upper() + cardtype.replace("â€”","—") + cardtext + pt

	await bot.say(match)

@bot.command()
async def cf(*, cardname: str):

	card = {"fuzzy": cardname}
	response = requests.get("https://api.scryfall.com/cards/named", params=card)
	cardinfo = json.loads(response.text)

	name = cardinfo['name'] + ' '
	if "mana_cost" in cardinfo:
		cost = cardinfo['mana_cost'] + '\n'
	else:
		cost = '\n'
	rarity = cardinfo['rarity'] + ' ('
	fromset = cardinfo['set'] + ')\n'
	cardtype = cardinfo['type_line'] + '\n'
	cardtext = cardinfo['oracle_text']
	if "power" in cardinfo:
		pt = '\n' + cardinfo['power'] + '/' + cardinfo['toughness']
	else:
		pt = ''

	match = name + cost + rarity.title() + fromset.upper() + cardtype.replace("â€”","—") + cardtext + pt

	await bot.say(match)

@bot.command()
async def cn(*, cardname: str):

	card = {"q": 'is:' + cardname}
	response = requests.get("https://api.scryfall.com/cards/search", params=card)
	cardinfo = json.loads(response.text)
	carddata = cardinfo['data'][0]

	name = carddata['name'] + ' '
	if "mana_cost" in carddata:
		cost = carddata['mana_cost'] + '\n'
	else:
		cost = '\n'
	rarity = carddata['rarity'] + ' ('
	fromset = carddata['set'] + ')\n'
	cardtype = carddata['type_line'] + '\n'
	cardtext = carddata['oracle_text']
	if "power" in carddata:
		pt = '\n' + carddata['power'] + '/' + carddata['toughness']
	else:
		pt = ''

	match = name + cost + rarity.title() + fromset.upper() + cardtype.replace("â€”","—") + cardtext + pt

	await bot.say(match)

@bot.command()
async def cs(setname: str, *, cardname: str):

	card = {"q": 'e:' + setname + ' ' + cardname}
	response = requests.get("https://api.scryfall.com/cards/search", params=card)
	cardinfo = json.loads(response.text)
	carddata = cardinfo['data'][0]

	name = carddata['name'] + ' '
	if "mana_cost" in carddata:
		cost = carddata['mana_cost'] + '\n'
	else:
		cost = '\n'
	rarity = carddata['rarity'] + ' ('
	fromset = carddata['set'] + ')\n'
	cardtype = carddata['type_line'] + '\n'
	cardtext = carddata['oracle_text']
	if "power" in carddata:
		pt = '\n' + carddata['power'] + '/' + carddata['toughness']
	else:
		pt = ''

	match = name + cost + rarity.title() + fromset.upper() + cardtype.replace("â€”","—") + cardtext + pt

	await bot.say(match)

@bot.command()
async def p(*, cardname: str):

	card = {"q": 'usd>=0.00 ' + cardname}
	response = requests.get("https://api.scryfall.com/cards/search", params=card)
	cardinfo = json.loads(response.text)
	carddata = cardinfo['data'][0]

	name = carddata['name'] + ' '
	cardset = '(' + carddata['set'] + ')' + ' ~ '
	price = '$' + carddata['usd']

	match = name + cardset.upper() + price

	await bot.say(match)

@bot.command()
async def pe(*, cardname: str):

	card = {"exact": cardname}
	response = requests.get("https://api.scryfall.com/cards/named", params=card)
	cardinfo = json.loads(response.text)

	name = cardinfo['name'] + ' '
	cardset = '(' + cardinfo['set'] + ')' + ' ~ '
	price = '$' + cardinfo['usd']

	match = name + cardset.upper() + price

	await bot.say(match)

@bot.command()
async def ps(setname: str, *, cardname: str):

	card = {"q": 'e:' + setname + ' ' + cardname}
	response = requests.get("https://api.scryfall.com/cards/search", params=card)
	cardinfo = json.loads(response.text)
	carddata = cardinfo['data'][0]

	name = carddata['name'] + ' '
	cardset = '(' + carddata['set'] + ')' + ' ~ '
	price = '$' + carddata['usd']

	match = name + cardset.upper() + price

	await bot.say(match)

@bot.command()
async def pf(*, cardname: str):

	card = {"fuzzy": 'usd>=0.00 ' + cardname}
	response = requests.get("https://api.scryfall.com/cards/named", params=card)
	cardinfo = json.loads(response.text)

	if 'code' in cardinfo:
		if cardinfo['code'] == 'not_found':
			match = cardinfo['details']
	else:
		name = cardinfo['name'] + ' '
		cardset = '(' + cardinfo['set'] + ')' + ' ~ '
		price = '$' + cardinfo['usd']
		match = name + cardset.upper() + price

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
