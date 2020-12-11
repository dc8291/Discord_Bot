import discord
import datetime
import os
from discord.ext import commands
from cogs.basic_commands import BasicCommands
from cogs.op_score import OPScore

import json

token = json.load(open("static/env.json"))["token"]

bot = commands.Bot("!")

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print('[{}] I\'m in!'.format(datetime.datetime.now()))
    print('----')

# Reloads cogs. Useful during debugging
@bot.command()
async def reload(ctx, extension):
    print("reloading...")
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(token, bot=True)
