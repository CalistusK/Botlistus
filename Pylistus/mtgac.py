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

	response = requests.get('https://api.scryfall.com/cards/' + stype, params={sfilter: cardname})
	cd = json.loads(response.text)

	if sfilter == 'q':
		cd = cd['data'][0]

	return cd

def cardMatch(cd, rtype, server = None):
	if rtype == 'cardtext':
		halves = ''
		if cd['layout'] in ['split', 'flip', 'transform']:
			if 'mana_cost' in cd:
				cost = emojify(cd['mana_cost'], server).replace('//',' // ')
			elif cd['layout'] == 'transform':
				cost = emojify(cd['card_faces'][0]['mana_cost'], server)
			else:
				cost = ''
			for face in [0, 1]:
				cardhalf = cd['card_faces'][face]
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
					if 'loyalty' in cd['card_faces'][0]:
						halves = halves + 'Loyalty: ' + cardhalf['loyalty']
					
					halves = halves + '\n'

			match = '%s\n%s\n%s (%s)\n%s' % (cd['name'], cost, cd['rarity'].title(), cd['set'].upper(), halves)

		else:
			if "mana_cost" in cd:
				cost = emojify(cd['mana_cost'], server)
			else:
				cost = '\n'
			if "power" in cd:
				pt = cd['power'] + '/' + cd['toughness']
			else:
				pt = ''
			if "oracle_text" in cd:
				ot = '```\n' + cd['oracle_text'].replace("â€”","—") + '```'
			else:
				ot = ''
			if "loyalty" in cd:
				pwl = 'Loyalty: ' + cd['loyalty']
			else:
				pwl = ''

			match = '%s %s\n%s (%s)\n%s\n%s%s%s' % (cd['name'], cost, cd['rarity'].title(), cd['set'].upper(), cd['type_line'].replace("â€”","—"), pt, ot, pwl)

	elif rtype == 'cardusd':
		match = '%s (%s) ~ $%s' % (cd['name'], cd['set'].upper(), cd['usd'])

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
	cd = getjson('q', cardname)
	server = ctx.message.server
	match = cardMatch(cd, 'cardtext', server)

	await bot.say(match)

@bot.command(pass_context=True)
async def ce(ctx, *, cardname: str):
	cd = getjson('exact', cardname)
	server = ctx.message.server
	match = cardMatch(cd, 'cardtext', server)

	await bot.say(match)

@bot.command(pass_context=True)
async def cf(ctx, *, cardname: str):
	cd = getjson('fuzzy', cardname)
	server = ctx.message.server
	match = cardMatch(cd, 'cardtext', server)

	await bot.say(match)

@bot.command(pass_context=True)
async def cn(ctx, *, cardname: str):
	cardname = 'is:' + cardname
	cd = getjson('q', cardname)
	server = ctx.message.server
	match = cardMatch(cd, 'cardtext', server)

	await bot.say(match)

@bot.command(pass_context=True)
async def cs(ctx, setname: str, *, cardname: str):
	cardname = 'e:' + setname + ' ' + cardname
	cd = getjson('q', cardname)
	server = ctx.message.server
	match = cardMatch(cd, 'cardtext', server)

	await bot.say(match)

@bot.command()
async def p(*, cardname=''):
	global latestcard
	if cardname == '':
		cardname = latestcard
	else:
		cardname = 'usd>=0.00 ' + cardname
		cd = getjson('q', cardname)
		match = cardMatch(cd, 'cardusd')            	

	await bot.say(match)

@bot.command()
async def pe(*, cardname=''):
	if cardname == '':
		cardname = latestcard
	else:
		cd = getjson('exact', cardname)
		match = cardMatch(cd, 'cardusd')

	await bot.say(match)

@bot.command()
async def pf(*, cardname=''):
	if cardname == '':
		cardname = latestcard
	else:
		cd = getjson('fuzzy', cardname)
		match = cardMatch(cd, 'cardusd')

	await bot.say(match)

@bot.command()
async def pn(*, cardname=''):
	if cardname == '':
		cardname = latestcard
	else:
		cardname = 'is:' + cardname
		cd = getjson('q', cardname)
		match = cardMatch(cd, 'cardusd')

	await bot.say(match)

@bot.command()
async def ps(setname: str, *, cardname=''):
	if cardname == '':
		cardname = latestcard
	else:
		cardname = 'e:' + setname + ' ' + cardname
		cd = getjson('q', cardname)
		match = cardMatch(cd, 'cardusd')

	await bot.say(match)

config.read('config.ini')
bot.run(config['DiscordAPI']['Key'])
