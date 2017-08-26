import asyncio
import configparser
import discord
import requests
import json
import re
import logging
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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

def cardMatch(carddata, rtype, *server):
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

			match = name + emojify(cost, server).replace(' ','') + rarity.title() + fromset.upper() + cardtype.replace("â€”","—") + pt + cardtext.replace("â€”","—")

	elif rtype == 'cardusd':
		name = carddata['name'] + ' '
		cardset = '(' + carddata['set'] + ')' + ' ~ '
		price = '$' + carddata['usd']

		match = name + cardset.upper() + price

	return match

def emojify(cost, server):
	cost = cost.lower().replace("{","mana").replace("}"," ").split(' ')
	for idx,manasym in enumerate(cost):
		for emo in server.emojis:
			if emo.name == manasym:
				cost[idx] = str(emo)

	return ' '.join(cost)

@bot.command(pass_context=True)
async def c(ctx, *, cardname: str):
	carddata = getjson('q', cardname)
	server = ctx.message.server
	match = cardMatch(carddata, 'cardtext', server)

	await bot.say(match)

@bot.command(pass_context=True)
async def ce(ctx, *, cardname: str):
	carddata = getjson('exact', cardname)
	server = ctx.message.server
	match = cardMatch(carddata, 'cardtext', server)

	await bot.say(match)

@bot.command(pass_context=True)
async def cf(ctx, *, cardname: str):
	carddata = getjson('fuzzy', cardname)
	server = ctx.message.server
	match = cardMatch(carddata, 'cardtext', server)

	await bot.say(match)

@bot.command(pass_context=True)
async def cn(ctx, *, cardname: str):
	cardname = 'is:' + cardname
	carddata = getjson('q', cardname)
	server = ctx.message.server
	match = cardMatch(carddata, 'cardtext', server)

	await bot.say(match)

@bot.command(pass_context=True)
async def cs(ctx, setname: str, *, cardname: str):
	cardname = 'e:' + setname + ' ' + cardname
	carddata = getjson('q', cardname)
	server = ctx.message.server
	match = cardMatch(carddata, 'cardtext', server)

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
