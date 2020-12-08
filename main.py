import discord
import datetime
from discord.ext import commands
from cogs.basic_commands import BasicCommands
from cogs.relationship import Relationship
import re
import json

token = json.load(open("static/env.json"))["token"]

bot = commands.Bot("$")

bot.add_cog(BasicCommands(bot))
bot.add_cog(Relationship(bot))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('[{}] I\'m in!'.format(datetime.datetime.now()))
    print('----')

#When someone types "i'm in" send the i'm in image
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    match = re.search("(i'?m\s*in)", message.content.lower())
    if  match:
        await message.channel.send(file=discord.File('pics/im_in.jpg'))

    await bot.process_commands(message)


bot.run(token, bot=True)
