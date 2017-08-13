import asyncio
import configparser
import discord
import requests
import json
from discord.ext import commands

client = discord.Client()
config = configparser.ConfigParser()
bot = commands.Bot(command_prefix='.')

def getjson(sfilter, cardname):
	if sfilter == 'exact' or sfilter == 'fuzzy':
		stype = 'named'
	elif sfilter == 'q':
		stype = 'search'

	card = {sfilter: cardname}
	response = requests.get('https://api.scryfall.com/cards/' + stype, params=card)
	carddata = json.loads(response.text)

	if sfilter == 'q':
		carddata = carddata['data'][0]

	return carddata

def cardMatch(carddata, rtype):
	if rtype == 'cardtext':
		halves = ''
		if carddata['layout'] in ['split', 'flip']:
			name = carddata['name'] + '\n'
			if 'mana_cost' in carddata:
				cost = carddata['mana_cost'] + '\n'
			else:
				cost = ''
			rarity = carddata['rarity'] + ' ('
			fromset = carddata['set'] + ')\n'
			for face in [0, 1]:
				cardhalf = carddata['card_faces'][face]
				halfname = '```' + cardhalf['name'] + ' '
				if 'mana_cost' in cardhalf:
					halfcost = cardhalf['mana_cost'] + '\n'
				else:
					halfcost = '\n'
				halftype = cardhalf['type_line'] + '\n'
				halftext = cardhalf['oracle_text']
				if 'power' in cardhalf:
					pt = '\n' + cardhalf['power'] + '/' + cardhalf['toughness']
				else:
					pt = ''

				halves = halves + halfname + halfcost + halftype.replace("â€”","—") + halftext + pt + '```'

				if face == 0:
					halves = halves + '\n'

			match = name + cost + rarity.title() + fromset.upper() + halves

		else:
			name = carddata['name'] + ' '
			if "mana_cost" in carddata:
				cost = carddata['mana_cost'] + '\n'
			else:
				cost = '\n'
			rarity = carddata['rarity'] + ' ('
			fromset = carddata['set'] + ')\n'
			cardtype = carddata['type_line'] + '\n'
			cardtext = '```' + carddata['oracle_text'] + '```'
			if "power" in carddata:
				pt = carddata['power'] + '/' + carddata['toughness']
			else:
				pt = ''

			match = name + cost + rarity.title() + fromset.upper() + cardtype.replace("â€”","—") + pt + cardtext
	elif rtype == 'cardusd':
		name = carddata['name'] + ' '
		cardset = '(' + carddata['set'] + ')' + ' ~ '
		price = '$' + carddata['usd']

		match = name + cardset.upper() + price

	return match

@bot.command()
async def c(*, cardname: str):
	carddata = getjson('q', cardname)
	match = cardMatch(carddata, 'cardtext')

	await bot.say(match)

@bot.command()
async def ce(*, cardname: str):
	carddata = getjson('exact', cardname)
	match = cardMatch(carddata, 'cardtext')

	await bot.say(match)

@bot.command()
async def cf(*, cardname: str):
	carddata = getjson('fuzzy', cardname)
	match = cardMatch(carddata, 'cardtext')

	await bot.say(match)

@bot.command()
async def cn(*, cardname: str):
	cardname = 'is:' + cardname
	carddata = getjson('q', cardname)
	match = cardMatch(carddata, 'cardtext')

	await bot.say(match)

@bot.command()
async def cs(setname: str, *, cardname: str):
	cardname = 'e:' + setname + ' ' + cardname
	carddata = getjson('q', cardname)
	match = cardMatch(carddata, 'cardtext')

	await bot.say(match)

@bot.command()
async def p(*, cardname: str):
	cardname = 'usd>=0.00 ' + cardname
	carddata = getjson('q', cardname)
	match = cardMatch(carddata, 'cardusd')

	await bot.say(match)

@bot.command()
async def pe(*, cardname: str):
	carddata = getjson('exact', cardname)
	match = cardMatch(carddata, 'cardusd')

	await bot.say(match)

@bot.command()
async def pf(*, cardname: str):
	carddata = getjson('fuzzy', cardname)
	match = cardMatch(carddata, 'cardusd')

	await bot.say(match)

@bot.command()
async def pn(*, cardname: str):
	cardname = 'is:' + cardname
	carddata = getjson('q', cardname)
	match = cardMatch(carddata, 'cardusd')

	await bot.say(match)

@bot.command()
async def ps(setname: str, *, cardname: str):
	cardname = 'e:' + setname + ' ' + cardname
	carddata = getjson('q', cardname)
	match = cardMatch(carddata, 'cardusd')

	await bot.say(match)

config.read('config.ini')
bot.run(config['DiscordAPI']['Key'])
