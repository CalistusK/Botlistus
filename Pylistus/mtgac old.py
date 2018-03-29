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
global latestcard
latestcard = ''

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

def cardMatch(carddata, rtype, server = None):
	latestcard = carddata['name']
	if rtype == 'cardtext':
		halves = ''
		if carddata['layout'] in ['split', 'flip', 'transform']:
			name = carddata['name']
			if 'mana_cost' in carddata:
				cost = emojify(carddata['mana_cost'], server).replace('//',' // ')
			elif carddata['layout'] == 'transform':
				cost = emojify(carddata['card_faces'][0]['mana_cost'], server)
			else:
				cost = ''
			rarity = carddata['rarity'].title()
			fromset = carddata['set'].upper()
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

			match = '%s\n%s\n%s (%s)\n%s' % (name, cost, rarity, fromset, halves)

		else:
			name = carddata['name']
			if "mana_cost" in carddata:
				cost = emojify(carddata['mana_cost'], server)
			else:
				cost = '\n'
			rarity = carddata['rarity'].title()
			fromset = carddata['set'].upper()
			cardtype = carddata['type_line'].replace("â€”","—")
			cardtext = carddata['oracle_text'].replace("â€”","—")
			if "power" in carddata:
				pt = carddata['power'] + '/' + carddata['toughness']
			else:
				pt = ''

			match = '%s %s\n%s (%s)\n%s\n%s```\n%s```' % (name, cost, rarity, fromset, cardtype, pt, cardtext)

	elif rtype == 'cardusd':
		name = carddata['name']
		cardset = carddata['set']
		price = carddata['usd']

		match = '%s (%s) ~ $%s' % (name, cardset.upper(), price)

	return match

def emojify(cost, server):
	cost = cost.lower().replace("{","mana").replace("}"," ").replace("/","").split(' ')
	cost = list(filter(None, cost))
	for idx,manasym in enumerate(cost):
		for emo in server.emojis:
			if emo.name == manasym:
				cost[idx] = str(emo)

	return ''.join(cost)

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
async def p(*, cardname=''):
	global latestcard
	if cardname == '':
		cardname = latestcard
	else:
		cardname = 'usd>=0.00 ' + cardname
		carddata = getjson('q', cardname)
		match = cardMatch(carddata, 'cardusd')            	

	await bot.say(match)

@bot.command()
async def pe(*, cardname=''):
	if cardname == '':
		cardname = latestcard
	else:
		carddata = getjson('exact', cardname)
		match = cardMatch(carddata, 'cardusd')

	await bot.say(match)

@bot.command()
async def pf(*, cardname=''):
	if cardname == '':
		cardname = latestcard
	else:
		carddata = getjson('fuzzy', cardname)
		match = cardMatch(carddata, 'cardusd')

	await bot.say(match)

@bot.command()
async def pn(*, cardname=''):
	if cardname == '':
		cardname = latestcard
	else:
		cardname = 'is:' + cardname
		carddata = getjson('q', cardname)
		match = cardMatch(carddata, 'cardusd')

	await bot.say(match)

@bot.command()
async def ps(setname: str, *, cardname=''):
	if cardname == '':
		cardname = latestcard
	else:
		cardname = 'e:' + setname + ' ' + cardname
		carddata = getjson('q', cardname)
		match = cardMatch(carddata, 'cardusd')

	await bot.say(match)

config.read('config.ini')
bot.run(config['DiscordAPI']['Key'])
