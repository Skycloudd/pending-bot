import discord
from discord.ext import commands

from utility_functions import *
from pending import *


bot = commands.Bot(
	command_prefix='?',
	intents=discord.Intents.all()
)

config = open_json('config')


@bot.event
async def on_ready():
	print('Ready')


@bot.event
async def on_message(message):
	if message.author.bot:
		return

	await bot.process_commands(message)


@bot.command()
async def pending(ctx, *, games):
	abbreviations = games.split()

	ids = []
	for abbreviation in abbreviations:
		id = abbr_to_id(abbreviation)
		if id:
			ids.append(id)

	names = [id_to_name(id) for id in ids]

	total = get_pending_count(ids)["total"]

	gamelist = '- ' + '\n- '.join(names)

	await ctx.send(f'{total} runs pending in\n{gamelist}')

bot.run(config["token"])
