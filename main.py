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
async def runs(ctx, channel: discord.TextChannel, game: str):
	await channel.purge(limit=None)

	id = abbr_to_id(game)

	if not id:
		await ctx.send(f'that is an invalid game!')
		return

	runs = get_pending_runs(id)
	for run in runs:
		embed = discord.Embed(
			title=run["category"],
			url=run["weblink"]
		)

		embed.add_field(
			name='Players',
			value=run["players"],
			inline=False
		)

		embed.add_field(
			name='Time',
			value=f'{run["time"]} seconds',
			inline=False
		)

		await channel.send(embed=embed)

	embed = discord.Embed(
		title='Total runs',
		description=f'{len(runs)} runs'
	)

	await channel.send(embed=embed)



@bot.command()
async def pending(ctx, *, games: str):
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
